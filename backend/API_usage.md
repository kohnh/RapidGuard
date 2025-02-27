# Fire Incident API Endpoints Documentation

**Base URL:** `http://54.167.238.174:5000`

---

## 1. POST `/ask`

**Description:**  
Handles interactive conversations with an AI assistant for fire incident management. Depending on the last message in the conversation thread, the endpoint either answers a direct question or updates the fire response solution based on new context.

### Request Details

- **Content-Type:** `application/json`
- **Parameters:**  
  - **conversation** (Array): An array of message objects representing the current conversation thread. Each message object should include:
    - **role** (String): e.g., `"user"`, `"assistant"`, or `"system"`.
    - **content** (String): The text content of the message.

### Example Request (cURL)
```bash
curl -X POST http://54.167.238.174:5000/ask \
  -H "Content-Type: application/json" \
  -d '{
        "conversation": [
            {"role": "user", "content": "Is there any update on the fire situation?"}
        ]
      }'
```
### Example Request (JavaScript - using fetch)
```javascript
fetch('http://54.167.238.174:5000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    conversation: [
      { role: "user", content: "Is there any update on the fire situation?" }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log('Conversation:', data.conversation))
  .catch(error => console.error('Error:', error));
```

### Response

**Success (HTTP 200):**
```json
{
    "conversation": [
        {"role": "system", "content": "<Default system prompt with context>"},
        {"role": "user", "content": "Is there any update on the fire situation?"},
        {"role": "assistant", "content": "<Response based on the question or updated context>"}
    ]
}
```

**Error (HTTP 400):**
```json
{
    "error": "<Error message>"
}
```

## 2. POST `/context_update`

**Description:**
Updates the fire response solution using the latest fire situation and any additional user context. This endpoint appends a new solution message to the existing conversation thread.

### Request Details
- **Content-Type:** `application/json`
- **Parameters:**
  - **conversation** (Array):  An array of message objects representing the current conversation thread.

### Example Request (cURL)
```bash
curl -X POST http://54.167.238.174:5000/context_update \
  -H "Content-Type: application/json" \
  -d '{
        "conversation": [
            {"role": "user", "content": "Please update the fire response plan with the latest details."}
        ]
      }'
```

### Example Request (JavaScript - using fetch)
```javascript
fetch('http://54.167.238.174:5000/context_update', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    conversation: [
      { role: "user", content: "Please update the fire response plan with the latest details." }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log('Updated Conversation:', data.conversation))
  .catch(error => console.error('Error:', error));
```

### Response

**Success (HTTP 200):**
```json
{
    "conversation": [
        {"role": "user", "content": "Please update the fire response plan with the latest details."},
        {"role": "assistant", "content": "I have updated the solution based on the latest fire situation and your context. \n <Updated solution text>"}
    ]
}
```

**Error (HTTP 400):**
```json
{
    "error": "<Error message>"
}
```