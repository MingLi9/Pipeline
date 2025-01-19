import React from "react";
import PropTypes from "prop-types";
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

InviteUserForm.propTypes = {
    inviteUserId: PropTypes.string.isRequired,
    setInviteUserId: PropTypes.func.isRequired,
    onInviteUser: PropTypes.func.isRequired,
};

export default InviteUserForm;
