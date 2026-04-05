import { protectedApiClient } from "./client";

export const fetchRepos = async () => {
    return await protectedApiClient.get(`/repos/`);
}