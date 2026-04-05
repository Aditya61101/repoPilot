/* eslint-disable react-refresh/only-export-components */
import { me } from "@/api/auth";
import type { User } from "@/interfaces/User";
import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext<{ user: User|null; loading: boolean } | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User|null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        me().then((res) => {
            if(res.status==401) throw new Error();
            return res.data;
        })
        .then(setUser)
        .catch(() => setUser(null))
        .finally(() => setLoading(false));
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext);