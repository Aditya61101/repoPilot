import { ThemeProvider } from 'next-themes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router'
import * as monaco from 'monaco-editor';
import { loader } from '@monaco-editor/react';

// pages
import SetupPage from './pages/SetupPage'
import ReviewPage from './pages/ReviewPage'
// Configure the loader to use the local monaco-editor package
loader.config({ monaco });

function App() {
  const queryClient = new QueryClient();
  const router = createBrowserRouter([
    { path: "/", element: <SetupPage /> },
    { path: "/review", element: <ReviewPage /> },
  ]);
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <RouterProvider router={router} />
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
