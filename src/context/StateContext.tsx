"use client";

import { createContext, useContext, useState, ReactNode } from "react";

interface CaseType {
    caseNumber: string;
    caseStatus: string;
    caseDescription: string;
    caseContext: string;
}

// Define the context type
interface StateContextType {
    activeCases: CaseType[];
    addActiveCase: (newCase: CaseType) => void;
    removeActiveCase: (caseNumber: string) => void;
    caseCount: number;
    setCaseCount: (count: number) => void;
}

// Create the context
const StateContext = createContext<StateContextType | undefined>(undefined);

// Context provider component
export function StateProvider({ children }: { children: ReactNode }) {
    const [activeCases, setActiveCases] = useState<CaseType[]>([]);
    const [caseCount, setCaseCount] = useState(0);
    const addActiveCase = (newCase: CaseType) => {
        setActiveCases((prevCases) => [...prevCases, newCase]);
    };

    return (
        <StateContext.Provider
            value={{ activeCases, addActiveCase, caseCount, setCaseCount }}
        >
            {children}
        </StateContext.Provider>
    );
}

// Custom hook to use context in child components
export function useAppState() {
    const context = useContext(StateContext);
    if (!context) {
        throw new Error("useAppState must be used within a StateProvider");
    }
    return context;
}
