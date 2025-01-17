# dverse-gateway
This repo contais the API gateway service it is our ingress to the outside world, built using Flask and integrates with NATS and Matrix services.

## NATS and Matrix integration
It needs to listen to NATS and API calls. This means that 2 "apps" are running at the same time. Because NATS cant call an endpoint and is based on Websockets, the Gateway needs to subscribe to channels on NATS.

using server.register_blueprint() allows us to have a cleaner overview of the endpoint because we can split the endpoint over multiple files. Each file for a group of endpoints dedicated to 1 cause.
in this case using it for the NATS_Client for http://localhost:8080/bots
Having the endpoints:
- /ask_connection: having the functionality to ask the services connection with the NATS to publish their account info in order for the Matrix-Gateway to create a client for them.
- /chat_message: having the functionality to publish a new message from Matrix to the NATS so all services can act on this new message.

Currently only listening to "send.matrix.message"-channel on NATS.
this provides the services connected with NATS to send messages to Matrix. Ofcourse only when they provide the right information and have an active client running for them.