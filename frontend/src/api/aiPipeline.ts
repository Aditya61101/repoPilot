import type { FileReview } from '@/interfaces/Review';
import { aiClient } from "./aiClient";

type StartPipelinePayload = {
    repo_key: string;
    commit_sha: string;
    issue: string;
};

export const startPipeline = async (payload: StartPipelinePayload) => {
    const response = await aiClient.post('/v2/start', { ...payload });
    return response.data;
}

export const submitReview = async (threadId: string, fileReviews: FileReview[]) => {
    console.log('thread id: ', threadId);
    console.log('file reviews: ', fileReviews);

    const res = await aiClient.post(`/v2/review`, {
        file_reviews: fileReviews, thread_id: threadId
    });
    return res.data;
}