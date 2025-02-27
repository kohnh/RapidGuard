"use client";

import { Card } from "@/components/ui/card";
import { type CoreMessage } from "ai";
import { useState, useEffect, useRef } from "react";
import { continueTextConversation } from "@/app/actions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { IconArrowUp } from "@/components/ui/icons";
import Link from "next/link";
import SummaryCard from "@/components/cards/summarycard";
import Image from "next/image";
import { useAppState } from "@/context/StateContext";
import io from "socket.io-client";
import axios from "axios";

export default function Chat() {
    const [messages, setMessages] = useState<CoreMessage[]>([]);
    const { activeCases } = useAppState();
    const [input, setInput] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    // Create a ref to always have access to the latest conversation state.
    const messagesRef = useRef(messages);
    useEffect(() => {
        messagesRef.current = messages;
    }, [messages]);

    // Clear the chat state and localStorage on initial load.
    useEffect(() => {
        localStorage.removeItem("chatMessages");
        setMessages([]);
    }, []);

    // Setup the Socket.IO client to listen for file change events.
    useEffect(() => {
        // Create a socket connection to the backend.
        // const socket = io("http://127.0.0.1:5001", { transports: ["websocket"] });
        const socket = io("http://127.0.0.1:5001");

        // Log when the socket is connected.
        socket.on("connect", () => {
            console.log("Socket connected with id:", socket.id);
        });

        // Optionally, log connection errors.
        socket.on("connect_error", (error) => {
            console.error("Socket connection error:", error);
        });

        // Listen for the "file_changed" event.
        socket.on("file_changed", (data: any) => {
            console.log("Received file_changed event:", data);

            // Trigger the /context_update endpoint to get the updated conversation.
            axios
                .post("http://127.0.0.1:5001/context_update", {
                    conversation: messagesRef.current,
                })
                .then((response) => {
                    console.log("Context update response:", response.data);
                    if (response.data && response.data.conversation) {
                        // Replace the current chat thread with the updated conversation.
                        setMessages(response.data.conversation);
                        localStorage.setItem(
                            "chatMessages",
                            JSON.stringify(response.data.conversation)
                        );
                    }
                })
                .catch((error) => {
                    console.error("Error updating conversation:", error);
                });
        });

        // Cleanup the socket connection when the component unmounts.
        return () => {
            socket.disconnect();
        };
    }, []);

    const clearChat = () => {
        localStorage.removeItem("chatMessages");
        setMessages([]);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Append the user's input to the conversation.
        const newMessages = [...messages, { content: input, role: "user" }];
        // Optimistically update the UI and save to localStorage.
        setMessages(newMessages);
        localStorage.setItem("chatMessages", JSON.stringify(newMessages));
        setInput("");

        // Query the Flask endpoint with the full conversation.
        const result = await continueTextConversation(newMessages);
        setMessages(result);
        localStorage.setItem("chatMessages", JSON.stringify(result));
        setLoading(false);
    };

    return (
        <div className="group w-full overflow-auto custom-scrollbar">
            {messages.length <= 0 ? (
                <SummaryCard />
            ) : (
                <div className="max-w-xl mx-auto mt-10 mb-24">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className="whitespace-pre-wrap flex mb-5"
                        >
                            <div
                                className={`${
                                    message.role === "user"
                                        ? "bg-slate-700 ml-auto"
                                        : "bg-transparent"
                                } p-2 rounded-lg`}
                            >
                                {message.content}
                            </div>
                        </div>
                    ))}
                </div>
            )}
            <div className="fixed inset-x-0 bottom-10 w-full ">
                <div className="w-full max-w-xl mx-auto">
                    <Card className="p-2">
                        <form onSubmit={handleSubmit}>
                            <div className="flex">
                                {loading ? (
                                    <div className="animate-spin rounded-full h-8 w-8 border-t-4 border-blue-950"></div>
                                ) : (
                                    <div></div>
                                )}
                                <Input
                                    type="text"
                                    value={input}
                                    onChange={(event) =>
                                        setInput(event.target.value)
                                    }
                                    className="w-[95%] mr-2 border-0 ring-offset-0 focus-visible:ring-0 focus-visible:outline-none focus:outline-none focus:ring-0 ring-0 focus-visible:border-none border-transparent focus:border-transparent focus-visible:ring-none"
                                    placeholder="Ask me anything..."
                                />
                                {messages.length <= 0 ? (
                                    <div></div>
                                ) : (
                                    <Button onClick={clearChat}>
                                        <Image
                                            src="/refresh.svg"
                                            alt="refresh"
                                            width={22}
                                            height={22}
                                        />
                                    </Button>
                                )}
                                <Button disabled={!input.trim()}>
                                    <IconArrowUp />
                                </Button>
                            </div>
                            {/* Additional UI elements can be added here */}
                        </form>
                    </Card>
                </div>
            </div>
        </div>
    );
}
