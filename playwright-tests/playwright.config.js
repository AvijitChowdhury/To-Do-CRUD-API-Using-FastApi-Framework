const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 60000,
  fullyParallel: false,
  use: {
    baseURL: 'http://127.0.0.1:8001',
    headless: true,
    screenshot: 'only-on-failure',
  },
  reporter: [['list']],
});
