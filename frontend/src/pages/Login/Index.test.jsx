import React from "react";
import { act } from "@testing-library/react";
import { render, screen, fireEvent } from "@testing-library/react";
import { ToastContainer } from "react-toastify";
import LoginPage from "./index";
import * as sdk from "matrix-js-sdk";

jest.mock("matrix-js-sdk", () => ({
    createClient: jest.fn(),
}));

jest.mock("react-toastify", () => ({
    toast: {
        info: jest.fn(),
        error: jest.fn(),
        success: jest.fn(),
        warn: jest.fn(),
    },
    ToastContainer: jest.fn(() => <div />),
}));

describe("LoginPage Component", () => {
    let mockClient;
    const mockOnLoginComplete = jest.fn();

    const setupMockClient = () => ({
        getSsoLoginUrl: jest.fn(() => "https://mock-sso-login-url.com"),
        login: jest.fn(() => Promise.resolve()),
        startClient: jest.fn(() => Promise.resolve()),
        once: jest.fn(),
    });

    beforeEach(() => {
        mockClient = setupMockClient();
        sdk.createClient.mockReturnValue(mockClient);
        delete window.location;
        window.location = { href: "", origin: "http://localhost" };
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test("renders the login page UI", () => {
        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        // Verify the header
        expect(screen.getByRole("heading", { name: /welcome to matrix chat/i })).toBeInTheDocument();

        // Verify the button
        const loginButton = screen.getByRole("button", { name: /log in with sso/i });
        expect(loginButton).toBeInTheDocument();
    });

    test("initializes the Matrix client on mount", () => {
        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        expect(sdk.createClient).toHaveBeenCalledWith({
            baseUrl: "https://matrix.org",
        });
    });

    test("shows a toast and redirects for SSO login when client is initialized", () => {
        delete window.location;
        window.location = { href: "" }; // Mock the location.href property

        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        const loginButton = screen.getByRole("button", { name: /log in with sso/i });

        fireEvent.click(loginButton);

        expect(mockClient.getSsoLoginUrl).toHaveBeenCalledWith(`${window.location.origin}/`);

        expect(window.location.href).toBe("https://mock-sso-login-url.com");
    });

    test("shows an error toast if the Matrix client is not initialized when logging in", () => {
        sdk.createClient.mockReturnValueOnce(null); // Simulate null client

        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        const loginButton = screen.getByRole("button", { name: /log in with sso/i });

        // Simulate clicking the login button
        fireEvent.click(loginButton);

        // Ensure the toast is called
        expect(require("react-toastify").toast.error).toHaveBeenCalledWith(
            "Matrix client not initialized. Please try again."
        );

        // Ensure no redirect occurred
        expect(window.location.href).toBe("");
    });

    test("handles SSO login completion correctly with a valid token", async () => {
        Object.defineProperty(window, "location", {
            value: {
                search: "?loginToken=mockToken",
            },
            writable: true,
        });

        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        mockClient.once.mockImplementation((event, callback) => {
            if (event === "sync") {
                callback("PREPARED"); // Simulate the sync event
            }
        });

        // Simulate login and client startup
        await act(async () => {
            await Promise.resolve();
        });

        expect(mockClient.login).toHaveBeenCalledWith("m.login.token", { token: "mockToken" });
        expect(mockClient.startClient).toHaveBeenCalledWith({ initialSyncLimit: 100 });

        // Ensure the callback was called
        expect(mockOnLoginComplete).toHaveBeenCalledTimes(1);
        expect(mockOnLoginComplete).toHaveBeenCalledWith(mockClient);
    });

    test("shows a warning if no login token is present during SSO login", async () => {
        // Simulate a URL with no login token
        Object.defineProperty(window, "location", {
            value: {
                search: "", // No loginToken present
            },
            writable: true,
        });

        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        // Wait for the useEffect to complete
        await act(async () => {
            await Promise.resolve();
        });

        // Assert that no login was attempted
        expect(mockClient.login).not.toHaveBeenCalled();

        // Assert that the toast.warn was triggered
        expect(require("react-toastify").toast.warn).toHaveBeenCalledWith(
            "No login token found. Please log in again."
        );
    });

    test("executes SSO login logic with valid client and token", async () => {
        // Mock a valid URL with a login token
        Object.defineProperty(window, "location", {
            value: {
                search: "?loginToken=validToken", // Simulate a valid loginToken
            },
            writable: true,
        });

        const mockClient = {
            login: jest.fn(() => Promise.resolve()),
            startClient: jest.fn(() => Promise.resolve()),
            once: jest.fn(),
        };

        // Mock Matrix client creation
        sdk.createClient.mockReturnValue(mockClient);

        render(<LoginPage onLoginComplete={mockOnLoginComplete} />);

        // Ensure client is initialized
        await act(async () => {
            // Simulate the `client` being set and `useEffect` running
            mockClient.once.mockImplementation((event, callback) => {
                if (event === "sync") callback("PREPARED"); // Simulate sync event
            });
        });

        // Verify login is called with the correct token
        expect(mockClient.login).toHaveBeenCalledWith("m.login.token", { token: "validToken" });

        // Verify startClient is called
        expect(mockClient.startClient).toHaveBeenCalledWith({ initialSyncLimit: 100 });

        // Verify onLoginComplete is triggered
        expect(mockOnLoginComplete).toHaveBeenCalledWith(mockClient);

        // Verify success toast
        expect(require("react-toastify").toast.success).toHaveBeenCalledWith(
            "Login successful. Matrix client is ready."
        );
    });

});
