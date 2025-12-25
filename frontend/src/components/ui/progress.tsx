import { cn } from "@/lib/utils"

interface ProgressProps {
  value: number
  className?: string
}

export function Progress({ value, className }: ProgressProps) {
  return (
    <div className={cn("relative h-2 w-full overflow-hidden rounded-full bg-gray-200", className)}>
      <div
        className="h-full bg-blue-600 transition-all duration-300"
        style={{ width: `${value}%` }}
      />
    </div>
  )
}
