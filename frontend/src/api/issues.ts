import { protectedApiClient } from "./client";

export const fetchIssues = async (username:string, repo:string) => {
    const res = await protectedApiClient.get(`/repos/issues?owner=${username}&repo=${repo}`);
    return res.data;
}