export type PageState = 'running' | 'pending_review' | 'resuming' | 'complete'
export type NodeStatus = 'pending' | 'running' | 'complete' | 'failed'

export type SSEEvent = {
    type: 'node_running' | 'pending_review' | 'complete'
    node?: string
    message?: string
    file_diffs?: FileDiff[]
    pr_url?: string
}

export interface PipelineNode {
    name: string
    status: NodeStatus
}

export interface FileDiff {
    file: string
    language: 'typescript' | 'javascript' | 'python' | 'sql'
    original: string
    modified: string
}

export interface FileReview {
    file: string
    approved: boolean
    feedback: string
}