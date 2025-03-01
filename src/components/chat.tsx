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
import ReactMarkdown from "react-markdown";

export default function Chat() {
    const [messages, setMessages] = useState<CoreMessage[]>([]);
    const { activeCases } = useAppState();
    const [input, setInput] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    // Track the number of context_update calls.
    const [contextUpdateCount, setContextUpdateCount] = useState<number>(0);
    // New state to manage custom alert messages.
    const [alertMessage, setAlertMessage] = useState<string | null>(null);

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

    // Automatically dismiss the alert after 15 seconds.
    useEffect(() => {
        if (alertMessage) {
            const timer = setTimeout(() => {
                setAlertMessage(null);
            }, 15000);
            return () => clearTimeout(timer);
        }
    }, [alertMessage]);

    // Setup the Socket.IO client to listen for file change events.
    useEffect(() => {
        // Create a socket connection to the backend.
        const socket = io("http://54.159.85.234:5000", {
            transports: ["websocket"],
            reconnection: true,
        });

        // Log when the socket is connected.
        socket.on("connect", () => {
            console.log("Socket connected with id:", socket.id);
        });

        // Optionally, log connection errors.
        socket.on("connect_error", (error) => {
            console.error("Socket connection error:", error);
        });

        // Listen for the "file_changed" event.
        socket.on("file_changed", (data_from_file_change: any) => {
            console.log("Received file_changed event:", data_from_file_change);

            // Trigger the /context_update endpoint to get the updated conversation.
            axios.post("http://54.159.85.234:5000/context_update", {
                conversation: messagesRef.current,
            })
            .then((response) => {
                console.log("Context update response:", response.data);
                if (response.data && response.data.conversation) {
                    // Show a custom alert based on the number of previous updates.
                    console.log(data_from_file_change.message)
                    if (data_from_file_change.message.includes("fire_context.txt")) {
                        console.log("an alert should appear because fire_context.txt changed")
                        setContextUpdateCount((prevCount) => {
                            if (prevCount === 0) {
                                setAlertMessage("There is a fire! Here is the initial solution based on the latest information we have.");
                            } else {
                                setAlertMessage("We have updates in the fire situation, here is the updated solution!");
                            }
                            return prevCount + 1;
                        })
                    };

                    // parse through the chat thread to remove backticks and the word "markdown"
                    const cleanedConversation = response.data.conversation.map((msg: CoreMessage) => ({
                        ...msg,
                        content: msg.content.replace(/`/g, "").replace(/\bmarkdown\b/gi, "")
                      }));

                    // Replace the current chat thread with the updated conversation.
                    setMessages(cleanedConversation);
                    localStorage.setItem("chatMessages", JSON.stringify(cleanedConversation));
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
        <div className="group w-full overflow-auto custom-scrollbar relative">
            {/* Custom Alert */}
            {alertMessage && (
                <div className="fixed inset-0 flex items-center justify-center z-50">
                    <div className="bg-white border-4 border-red-500 p-6 rounded shadow-lg text-center text-black">
                        {alertMessage}
                    </div>
                </div>
            )}

            {messages.length <= 0 ? (
                <SummaryCard />
            ) : (
                <div className="max-w-xl mx-auto mt-10 mb-24">
                    {messages.map((message, index) => (
                        <div key={index} className="whitespace-pre-wrap flex mb-5">
                            <div
                                className={`${
                                    message.role === "user" ? "bg-slate-700 ml-auto" : "bg-cyan-900"
                                } p-2 rounded-lg`}
                            >
                                <ReactMarkdown>{message.content}</ReactMarkdown>
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
                                    onChange={(event) => setInput(event.target.value)}
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
                        </form>
                    </Card>
                </div>
            </div>
        </div>
    );
}
