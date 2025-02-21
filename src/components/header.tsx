"use client";

import * as React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { IconSeparator } from "@/components/ui/icons";
// import EnvCard from "./cards/envcard";
import Image from "next/image";
import { useState } from "react";

export default function Header() {
    const [activeTab, setActiveTab] = useState("Dashboard");
    return (
        <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 ">
            {/* <EnvCard /> */}

            <Link
                href="/"
                rel="nofollow"
                onClick={() => setActiveTab("root")}
                className={cn(
                    buttonVariants({
                        variant: activeTab === "root" ? "secondary" : "link",
                    }),
                    "mr-2 font-bold  flex items-center gap-2"
                )}
            >
                <Image
                    src="/drms.svg"
                    alt="DRMS Logo"
                    width={28}
                    height={28}
                    // className="rounded-lg bg-slate-500"
                />
                <span>Disaster Recovery Management System (DRMS)</span>
            </Link>
            {/* <IconSeparator /> */}
            <Link
                href="/dashboard"
                onClick={() => setActiveTab("dashboard")}
                className={cn(
                    buttonVariants({
                        variant:
                            activeTab === "dashboard" ? "secondary" : "link",
                    }),
                    "m-auto font-normal"
                )}
            >
                <span className="hidden md:flex">Dashboard</span>
            </Link>
            {/* <IconSeparator /> */}
            <Link
                href="/cases"
                onClick={() => setActiveTab("cases")}
                className={cn(
                    buttonVariants({
                        variant: activeTab === "cases" ? "secondary" : "link",
                    }),
                    "m-auto font-normal"
                )}
            >
                <span className="hidden md:flex">Cases</span>
            </Link>
            <Link href="/settings" className={cn(buttonVariants())}>
                <Image
                    src="/setting.svg"
                    alt="setting"
                    width={32}
                    height={32}
                />
            </Link>
        </header>
    );
}
