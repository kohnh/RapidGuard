"use client";

import { Card } from "@/components/ui/card";
import { type CoreMessage } from "ai";
import { useState } from "react";
import { useEffect } from "react";
import { continueTextConversation } from "@/app/actions";
import { readStreamableValue } from "ai/rsc";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { IconArrowUp } from "@/components/ui/icons";
import Link from "next/link";
import SummaryCard from "@/components/cards/summarycard";
import Image from "next/image";
export const maxDuration = 30;

export default function Chat() {
    const [messages, setMessages] = useState<[]>([]);
    // const [messages, setMessages] = useState<CoreMessage[]>([]);
    const [input, setInput] = useState<string>("");

    // const handleSubmit = async (e: React.FormEvent) => {
    //     e.preventDefault();
    //     const newMessages: CoreMessage[] = [
    //         ...messages,
    //         { content: input, role: "user" },
    //     ];
    //     setMessages(newMessages);
    //     setInput("");
    //     const result = await continueTextConversation(newMessages);
    //     for await (const content of readStreamableValue(result)) {
    //         setMessages([
    //             ...newMessages,
    //             {
    //                 role: "assistant",
    //                 content: content as string,
    //             },
    //         ]);
    //     }
    // };
    console.log(messages);
    const clearChat = () => {
        localStorage.removeItem("chatMessages");
        setMessages([]); // Also clear the state
    };

    useEffect(() => {
        // Load messages from localStorage when component mounts
        const savedMessages = localStorage.getItem("chatMessages");
        if (savedMessages) {
            setMessages(JSON.parse(savedMessages));
        }
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        // const newMessages: CoreMessage[] = [
        const newMessages = [...messages, { content: input, role: "user" }];

        setMessages(newMessages);
        localStorage.setItem("chatMessages", JSON.stringify(newMessages)); // Save messages

        const temp = input;
        setInput("");
        const result = await continueTextConversation(messages, temp);
        setMessages(result);

        localStorage.setItem("chatMessages", JSON.stringify(result)); // Update storage
        console.log(
            "chat side----------------------------------------------------------------"
        );
        console.log(result);
        console.log(
            "chat side----------------------------------------------------------------"
        );
        console.log(messages);

        //   for await (const content of readStreamableValue(result)) {
        //     const updatedMessages = [
        //       ...newMessages,
        //       { role: "assistant", content: content as string },
        //     ];
        //     setMessages(updatedMessages);
        //     localStorage.setItem("chatMessages", JSON.stringify(updatedMessages)); // Update storage
        //   }
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
                                className={`${message.role === "user" ? "bg-slate-700 ml-auto" : "bg-transparent"} p-2 rounded-lg`}
                            >
                                {message.content as string}
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
                                <Input
                                    type="text"
                                    value={input}
                                    onChange={(event) => {
                                        setInput(event.target.value);
                                    }}
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
                            {/* {messages.length > 1 && (
                                <div className="text-center">
                                    <Link
                                        href="/genui"
                                        className="text-xs text-blue-400"
                                    >
                                        Try GenUI and streaming components
                                        &rarr;
                                    </Link>
                                </div>
                            )} */}
                        </form>
                    </Card>
                </div>
            </div>
        </div>
    );
}
