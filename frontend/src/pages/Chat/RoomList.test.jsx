import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import RoomList from "./roomList";

describe("RoomList Component", () => {
    let mockOnJoinRoom;

    beforeEach(() => {
        mockOnJoinRoom = jest.fn();
    });

    test("renders the list of rooms", () => {
        const rooms = [
            { id: "1", name: "Room One" },
            { id: "2", name: "Room Two" },
        ];

        render(<RoomList rooms={rooms} onJoinRoom={mockOnJoinRoom} />);

        // Verify the header
        expect(screen.getByRole("heading", { name: /available rooms/i })).toBeInTheDocument();

        // Verify all rooms are displayed
        rooms.forEach((room) => {
            expect(screen.getByText(`${room.name} (ID: ${room.id})`)).toBeInTheDocument();
        });

        // Verify buttons are present
        const buttons = screen.getAllByRole("button", { name: /join/i });
        expect(buttons).toHaveLength(rooms.length);
    });

    test("calls onJoinRoom with the correct room ID when a button is clicked", () => {
        const rooms = [{ id: "1", name: "Room One" }];

        render(<RoomList rooms={rooms} onJoinRoom={mockOnJoinRoom} />);

        const button = screen.getByRole("button", { name: /join/i });

        // Simulate clicking the join button
        fireEvent.click(button);

        expect(mockOnJoinRoom).toHaveBeenCalledTimes(1);
        expect(mockOnJoinRoom).toHaveBeenCalledWith("1");
    });

    test("renders an empty list gracefully", () => {
        render(<RoomList rooms={[]} onJoinRoom={mockOnJoinRoom} />);

        // Verify the header is still present
        expect(screen.getByRole("heading", { name: /available rooms/i })).toBeInTheDocument();

        // Ensure no list items or buttons are present
        expect(screen.queryAllByRole("listitem")).toHaveLength(0);
        expect(screen.queryAllByRole("button")).toHaveLength(0);
    });
});
