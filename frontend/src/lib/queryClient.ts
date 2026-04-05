import { QueryCache, QueryClient } from "@tanstack/react-query"
import { toast } from "sonner";

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            throwOnError: false,
        },
    },
    queryCache: new QueryCache({
        onError: (error) => {
            toast.error(error.message);
        },
    }),
})