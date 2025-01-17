import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Hub from "./index";
import apps from "../../components/apps";

describe("Hub Component", () => {
    beforeEach(() => {
        jest.spyOn(console, "warn").mockImplementation((message) => {
            if (message.includes("React Router Future Flag Warning")) {
                return; // Suppress specific warning
            }
            console.warn(message); // Allow other warnings
        });
    });

    afterEach(() => {
        jest.restoreAllMocks(); // Restore original behavior
    });

    const renderComponent = () =>
        render(
            <BrowserRouter>
                <Hub />
            </BrowserRouter>
        );

    test("renders the header and description", () => {
        renderComponent();

        // Verify the header
        expect(
            screen.getByRole("heading", { name: /welcome to the hub/i })
        ).toBeInTheDocument();

        // Verify the description
        expect(
            screen.getByText(/select an app to navigate/i)
        ).toBeInTheDocument();
    });

    test("renders the correct number of app links", () => {
        renderComponent();

        // Verify the number of list items matches apps array
        const listItems = screen.getAllByRole("listitem");
        expect(listItems).toHaveLength(apps.length);
    });

    test("renders app links with correct paths and names", () => {
        renderComponent();

        apps.forEach((app) => {
            // Check if the link with the correct name exists
            const link = screen.getByRole("link", { name: app.name });
            expect(link).toBeInTheDocument();

            // Check if the link has the correct path
            expect(link).toHaveAttribute("href", app.path);
        });
    });
});
