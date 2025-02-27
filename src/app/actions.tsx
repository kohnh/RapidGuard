"use server";

import { createStreamableValue } from "ai/rsc";
import { CoreMessage, streamText } from "ai";
import { openai } from "@ai-sdk/openai";
import { google } from "@ai-sdk/google";
import { Weather } from "@/components/weather";
import { generateText } from "ai";
import { createStreamableUI } from "ai/rsc";
import { ReactNode } from "react";
import { z } from "zod";

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
      { role: "user", content: input }
    ];

    // const response = await fetch("http://54.167.238.174:5000/ask", {
    const response = await fetch("http://127.0.0.1:5001/ask", {
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