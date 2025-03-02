"use client";

import { useState } from "react";

interface SettingsSelectProps {
    label: string;
    value: string;
    options: string[];
    onChange: (value: string) => void;
}

function SettingsSelect({
    label,
    value,
    options,
    onChange,
}: SettingsSelectProps) {
    return (
        <div className="flex items-center justify-between mb-4">
            <label className="text-gray-300">{label}</label>
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="bg-[#1a1a1a] text-gray-300 px-3 py-2 rounded border border-[#333] focus:outline-none focus:border-gray-500"
            >
                {options.map((option) => (
                    <option key={option} value={option}>
                        {option}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default function Settings() {
    const [resolution, setResolution] = useState("1080p");
    const [frameRate, setFrameRate] = useState("30fps");
    const [nightMode, setNightMode] = useState("Enabled");
    const [emailAlerts, setEmailAlerts] = useState("Enabled");
    const [pushNotifications, setPushNotifications] = useState("Disabled");
    const [alertFrequency, setAlertFrequency] = useState("High");
    return (
        <div className="group p-4 overflow-auto custom-scrollbar">
            <div className="space-y-6">
                <div className="bg-[#1a1a1a] p-4 rounded">
                    <h3 className="text-gray-200 font-medium mb-4">
                        Camera Settings
                    </h3>
                    <SettingsSelect
                        label="Resolution"
                        value={resolution}
                        options={["144p", "240p", "480p", "720p", "1080p"]}
                        onChange={setResolution}
                    />
                    <SettingsSelect
                        label="Frame Rate"
                        value={frameRate}
                        options={["24fps", "30fps", "60fps"]}
                        onChange={setFrameRate}
                    />
                    <SettingsSelect
                        label="Night Mode"
                        value={nightMode}
                        options={["Enabled", "Disabled", "Auto"]}
                        onChange={setNightMode}
                    />
                </div>

                <div className="bg-[#1a1a1a] p-4 rounded">
                    <h3 className="text-gray-200 font-medium mb-4">
                        Notification Settings
                    </h3>
                    <SettingsSelect
                        label="Email Alerts"
                        value={emailAlerts}
                        options={["Enabled", "Disabled"]}
                        onChange={setEmailAlerts}
                    />
                    <SettingsSelect
                        label="Push Notifications"
                        value={pushNotifications}
                        options={["Enabled", "Disabled"]}
                        onChange={setPushNotifications}
                    />
                    <SettingsSelect
                        label="Alert Frequency"
                        value={alertFrequency}
                        options={["Low", "Medium", "High"]}
                        onChange={setAlertFrequency}
                    />
                </div>
            </div>
        </div>
    );
}
