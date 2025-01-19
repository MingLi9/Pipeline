import React from "react";
import PropTypes from "prop-types";
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

CreateRoomForm.propTypes = {
    newRoomName: PropTypes.string.isRequired,
    setNewRoomName: PropTypes.func.isRequired,
    onCreateRoom: PropTypes.func.isRequired,
};

export default CreateRoomForm;
