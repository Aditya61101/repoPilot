import type { SSEEvent } from '@/interfaces/Review'
import { useEffect, useRef } from 'react'

export function useSSEStream(
    threadId: string | null,
    onEvent: (event: SSEEvent) => void,
    enabled: boolean = true
) {
    const esRef = useRef<EventSource | null>(null)

    useEffect(() => {
        if (!threadId || !enabled) return

        const es = new EventSource(`/api/run/${threadId}/stream`)
        esRef.current = es

        es.onmessage = (e) => {
            try {
                const data: SSEEvent = JSON.parse(e.data)
                onEvent(data)
            } catch {
                console.error('Failed to parse SSE event:', e.data)
            }
        }

        es.onerror = () => {
            console.error('SSE connection error')
            es.close()
        }

        return () => {
            es.close()
            esRef.current = null
        }
    }, [threadId, enabled])
}