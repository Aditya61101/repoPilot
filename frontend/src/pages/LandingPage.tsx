'use client'

import { ThemeToggle } from '@/components/shared/ThemeToggle';
import { Button } from '@/components/ui/button'
import { useAuth } from '@/context/AuthContext';
import { GitBranch, CheckCircle2, Eye, Zap, LoaderCircle } from 'lucide-react'
import { useState } from 'react';
import { useNavigate } from 'react-router'

function LoginCTA() {
    const [loading, setLoading] = useState(false);

    const handleLogin = () => {
        setLoading(true);
        window.location.href = `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8080/api"}/auth/github`;

    }
    return (
        <Button
            onClick={handleLogin}
            className="rounded-full min-w-30"
        >
            {loading ? <LoaderCircle className='animate-spin' /> : <span> Login with Github </span>}
        </Button>
    )
}

function DashBoardCTA() {
    const navigate = useNavigate();
    return (
        <Button
            className="rounded-full"
            onClick={() => navigate('/setup')}
        >
            Go to Dashboard
        </Button>
    )
}

function ButtonCTA() {
    const auth = useAuth();
    if (!auth) return;

    const { user, loading } = auth;
    if (loading) return;

    return user ? <DashBoardCTA/> : <LoginCTA />;

}

function NavBar() {

    return (
        <nav className="fixed top-0 w-full bg-background/80 backdrop-blur-sm border-b border-border z-50">
            <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    {/* <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                        <span className="text-primary-foreground font-bold">RP</span>
                    </div> */}
                    <span className="font-semibold text-foreground">RepoPilot</span>
                </div>
                <div className="flex items-center gap-3">
                    <ButtonCTA />
                    <ThemeToggle />
                </div>
            </div>
        </nav>
    )
}

