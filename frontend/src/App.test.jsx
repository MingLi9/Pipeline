import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter, MemoryRouter } from "react-router-dom";
import App from "./App";

// Mock subcomponents
jest.mock("./pages/Login", () => ({ onLoginComplete }) => (
    <div data-testid="login-page">
        <button onClick={() => onLoginComplete({ stopClient: jest.fn() })}>Login</button>
    </div>
));
jest.mock("./pages/Hub", () => ({ client }) => (
    <div data-testid="hub-page">Hub (Client: {client ? "Connected" : "Disconnected"})</div>
));
jest.mock("./pages/Chat", () => ({ client }) => (
    <div data-testid="chat-page">Chat (Client: {client ? "Connected" : "Disconnected"})</div>
));
jest.mock("./components/Footer", () => () => <div data-testid="footer">Footer</div>);

describe("App component", () => {
    it("renders LoginPage initially", () => {
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );
        expect(screen.getByTestId("login-page")).toBeInTheDocument();
    });

    it("navigates to Hub after login and covers handleLoginComplete", () => {
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );

        // Simulate login
        const loginButton = screen.getByText("Login");
        fireEvent.click(loginButton);

        // Ensure Hub is displayed
        expect(screen.getByTestId("hub-page")).toBeInTheDocument();

        // Verify that the client is set (mocked)
        expect(screen.getByTestId("hub-page")).toHaveTextContent("Connected");
    });

    it("renders Footer for non-login routes", () => {
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );

        const loginButton = screen.getByText("Login");
        fireEvent.click(loginButton);

        expect(screen.getByTestId("footer")).toBeInTheDocument();
    });

    it("does not render Footer for the login route", () => {
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>
        );

        expect(screen.queryByTestId("footer")).not.toBeInTheDocument();
    });

    it("handles logout and redirects to login page", () => {
        render(
            <MemoryRouter initialEntries={["/logout"]}>
                <App />
            </MemoryRouter>
        );

        // Verify redirection to login page after logout
        expect(screen.getByTestId("login-page")).toBeInTheDocument();
    });

});
