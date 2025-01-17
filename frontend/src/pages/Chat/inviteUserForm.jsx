import React from "react";
import styles from "./chat.module.css";

const InviteUserForm = ({ inviteUserId, setInviteUserId, onInviteUser }) => (
    <div className={styles.inviteUserContainer}>
        <h2>Invite Users</h2>
        <input
            type="text"
            placeholder="Matrix User ID (e.g., @username:matrix.org)"
            value={inviteUserId}
            onChange={(e) => setInviteUserId(e.target.value)}
            className={styles.input}
        />
        <button className={styles.button} onClick={onInviteUser}>
            Invite
        </button>
    </div>
);

export default InviteUserForm;
