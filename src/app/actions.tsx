"use server";

import { CoreMessage } from "ai";
import { ReactNode } from "react";

export interface Message {
    role: "user" | "assistant";
    content: string;
    display?: ReactNode;
}

// Streaming Chat
export async function continueTextConversation(
    messages: CoreMessage[],
    input: string
) {
    try {
        // Append the new user message to the conversation array
        const updatedConversation = [
            ...messages,
            { role: "user", content: input },
        ];

    const response = await fetch("http://54.159.85.234:5000/ask", {
    // const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      // Send only the conversation, as expected by the Flask endpoint.
      body: JSON.stringify({ conversation: updatedConversation })
    });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Updated Conversation:", data.conversation);

        // Return the updated conversation array received from the Flask endpoint.
        return data.conversation;
    } catch (error) {
        console.error("Error:", error);
        return []; // Return an empty array in case of failure
    }
}
