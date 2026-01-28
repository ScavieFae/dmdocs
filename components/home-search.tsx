"use client";

import { useSearchContext } from "fumadocs-ui/provider";
import { Search } from "lucide-react";

export function HomeSearch() {
  const { setOpenSearch } = useSearchContext();

  return (
    <button
      onClick={() => setOpenSearch(true)}
      className="flex items-center gap-3 w-full px-5 py-3.5 text-sm text-fd-muted-foreground bg-fd-muted border-2 border-fd-border rounded-lg hover:border-fd-primary/50 transition-colors text-left"
    >
      <Search className="h-4 w-4 shrink-0" />
      <span>Search spells, monsters, rules...</span>
      <kbd className="ml-auto hidden sm:inline-flex h-5 items-center gap-1 rounded border border-fd-border bg-fd-background px-1.5 font-mono text-[10px] font-medium text-fd-muted-foreground">
        <span className="text-xs">⌘</span>K
      </kbd>
    </button>
  );
}
