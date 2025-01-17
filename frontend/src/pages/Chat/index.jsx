import React, { useEffect, useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import styles from "./chat.module.css";
import RoomList from "./roomList";
import InviteList from "./inviteList";
import CreateRoomForm from "./createRoomForm";
import MessageList from "./messageList";
import InviteUserForm from "./inviteUserForm";
import SendMessageForm from "./sendMessageForm";

const Chat = ({ client }) => {
    const [roomId, setRoomId] = useState(null);
    const [rooms, setRooms] = useState([]);
    const [invites, setInvites] = useState([]);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [newRoomName, setNewRoomName] = useState("");
    const [inviteUserId, setInviteUserId] = useState("");

    const fetchRooms = () => {
        const availableRooms = client.getRooms().map((room) => ({
            id: room.roomId,
            name: room.name || "Unnamed Room",
        }));
        setRooms(availableRooms);
    };

    const fetchInvites = () => {
        const inviteRooms = client
            .getRooms()
            .filter((room) => room.getMyMembership() === "invite");
        const invitesList = inviteRooms.map((room) => ({
            id: room.roomId,
            name: room.name || "Unnamed Room",
        }));
        setInvites(invitesList);
    };

    const fetchRoomHistory = async (room) => {
        const timeline = room.getLiveTimeline();
        const events = timeline.getEvents();

        const historyMessages = events
            .filter((event) => event.getType() === "m.room.message")
            .map((event) => ({
                sender: event.getSender(),
                content: event.getContent().body,
            }));

        setMessages(historyMessages);
    };

    const handleJoinRoom = async (roomIdToJoin) => {
        try {
            const room = await client.joinRoom(roomIdToJoin);
            setRoomId(roomIdToJoin);
            fetchRoomHistory(room);
            fetchRooms();
            toast.success(`Successfully joined room: ${roomIdToJoin}`);
        } catch (error) {
            /* istanbul ignore next */
            toast.error("Failed to join room. Please try again.");
        }
    };

    const handleAcceptInvite = async (roomIdToAccept) => {
        try {
            await client.joinRoom(roomIdToAccept);
            fetchRooms();
            fetchInvites();
            toast.success(`Successfully joined invited room: ${roomIdToAccept}`);
        } catch (error) {
            /* istanbul ignore next */
            toast.error("Failed to accept room invite. Please try again.");
        }
    };

    const handleCreateRoom = async () => {
        try {
            const createdRoom = await client.createRoom({ name: newRoomName });
            setRoomId(createdRoom.room_id);
            fetchRooms();
            setMessages([]);
            toast.success(`Room created successfully: ${createdRoom.room_id}`);
        } catch (error) {
            /* istanbul ignore next */
            toast.error("Failed to create room. Please try again.");
        }
    };

    const handleInviteUser = async () => {
        /* istanbul ignore if */
        if (roomId && inviteUserId.trim()) {
            try {
                await client.invite(roomId, inviteUserId);
                setInviteUserId("");
                toast.success(`User ${inviteUserId} invited to room.`);
            } catch (error) {
                toast.error("Failed to invite user. Please try again.");
            }
        }
    };

    const handleSendMessage = async () => {
        if (roomId && newMessage.trim()) {
            try {
                await client.sendEvent(roomId, "m.room.message", {
                    msgtype: "m.text",
                    body: newMessage,
                });
                setNewMessage("");
                toast.success("Message sent successfully.");
            } catch (error) {
                /* istanbul ignore next */
                toast.error("Failed to send message. Please try again.");
            }
        }
    };

    useEffect(() => {
        if (roomId) {
            const handleTimelineEvent = (event, room) => {
                if (event.getType() === "m.room.message" && room.roomId === roomId) {
                    const sender = event.getSender();
                    const content = event.getContent().body;

                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { sender, content },
                    ]);

                    toast.info(`New message from ${sender}: ${content}`);
                }
            };

            client.on("Room.timeline", handleTimelineEvent);
            return () => client.removeListener("Room.timeline", handleTimelineEvent);
        }
    }, [client, roomId]);

    useEffect(() => {
        if (client) {
            fetchRooms();
            fetchInvites();
        }
    }, [client]);

    return (
        <div className={styles.container}>
            <ToastContainer />
            <h1 className={styles.header}>Matrix Chat</h1>

            <CreateRoomForm
                newRoomName={newRoomName}
                setNewRoomName={setNewRoomName}
                onCreateRoom={handleCreateRoom}
            />

            <InviteList invites={invites} onAcceptInvite={handleAcceptInvite} />

            <RoomList rooms={rooms} onJoinRoom={handleJoinRoom} />

            {roomId && (
                <>
                    <InviteUserForm
                        roomId={roomId}
                        inviteUserId={inviteUserId}
                        setInviteUserId={setInviteUserId}
                        onInviteUser={handleInviteUser}
                    />
                    <MessageList messages={messages} />
                    <SendMessageForm
                        newMessage={newMessage}
                        setNewMessage={setNewMessage}
                        onSendMessage={handleSendMessage}
                    />
                </>
            )}
        </div>
    );
};

export default Chat;
