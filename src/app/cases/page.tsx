"use client";

import { useState } from "react";
import { ChevronRight } from "lucide-react";

interface ExpandableSectionProps {
    title: string;
    content: string;
}

function ExpandableSection({ title, content }: ExpandableSectionProps) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div className="mb-2">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between p-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] rounded text-left"
            >
                <span className="text-gray-300">{title}</span>
                <ChevronRight
                    className={`h-4 w-4 text-gray-400 transform transition-transform ${isExpanded ? "rotate-90" : ""}`}
                />
            </button>
            {isExpanded && (
                <div className="p-3 text-sm text-gray-400 bg-[#1a1a1a] mt-1 rounded">
                    {content}
                </div>
            )}
        </div>
    );
}

export default function Cases() {
    return (
        <>
            <ExpandableSection
                title="Active Cases"
                content="Case #1234 - Suspicious Activity
          Case #1235 - Unauthorized Access
          Case #1236 - Security Breach"
            />
            <ExpandableSection
                title="Resolved Cases"
                content="Case #1230 - False Alarm
          Case #1231 - System Test
          Case #1232 - Maintenance"
            />
        </>
    );
}
