import React from "react";
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom"; // Required for <Link> components
import Footer from "./Footer";
import apps from "./apps"; // Import the shared apps list

describe("Footer component", () => {
    it("renders the footer with a list of apps", () => {
        const { getByText } = render(
            <BrowserRouter>
                <Footer />
            </BrowserRouter>
        );

        // Check that all app links are rendered
        apps.forEach((app) => {
            const linkElement = getByText(app.name);
            expect(linkElement).toBeInTheDocument();
            expect(linkElement.closest("a")).toHaveAttribute("href", app.path);
        });
    });

    it("applies the correct styles", () => {
        const { container } = render(
            <BrowserRouter>
                <Footer />
            </BrowserRouter>
        );

        const footer = container.querySelector("footer");
        expect(footer).toHaveClass("footer");

        const list = container.querySelector("ul");
        expect(list).toHaveClass("list");

        const listItem = container.querySelector("li");
        expect(listItem).toHaveClass("listItem");
    });
});
