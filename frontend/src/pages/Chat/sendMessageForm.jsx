import React from "react";
import PropTypes from "prop-types";
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

SendMessageForm.propTypes = {
    newMessage: PropTypes.string.isRequired,
    setNewMessage: PropTypes.func.isRequired,
    onSendMessage: PropTypes.func.isRequired,
};

export default SendMessageForm;
