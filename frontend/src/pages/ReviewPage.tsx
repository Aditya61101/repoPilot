/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useState, useMemo, useCallback, Suspense } from 'react'
import { ChevronDown, ArrowLeft, CheckCircle2, AlertCircle, GitPullRequest } from 'lucide-react'
// import {DiffEditor} from '@monaco-editor/react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { cn } from '@/lib/utils'
import { useSearchParams } from 'react-router'
import type { FileDiff, FileReview, PageState, PipelineNode, SSEEvent } from '@/interfaces/Review'
import { useSSEStream } from '@/hooks/useSSEStream'
import { ThemeToggle } from '@/components/shared/ThemeToggle'

// Mock data
const INITIAL_NODES: PipelineNode[] = [
    { name: 'chk_idx', status: 'complete' },
    { name: 'analyze', status: 'complete' },
    { name: 'plan', status: 'complete' },
    { name: 'generate', status: 'complete' },
    { name: 'diff', status: 'complete' },
    { name: 'review', status: 'running' },
]

const MOCK_FILE_DIFFS: FileDiff[] = [
    {
        file: 'client/src/routes/dashboard/code/page.tsx',
        language: 'typescript',
        original: "/* eslint-disable @typescript-eslint/no-explicit-any */\nimport { useState } from \"react\";\nimport { Heading } from \"@/components/dashboard/heading\";\nimport { Loader } from \"@/components/dashboard/loader\";\nimport { UserAvatar } from \"@/components/dashboard/userAvatar\";\nimport { BotAvatar } from \"@/components/dashboard/botAvatar\";\nimport Empty from \"@/components/dashboard/empty\";\nimport { Button } from \"@/components/ui/button\";\nimport { Form, FormControl, FormField, FormItem } from \"@/components/ui/form\";\nimport { Input } from \"@/components/ui/input\";\nimport { MessageSquare } from \"lucide-react\";\nimport { zodResolver } from \"@hookform/resolvers/zod\";\nimport * as z from \"zod\";\nimport { useForm } from \"react-hook-form\";\nimport { cn } from \"@/lib/utils\";\nimport { ChatCompletionUserMessageParam } from 'openai/resources/chat/index.mjs';\nimport { openModal } from \"@/store/reducers/modalReducer\";\nimport toast from \"react-hot-toast\";\nimport { useDispatch } from \"react-redux\";\nimport { useQueryClient } from \"@tanstack/react-query\";\nimport { useUser } from \"@clerk/clerk-react\";\nimport { apiCall } from \"@/lib/axios\";\n\nconst Conversation = () => {\n  const { user } = useUser();\n  const queryClient = useQueryClient();\n  const dispatch = useDispatch();\n  const [messages, setMessages] = useState<ChatCompletionUserMessageParam[]>([]);\n\n  const formSchema = z.object({\n    prompt: z.string().min(1, {\n      message: \"Prompt is required.\"\n    }),\n  });\n  const form = useForm<z.infer<typeof formSchema>>({\n    resolver: zodResolver(formSchema),\n    defaultValues: {\n      prompt: \"\"\n    }\n  });\n\n  const isLoading = form.formState.isSubmitting;\n\n  const onSubmit = async (values: z.infer<typeof formSchema>) => {\n    try {\n      const userMessage: ChatCompletionUserMessageParam = { role: \"user\", content: values.prompt };\n      const newMessages = [...messages, userMessage];\n\n      const api = apiCall(user);\n      const response = await api.post(\"conversation\", { messages: newMessages });\n      setMessages((current) => [...current, userMessage, response.data]);\n\n      queryClient.invalidateQueries({ queryKey: ['user-status'] });\n      form.reset();\n    } catch (error: any) {\n      console.error('error', error);\n      if (error?.response?.status === 403) {\n        dispatch(openModal());\n      } else {\n        toast.error(\"Something went wrong.\");\n      }\n    }\n  }\n\n  return (\n    <div>\n      <Heading\n        title=\"Conversation\"\n        description=\"Our most advanced conversation model!\"\n        icon={MessageSquare}\n        iconColor=\"text-violet-500\"\n        bgColor=\"bg-violet-500/10\"\n      />\n      <div className=\"px-4 lg:px-8\">\n        <div>\n          <Form {...form}>\n            <form\n              onSubmit={form.handleSubmit(onSubmit)}\n              className=\"\n                border \n                rounded-lg\n                w-full \n                p-4 \n                px-3 \n                md:px-6 \n                focus-within:shadow-sm\n                grid\n                grid-cols-12\n                gap-2\n              \"\n            >\n              <FormField\n                name=\"prompt\"\n                render={({ field }) => (\n                  <FormItem className=\"col-span-12 lg:col-span-10\">\n                    <FormControl className=\"m-0 p-0\">\n                      <Input\n                        className=\"border-0 outline-none focus-visible:ring-0 focus-visible:ring-transparent\"\n                        disabled={isLoading}\n                        placeholder=\"How do I calculate the radius of a circle?\"\n                        {...field}\n                      />\n                    </FormControl>\n                  </FormItem>\n                )}\n              />\n              <Button className=\"col-span-12 lg:col-span-2 w-full\" type=\"submit\" disabled={isLoading} size=\"icon\">\n                Generate\n              </Button>\n            </form>\n          </Form>\n        </div>\n        <div className=\"space-y-4 mt-4\">\n          {isLoading && (\n            <div className=\"p-8 rounded-lg w-full flex items-center justify-center bg-muted\">\n              <Loader />\n            </div>\n          )}\n          {messages.length === 0 && !isLoading && (\n            <Empty label=\"No conversation started.\" />\n          )}\n          <div className=\"flex flex-col-reverse gap-y-4\">\n            {messages.map((message, index) => (\n              <div\n                key={index}\n                className={cn(\n                  \"p-8 w-full flex items-start gap-x-8 rounded-lg\",\n                  message.role === \"user\" ? \"border\" : \"bg-muted\",\n                )}\n              >\n                {message.role === \"user\" ? <UserAvatar /> : <BotAvatar />}\n                {Array.isArray(message.content)\n                  ? message.content.map((part, idx) => {\n                    if (\"text\" in part) {\n                      return <span key={idx}>{part.text}</span>\n                    } else {\n                      return null;\n                    }\n                  })\n                  : <p className=\"text-sm\">{message.content}</p>\n                }\n              </div>\n            ))}\n          </div>\n        </div>\n      </div>\n    </div>\n  );\n\n}\n\nexport default Conversation;",
        modified: "/* eslint-disable @typescript-eslint/no-explicit-any */\nimport { useState } from \"react\";\nimport { Heading } from \"@/components/dashboard/heading\";\nimport { Loader } from \"@/components/dashboard/loader\";\nimport { UserAvatar } from \"@/components/dashboard/userAvatar\";\nimport { BotAvatar } from \"@/components/dashboard/botAvatar\";\nimport Empty from \"@/components/dashboard/empty\";\nimport { Button } from \"@/components/ui/button\";\nimport { Form, FormControl, FormField, FormItem } from \"@/components/ui/form\";\nimport { Input } from \"@/components/ui/input\";\nimport { MessageSquare } from \"lucide-react\";\nimport { zodResolver } from \"@hookform/resolvers/zod\";\nimport * as z from \"zod\";\nimport { useForm } from \"react-hook-form\";\nimport { cn } from \"@/lib/utils\";\nimport { ChatCompletionUserMessageParam } from 'openai/resources/chat/index.mjs';\nimport { openModal } from \"@/store/reducers/modalReducer\";\nimport toast from \"react-hot-toast\";\nimport { useDispatch } from \"react-redux\";\nimport { useQueryClient } from \"@tanstack/react-query\";\nimport { useUser } from \"@clerk/clerk-react\";\nimport { apiCall } from \"@/lib/axios\";\n\nconst Conversation = () => {\n  const { user } = useUser();\n  const queryClient = useQueryClient();\n  const dispatch = useDispatch();\n  const [messages, setMessages] = useState<ChatCompletionUserMessageParam[]>([]);\n\n  const formSchema = z.object({\n    prompt: z.string().min(1, {\n      message: \"Prompt is required.\"\n    }),\n  });\n  const form = useForm<z.infer<typeof formSchema>>({\n    resolver: zodResolver(formSchema),\n    defaultValues: {\n      prompt: \"\"\n    }\n  });\n\n  const isLoading = form.formState.isSubmitting;\n\nconst onSubmit = async (values: z.infer<typeof formSchema>) => {\n\n  try {\n\n    const userMessage: ChatCompletionUserMessageParam = { role: \"user\", content: values.prompt };\n\n    const newMessages = [...messages, userMessage];\n\n\n\n    const api = apiCall(user);\n\n    const response = await api.post(\"conversation\", { messages: newMessages }, {\n\n      responseType: 'stream'\n\n    });\n\n\n\n    const reader = response.data.getReader();\n\n    const decoder = new TextDecoder(\"utf-8\");\n\n\n\n    let botMessage = { role: \"bot\", content: \"\" };\n\n    setMessages((current) => [...current, userMessage, botMessage]);\n\n\n\n    const processStream = async () => {\n\n      while (true) {\n\n        const { done, value } = await reader.read();\n\n        if (done) break;\n\n        const chunk = decoder.decode(value, { stream: true });\n\n        botMessage.content += chunk;\n\n        setMessages((current) => {\n\n          const updatedMessages = [...current];\n\n          updatedMessages[updatedMessages.length - 1] = botMessage;\n\n          return updatedMessages;\n\n        });\n\n      }\n\n    };\n\n\n\n    await processStream();\n\n\n\n    queryClient.invalidateQueries({ queryKey: ['user-status'] });\n\n    form.reset();\n\n  } catch (error: any) {\n\n    console.error('error', error);\n\n    if (error?.response?.status === 403) {\n\n      dispatch(openModal());\n\n    } else {\n\n      toast.error(\"Something went wrong.\");\n\n    }\n\n  }\n\n}\n\n  return (\n    <div>\n      <Heading\n        title=\"Conversation\"\n        description=\"Our most advanced conversation model!\"\n        icon={MessageSquare}\n        iconColor=\"text-violet-500\"\n        bgColor=\"bg-violet-500/10\"\n      />\n      <div className=\"px-4 lg:px-8\">\n        <div>\n          <Form {...form}>\n            <form\n              onSubmit={form.handleSubmit(onSubmit)}\n              className=\"\n                border \n                rounded-lg\n                w-full \n                p-4 \n                px-3 \n                md:px-6 \n                focus-within:shadow-sm\n                grid\n                grid-cols-12\n                gap-2\n              \"\n            >\n              <FormField\n                name=\"prompt\"\n                render={({ field }) => (\n                  <FormItem className=\"col-span-12 lg:col-span-10\">\n                    <FormControl className=\"m-0 p-0\">\n                      <Input\n                        className=\"border-0 outline-none focus-visible:ring-0 focus-visible:ring-transparent\"\n                        disabled={isLoading}\n                        placeholder=\"How do I calculate the radius of a circle?\"\n                        {...field}\n                      />\n                    </FormControl>\n                  </FormItem>\n                )}\n              />\n              <Button className=\"col-span-12 lg:col-span-2 w-full\" type=\"submit\" disabled={isLoading} size=\"icon\">\n                Generate\n              </Button>\n            </form>\n          </Form>\n        </div>\n        <div className=\"space-y-4 mt-4\">\n          {isLoading && (\n            <div className=\"p-8 rounded-lg w-full flex items-center justify-center bg-muted\">\n              <Loader />\n            </div>\n          )}\n          {messages.length === 0 && !isLoading && (\n            <Empty label=\"No conversation started.\" />\n          )}\n          <div className=\"flex flex-col-reverse gap-y-4\">\n            {messages.map((message, index) => (\n              <div\n                key={index}\n                className={cn(\n                  \"p-8 w-full flex items-start gap-x-8 rounded-lg\",\n                  message.role === \"user\" ? \"border\" : \"bg-muted\",\n                )}\n              >\n                {message.role === \"user\" ? <UserAvatar /> : <BotAvatar />}\n                {Array.isArray(message.content)\n                  ? message.content.map((part, idx) => {\n                    if (\"text\" in part) {\n                      return <span key={idx}>{part.text}</span>\n                    } else {\n                      return null;\n                    }\n                  })\n                  : <p className=\"text-sm\">{message.content}</p>\n                }\n              </div>\n            ))}\n          </div>\n        </div>\n      </div>\n    </div>\n  );\n\n}\n\nexport default Conversation;",
    },
    {
        file: 'client/src/lib/axios.ts',
        language: 'typescript',
        original: 'timeout: 3000',
        modified: 'timeout: 5000',
    },
]

