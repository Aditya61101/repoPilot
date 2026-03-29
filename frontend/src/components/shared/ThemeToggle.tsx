import { useTheme } from 'next-themes'
import { Sun, Moon, Monitor } from 'lucide-react'
import { cn } from '@/lib/utils'

const options = [
    { value: 'light', icon: Sun, label: 'Light' },
    { value: 'dark', icon: Moon, label: 'Dark' },
    { value: 'system', icon: Monitor, label: 'System' },
] as const

export function ThemeToggle() {
    const { theme, setTheme } = useTheme()

    return (
        <div className="flex items-center gap-1 rounded-lg border border-border p-1">
            {options.map(({ value, icon: Icon, label }) => (
                <button
                    key={value}
                    onClick={() => setTheme(value)}
                    title={label}
                    className={cn(
                        "p-1.5 rounded-md transition-colors cursor-pointer",
                        theme === value
                            ? "bg-primary text-white"
                            : "text-muted-foreground hover:bg-muted"
                    )}
                >
                    <Icon size={14} />
                </button>
            ))}
        </div>
    )
}