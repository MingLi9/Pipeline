import React from "react";
import PropTypes from "prop-types";
import styles from "./chat.module.css";

const MessageList = ({ messages }) => (
    <div className={styles.messageContainer}>
        <h2>Messages</h2>
        <div className={styles.messageBox}>
            {messages.map((msg, index) => (
                <div key={msg.id} className={styles.message}>
                    <strong>{msg.sender}</strong>: {msg.content}
                </div>
            ))}
        </div>
    </div>
);
MessageList.propTypes = {
    messages: PropTypes.arrayOf(
        PropTypes.shape({
            sender: PropTypes.string.isRequired,
            content: PropTypes.string.isRequired,
        })
    ).isRequired,
};

export default MessageList;
