type SkeletonProps = {className?: String}

export function Skeleton({className = ''}: SkeletonProps){
    return <div className={`animate-pulse rounded-md bg-skeleton ${className}`} />
}