import React from "react";
import styles from "./chat.module.css";

const RoomList = ({ rooms, onJoinRoom }) => (
    <div className={styles.roomContainer}>
        <h2>Available Rooms</h2>
        <ul className={styles.list}>
            {rooms.map((room) => (
                <li key={room.id} className={styles.listItem}>
                    {room.name} (ID: {room.id}){" "}
                    <button onClick={() => onJoinRoom(room.id)} className={styles.button}>
                        Join
                    </button>
                </li>
            ))}
        </ul>
    </div>
);

export default RoomList;
