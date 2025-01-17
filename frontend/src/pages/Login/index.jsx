import React, { useEffect, useState } from "react";
import * as sdk from "matrix-js-sdk";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import styles from "./login.module.css";

window.global = window;

const LoginPage = ({ onLoginComplete }) => {
    const [client, setClient] = useState(null);

    useEffect(() => {
        const matrixClient = sdk.createClient({
            baseUrl: "https://matrix.org", // Replace with your Matrix server URL
        });
        setClient(matrixClient);
        toast.info("Matrix client initialized.");
    }, []);

    const handleSSOLogin = () => {
        if (!client) {
            toast.error("Matrix client not initialized. Please try again.");
            return; // Prevent further execution
        }

        const ssoUrl = client.getSsoLoginUrl(`${window.location.origin}/`);
        toast.info("Redirecting to SSO login...");
        window.location.href = ssoUrl;
    };


    const completeSSOLogin = async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const loginToken = urlParams.get("loginToken");

        if (client && loginToken) {
            try {
                await client.login("m.login.token", { token: loginToken });
                await client.startClient({ initialSyncLimit: 100 });

                /* istanbul ignore next */
                client.once("sync", (state) => {
                    if (state === "PREPARED") {
                        toast.success("Login successful. Matrix client is ready.");
                        onLoginComplete(client); // Pass the client back to the parent.
                    }
                });
            } catch (error) {
                /* istanbul ignore next */
                toast.error("SSO Login failed. Please try again.");
                /* istanbul ignore next */
                console.error("SSO Login failed:", error); // Retain for debugging.
            }
        } else if (!loginToken) {
            toast.warn("No login token found. Please log in again.");
        }
    };

    useEffect(() => {
        completeSSOLogin();
    }, [client]);

    return (
        <div className={styles.container}>
            <ToastContainer position="top-right" autoClose={3000} hideProgressBar closeOnClick />
            <h1 className={styles.header}>Welcome to Matrix Chat</h1>
            <button className={styles.button} onClick={handleSSOLogin}>
                Log In with SSO
            </button>
        </div>
    );
};

export default LoginPage;
