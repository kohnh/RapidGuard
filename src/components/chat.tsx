"use client";

import { Card } from "@/components/ui/card";
import { type CoreMessage } from "ai";
import { useState, useEffect } from "react";
import { continueTextConversation } from "@/app/actions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { IconArrowUp } from "@/components/ui/icons";
import Link from "next/link";
import SummaryCard from "@/components/cards/summarycard";
import Image from "next/image";
import { useAppState } from "@/context/StateContext";

export default function Chat() {
  const [messages, setMessages] = useState<CoreMessage[]>([]);
  const { activeCases } = useAppState();
  const [input, setInput] = useState<string>("");

  // Clear the chat state and localStorage whenever the website is loaded.
  useEffect(() => {
    localStorage.removeItem("chatMessages");
    setMessages([]);
  }, []);

  const clearChat = () => {
    localStorage.removeItem("chatMessages");
    setMessages([]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
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
  };

  return (
    <div className="group w-full overflow-auto custom-scrollbar">
      {messages.length <= 0 ? (
        <SummaryCard />
      ) : (
        <div className="max-w-xl mx-auto mt-10 mb-24">
          {messages.map((message, index) => (
            <div key={index} className="whitespace-pre-wrap flex mb-5">
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
              {/*
              {messages.length > 1 && (
                <div className="text-center">
                  <Link href="/genui" className="text-xs text-blue-400">
                    Try GenUI and streaming components &rarr;
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