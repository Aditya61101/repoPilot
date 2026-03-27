import type { Issue } from "../interfaces/Issue";


export function IssuePreview({ issue }: { issue: Issue | null }) {
    if (!issue) {
        return (
            <div className="flex items-center justify-center h-100 text-gray-500">
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
        <div className="border border-gray-200 rounded-md h-100 flex flex-col">
            <div className="p-4 border-b border-gray-200">
                <h2 className="text-base font-semibold text-gray-800 mb-3">
                    {issue.title}
                </h2>
                <div className="space-y-2 text-xs text-gray-600">
                    <div className="flex items-center gap-4">
                        <span>#{issue.number}</span>
                        <span className="capitalize px-2 py-0.5 rounded bg-gray-100 text-gray-700">
                            {issue.state}
                        </span>
                        <span>{createdDate}</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                        {issue.labels.map((label) => (
                            <span
                                key={label}
                                className="px-2 py-1 rounded text-xs bg-indigo-50 text-indigo-700 border border-indigo-200"
                            >
                                {label}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
                <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {issue.body}
                </p>
            </div>
        </div>
    );
}