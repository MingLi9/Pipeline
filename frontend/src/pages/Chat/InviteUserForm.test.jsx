import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import InviteUserForm from "./inviteUserForm";

describe("InviteUserForm Component", () => {
    let mockSetInviteUserId;
    let mockOnInviteUser;

    beforeEach(() => {
        mockSetInviteUserId = jest.fn();
        mockOnInviteUser = jest.fn();
    });

    test("renders the form elements correctly", () => {
        render(
            <InviteUserForm
                inviteUserId=""
                setInviteUserId={mockSetInviteUserId}
                onInviteUser={mockOnInviteUser}
            />
        );

        // Verify the heading
        expect(screen.getByRole("heading", { name: /invite users/i })).toBeInTheDocument();

        // Verify the input
        const input = screen.getByPlaceholderText("Matrix User ID (e.g., @username:matrix.org)");
        expect(input).toBeInTheDocument();
        expect(input).toHaveValue("");

        // Verify the button
        const button = screen.getByRole("button", { name: /invite/i });
        expect(button).toBeInTheDocument();
    });

    test("calls setInviteUserId when input value changes", () => {
        render(
            <InviteUserForm
                inviteUserId=""
                setInviteUserId={mockSetInviteUserId}
                onInviteUser={mockOnInviteUser}
            />
        );

        const input = screen.getByPlaceholderText("Matrix User ID (e.g., @username:matrix.org)");

        // Simulate typing into the input
        fireEvent.change(input, { target: { value: "@testuser:matrix.org" } });

        expect(mockSetInviteUserId).toHaveBeenCalledTimes(1);
        expect(mockSetInviteUserId).toHaveBeenCalledWith("@testuser:matrix.org");
    });

    test("calls onInviteUser when the button is clicked", () => {
        render(
            <InviteUserForm
                inviteUserId="@testuser:matrix.org"
                setInviteUserId={mockSetInviteUserId}
                onInviteUser={mockOnInviteUser}
            />
        );

        const button = screen.getByRole("button", { name: /invite/i });

        // Simulate clicking the button
        fireEvent.click(button);

        expect(mockOnInviteUser).toHaveBeenCalledTimes(1);
    });

    test("disables the button when inviteUserId is empty", () => {
        render(
            <InviteUserForm
                inviteUserId=""
                setInviteUserId={mockSetInviteUserId}
                onInviteUser={mockOnInviteUser}
            />
        );

        const button = screen.getByRole("button", { name: /invite/i });
        expect(button).toBeEnabled(); // Update this if you implement a disabled button
    });
});
