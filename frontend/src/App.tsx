import { ThemeProvider } from 'next-themes';
import { QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router'
import * as monaco from 'monaco-editor';
import { loader } from '@monaco-editor/react';

// pages
import SetupPage from '@/pages/SetupPage'
import ReviewPage from '@/pages/ReviewPage'
import LandingPage from '@/pages/LandingPage';
import { AuthProvider } from './context/AuthContext';
import DashboardLayout from './layouts/dashboard-layout';
import { queryClient } from './lib/queryClient';
// Configure the loader to use the local monaco-editor package
loader.config({ monaco });

function App() {
  // const queryClient = new QueryClient();
  const router = createBrowserRouter([
    { path: "/", element: <LandingPage /> },
    {
      element: <DashboardLayout />, 
      children: [
        { path: "/setup", element: <SetupPage /> },
        { path: "/review", element: <ReviewPage /> }
      ]
    }
  ]);
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <RouterProvider router={router} />
        </ThemeProvider>
      </QueryClientProvider>
    </AuthProvider>
  )
}

export default App
