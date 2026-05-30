import { Page, Locator, expect } from "@playwright/test";

export class HomePage {
  readonly page: Page;
  readonly header: Locator;
  readonly logo: Locator;
  readonly heroSection: Locator;
  readonly footer: Locator;
  readonly signInLink: Locator;
  readonly signUpButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.header = page.locator("header");
    this.logo = page.locator('a[href="/"]').filter({ hasText: "" }).first();
    this.heroSection = page.locator("main").first();
    this.footer = page.locator("footer");
    this.signInLink = page.getByRole("link", { name: /sign in/i });
    this.signUpButton = page.getByRole("link", { name: /sign up/i }).first();
  }

  async goto(): Promise<void> {
    await this.page.goto("/", { waitUntil: "domcontentloaded" });
  }

  async navigateToTrending(): Promise<void> {
    await this.page.goto("/trending", { waitUntil: "domcontentloaded" });
  }

  async navigateToExplore(): Promise<void> {
    await this.page.goto("/explore", { waitUntil: "domcontentloaded" });
  }

  async assertPageLoaded(): Promise<void> {
    await expect(this.header).toBeVisible({ timeout: 15_000 });
    await expect(this.footer).toBeVisible({ timeout: 15_000 });
  }

  async assertTitle(expectedSubstring: string): Promise<void> {
    await expect(this.page).toHaveTitle(new RegExp(expectedSubstring, "i"));
  }

  async assertUnauthenticatedState(): Promise<void> {
    await expect(this.signInLink).toBeVisible({ timeout: 10_000 });
  }

  async getCurrentPath(): Promise<string> {
    const url = new URL(this.page.url());
    return url.pathname;
  }

  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  async footerContainsLink(linkText: string): Promise<boolean> {
    const link = this.footer.getByRole("link", { name: linkText });
    return await link.isVisible().catch(() => false);
  }
}
