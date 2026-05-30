import logging
import time
from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff_factor: float = 1.0,
        extra_headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff_factor = retry_backoff_factor
        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_backoff_factor,
            allowed_methods=["GET", "HEAD", "OPTIONS"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update(self._get_default_headers())
        if extra_headers:
            self.session.headers.update(extra_headers)

    def _get_default_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "TestForge-APIClient/1.0",
        }

    def _request(self, method: str, endpoint: str, handle_rate_limit: bool = True, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        last_exception: Optional[Exception] = None
        max_rate_limit_retries = 3

        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = time.monotonic()
                response = self.session.request(method, url, **kwargs)
                elapsed_ms = (time.monotonic() - start_time) * 1000
                logger.info(f"HTTP {method} {endpoint} → {response.status_code} [{elapsed_ms:.0f}ms] (attempt {attempt}/{self.max_retries})")

                if response.status_code == 429 and handle_rate_limit:
                    if max_rate_limit_retries <= 0:
                        return response
                    retry_after_raw = response.headers.get("Retry-After")
                    reset_timestamp = response.headers.get("X-RateLimit-Reset")
                    if retry_after_raw:
                        wait_seconds = int(retry_after_raw)
                    elif reset_timestamp:
                        wait_seconds = max(0, int(reset_timestamp) - int(time.time())) + 1
                    else:
                        wait_seconds = 60
                    logger.warning(f"Rate limited (429). Waiting {wait_seconds}s before retry {attempt}/{self.max_retries}.")
                    time.sleep(wait_seconds)
                    max_rate_limit_retries -= 1
                    continue
                return response
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
                logger.warning(f"Error on attempt {attempt}/{self.max_retries}: {exc}")
                last_exception = exc
                if attempt < self.max_retries:
                    sleep_time = self.retry_backoff_factor * (2 ** (attempt - 1))
                    time.sleep(sleep_time)
        raise last_exception or RuntimeError(f"Request {method} {url} failed after {self.max_retries} attempts")

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs: Any) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs: Any) -> requests.Response:
        return self._request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: Optional[Dict] = None, **kwargs: Any) -> requests.Response:
        return self._request("PUT", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        self.session.close()

class GitHubAPIClient(BaseAPIClient):
    GITHUB_API_V3_ACCEPT = "application/vnd.github.v3+json"

    def __init__(
        self,
        base_url: str = "https://api.github.com",
        token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self._token = token
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

    def _get_default_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Accept": self.GITHUB_API_V3_ACCEPT,
            "User-Agent": "TestForge-E2E-Suite/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        token = getattr(self, "_token", None)
        if token:
            headers["Authorization"] = f"token {token}"
        return headers
