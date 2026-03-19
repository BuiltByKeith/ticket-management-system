import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines clsx and tailwind-merge.
 * clsx handles conditional classes.
 * twMerge resolves Tailwind class conflicts (e.g. p-2 and p-4 won't both apply).
 */

export { cn } from '../lib/utils'
