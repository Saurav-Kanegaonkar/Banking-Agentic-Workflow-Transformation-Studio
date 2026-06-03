import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const baseUrl = process.env.ARTIFACT_URL || "http://127.0.0.1:4173";
const outputDir = new URL("../docs/images/", import.meta.url);

const shots = [
  { file: "intake-portfolio.png", tab: "intake" },
  { file: "prd-controls.png", tab: "prd" },
  { file: "release-gates.png", tab: "gates" },
];

await mkdir(outputDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1 });
await page.goto(baseUrl, { waitUntil: "networkidle" });

for (const shot of shots) {
  await page.locator(`[data-tab="${shot.tab}"]`).click();
  await page.locator("#detailSurface").waitFor({ state: "visible" });
  await page.screenshot({ path: fileURLToPath(new URL(shot.file, outputDir)), fullPage: true });
}

await browser.close();
console.log("Captured portfolio artifact screenshots.");
