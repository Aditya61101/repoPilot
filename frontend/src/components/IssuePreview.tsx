import type { Issue } from "../interfaces/Issue";
import { cn } from "@/lib/utils";

export function IssuePreview({ issue }: { issue: Issue | null }) {
    if (!issue) {
        return (
            <div className="flex items-center justify-center h-100 text-muted-foreground font-sans">
                Select an issue to preview
            </div>
        );
    }

    const createdDate = new Date(issue.createdAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });

    return (
        <div className="border border-border rounded-md h-100 flex flex-col">
            {/* Header */}
            <div className="p-4 border-b border-border">
                <h2 className="text-base font-semibold text-foreground font-sans mb-3">
                    {issue.title}
                </h2>
                <div className="space-y-2 text-xs text-muted-foreground">
                    {/* Metadata row */}
                    <div className="flex items-center gap-4">
                        <span className="font-mono">#{issue.id}</span>
                        <span className={cn(
                            "capitalize px-2 py-0.5 rounded font-sans",
                            "bg-muted text-muted-foreground"
                        )}>
                            {issue.state}
                        </span>
                        <span className="font-mono">{createdDate}</span>
                    </div>
                    {/* Labels */}
                    <div className="flex flex-wrap gap-1">
                        {issue.labels?.map((label) => {
                            const bg = `#${label.color}`
                            return (
                                <span
                                    key={label.name}
                                    style={{
                                        backgroundColor: `#${label.color}33`,
                                        color: bg,
                                        border: `1px solid #${label.color}66`
                                    }}
                                    className="px-2 py-0.5 rounded-full text-xs font-sans"
                                >
                                    {label.name}
                                </span>
                            )
                        })}
                    </div>
                </div>
            </div>
            {/* Body */}
            <div className="flex-1 overflow-y-auto p-4">
                {issue.body != 'null' ? (
                    <p className="text-sm text-foreground font-sans whitespace-pre-wrap leading-relaxed">
                        {issue.body}
                    </p>
                ) : (
                    <p className="text-sm text-muted-foreground font-sans italic">
                        No description provided.
                    </p>
                )}
            </div>
        </div>
    );
}