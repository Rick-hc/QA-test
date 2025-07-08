import { test, expect } from '@playwright/test'

test('homepage', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await expect(page).toHaveTitle(/React App/)
})
