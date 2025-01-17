import React from "react";
import { render, screen, fireEvent, act } from "@testing-library/react";
import Chat from "./index";

jest.mock("react-toastify", () => ({
    toast: {
        success: jest.fn(),
        error: jest.fn(),
        info: jest.fn(),
    },
    ToastContainer: jest.fn(() => <div />),
}));

describe("Chat Component - Additional Tests", () => {
    let mockClient, mockTimeline;

    beforeEach(() => {
        jest.clearAllMocks();

        mockTimeline = {
            getEvents: jest.fn(() => [
                {
                    getType: jest.fn(() => "m.room.message"),
                    getSender: jest.fn(() => "User1"),
                    getContent: jest.fn(() => ({ body: "Hello" })),
                },
            ]),
        };

        mockClient = {
            getRooms: jest.fn(() => [
                { roomId: "1", name: "Room One", getMyMembership: jest.fn(() => "join") },
                { roomId: "2", name: "Room Two", getMyMembership: jest.fn(() => "invite") },
            ]),
            joinRoom: jest.fn(() =>
                Promise.resolve({
                    roomId: "1",
                    getLiveTimeline: jest.fn(() => mockTimeline),
                })
            ),
            createRoom: jest.fn(() => Promise.resolve({ room_id: "3" })),
            invite: jest.fn(() => Promise.resolve()),
            sendEvent: jest.fn(() => Promise.resolve()),
            on: jest.fn(),
            removeListener: jest.fn(),
        };
    });

    test("fetches room history correctly (lines 45-46)", async () => {
        render(<Chat client={mockClient} />);

        const joinButton = screen.getAllByRole("button", { name: /join/i })[0];
        await act(async () => {
            fireEvent.click(joinButton);
        });

        // Verify `getLiveTimeline` and `getEvents` were called
        expect(mockClient.joinRoom).toHaveBeenCalledWith("1");
        expect(mockTimeline.getEvents).toHaveBeenCalledTimes(1);
    });
});