function ReviewHeader({ pageState, issueTitle }: { pageState: PageState; issueTitle: string }) {
    const isRunning = pageState === 'running' || pageState === 'resuming'
    const isDotGreen = pageState === 'complete'
    const isDotGray = pageState === 'pending_review'

    return (
        <header className="fixed top-0 left-0 right-0 h-16 border-b border-border bg-background/95 backdrop-blur-sm flex items-center px-6 z-40">
            <button className="p-2 hover:bg-muted rounded-md transition-colors mr-4">
                <ArrowLeft className="w-5 h-5" />
            </button>

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

function StatusPulse() {
    return (
        <div className="flex flex-col items-center justify-center gap-3">
            <div className="w-3 h-3 bg-primary rounded-full animate-pulse" />
            <p className="text-sm text-muted-foreground animate-pulse">Analyzing your issue...</p>
        </div>
    )
}

function PipelineStepper({
    nodes,
    isSidebar,
}: {
    nodes: PipelineNode[]
    isSidebar: boolean
}) {
    return (
        <div
            className={cn(
                'flex transition-all duration-500',
                isSidebar
                    ? 'w-44 border-r border-border px-4 py-6 flex-col gap-6'
                    : 'flex-1 items-center justify-center'
            )}
        >
            {isSidebar ? (
                <div className="space-y-4">
                    {nodes.map((node) => (
                        <div key={node.name} className="flex items-start gap-3">
                            <div className="mt-1 shrink-0">
                                {node.status === 'complete' && (
                                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                                )}
                                {node.status === 'running' && (
                                    <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                                )}
                                {node.status === 'pending' && (
                                    <div className="w-5 h-5 border-2 border-muted-foreground rounded-full" />
                                )}
                                {node.status === 'failed' && (
                                    <AlertCircle className="w-5 h-5 text-destructive" />
                                )}
                            </div>
                            <span className="font-mono text-xs text-muted-foreground">{node.name}</span>
                        </div>
                    ))}
                </div>
            ) : (
                <StatusPulse />
            )}
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
    //   const filename = fileDiff.file.split('/').pop() || fileDiff.file
    const displayFilename = fileDiff.file.length > 30
        ? '...' + fileDiff.file.slice(-27)
        : fileDiff.file
    const lineCount = Math.max(
        fileDiff.original.split('\n').length,
        fileDiff.modified.split('\n').length
    )

    const isAccepted = fileReview?.accepted ?? true
    const isRejected = fileReview?.accepted === false

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

function PROpenedCard({ prURL }: { prURL: string }) {
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

    const [pageState, setPageState] = useState<PageState>('pending_review')
    const [prUrl, setPrUrl] = useState<string | null>(null)
    const [streamEnabled, setStreamEnabled] = useState(true)
    const [fileDiffs, setFileDiffs] = useState<FileDiff[]>(MOCK_FILE_DIFFS)
    const [fileReviews, setFileReviews] = useState<Record<string, FileReview>>({})
    const [nodes, setNodes] = useState<PipelineNode[]>(INITIAL_NODES)

    // const handleSSEEvent = useCallback((event: SSEEvent) => {
    //     switch (event.type) {
    //         case 'node_complete':
    //             // mark node as complete in stepper
    //             setNodes((prev) =>
    //                 prev.map((n) =>
    //                     n.name === event.node
    //                         ? { ...n, status: 'complete' }
    //                         : n.status === 'pending'
    //                         ? { ...n, status: 'running' }  // next node starts
    //                         : n
    //                 )
    //             )
    //             break

    //         case 'pending_review':
    //             setFileDiffs(event.file_diffs ?? [])
    //             setFileReviews({})              // reset reviews for new cycle
    //             setPageState('pending_review')
    //             setStreamEnabled(false)         // close stream, wait for user
    //             break

    //         case 'complete':
    //             setPrUrl(event.pr_url ?? null)
    //             setPageState('complete')
    //             setStreamEnabled(false)
    //             break
    //     }
    // }, [])

    // useSSEStream(threadId, handleSSEEvent, streamEnabled)

    const showDiff = pageState === 'pending_review'
    const isSidebar = pageState === 'pending_review' || pageState === 'complete' || pageState === 'running'

    const handleSubmitReview = async () => {
        if (!threadId) return
        setPageState('resuming')
        setFileDiffs([])

        await fetch(`/api/run/${threadId}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_reviews: fileReviews }),
        })

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
        accepted: boolean
    ) => {
        setFileReviews((prev) => ({
            ...prev,
            [filename]: { accepted, feedback },
        }))
    }

    return (
        <div className="min-h-screen pt-16">
            <ReviewHeader pageState={pageState} issueTitle={issueTitle} />

            <div className="flex flex-col h-[calc(100vh-4rem)]">
                <div className="flex flex-1 overflow-hidden">
                    <PipelineStepper nodes={nodes} isSidebar={isSidebar} />

                    {showDiff && (
                        <DiffPanel
                            fileDiffs={fileDiffs}
                            fileReviews={fileReviews}
                            onFileReviewChange={handleFileReviewChange}
                        />
                    )}

                    {pageState === 'complete' && prUrl && <PROpenedCard prURL={prUrl} />}
                </div>

                {pageState === 'pending_review' && (
                    <ReviewFooter onSubmit={handleSubmitReview} disabled={isSubmitDisabled} />
                )}
            </div>
        </div>
    )
}
