import { useAuth } from "@/context/AuthContext";
import { Outlet, useNavigate } from "react-router";

export default function DashboardLayout() {
    const auth = useAuth();
    const navigate = useNavigate();
    
    if(!auth) return <div>Loading...</div>;
    
    const { user, loading } = auth;
    
    if(loading) return <div>Loading...</div>;

    if(!user) navigate("/");

    return <Outlet/>;
}