function HeroSection() {
    // const navigate = useNavigate()

    return (
        <section className="min-h-screen pt-32 pb-20 px-6 flex flex-col items-center justify-center text-center relative overflow-hidden">
            {/* Subtle background gradient */}
            <div className="absolute inset-0 -z-10 opacity-40">
                <div className="absolute top-40 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
                <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl" />
            </div>

            <div className="max-w-3xl mx-auto space-y-8">
                {/* Pre-headline */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                    <span className="w-2 h-2 bg-primary rounded-full" />
                    <span className="text-sm text-muted-foreground">Powered by AI</span>
                </div>

                {/* Main headline */}
                <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-foreground leading-tight font-sans">
                    Turn GitHub issues into{' '}
                    <span className="bg-linear-to-r from-primary to-accent bg-clip-text text-transparent">
                        pull requests in minutes
                    </span>
                </h1>

                {/* Subheading */}
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                    Select a repo. Pick an issue. Get AI-generated code changes. Review and merge. No context switching required.
                </p>

                {/* CTAs */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                    <ButtonCTA />
                    <Button
                        variant="outline"
                        className="rounded-full"
                        asChild
                    >
                        <a href="#preview">
                            View Demo
                        </a>
                    </Button>
                </div>
            </div>
        </section>
    )
}

function FlowSection() {
    const steps = [
        { icon: GitBranch, label: 'Repository', description: 'Connect your GitHub repo' },
        { icon: CheckCircle2, label: 'Issue', description: 'Select the issue to solve' },
        { icon: Zap, label: 'AI Processing', description: 'Generates code changes' },
        { icon: Eye, label: 'Review', description: 'Inspect the diff' },
        { icon: GitBranch, label: 'Pull Request', description: 'Create PR automatically' },
    ]

    return (
        <section className="py-20 px-6 border-t border-border">
            <div className="max-w-7xl mx-auto space-y-16">
                <div className="text-center space-y-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-foreground">
                        Five steps to deployment
                    </h2>
                    <p className="text-muted-foreground text-lg">
                        A seamless workflow designed for developer efficiency
                    </p>
                </div>

                {/* Flow visualization */}
                <div className="flex items-center justify-center overflow-x-auto pb-4">
                    <div className="flex items-center gap-2 md:gap-4 min-w-max md:min-w-0">
                        {steps.map((step, idx) => {
                            const Icon = step.icon
                            return (
                                <div key={idx} className="flex items-center gap-2 md:gap-4">
                                    <div className="flex flex-col items-center gap-2">
                                        <div className="w-14 h-14 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center hover:bg-primary/20 transition-colors">
                                            <Icon className="w-6 h-6 text-primary" />
                                        </div>
                                        <span className="text-xs md:text-sm font-medium text-foreground text-center whitespace-nowrap">
                                            {step.label}
                                        </span>
                                    </div>
                                    {idx < steps.length - 1 && (
                                        <div className="w-6 md:w-12 h-0.5 bg-linear-to-r from-primary/50 to-transparent" />
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
        </section>
    )
}

function PreviewSection() {
    return (
        <section id="preview" className="py-20 px-6 border-t border-border">
            <div className="max-w-7xl mx-auto space-y-12">
                <div className="text-center space-y-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-foreground">
                        See it in action
                    </h2>
                    <p className="text-muted-foreground text-lg">
                        Watch how RepoPilot transforms issues into production-ready code
                    </p>
                </div>

                {/* Mock UI Preview */}
                <div className="bg-card border border-border rounded-xl overflow-hidden shadow-lg">
                    <div className="aspect-video bg-linear-to-b from-card to-card/50 flex items-center justify-center">
                        <div className="text-center space-y-4">
                            <div className="w-16 h-16 rounded-lg bg-primary/20 flex items-center justify-center mx-auto">
                                <GitBranch className="w-8 h-8 text-primary" />
                            </div>
                            <div className="space-y-2">
                                <p className="text-foreground font-semibold">Live Demo</p>
                                <p className="text-muted-foreground text-sm">See the full workflow in action</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Code preview below */}
                <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-card border border-border rounded-lg p-6 space-y-4">
                        <h3 className="font-mono text-sm text-primary">Issue Selected</h3>
                        <pre className="text-xs text-muted-foreground overflow-auto">
                            {`#2384 - Fix: Memory leak in scheduler
Status: open
Created: Mar 15, 2024

There is a memory leak detected in
the task scheduler module...`}
                        </pre>
                    </div>
                    <div className="bg-card border border-border rounded-lg p-6 space-y-4">
                        <h3 className="font-mono text-sm text-primary">Generated Diff</h3>
                        <pre className="text-xs text-muted-foreground overflow-auto">
                            {`- leaked_memory += size
+ ref_count_dec(block)
  
- if (ptr) free(ptr)
+ if (ptr) {
+   remove_from_list(ptr)
+   free(ptr)
+ }`}
                        </pre>
                    </div>
                </div>
            </div>
        </section>
    )
}

function BenefitsSection() {
    const benefits = [
        {
            title: 'No context switching',
            description: 'Stay in GitHub. Everything happens right there.',
        },
        {
            title: 'AI-assisted code changes',
            description: 'Get production-ready diffs in seconds, not hours.',
        },
        {
            title: 'Review before commit',
            description: 'Always inspect changes before creating a pull request.',
        },
        {
            title: 'Fits your workflow',
            description: 'Integrates seamlessly with your existing GitHub process.',
        },
    ]

    return (
        <section className="py-20 px-6 border-t border-border">
            <div className="max-w-7xl mx-auto space-y-12">
                <div className="text-center space-y-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-foreground">
                        Built for developers
                    </h2>
                    <p className="text-muted-foreground text-lg">
                        Everything you need, nothing you don&apos;t
                    </p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                    {benefits.map((benefit, idx) => (
                        <div
                            key={idx}
                            className="bg-card border border-border rounded-lg p-6 space-y-3 hover:border-primary/50 transition-colors"
                        >
                            <h3 className="font-semibold text-foreground text-lg">
                                {benefit.title}
                            </h3>
                            <p className="text-muted-foreground">
                                {benefit.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

function CTASection() {
    // const navigate = useNavigate()

    return (
        <section className="py-20 px-6 border-t border-border">
            <div className="max-w-4xl mx-auto text-center space-y-8">
                <h2 className="text-4xl md:text-5xl font-bold text-foreground">
                    Start building faster
                </h2>
                <p className="text-lg text-muted-foreground">
                    Connect your GitHub account and transform your issue management today.
                </p>
                <ButtonCTA />
            </div>
        </section>
    )
}

function Footer() {
    return (
        <footer className="border-t border-border px-6 py-12 bg-card/30">
            <div className="max-w-7xl mx-auto">
                {/* <div className="grid md:grid-cols-4 gap-8 mb-12">
                    <div className="space-y-4">
                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-primary rounded-lg flex items-center justify-center">
                                <span className="text-primary-foreground text-xs font-bold">RP</span>
                            </div>
                            <span className="font-semibold text-foreground">RepoPilot</span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                            GitHub issues to pull requests, powered by AI.
                        </p>
                    </div>
                    <div className="space-y-3">
                        <h4 className="font-semibold text-foreground">Product</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground transition-colors">Features</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Pricing</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Docs</a></li>
                        </ul>
                    </div>
                    <div className="space-y-3">
                        <h4 className="font-semibold text-foreground">Company</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground transition-colors">About</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Blog</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Status</a></li>
                        </ul>
                    </div>
                    <div className="space-y-3">
                        <h4 className="font-semibold text-foreground">Legal</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><a href="#" className="hover:text-foreground transition-colors">Privacy</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Terms</a></li>
                            <li><a href="#" className="hover:text-foreground transition-colors">Contact</a></li>
                        </ul>
                    </div>
                </div> */}
                <div className="flex flex-col md:flex-row items-center justify-between text-sm text-muted-foreground">
                    <p>&copy; {new Date().getFullYear()} RepoPilot. All rights reserved.</p>
                    <div className="flex gap-6 mt-4 md:mt-0">
                        <a
                            href="https://www.linkedin.com/in/aditya-kumar-337a08218/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-foreground transition-colors">
                            Linkedin
                        </a>
                        <a
                            href="https://github.com/Aditya61101/repopilot"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-foreground transition-colors">
                            GitHub
                        </a>
                        <a
                            href="https://aditya-folio.vercel.app/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-foreground transition-colors">
                            Portfolio
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-background text-foreground">
            <NavBar />
            <HeroSection />
            <FlowSection />
            <PreviewSection />
            <BenefitsSection />
            <CTASection />
            <Footer />
        </div>
    )
}
