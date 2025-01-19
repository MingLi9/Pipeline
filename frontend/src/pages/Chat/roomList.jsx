import React from "react";
import PropTypes from "prop-types";
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
RoomList.propTypes = {
    rooms: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            name: PropTypes.string.isRequired,
        })
    ).isRequired,
    onJoinRoom: PropTypes.func.isRequired,
};

export default RoomList;
