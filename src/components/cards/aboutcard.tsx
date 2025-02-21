import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import Link from "next/link";

export default function AboutCard() {
    return (
        <div className="max-w-xl mx-auto mt-10">
            <Card>
                <CardHeader>
                    <CardTitle>No Active Case</CardTitle>
                    <CardDescription>
                        Nothing requires your attention
                    </CardDescription>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground/90 leading-normal prose">
                    <p className="mb-3">
                        Ask me anything about the system, I am here to help you.
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
