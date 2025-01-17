import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import SendMessageForm from "./sendMessageForm";

describe("SendMessageForm Component", () => {
    let mockSetNewMessage;
    let mockOnSendMessage;

    beforeEach(() => {
        mockSetNewMessage = jest.fn();
        mockOnSendMessage = jest.fn();
    });

    test("renders the form elements correctly", () => {
        render(
            <SendMessageForm
                newMessage=""
                setNewMessage={mockSetNewMessage}
                onSendMessage={mockOnSendMessage}
            />
        );

        // Verify the header
        expect(screen.getByRole("heading", { name: /send a message/i })).toBeInTheDocument();

        // Verify the input
        const input = screen.getByPlaceholderText("Type your message");
        expect(input).toBeInTheDocument();
        expect(input).toHaveValue("");

        // Verify the button
        const button = screen.getByRole("button", { name: /send/i });
        expect(button).toBeInTheDocument();
    });

    test("calls setNewMessage when input value changes", () => {
        render(
            <SendMessageForm
                newMessage=""
                setNewMessage={mockSetNewMessage}
                onSendMessage={mockOnSendMessage}
            />
        );

        const input = screen.getByPlaceholderText("Type your message");
        fireEvent.change(input, { target: { value: "Hello, world!" } });

        expect(mockSetNewMessage).toHaveBeenCalledTimes(1);
        expect(mockSetNewMessage).toHaveBeenCalledWith("Hello, world!");
    });

    test("calls onSendMessage when the button is clicked", () => {
        render(
            <SendMessageForm
                newMessage="Hello, world!"
                setNewMessage={mockSetNewMessage}
                onSendMessage={mockOnSendMessage}
            />
        );

        const button = screen.getByRole("button", { name: /send/i });
        fireEvent.click(button);

        expect(mockOnSendMessage).toHaveBeenCalledTimes(1);
    });

    test("button is enabled regardless of input state", () => {
        render(
            <SendMessageForm
                newMessage=""
                setNewMessage={mockSetNewMessage}
                onSendMessage={mockOnSendMessage}
            />
        );

        const button = screen.getByRole("button", { name: /send/i });
        expect(button).toBeEnabled();
    });
});
