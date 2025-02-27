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

    const response = await fetch("http://54.167.238.174:5000/ask", {
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

// // Streaming Chat
// export async function continueTextConversation(
//     messages: CoreMessage[],
//     input: string
// ) {
//     try {
//         const response = await fetch("http://54.167.238.174:5000/ask", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 conversation: messages,
//                 question: input,
//                 initial_solution: "<solution text from /generate_solution>",
//             }),
//         });

//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }

//         const data = await response.json();
//         console.log("Conversation:", data.conversation);

//         return data.conversation; // Ensure the function properly returns the conversation array
//     } catch (error) {
//         console.error("Error:", error);
//         return []; // Return an empty array in case of failure
//     }
//     // const result = await streamText({
//     //     model: google("gemini-1.5-flash"),
//     //     // model: openai("gpt-4-turbo"),
//     //     messages,
//     // });

//     // const stream = createStreamableValue(result.textStream);
//     // return stream.value;
// }

// Gen UIs
export async function continueConversation(history: Message[]) {
    const stream = createStreamableUI();

    const { text, toolResults } = await generateText({
        model: google("gemini-1.5-flash"),
        // model: openai("gpt-3.5-turbo"),
        system: "You are a friendly weather assistant!",
        messages: history,
        tools: {
            showWeather: {
                description: "Show the weather for a given location.",
                parameters: z.object({
                    city: z
                        .string()
                        .describe("The city to show the weather for."),
                    unit: z
                        .enum(["F"])
                        .describe("The unit to display the temperature in"),
                }),
                execute: async ({ city, unit }) => {
                    stream.done(<Weather city={city} unit={unit} />);
                    return `Here's the weather for ${city}!`;
                },
            },
        },
    });

    return {
        messages: [
            ...history,
            {
                role: "assistant" as const,
                content:
                    text ||
                    toolResults.map((toolResult) => toolResult.result).join(),
                display: stream.value,
            },
        ],
    };
}

// Utils
export async function checkAIAvailability() {
    const envVarExists = !!process.env.GOOGLE_GENERATIVE_AI_API_KEY;
    // const envVarExists = !!process.env.OPENAI_API_KEY;
    return envVarExists;
}
