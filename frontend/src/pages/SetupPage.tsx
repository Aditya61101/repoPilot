import { useState } from "react";
import { IssuePreview } from "../components/IssuePreview";
import { IssueList } from "../components/IssueList";
import { fetchRepos } from "@/api/repos";
import { Button } from "@/components/ui/button";
import { Input } from '@/components/ui/input'
// import { Card } from '@/components/ui/card'
// import {
//     Select,
//     SelectContent,
//     SelectItem,
//     SelectTrigger,
//     SelectValue,
// } from '@/components/ui/select'
import type { Repo } from "@/interfaces/Issue";
import { LoaderCircle } from "lucide-react";

const mockIssues = [
    {
        id: 1,
        number: 58234,
        title: 'Image optimization not working with dynamic imports',
        state: 'open',
        createdAt: '2024-01-15T10:30:00Z',
        labels: ['bug', 'performance'],
        body: 'When using dynamic imports with next/image, the optimization is not applied. The component still loads unoptimized images even with the `priority` prop set.\n\n**Steps to reproduce:**\n1. Create a component with dynamic import\n2. Use next/image inside it\n3. Check network tab\n\n**Expected behavior:** Images should be optimized\n\n**Actual behavior:** Images load unoptimized',
    },
    {
        id: 2,
        number: 58215,
        title: 'SSR fails when using external library with browser APIs',
        state: 'open',
        createdAt: '2024-01-14T14:22:00Z',
        labels: ['bug', 'ssr'],
        body: 'External library xyz requires window object during module import, causing SSR to fail.\n\n**Error:**\n```\nReferenceError: window is not defined\n```\n\n**Workaround:** Using dynamic import with ssr: false',
    },
    {
        id: 3,
        number: 58190,
        title: 'Improve TypeScript types for middleware context',
        state: 'open',
        createdAt: '2024-01-12T09:15:00Z',
        labels: ['enhancement', 'types'],
        body: 'The middleware context object lacks proper TypeScript inference for custom properties. Adding better type support would improve DX.',
    },
    {
        id: 4,
        number: 58156,
        title: 'Memory leak in hot reload during development',
        state: 'open',
        createdAt: '2024-01-10T16:45:00Z',
        labels: ['bug', 'performance'],
        body: 'When making rapid file changes, the dev server accumulates memory and eventually crashes. Appears to be event listeners not being cleaned up.',
    },
    {
        id: 5,
        number: 58102,
        title: 'Documentation needs update for new API route handlers',
        state: 'open',
        createdAt: '2024-01-08T11:20:00Z',
        labels: ['documentation'],
        body: 'The new API route handler patterns should be documented with examples.',
    },
];

const SetupPage = () => {
    const [username, setUsername] = useState('');
    const [repos, setRepos] = useState<Repo[]|null>(null);
    const [isFetchingRepos, setIsFetchingRepos] = useState(false);
    const [selectedRepoId, setSelectedRepoId] = useState<number | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedIssueId, setSelectedIssueId] = useState<number | null>(null);

    const filteredIssues = mockIssues.filter(
        (issue) =>
            issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            issue.number.toString().includes(searchQuery)
    );

    const selectedIssue = selectedIssueId
        ? mockIssues.find((i) => i.id === selectedIssueId) || null
        : null;

    const handleRepoChange = (repoId: number) => {
        // make api call
        setSelectedRepoId(repoId);
        setSelectedIssueId(null);
    };

    const fetchReposForUser = async () => {
        setIsFetchingRepos(true);
        setRepos(null);
        try {
            const fetchedRepos = await fetchRepos(username);
            setRepos(fetchedRepos);
        } catch(e:unknown) {
            console.error(e);
        } finally {
            setIsFetchingRepos(false);
        }
    }

    return (
        <div className="min-h-screen bg-white p-6">
            <div className="max-w-6xl mx-auto">
                <h1 className="text-2xl font-semibold text-gray-800 mb-8">
                    AI Assistant Setup
                </h1>

                {/* Username Input + Fetch Repos */}
                <div className="flex gap-3 mb-6">
                    <Input
                        id="username"
                        type="text"
                        placeholder="Enter your GitHub username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="flex-1"
                    />
                    <Button
                        onClick={fetchReposForUser}
                        disabled={!username.trim()}
                        className="bg-primary hover:bg-primary/90 min-w-30"
                    >
                        {isFetchingRepos ? <LoaderCircle className='animate-spin'/> : <span> Fetch Repos </span>}
                    </Button>
                </div>

                {!repos ? (
                    <div className="flex items-center justify-center h-96 text-gray-500">
                        {isFetchingRepos ? `Fetching repos for ${username}...`: 'Enter a username to load repositories'}
                    </div>
                ) : (
                    <>
                        {/* Repo Select */}
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Repository
                            </label>
                            <select
                                value={selectedRepoId || ''}
                                onChange={(e) => handleRepoChange(Number(e.target.value))}
                                className="w-full px-4 py-2 border border-gray-200 rounded-md text-sm text-gray-800 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 bg-white"
                            >
                                <option value="">Select a repository...</option>
                                {repos.map((repo:Repo) => (
                                    <option key={repo.id} value={repo.id}>
                                        {repo.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {!selectedRepoId ? (
                            <div className="flex items-center justify-center h-96 text-gray-500">
                                Select a repository to view issues
                            </div>
                        ) : (
                            <>
                                {/* Issue Search */}
                                <div className="mb-6">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Search Issues
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="Search by title or issue number..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="w-full px-4 py-2 border border-gray-200 rounded-md text-sm text-gray-800 placeholder-gray-500 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0"
                                    />
                                </div>

                                {/* Two-Column Grid */}
                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div>
                                        <h3 className="text-sm font-medium text-gray-700 mb-2">
                                            Issues
                                        </h3>
                                        <IssueList
                                            issues={filteredIssues}
                                            selectedIssueId={selectedIssueId}
                                            onSelectIssue={setSelectedIssueId}
                                        />
                                    </div>
                                    <div>
                                        <h3 className="text-sm font-medium text-gray-700 mb-2">
                                            Preview
                                        </h3>
                                        <IssuePreview issue={selectedIssue} />
                                    </div>
                                </div>

                                {/* Start Pipeline Button */}
                                <div className="flex justify-end">
                                    <button
                                        disabled={!selectedRepoId || !selectedIssueId}
                                        className="px-6 py-2 bg-indigo-500 text-white text-sm font-medium rounded-md hover:bg-indigo-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                    >
                                        Start Pipeline
                                    </button>
                                </div>
                            </>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}

export default SetupPage;