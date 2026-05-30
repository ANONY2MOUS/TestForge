import { test, expect } from "@playwright/test";
import { HomePage } from "../pages/HomePage";

test.describe("GitHub Homepage — Navigation", () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();
  });

  test("homepage loads with correct page title", async ({ page }) => {
    const title = await page.title();
    expect(title).toContain("GitHub");
  });

  test("header is visible and contains key elements", async ({ page }) => {
    await expect(homePage.header).toBeVisible({ timeout: 15_000 });
    const headerLogo = page.locator('header a[href="/"], header [aria-label="Homepage"]').first();
    await expect(headerLogo).toBeVisible({ timeout: 10_000 });
  });

  test("footer is visible and contains essential links", async ({ page }) => {
    await expect(homePage.footer).toBeVisible({ timeout: 15_000 });
    const termsLink = page.locator('footer a').filter({ hasText: /terms/i }).first();
    await expect(termsLink).toBeVisible({ timeout: 10_000 });
  });

  test("unauthenticated users see sign-in link", async () => {
    await homePage.assertUnauthenticatedState();
  });

  test("sign up button is visible", async ({ page }) => {
    const signUpBtn = page.getByRole("link", { name: /sign up/i }).first();
    await expect(signUpBtn).toBeVisible({ timeout: 10_000 });
  });

  test("sign in link navigates to login page", async ({ page }) => {
    const signInLink = page.getByRole("link", { name: /sign in/i }).first();
    await expect(signInLink).toBeVisible({ timeout: 10_000 });
    await signInLink.click();
    await expect(page).toHaveURL(/login|session/i, { timeout: 15_000 });
  });

  test("direct navigation to /trending works", async ({ page }) => {
    await page.goto("/trending", { waitUntil: "domcontentloaded" });
    expect(page.url()).toContain("/trending");
  });

  test("direct navigation to /explore works", async ({ page }) => {
    await page.goto("/explore", { waitUntil: "domcontentloaded" });
    expect(page.url()).toContain("/explore");
  });
});
