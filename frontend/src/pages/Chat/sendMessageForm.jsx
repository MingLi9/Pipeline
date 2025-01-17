import React from "react";
import styles from "./chat.module.css";

const SendMessageForm = ({ newMessage, setNewMessage, onSendMessage }) => (
    <div className={styles.sendMessageContainer}>
        <h3>Send a Message</h3>
        <input
            type="text"
            placeholder="Type your message"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className={styles.input}
        />
        <button className={styles.button} onClick={onSendMessage}>
            Send
        </button>
    </div>
);

export default SendMessageForm;
