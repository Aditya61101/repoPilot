import { ThemeProvider } from 'next-themes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router'
// pages
import SetupPage from './pages/SetupPage'
import ReviewPage from './pages/ReviewPage'

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
