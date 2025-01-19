const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './e2e', // Directory where your E2E tests will be located
    timeout: 30000, // 30 seconds timeout per test
    use: {
        // Configure browser options here
        headless: true,
        viewport: { width: 1280, height: 720 },
        actionTimeout: 0,
    },
});