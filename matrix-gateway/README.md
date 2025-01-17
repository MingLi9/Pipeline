# DVerse Matrix-Gateway
# Author: @MingLi9
# Date: 2024-12-02
# Description: Matrix client pool for bots from DVerse.
# Version: 1.0.0
# License: MIT License
# Copyright (c) 2022 Ming Li

# Matrix Microservice

This microservice manages multiple Matrix bot accounts and allows bots to send messages, listen to events, and interact with rooms.

## About this service
This service handles incomming messages from Matrix based on the active clients. All clients are bots, created within the DVerse network.
It provides an automatic joining protocol that allows the bots to accept every room invite that is sent to them.
On every new message received in every room for each bot seperate, a message is sent to the Gateway-service that will post this message on the event-bus(aka NATS)

When services want to sent a message to Matrix, they need to have a client in the client pool. Sending to the NATS a structured message containing the actual text-message, the Gateway will pick-up this message and forwards it to this service.
In this service the message is being send if also the sender and room_id are provided to specify who and where the message needs to be sent.

## Features
- Manage multiple bots with a client pool
- Send messages to Matrix rooms
- Listen for events like new messages
- REST API for bot management and messaging

## More API info
- For the swagger-ui: http://localhost:8000/docs
- For the openapi.json to import the template in Postman: http://localhost:8000/openapi.json

## Bot account names
- `chat-assistant`: @dverse-chat-assistant:matrix.org
- `chat-assistant2`: @dverse-chat-assistant2:matrix.org