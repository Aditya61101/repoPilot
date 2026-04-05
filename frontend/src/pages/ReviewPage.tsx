import React, { useState, useMemo, useCallback, Suspense } from 'react'
import { ChevronDown, ArrowLeft, GitPullRequest } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { cn } from '@/lib/utils'
import { useNavigate, useSearchParams } from 'react-router'
import type { FileDiff, FileReview, PageState, SSEEvent } from '@/interfaces/Review'
import { useSSEStream } from '@/hooks/useSSEStream'
import { ThemeToggle } from '@/components/shared/ThemeToggle'
import { submitReview } from '@/api/pipeline'


function ReviewHeader({ pageState, issueTitle }: { pageState: PageState; issueTitle: string }) {
    const isRunning = pageState === 'running' || pageState === 'resuming'
    const isDotGreen = pageState === 'complete'
    const isDotGray = pageState === 'pending_review'
    const navigate = useNavigate();

    return (
        <header className="fixed top-0 left-0 right-0 h-16 border-b border-border bg-background/95 backdrop-blur-sm flex items-center px-6 z-40">
            <Button variant={"ghost"} className="p-2 hover:bg-muted hover:cursor-pointer  rounded-md transition-colors mr-4" onClick={() => navigate(-1)}>
                <ArrowLeft className="w-5 h-5" />
            </Button>

            <div className="flex flex-1 items-center gap-2">
                <h1 className="text-sm font-medium text-muted-foreground">
                    AI Assistant — fixing:{' '}
                    <span className="font-serif text-foreground">{issueTitle}</span>
                </h1>
                <div
                    className={cn(
                        'w-2 h-2 rounded-full transition-colors',
                        isRunning && 'bg-primary animate-pulse',
                        isDotGray && 'bg-muted-foreground',
                        isDotGreen && 'bg-green-500'
                    )}
                />
            </div>
            <ThemeToggle/>
        </header>
    )
}

function StatusPulse({ message }: { message: string }) {
    return (
        <div className="flex flex-col items-center justify-center gap-3 w-full">
            <div className="w-3 h-3 bg-primary rounded-full animate-pulse" />
            <p className="text-sm text-muted-foreground animate-pulse">{message}</p>
        </div>
    )
}

interface DiffFileBlockProps {
    fileDiff: FileDiff
    index: number
    fileReview: FileReview | undefined
    onReviewChange: (feedback: string, accepted: boolean) => void
}

