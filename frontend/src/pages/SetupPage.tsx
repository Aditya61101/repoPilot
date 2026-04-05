import { useMemo, useState } from "react";
import { IssuePreview } from "../components/IssuePreview";
import { IssueList } from "../components/IssueList";
import { Button } from "@/components/ui/button";
import { Input } from '@/components/ui/input';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import type { Issue, Repo } from "@/interfaces/Issue";
import { fetchRepos } from "@/api/repos";
import { fetchIssues } from "@/api/issues";
import { ThemeToggle } from "@/components/shared/ThemeToggle";
import { useNavigate } from "react-router";
import { startPipeline } from "@/api/pipeline";
import { useQuery } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";

const SetupPage = () => {
    const auth = useAuth();
    
    // UI states
    const [selectedRepoName, setSelectedRepoName] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedIssueId, setSelectedIssueId] = useState<number | null>(null);
    // data states
    // const [repos, setRepos] = useState<Repo[] | null>(null);
    const [issues, setIssues] = useState<Issue[] | null>(null);
    const [commitSHA, setCommitSHA] = useState<string>('');
    // loading states
    const [isFetchingIssues, setIsFetchingIssues] = useState(false);

    const navigate = useNavigate();

    const { isPending, data } = useQuery({
        queryKey: ['repos'],
        queryFn: () => fetchRepos().then((res) => res.data),
    })

    const selectedIssue:Issue | null = useMemo(() => {
        if (!selectedIssueId) return null;
        return issues?.find((i) => i.id === selectedIssueId) || null;
    }, [selectedIssueId, issues]);

    const filteredIssues = useMemo(() => {
        if (searchQuery.trim() === '') return issues || [];
        setSelectedIssueId(null);
        return issues?.filter(
            (issue) =>
                issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                issue.id.toString().includes(searchQuery)
        ) || [];
    }, [issues, searchQuery]);

    if(!auth) return;
    const { user, loading } = auth;
    if(loading) return;

    const handleRepoChange = async (repoName: string) => {
        console.log("repo name: ", repoName);
        setSelectedIssueId(null);
        setIssues(null);
        setIsFetchingIssues(true);
        setSelectedRepoName(repoName);
        
        const repo = data?.find((r: Repo) => r.name === repoName)
        if (!repo) return;
        
        try {
            const response = await fetchIssues(repo.owner, repo.name);
            console.log("fetched issues: ", response);
            setIssues(response.issues);
            setCommitSHA(response.commitSHA);
        } catch (error) {
            console.error("Error fetching issues: ", error);
        } finally {
            setIsFetchingIssues(false);
        }
    };

    const handleStartPipeline = async () => {
        if (!selectedRepoName || !selectedIssue) return;

        console.log("selected issue: ", selectedIssue);
        const issueDetails = selectedIssue.body ? `${selectedIssue.title}: ${selectedIssue.body}` : selectedIssue.title;

        const repo = data?.find((r: Repo) => r.name === selectedRepoName);
        if (!repo) return;

        const payload = {
            "repo_key": `${repo.owner}/${repo.name}`,
            "commit_sha": commitSHA,
            "issue": issueDetails,
        }
        console.log(payload);
        try {
            const response = await startPipeline(payload);
            await navigate(`/review?thread_id=${response.thread_id}&issue=${encodeURIComponent(selectedIssue.title)}`);
        } catch (error) {
            console.error('error while posting ', error);
        }

    }

    return (
        <div className="min-h-screen p-6 font-sans">
            <div className="max-w-6xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-semibold text-foreground">AI Code Assistant</h1>
                        <p className="text-muted-foreground">
                            Connect your repository and select an issue to get started
                        </p>
                    </div>
                    <ThemeToggle />
                </div>

                {!data ? (
                    <div className="flex items-center justify-center h-96">
                        {isPending
                            ? <span className="animate-pulse text-muted-foreground font-mono">Fetching repos for {user?.username}...</span>
                            : <span>Enter a username to load repositories</span>
                        }
                    </div>
                ) : (
                    <>
                        <div className="mb-6">
                            <label htmlFor="repo" className="text-sm font-medium text-foreground mb-2">
                                Repositories
                            </label>
                            <Select value={selectedRepoName || ''} onValueChange={handleRepoChange}>
                                <SelectTrigger className="w-full font-mono" id="repo">
                                    <SelectValue placeholder="Select a repository" />
                                </SelectTrigger>
                                <SelectContent>
                                    {data.map((repo: Repo) => (
                                        <SelectItem key={repo.id} value={repo.name} className="font-mono">
                                            {repo.name}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {!issues ? (
                            <div className="flex items-center justify-center h-96">
                                {isFetchingIssues
                                    ? <span className="animate-pulse text-muted-foreground font-mono">Fetching issues for {selectedRepoName}...</span>
                                    : <span className="font-sans">Select a repository to view issues</span>
                                }
                            </div>
                        ) : issues.length === 0 ? (
                            <div className="flex items-center justify-center h-96 text-muted-foreground">
                                <span>
                                    <span className="font-mono">{selectedRepoName}</span> has no issues to solve
                                </span>
                            </div>
                        ) : (
                            <>
                                {/* Issue Search */}
                                <div className="mb-6">
                                    <label className="block text-sm font-medium mb-2">
                                        Search Issues
                                    </label>
                                    <Input
                                        type="text"
                                        placeholder="Search by title or issue number..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="flex-1"
                                    />
                                </div>

                                {/* Two-Column Grid */}
                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div>
                                        <h3 className="text-sm font-medium mb-2">
                                            Issues
                                        </h3>
                                        <div className="max-h-100 overflow-y-auto">
                                            <IssueList
                                                issues={filteredIssues}
                                                selectedIssueId={selectedIssueId}
                                                onSelectIssue={setSelectedIssueId}
                                            />
                                        </div>
                                    </div>
                                    <div>
                                        <h3 className="text-sm font-medium mb-2">
                                            Preview
                                        </h3>
                                        <div className="max-h-100 overflow-y-auto">
                                            <IssuePreview issue={selectedIssue} />
                                        </div>
                                    </div>
                                </div>

                                {/* Start Pipeline Button */}
                                <div className="flex justify-end sticky bottom-0 border-t border-border bg-background py-4">
                                    <Button
                                        disabled={!selectedRepoName || !selectedIssueId}
                                        onClick={handleStartPipeline}
                                    >
                                        Start Pipeline
                                    </Button>
                                </div>
                            </>
                        )}
                    </>
                )}
            </div>
        </div >
    );
}

export default SetupPage;