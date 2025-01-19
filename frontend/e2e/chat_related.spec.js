// e2e/example.spec.js
const { test, expect } = require('@playwright/test');
const { timeout } = require('../playwright.config');

// All tests are skipped in CI if it needs the SSO login
const isCI = process.env.CI === 'true';

// This test should always pass
test('should navigate to the homepage and check the title', async ({ page }) => {
    // Navigate to your application
    await page.goto('http://localhost:3000'); // Adjust the URL to match your local development server

    // Check the page title
    const title = await page.title();
    expect(title).toBe('DVerse UI'); // Replace with the actual title of your application
});

test('SSO GitHub, create room, invite and send msg ', async ({ page }) => {
    if (isCI) {
        test.fixme(); // Mark the test as expected to fail in CI
    }
    await page.goto('http://localhost:3000/'); // Check if the page can load
    await page.getByRole('button', { name: 'Log In with SSO' }).click(); // Check if the SSO login button exists and works
    await page.getByRole('link', { name: 'GitHub' }).click(); // Preventing any security issues, GitHub login is used
    // Codeblock for SSO GitHub login
    await page.getByLabel('Username or email address').click();
    await page.getByLabel('Username or email address').fill('mingjanssen99@gmail.com');
    await page.getByLabel('Username or email address').press('Tab'); // Pressing tab to move to the password input field
    await page.getByLabel('Password').fill('dverse123');
    await page.getByRole('button', { name: 'Sign in', exact: true }).click();
    await page.getByRole('link', { name: 'Continue' }).click();
    // End of codeblock
    // Expecting to be in the hub page where a link should be to go to Chat page
    await page.getByRole('link', { name: 'Chat' }).first().click();
    // Create a room
    await page.getByPlaceholder('Room Name').click();
    await page.getByPlaceholder('Room Name').fill('test room e2e');
    await page.getByRole('button', { name: 'Create Room' }).click();
    // Invite the bot to the room
    await page.getByPlaceholder('Matrix User ID (e.g., @').click();
    await page.getByPlaceholder('Matrix User ID (e.g., @').fill('@dverse-chat-assistant:matrix.org');
    await page.getByRole('button', { name: 'Invite' }).click();
    // Send a message to the room
    await page.getByPlaceholder('Type your message').click();
    await page.getByPlaceholder('Type your message').fill('e2e testing: login, room creating, bot invite and messages');
    await page.getByRole('button', { name: 'Send' }).click();
    // Check if the message is displayed after sending  
    await page.getByText('@mingli99:matrix.org: e2e testing: login, room creating, bot invite and messages', { exact: true }).click();
    // Check if the bot has responded
    await page.getByText('@dverse-chat-assistant:matrix.org: e2e testing: login, room creating, bot').nth(1).click();
});

test('Switch between 2 chats', async ({ page }) => {
    if (isCI) {
        test.fixme(); // Mark the test as expected to fail in CI
    }
    await page.goto('http://localhost:3000/');
    await page.getByRole('button', { name: 'Log In with SSO' }).click();
    await page.getByRole('link', { name: 'GitHub' }).click();
    await page.getByLabel('Username or email address').fill('mingjanssen99@gmail.com');
    await page.getByLabel('Username or email address').press('Tab');
    await page.getByLabel('Password').fill('dverse123');
    await page.getByRole('button', { name: 'Sign in', exact: true }).click();
    await page.getByRole('link', { name: 'Continue' }).click();

    await page.getByRole('link', { name: 'Chat' }).first().click();
    // Switch between chat 1 and chat 2
    await page.locator('li').filter({ hasText: 'chat 1 (ID: !FbeBygqahHSBodbJFL:matrix.org) Join' }).getByRole('button').click();
    await page.getByText('@mingli99:matrix.org: chat 1').click();
    await page.locator('li').filter({ hasText: 'chat 2 (ID: !JjHOcwcQlcobjeYHlG:matrix.org) Join' }).getByRole('button').click();
    await page.getByText('@mingli99:matrix.org: chat 2').click();
});

test('Menu/footer with Logout', async ({ page }) => {
    if (isCI) {
        test.fixme(); // Mark the test as expected to fail in CI
    }
    await page.goto('http://localhost:3000/');
    await page.getByRole('button', { name: 'Log In with SSO' }).click();
    await page.getByRole('link', { name: 'GitHub' }).click();
    await page.getByLabel('Username or email address').fill('mingjanssen99@gmail.com');
    await page.getByLabel('Username or email address').press('Tab');
    await page.getByLabel('Password').fill('dverse123');
    await page.getByRole('button', { name: 'Sign in', exact: true }).click();
    await page.getByRole('link', { name: 'Continue' }).click();

    // Swapping between chat and hub page
    await page.getByRole('contentinfo').getByRole('link', { name: 'Chat' }).click();
    await page.getByRole('heading', { name: 'Matrix Chat' }).click();
    await page.getByRole('link', { name: 'Hub' }).click();
    await page.getByRole('heading', { name: 'Welcome to the Hub' }).click();
    // Logout
    await page.getByRole('contentinfo').getByRole('link', { name: 'Logout' }).click();
    await page.getByRole('heading', { name: 'Welcome to Matrix Chat' }).click();
});