import React from "react";
import PropTypes from "prop-types";
import styles from "./chat.module.css";

const InviteList = ({ invites, onAcceptInvite }) => (
    <div className={styles.inviteContainer}>
        <h2>Room Invites</h2>
        <ul className={styles.list}>
            {invites.length > 0 ? (
                invites.map((invite) => (
                    <li key={invite.id} className={styles.listItem}>
                        {invite.name} (ID: {invite.id}){" "}
                        <button onClick={() => onAcceptInvite(invite.id)} className={styles.button}>
                            Accept
                        </button>
                    </li>
                ))
            ) : (
                <p className={styles.noInvites}>No pending invites.</p>
            )}
        </ul>
    </div>
);
InviteList.propTypes = {
    invites: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            name: PropTypes.string.isRequired,
        })
    ).isRequired,
    onAcceptInvite: PropTypes.func.isRequired,
};

export default InviteList;
