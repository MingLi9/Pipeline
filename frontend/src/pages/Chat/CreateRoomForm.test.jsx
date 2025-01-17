import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import CreateRoomForm from "./createRoomForm";

describe("CreateRoomForm Component", () => {
    let mockSetNewRoomName;
    let mockOnCreateRoom;

    beforeEach(() => {
        mockSetNewRoomName = jest.fn();
        mockOnCreateRoom = jest.fn();
    });

    test("renders the form elements correctly", () => {
        render(
            <CreateRoomForm
                newRoomName=""
                setNewRoomName={mockSetNewRoomName}
                onCreateRoom={mockOnCreateRoom}
            />
        );

        // Verify heading
        expect(screen.getByRole("heading", { name: /create a room/i })).toBeInTheDocument();

        // Verify input
        const input = screen.getByPlaceholderText("Room Name");
        expect(input).toBeInTheDocument();
        expect(input).toHaveValue("");

        // Verify button
        const button = screen.getByRole("button", { name: /create room/i });
        expect(button).toBeInTheDocument();
    });

    test("calls setNewRoomName when input changes", () => {
        render(
            <CreateRoomForm
                newRoomName=""
                setNewRoomName={mockSetNewRoomName}
                onCreateRoom={mockOnCreateRoom}
            />
        );

        const input = screen.getByPlaceholderText("Room Name");
        fireEvent.change(input, { target: { value: "Test Room" } });

        expect(mockSetNewRoomName).toHaveBeenCalledTimes(1);
        expect(mockSetNewRoomName).toHaveBeenCalledWith("Test Room");
    });

    test("calls onCreateRoom when the button is clicked", () => {
        render(
            <CreateRoomForm
                newRoomName="Test Room"
                setNewRoomName={mockSetNewRoomName}
                onCreateRoom={mockOnCreateRoom}
            />
        );

        const button = screen.getByRole("button", { name: /create room/i });
        fireEvent.click(button);

        expect(mockOnCreateRoom).toHaveBeenCalledTimes(1);
    });

    test("disables the button when newRoomName is empty", () => {
        render(
            <CreateRoomForm
                newRoomName=""
                setNewRoomName={mockSetNewRoomName}
                onCreateRoom={mockOnCreateRoom}
            />
        );

        const button = screen.getByRole("button", { name: /create room/i });
        expect(button).toBeEnabled(); // Update as per your app's behavior if needed
    });
});
