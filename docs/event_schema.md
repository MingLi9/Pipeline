# EventMessage Schema Documentation

DVerse uses events for its vocabulary, which is advantageous because events encompass all the common terms needed to represent activities and content flowing through a social network. This schema defines the structure for event messages in a system and is intended for use in microservice architectures, where events are sent to NATS.io queues and processed by various services.

## Generic Event Schema

This is a generic model that serves as a template for event messages.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "title": "EventMessage",
  "type": "object",
  "required": ["event_id", "timestamp", "platform", "service", "event_type", "actor", "object"],
  "properties": {
    "event_id": {
      "type": "string",
      "description": "Unique identifier for the event, typically a UUID"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp in ISO 8601 format (e.g., 2024-11-13T12:34:56Z)"
    },
    "platform": {
      "type": "string",
      "description": "Name of the platform generating the event (e.g., LineVerse, MarketPlace)"
    },
    "service": {
      "type": "string",
      "description": "Name of the service within the platform (e.g., auth, toots)"
    },
    "event_type": {
      "type": "string",
      "description": "Type of event (e.g., post, chat, like, share, buy), representing the action taken"
    },
    "actor": {
      "type": "object",
      "description": "Details about the user or entity that triggered the event",
      "required": ["actor_id", "username"],
      "properties": {
        "actor_id": {
          "type": "string",
          "description": "Unique identifier for the actor (user or system) performing the action"
        },
        "username": {
          "type": "string",
          "description": "Username of the actor"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "Email address of the actor (optional)"
        }
      }
    },
    "object": {
      "type": "object",
      "description": "Object related to the event (e.g., a specific post, product, or comment)",
      "additionalProperties": true
    }
  }
}
```

## Schema Details

### Root Object

The root of the schema represents the event message and must contain the following required fields:

### 1. **event_id (string) [Required]**

A unique identifier for the event (e.g., a UUID).

**Example:**
```json
"event_id": "123e4567-e89b-12d3-a456-426614174000"
```


### 2. **timestamp (string) [Required]**

The timestamp of the event in ISO 8601 format.

**Example:**
```json
"timestamp": "2024-11-13T12:34:56Z"
```


### 3. **platform (string) [Required]**

The name of the platform where the event took place.

**Example:**
```json
"platform": "LineVerse"
```


### 4. **service (string) [Required]**

The service within the platform that generated the event.

**Example:**
```json
"service": "content"
```


### 5. **event_type (string) [Required]**

The type of the event or action performed.

**Example:**
```json
"event_type": "post"
```


### actor Object (Required)

Contains details about the user or entity performing the event:

1. **actor_id (string) [Required]**  
   A unique identifier for the actor (e.g., a user ID or system identifier).

   **Example:**
   ```json
   "actor_id": "user-987"
   ```

2. **username (string) [Required]**  
   The username of the actor.

   **Example:**
   ```json
   "username": "john_doe"
   ```

3. **email (string) [Optional]**  
   The email address of the actor (if available).

   **Example:**
   ```json
   "email": "john@example.com"
   ```


### object Object (Required)

The main object involved in the event (e.g., the content of a post, product details, etc.). The `additionalProperties: true` allows for flexibility in the data, meaning you can add any relevant fields related to the event.

**Example (Post Event):**

```json
"object": {
  "post_id": "post-123",
  "content": "This is my first post!",
  "media_url": "https://example.com/image.jpg",
  "tags": ["intro", "firstpost"],
  "visibility": "public"
}
```

## Usage Examples

### 1. **User Posting a Toot**

```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2024-11-13T12:34:56Z",
  "platform": "LineVerse",
  "service": "content",
  "event_type": "post",
  "actor": {
    "actor_id": "user-987",
    "username": "john_doe",
    "email": "john@example.com"
  },
  "object": {
    "toot_id": "toot-456",
    "content": "Here's my first post on LineVerse!",
    "media_url": "https://example.com/image.jpg",
    "tags": ["introduction", "firstpost"],
    "visibility": "public"
  }
}
```


### 2. **User Buying a Product**

```json
{
  "event_id": "789e1234-e89b-12d3-a456-426614174111",
  "timestamp": "2024-11-13T15:20:30Z",
  "platform": "MarketPlace",
  "service": "purchase",
  "event_type": "buy",
  "actor": {
    "actor_id": "user-456",
    "username": "jane_smith",
    "email": "jane@example.com"
  },
  "object": {
    "product_id": "prod-123",
    "product_name": "Wireless Headphones",
    "price": 59.99,
    "currency": "USD",
    "quantity": 1,
    "total_price": 59.99,
    "order_id": "order-789",
    "payment_method": "credit_card",
    "shipping_address": {
      "street": "123 Maple St",
      "city": "Anytown",
      "state": "CA",
      "zip": "90210",
      "country": "USA"
    }
  }
}
```


## Additional Notes

- **Flexible Data:** The `object` field can include additional properties based on the event type, which makes this schema adaptable to various event types (e.g., product details, post content).
  
- **Optional Fields:** Some fields, like the actor's email, are optional and can be omitted if not relevant to the event.


## Conclusion

This schema provides a structured and flexible way to represent events across different platforms and services. It ensures consistency while allowing for a variety of event types and data to be included, facilitating seamless integration across microservices in event-driven architectures.
