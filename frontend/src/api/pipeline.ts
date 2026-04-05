import type { FileReview } from '@/interfaces/Review';
import { protectedApiClient } from './client';

type StartPipelinePayload = {
    repo_key: string;
    commit_sha: string;
    issue: string;
};

export const startPipeline = async (payload: StartPipelinePayload) => {
    const response = await protectedApiClient.post('/pipeline/start', { ...payload });
    return response.data;
}

export const submitReview = async (threadId: string, fileReviews: FileReview[]) => {
    console.log('thread id: ', threadId);
    console.log('file reviews: ', fileReviews);

    const res = await protectedApiClient.post(`/pipeline/review`, {
        file_reviews: fileReviews, thread_id: threadId
    });
    return res.data;
}