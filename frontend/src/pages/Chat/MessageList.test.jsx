import React from "react";
import { render, screen } from "@testing-library/react";
import MessageList from "./messageList";

describe("MessageList Component", () => {
    test("renders the message list with messages", () => {
        const messages = [
            { sender: "User1", content: "Hello!" },
            { sender: "User2", content: "Hi there!" },
        ];

        render(<MessageList messages={messages} />);

        // Verify the header
        expect(screen.getByRole("heading", { name: /messages/i })).toBeInTheDocument();

        // Verify messages are rendered
        messages.forEach((msg) => {
            expect(
                screen.getByText((content, element) => {
                    const hasText = (node) => node.textContent === `${msg.sender}: ${msg.content}`;
                    const elementHasText = hasText(element);
                    const childrenDontHaveText = Array.from(element.children).every(
                        (child) => !hasText(child)
                    );
                    return elementHasText && childrenDontHaveText;
                })
            ).toBeInTheDocument();
        });
    });

    test("renders an empty message list gracefully", () => {
        render(<MessageList messages={[]} />);

        // Verify the header
        expect(screen.getByRole("heading", { name: /messages/i })).toBeInTheDocument();

        // Ensure no messages are displayed
        expect(screen.queryByText(/:/)).not.toBeInTheDocument();
    });
});
