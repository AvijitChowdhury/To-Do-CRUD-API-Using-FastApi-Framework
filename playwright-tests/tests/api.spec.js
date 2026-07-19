const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const screenshotsDir = path.resolve(__dirname, '..', '..', 'assests', 'playwright');
fs.mkdirSync(screenshotsDir, { recursive: true });
const baseURL = 'http://127.0.0.1:8001';

test.describe('Task API end-to-end API testing', () => {
  test('health endpoint responds correctly', async ({ request }) => {
    const response = await request.get(`${baseURL}/health`);
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body).toEqual({ status: 'ok' });
  });

  test('CRUD flow works end to end via API', async ({ request }) => {
    const createResponse = await request.post(`${baseURL}/tasks`, {
      data: { title: 'Playwright test task' },
    });
    expect(createResponse.status()).toBe(201);
    const createdTask = await createResponse.json();
    expect(createdTask.title).toBe('Playwright test task');
    expect(createdTask.done).toBe(false);

    const readResponse = await request.get(`${baseURL}/tasks/${createdTask.id}`);
    expect(readResponse.status()).toBe(200);
    const fetchedTask = await readResponse.json();
    expect(fetchedTask.id).toBe(createdTask.id);

    const updateResponse = await request.put(`${baseURL}/tasks/${createdTask.id}`, {
      data: { done: true },
    });
    expect(updateResponse.status()).toBe(200);
    const updatedTask = await updateResponse.json();
    expect(updatedTask.done).toBe(true);

    const statsResponse = await request.get(`${baseURL}/stats`);
    expect(statsResponse.status()).toBe(200);
    const stats = await statsResponse.json();
    expect(stats.total).toBeGreaterThan(0);

    const deleteResponse = await request.delete(`${baseURL}/tasks/${createdTask.id}`);
    expect(deleteResponse.status()).toBe(204);

    const missingResponse = await request.get(`${baseURL}/tasks/${createdTask.id}`);
    expect(missingResponse.status()).toBe(404);
  });

  test('captures screenshots of the Swagger UI and API landing page', async ({ page }) => {
    await page.goto(`${baseURL}/docs`);
    await page.waitForLoadState('networkidle');
    await page.screenshot({
      path: path.join(screenshotsDir, 'swagger-ui.png'),
      fullPage: true,
    });

    await page.goto(`${baseURL}/`);
    await page.waitForLoadState('networkidle');
    await page.screenshot({
      path: path.join(screenshotsDir, 'landing-page.png'),
      fullPage: true,
    });
  });
});
