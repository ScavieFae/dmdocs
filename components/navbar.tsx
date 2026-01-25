"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSearchContext } from "fumadocs-ui/provider";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Search, Home, BookOpen, Skull, Sun, Moon, ScanEye } from "lucide-react";

const navLinks = [
  { href: "/", label: "Home", icon: Home },
  { href: "/docs", label: "Rules", icon: BookOpen },
  { href: "/spellbook", label: "Spellbook", icon: ScanEye },
  { href: "/bestiary", label: "Bestiary", icon: Skull },
];

export function Navbar() {
  const pathname = usePathname();
  const { setOpenSearch } = useSearchContext();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-fd-border bg-fd-background/95 backdrop-blur supports-[backdrop-filter]:bg-fd-background/80 pt-3">
      {/* Top row: masthead + search + theme toggle */}
      <div
        className="flex h-14 items-center gap-4"
        style={{ paddingLeft: "var(--fd-layout-offset, 0px)", paddingRight: "var(--fd-layout-offset, 0px)" }}
      >
        <div className="flex items-center gap-4 px-4">
          <Link href="/" className="font-bold text-2xl shrink-0">
            DNDocs
          </Link>
        </div>

        {/* Search bar - centered, expandable */}
        <div className="flex-1 flex justify-center">
          <button
            onClick={() => setOpenSearch(true)}
            className="flex items-center gap-2 px-4 py-2.5 text-sm text-fd-muted-foreground bg-fd-muted border border-fd-border rounded-lg hover:bg-fd-accent transition-colors w-full max-w-md"
          >
            <Search className="h-4 w-4" />
            <span>Search...</span>
            <kbd className="ml-auto hidden sm:inline-flex h-5 items-center gap-1 rounded border border-fd-border bg-fd-muted px-1.5 font-mono text-[10px] font-medium text-fd-muted-foreground">
              <span className="text-xs">⌘</span>K
            </kbd>
          </button>
        </div>

        {/* Right side - theme toggle */}
        <div className="shrink-0 px-4">
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 rounded-md hover:bg-fd-accent transition-colors"
            aria-label="Toggle theme"
          >
            {mounted && (theme === "dark" ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            ))}
          </button>
        </div>
      </div>

      {/* Bottom row: navigation links - Shadcn-style pill tabs */}
      <div
        className="flex items-center h-12 pb-2"
        style={{ paddingLeft: "calc(var(--fd-layout-offset, 0px) + 1rem)", paddingRight: "var(--fd-layout-offset, 0px)" }}
      >
        <nav className="inline-flex items-center gap-1 p-1 bg-fd-muted rounded-lg text-sm">
          {navLinks.map((link) => {
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
                  isActive(link.href)
                    ? "bg-fd-background text-fd-foreground font-medium shadow-sm"
                    : "text-fd-muted-foreground hover:text-fd-foreground hover:bg-fd-background/50"
                }`}
              >
                <Icon className="h-4 w-4" />
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
