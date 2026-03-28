import type { Issue } from "../interfaces/Issue";
import { cn } from "@/lib/utils";

export function IssueList({
    issues,
    selectedIssueId,
    onSelectIssue,
}: {
    issues: Issue[];
    selectedIssueId: number | null;
    onSelectIssue: (id: number) => void;
}) {
    if (issues.length === 0) {
        return (
            <div className="flex items-center justify-center h-100 text-muted-foreground font-sans">
                Select a repository to view issues
            </div>
        );
    }

    return (
        <div className="border border-border rounded-md h-100 overflow-y-auto">
            {issues.map((issue) => (
                <button
                    key={issue.id}
                    onClick={() => onSelectIssue(issue.id)}
                    className={cn(
                        "w-full text-left px-4 py-3 border-b border-border transition-colors",
                        "hover:bg-muted hover:cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary focus:ring-inset",
                        selectedIssueId === issue.id
                            ? "bg-primary/10 border-l-4 border-l-primary"
                            : "border-l-4 border-l-transparent"
                    )}
                >
                    <div className="flex items-baseline justify-between gap-2">
                        <p className="text-sm text-foreground font-sans truncate flex-1">
                            {issue.title}
                        </p>
                        <span className="text-xs text-muted-foreground font-mono shrink-0">
                            #{issue.id}
                        </span>
                    </div>
                </button>
            ))}
        </div>
    );
}