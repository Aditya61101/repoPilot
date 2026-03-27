import type { Issue } from "../interfaces/Issue";

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
            <div className="flex items-center justify-center h-100 text-gray-500">
                Select a repository to view issues
            </div>
        );
    }

    return (
        <div className="border border-gray-200 rounded-md h-100 overflow-y-auto">
            {issues.map((issue) => (
                <button
                    key={issue.id}
                    onClick={() => onSelectIssue(issue.id)}
                    className={`w-full text-left px-4 py-3 border-b border-gray-200 hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-inset ${selectedIssueId === issue.id
                            ? 'bg-indigo-50 border-l-4 border-l-indigo-500'
                            : ''
                        }`}
                >
                    <div className="flex items-baseline justify-between gap-2">
                        <p className="text-sm text-gray-800 truncate flex-1">
                            {issue.title}
                        </p>
                        <span className="text-xs text-gray-500 shrink-0">
                            #{issue.number}
                        </span>
                    </div>
                </button>
            ))}
        </div>
    );
}