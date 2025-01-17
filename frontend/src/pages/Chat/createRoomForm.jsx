import React from "react";
import styles from "./chat.module.css";

const CreateRoomForm = ({ newRoomName, setNewRoomName, onCreateRoom }) => (
    <div className={styles.createRoomContainer}>
        <h2>Create a Room</h2>
        <input
            type="text"
            placeholder="Room Name"
            value={newRoomName}
            onChange={(e) => setNewRoomName(e.target.value)}
            className={styles.input}
        />
        <button className={styles.button} onClick={onCreateRoom}>
            Create Room
        </button>
    </div>
);

export default CreateRoomForm;
