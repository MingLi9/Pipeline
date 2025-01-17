# NATS Server for Group Project

This folder contains the necessary configuration to set up a NATS server for event-driven communication in the group project.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Publisher & Subscriber Scripts](#publisher--subscriber-scripts)
- [How to Test](#how-to-test)
- [Monitoring NATS](#monitoring-nats)
- [Troubleshooting](#troubleshooting)

## Overview

The **NATS server** is set up using Docker and Docker Compose to facilitate real-time, event-driven communication across the services in the project. The provided setup includes:
- A **Dockerfile** for running NATS.
- **Docker Compose** configuration to easily manage the server.
- Example **publisher** and **subscriber** Python scripts to test message communication.

## Prerequisites

To run and test the NATS server, ensure you have the following tools installed:
- **Docker** and **Docker Compose**
- **Python 3.10+** (for running test scripts)

## Setup Instructions

### Step 1: Clone the Repository

First, navigate to the group project repo and find the NATS server setup in the **nats-server** folder.

```bash
git clone https://github.com/fuas-dverse/group.git
cd group/nats-server
```

### Step 2: Running the NATS Server

The NATS server can be launched using Docker Compose.

1. **Run the following command** in the terminal:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Set up the NATS server.
   - Expose the necessary ports:
     - `4222`: For client connections.
     - `8222`: For monitoring NATS.
     - `6222`: For internal cluster communication (optional).

2. **Stopping the Server**:
   When you're done, you can stop the server with:
   ```bash
   docker-compose down
   ```

## Publisher & Subscriber Scripts

### Publisher (`pub.py`)
This script is designed to publish a message to a specific subject (`test`) on the NATS server. It connects to the server at `nats://localhost:4222` and sends a message such as `"Hello NATS!"`.

### Subscriber (`sub.py`)
This script listens for messages on the same subject (`test`). Once a message is published, it receives and displays it.

Both scripts use the **asyncio** library to handle asynchronous communication with the NATS server.

## How to Test

1. **Run the Subscriber**:
   - Start the subscriber first to listen for messages:
     ```bash
     python sub.py
     ```

2. **Run the Publisher**:
   - In another terminal, run the publisher to send a message:
     ```bash
     python pub.py
     ```

3. **Expected Output**:
   - In the subscriber terminal, you should see:
     ```bash
     Received a message: Hello NATS!
     ```

## Monitoring NATS

You can monitor the NATS server by accessing the monitoring port at `http://localhost:8222`. This will provide information about active connections, subscriptions, and other useful metrics.

## Troubleshooting

- **Connection Issues**: If you are having trouble connecting to the NATS server, ensure that Docker is running and check that the correct ports are exposed.
- **Python Errors**: Ensure you have the necessary Python dependencies installed via the `requirements.txt` file by running:
   ```bash
   pip install -r requirements.txt
   ```