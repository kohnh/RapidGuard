# Fire Incident API Endpoints Documentation

**Base URL:** `http://54.161.142.111:5000`

---

## 1. POST `/image_context`

**Description:**  
Analyzes a CCTV image for fire detection. Returns a formatted response detailing the fire (if detected) or indicates that no fire or smoke is present.

### Request Details

- **Content-Type:** `multipart/form-data`
- **Parameters:**  
  - **image** (File): JPEG image file uploaded with the key `"image"`.
  - **cctv_number** (String): Identifier for the CCTV camera. Must match one of the keys defined in the CCTV locations mapping.

### Example Request (cURL)
```bash
curl -X POST http://54.161.142.111:5000/image_context \
  -F "image=@fire_tampines_mall.jpeg" \
  -F "cctv_number=5"
```


### Example Request (JavaScript - using fetch)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]); // fileInput: HTML input element for file selection
formData.append('cctv_number', '5');

fetch('http://54.161.142.111:5000/image_context', {
  method: 'POST',
  body: formData,
})
  .then(response => response.json())
  .then(data => console.log('Image Context:', data.response))
  .catch(error => console.error('Error:', error));
```

### Response
Success (HTTP 200):
```json
{
    "response": "<OpenAI-generated analysis text>"
}
```

Error (HTTP 400/500):
```json
{
    "error": "<Error message>"
}
```

## 2. POST /generate_solution

Description:
Generates a detailed fire response plan based on the context provided by the image analysis. The plan includes multiple phases and integrates data such as manpower, mall layout, fire alarm stations, and the fire management SOP.

### Request Details
Content-Type: application/json

Payload:
```json
{
    "context": "<Context text from /image_context>"
}
```

### Example Request (cURL)
```bash
curl -X POST http://54.161.142.111:5000/generate_solution \
  -H "Content-Type: application/json" \
  -d '{"context": "context details from /image_context"}'
```

### Example Request (JavaScript - using fetch)
```javascript
fetch('http://54.161.142.111:5000/generate_solution', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    context: "context details from /image_context"
  })
})
  .then(response => response.json())
  .then(data => console.log('Generated Solution:', data.response))
  .catch(error => console.error('Error:', error));
```

### Response
Success (HTTP 200):
```json
{
    "response": "<OpenAI-generated fire response plan>"
}
```

Error (HTTP 400/500):
```json
{
    "error": "<Error message>"
}
```

## 3. POST /ask
Description:
Facilitates an interactive conversation with an AI assistant for follow-up questions or clarifications regarding the fire response plan. Maintains a conversation thread that includes both prior messages and new queries.

### Request Details
Content-Type: application/json

Payload:
```json
{
    "conversation": [
        // Array of message objects, e.g.,
        // {"role": "user", "content": "Where is the fire?"}
    ],
    "question": "<New question or context update>",
    "initial_solution": "<Response text from /generate_solution>"
}
```

### Example Request (cURL)
```bash
curl -X POST http://54.161.142.111:5000/ask \
  -H "Content-Type: application/json" \
  -d '{
        "conversation": [],
        "question": "Where is the fire?",
        "initial_solution": "<solution text from /generate_solution>"
      }'
```

### Example Request (JavaScript - using fetch)
```javascript
fetch('http://54.161.142.111:5000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    conversation: [],
    question: "Where is the fire?",
    initial_solution: "<solution text from /generate_solution>"
  })
})
  .then(response => response.json())
  .then(data => {
    // data.conversation is an array with the conversation thread
    console.log('Conversation:', data.conversation);
  })
  .catch(error => console.error('Error:', error));
```

### Response
Success (HTTP 200):
```json
{
    "conversation": [
        {"role": "system", "content": "<Default system prompt with context>"},
        {"role": "user", "content": "<User's question>"},
        {"role": "assistant", "content": "<Assistant's response>"}
        // Additional messages as the conversation continues.
    ]
}
```

Error (HTTP 400/500):
```json
{
    "error": "<Error message>"
}
```