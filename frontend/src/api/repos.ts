import { apiClient } from "./apiClient";

export const fetchRepos = async (username:string) => {
    const res = await apiClient.get(`/repos?owner=${username}`);
    return res.data;
}