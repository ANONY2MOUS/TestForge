.PHONY: install install-python install-node test-e2e test-api test-all report clean help

help:
	@echo ""
	@echo "  TestForge — Available Commands"
	@echo "  ───────────────────────────────────────────────"
	@echo "  make install        Install all Python + Node dependencies"
	@echo "  make install-python Install Python dependencies only"
	@echo "  make install-node   Install Node + Playwright browsers"
	@echo "  make test-e2e       Run E2E tests (chromium only)"
	@echo "  make test-api       Run API tests"
	@echo "  make test-all       Run both suites + generate combined report"
	@echo "  make report         Generate combined HTML report only"
	@echo "  make clean          Remove all test artifacts and reports"
	@echo ""

install: install-python install-node
	@echo "✅ All dependencies installed."

install-python:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

install-node:
	@echo "📦 Installing Node dependencies..."
	npm install
	@echo "🌐 Installing Playwright browsers..."
	npx playwright install --with-deps chromium

test-e2e:
	@echo "🎭 Running E2E tests (chromium)..."
	@mkdir -p test-results reports
	npx playwright test --project=chromium

test-api:
	@echo "🐍 Running API tests..."
	@mkdir -p test-results reports
	pytest api/tests/ -v

test-all: test-e2e test-api report
	@echo "✅ All tests complete. Open reports/combined-test-report.html to view results."

report:
	@echo "📊 Generating combined test report..."
	@mkdir -p reports
	python scripts/generate_combined_report.py
	@echo "📄 Report: reports/combined-test-report.html"

clean:
	@echo "🧹 Cleaning test artifacts..."
	rm -rf test-results/ playwright-report/ reports/ .pytest_cache/ __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete."
