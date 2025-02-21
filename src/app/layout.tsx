import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import type React from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
    title: "DRMS",
    description: "Disaster Recovery Management System",
    icons: {
        icon: "/drms.svg",
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <body className={inter.className}>
                <Header />
                <main className="bg-muted/50 flex h-100vh flex-1 flex-col">
                    {children}
                </main>
            </body>
        </html>
    );
}
