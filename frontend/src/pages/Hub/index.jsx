import React from "react";
import { Link } from "react-router-dom";
import apps from "../../components/apps";
import styles from "./hub.module.css";

const Hub = () => {
    return (
        <div className={styles.container}>
            <h1 className={styles.header}>Welcome to the Hub</h1>
            <p className={styles.description}>Select an app to navigate:</p>
            <ul className={styles.list}>
                {apps.map((app, index) => (
                    <li key={app.id} className={styles.listItem}>
                        <Link to={app.path} className={styles.link}>
                            {app.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Hub;
