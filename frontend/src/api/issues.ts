import { apiClient } from "./apiClient";

export const fetchIssues = async (username:string, repo:string) => {
    const res = await apiClient.get(`/issues?owner=${username}&repo=${repo}`);
    return res.data;
}