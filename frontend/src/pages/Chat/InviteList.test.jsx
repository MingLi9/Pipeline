import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import InviteList from "./inviteList";

describe("InviteList Component", () => {
    let mockOnAcceptInvite;

    beforeEach(() => {
        mockOnAcceptInvite = jest.fn();
    });

    test("renders the invite list with invites", () => {
        const invites = [
            { id: "1", name: "Room One" },
            { id: "2", name: "Room Two" },
        ];

        render(<InviteList invites={invites} onAcceptInvite={mockOnAcceptInvite} />);

        // Verify the header
        expect(screen.getByRole("heading", { name: /room invites/i })).toBeInTheDocument();

        // Verify all invites are rendered
        invites.forEach((invite) => {
            expect(screen.getByText(`${invite.name} (ID: ${invite.id})`)).toBeInTheDocument();
        });

        // Verify buttons are present
        const buttons = screen.getAllByRole("button", { name: /accept/i });
        expect(buttons).toHaveLength(invites.length);
    });

    test("renders a message when there are no invites", () => {
        render(<InviteList invites={[]} onAcceptInvite={mockOnAcceptInvite} />);

        // Verify the "No pending invites" message
        expect(screen.getByText(/no pending invites/i)).toBeInTheDocument();

        // Ensure no list items or buttons are present
        expect(screen.queryAllByRole("listitem")).toHaveLength(0);
        expect(screen.queryAllByRole("button")).toHaveLength(0);
    });

    test("calls onAcceptInvite with the correct invite ID when the button is clicked", () => {
        const invites = [{ id: "1", name: "Room One" }];

        render(<InviteList invites={invites} onAcceptInvite={mockOnAcceptInvite} />);

        const button = screen.getByRole("button", { name: /accept/i });

        // Simulate clicking the accept button
        fireEvent.click(button);

        expect(mockOnAcceptInvite).toHaveBeenCalledTimes(1);
        expect(mockOnAcceptInvite).toHaveBeenCalledWith("1");
    });
});
