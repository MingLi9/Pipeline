import React from "react";
import styles from "./chat.module.css";

const MessageList = ({ messages }) => (
    <div className={styles.messageContainer}>
        <h2>Messages</h2>
        <div className={styles.messageBox}>
            {messages.map((msg, index) => (
                <div key={index} className={styles.message}>
                    <strong>{msg.sender}</strong>: {msg.content}
                </div>
            ))}
        </div>
    </div>
);

export default MessageList;
