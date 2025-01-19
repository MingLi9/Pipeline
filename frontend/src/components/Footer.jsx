import React from "react";
import { Link } from "react-router-dom";
import apps from "./apps"; // Import the shared apps list
import styles from "./footer.module.css";

const Footer = () => {
    return (
        <footer className={styles.footer}>
            <ul className={styles.list}>
                {apps.map((app, index) => (
                    <li key={app.id} className={styles.listItem}>
                        <Link to={app.path} className={styles.link}>
                            {app.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </footer>
    );
};

export default Footer;
