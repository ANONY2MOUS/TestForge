import { defineConfig, devices } from "@playwright/test";
import * as dotenv from "dotenv";
import * as path from "path";

dotenv.config({ path: path.resolve(__dirname, ".env") });

const BASE_URL = process.env.E2E_BASE_URL || "https://github.com";

export default defineConfig({
  testDir: "./e2e/tests",
  testMatch: "**/*.spec.ts",
  fullyParallel: false,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : 1,
  forbidOnly: !!process.env.CI,
  timeout: 45_000,
  expect: {
    timeout: 10_000,
  },
  reporter: [
    ["list"],
    ...(process.env.CI ? [["github"] as const] : []),
    ["html", { outputFolder: "playwright-report", open: "never" }],
    ["json", { outputFile: "test-results/e2e-report.json" }],
  ],
  use: {
    baseURL: BASE_URL,
    screenshot: "only-on-failure",
    video: "on-first-retry",
    trace: "on-first-retry",
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 TestForge/1.0",
    navigationTimeout: 30_000,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: false,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
  outputDir: "test-results/e2e-artifacts",
});