function DiffFileBlock({
    fileDiff,
    index,
    fileReview,
    onReviewChange,
}: DiffFileBlockProps) {
    const [isExpanded, setIsExpanded] = useState(index === 0)
    const displayFilename = fileDiff.file.length > 30
        ? '...' + fileDiff.file.slice(-27)
        : fileDiff.file
    const lineCount = Math.max(
        fileDiff.original.split('\n').length,
        fileDiff.modified.split('\n').length
    )

    const isAccepted = fileReview?.approved ?? true
    const isRejected = fileReview?.approved === false

    const LazyDiffEditor = React.lazy(() => import('@monaco-editor/react').then(module => ({ default: module.DiffEditor })));
    
    return (
        <div
            className={cn(
                'border border-border rounded-lg overflow-hidden transition-colors',
                isAccepted && 'border-l-4 border-l-green-500',
                isRejected && 'border-l-4 border-l-destructive'
            )}
        >
            <Button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full px-4 py-3 flex items-center justify-between hover:bg-muted transition-colors"
            >
                <div className="flex items-center gap-2 min-w-0">
                    <span className="text-lg">📄</span>
                    <code className="font-mono text-xs text-muted-foreground truncate" title={fileDiff.file}>
                        {displayFilename}
                    </code>
                </div>
                <ChevronDown
                    className={cn('w-4 h-4 transition-transform shrink-0', isExpanded && 'rotate-180')}
                />
            </Button>

            {isExpanded && (
                <div className="border-t border-border">
                    <div className="bg-muted/50 p-4">
                    <Suspense fallback={<div className='animate-pulse text-muted-foreground'>Loading editor...</div>}>
                        <LazyDiffEditor
                            height={Math.min(500, Math.max(200, lineCount * 19 + 40))}
                            original={fileDiff.original}
                            modified={fileDiff.modified}
                            language={fileDiff.language}
                            theme="vs-dark"
                            options={{
                                readOnly: true,
                                renderSideBySide: true,
                                minimap: { enabled: false },
                                scrollBeyondLastLine: false,
                                fontSize: 13,
                                lineNumbers: 'on',
                                folding: false,
                                wordWrap: 'on',
                                renderOverviewRuler: false,
                                overviewRulerBorder: false,
                                padding: { top: 8, bottom: 8 },
                            }}
                        />
                    </Suspense>
                    </div>

                    <div className="p-4 border-t border-border space-y-3">
                        <Textarea
                            placeholder="Any issues with this file? (optional)"
                            value={fileReview?.feedback || ''}
                            onChange={(e) => onReviewChange(e.target.value, isAccepted)}
                            className="text-sm"
                        />

                        <div className="flex gap-2">
                            <Button
                                variant={isRejected ? 'default' : 'outline'}
                                size="sm"
                                onClick={() => onReviewChange(fileReview?.feedback || '', false)}
                                className={cn(
                                    isRejected && 'bg-destructive hover:bg-destructive/90 text-white border-destructive'
                                )}
                            >
                                ✗ Reject file
                            </Button>
                            <Button
                                variant={isAccepted ? 'default' : 'outline'}
                                size="sm"
                                onClick={() => onReviewChange(fileReview?.feedback || '', true)}
                                className={cn(isAccepted && 'bg-primary hover:bg-primary/90 text-white')}
                            >
                                ✓ Accept
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

function DiffPanel({
    fileDiffs,
    fileReviews,
    onFileReviewChange,
}: {
    fileDiffs: FileDiff[]
    fileReviews: Record<string, FileReview>
    onFileReviewChange: (filename: string, feedback: string, accepted: boolean) => void
}) {
    return (
        <div className="flex-1 overflow-y-auto px-6 py-4 animate-in fade-in slide-in-from-right-4 duration-500">
            <h2 className="text-sm text-muted-foreground mb-4">{fileDiffs.length} files changed</h2>

            <div className="space-y-3">
                {fileDiffs.map((diff, idx) => (
                    <DiffFileBlock
                        key={diff.file}
                        fileDiff={diff}
                        index={idx}
                        fileReview={fileReviews[diff.file]}
                        onReviewChange={(feedback, accepted) =>
                            onFileReviewChange(diff.file, feedback, accepted)
                        }
                    />
                ))}
            </div>
        </div>
    )
}

function ReviewFooter({
    onSubmit,
    disabled,
}: {
    onSubmit: () => void
    disabled: boolean
}) {
    return (
        <footer className="fixed bottom-0 left-0 right-0 h-16 border-t border-border bg-background/95 backdrop-blur-sm flex items-center justify-end px-6">
            <Button onClick={onSubmit} disabled={disabled} className="gap-2">
                Submit Review
                <span>→</span>
            </Button>
        </footer>
    )
}

function PROpenedCard({ prURL }: { prURL: string | null }) {
    if (!prURL) return null;
    return (
        <div className="flex-1 flex items-center justify-center p-6">
            <div className="max-w-md text-center space-y-4">
                <div className="flex justify-center">
                    <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                        <GitPullRequest className="w-8 h-8 text-green-600 dark:text-green-400" />
                    </div>
                </div>
                <h2 className="text-xl font-semibold text-foreground">PR Opened!</h2>
                <p className="text-sm text-muted-foreground">
                    Your pull request has been created and is ready for review.
                </p>
                <a
                    href={prURL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 text-sm font-medium"
                >
                    View on GitHub
                </a>
            </div>
        </div>
    )
}

export default function ReviewPage() {
    const [searchParams] = useSearchParams()
    const threadId = searchParams.get('thread_id')
    const issueTitle = searchParams.get('issue') ?? 'Unknown Issue'

    const [pageState, setPageState] = useState<PageState>('running')
    const [prUrl, setPrUrl] = useState<string | null>(null)
    const [streamEnabled, setStreamEnabled] = useState(true)
    const [fileDiffs, setFileDiffs] = useState<FileDiff[]>([])
    const [fileReviews, setFileReviews] = useState<Record<string, FileReview>>({})
    const [statusMessage, setStatusMessage] = useState('Starting pipeline...')

    const handleSSEEvent = useCallback((event: SSEEvent) => {
        if (event.message) setStatusMessage(event.message)
        switch (event.type) {
            case 'node_running':
                setPageState('running')
                break

            case 'pending_review':
                setFileDiffs(event.file_diffs ?? [])
                setFileReviews({})
                setPageState('pending_review')
                setStreamEnabled(false)
                break

            case 'complete':
                setPrUrl(event.pr_url ?? null)
                setPageState('complete')
                setStreamEnabled(false)
                break
        }
    }, [])

    useSSEStream(threadId, handleSSEEvent, streamEnabled)

    const showDiff = pageState === 'pending_review'
    const showStatusPulse = pageState === 'running' || pageState === 'resuming'
    const showPROpened = pageState === 'complete' && prUrl

    const handleSubmitReview = async () => {
        if (!threadId) return
        setPageState('resuming')
        setFileDiffs([])

        await submitReview(threadId, Object.values(fileReviews))

        // re-open stream for next cycle
        setStreamEnabled(true)
    }

    const isSubmitDisabled = useMemo(() => {
        if (pageState !== 'pending_review') return true
        return Object.keys(fileReviews).length === 0
    }, [pageState, fileReviews])

    const handleFileReviewChange = (
        filename: string,
        feedback: string,
        approved: boolean
    ) => {
        setFileReviews((prev) => ({
            ...prev,
            [filename]: { file: filename, approved, feedback },
        }))
    }

    return (
        <div className="min-h-screen pt-16">
            <ReviewHeader pageState={pageState} issueTitle={issueTitle} />

            <div className="flex flex-col h-[calc(100vh-4rem)]">
                <div className="flex flex-1 relative">
                    {/* <PipelineStepper nodes={nodes} /> */}

                    <div className={cn(
                        "absolute inset-0 flex items-center justify-center transition-all duration-500",
                        showStatusPulse
                            ? "opacity-100 pointer-events-auto"
                            : "opacity-0 pointer-events-none"
                    )}>
                        <StatusPulse message={statusMessage} />
                    </div>

                    {/* DiffPanel — visible when pending_review */}
                    <div className={cn(
                        "absolute inset-0 transition-all duration-500",
                        showDiff
                            ? "opacity-100 pointer-events-auto translate-y-0"
                            : "opacity-0 pointer-events-none translate-y-4"
                    )}>
                        <DiffPanel
                            fileDiffs={fileDiffs}
                            fileReviews={fileReviews}
                            onFileReviewChange={handleFileReviewChange}
                        />
                    </div>

                    {/* PROpenedCard — visible when complete */}
                    <div className={cn(
                        "absolute inset-0 flex items-center justify-center transition-all duration-500",
                        showPROpened
                            ? "opacity-100 pointer-events-auto translate-y-0"
                            : "opacity-0 pointer-events-none translate-y-4"
                    )}>
                        <PROpenedCard prURL={prUrl} />
                    </div>
                </div>

                <div className={cn(
                    "transition-all duration-500",
                    pageState === 'pending_review'
                        ? "opacity-100 pointer-events-auto"
                        : "opacity-0 pointer-events-none h-0 overflow-hidden"
                )}>
                    <ReviewFooter onSubmit={handleSubmitReview} disabled={isSubmitDisabled} />
                </div>
            </div>
        </div>
    )
}
