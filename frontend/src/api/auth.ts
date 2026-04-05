import { protectedApiClient } from "./client";

export const me = async () => {
    return await protectedApiClient.get(`/auth/me`);
}