import Link from "next/link";
import { BookOpen, Skull, Sparkles, Gem } from "lucide-react";
import { HomeSearch } from "@/components/home-search";

const sections = [
  {
    title: "Rules",
    description: "Classes, character creation, combat, spellcasting, equipment",
    href: "/docs",
    icon: BookOpen,
    color: "hsl(48, 85%, 48%)",
    count: "100+ pages",
  },
  {
    title: "Spellbook",
    description: "Every spell by school from cantrips to 9th level",
    href: "/spellbook",
    icon: Sparkles,
    color: "hsl(182, 70%, 40%)",
    count: "339 spells",
  },
  {
    title: "Bestiary",
    description: "Stat blocks for every creature, CR 0 to CR 30",
    href: "/bestiary",
    icon: Skull,
    color: "hsl(350, 70%, 45%)",
    count: "330 monsters",
  },
  {
    title: "Magic Items",
    description: "Wondrous items, weapons, armor, potions, and artifacts",
    href: "/magicitems",
    icon: Gem,
    color: "hsl(270, 35%, 55%)",
    count: "257 items",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col justify-center max-w-2xl mx-auto px-6 py-16 md:py-24">
      {/* Header lockup — logo left, title + tagline stacked right */}
      <div className="flex items-center gap-5 mb-8">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" className="h-16 w-16 shrink-0">
          <mask id="hero-hex-cuts">
            <polygon points="16,1 28,8 28,24 16,31 4,24 4,8" fill="white"/>
            <line x1="16" y1="0" x2="16" y2="32" stroke="black" strokeWidth="2.5"/>
            <line x1="3" y1="7" x2="29" y2="25" stroke="black" strokeWidth="2.5"/>
            <line x1="29" y1="7" x2="3" y2="25" stroke="black" strokeWidth="2.5"/>
          </mask>
          <polygon points="16,1 28,8 28,24 16,31 4,24 4,8" fill="#E8B923" mask="url(#hero-hex-cuts)"/>
        </svg>
        <div>
          <h1 className="text-3xl font-bold">DMDocs</h1>
          <p className="text-fd-muted-foreground">
            D&D 5e System Reference Document – searchable, browsable, free.
          </p>
        </div>
      </div>

      {/* Search — wider than content on desktop, contained on mobile */}
      <div className="mb-10 md:-mx-12">
        <HomeSearch />
      </div>

      {/* Sections — typographic list, not cards */}
      <nav className="space-y-0 mb-12">
        {sections.map((section) => (
          <Link
            key={section.title}
            href={section.href}
            className="group flex items-center justify-between gap-3 py-3 border-b border-fd-border hover:border-fd-primary/40 transition-colors"
          >
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <section.icon
                  className="h-4 w-4 shrink-0"
                  style={{ color: section.color }}
                />
                <span
                  className="text-lg font-semibold group-hover:underline underline-offset-4"
                  style={{ color: section.color }}
                >
                  {section.title}
                </span>
              </div>
              <p className="text-sm text-fd-muted-foreground mt-0.5 ml-6">
                {section.description}
              </p>
            </div>
            <span className="text-xs text-fd-muted-foreground font-mono shrink-0">
              {section.count}
            </span>
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <p className="text-xs text-fd-muted-foreground">
        Based on the{" "}
        <a
          href="https://www.dndbeyond.com/srd"
          className="underline underline-offset-2 hover:text-fd-foreground transition-colors"
          target="_blank"
          rel="noopener noreferrer"
        >
          SRD 5.2.1
        </a>{" "}
        by Wizards of the Coast LLC, licensed under CC-BY-4.0.
      </p>
    </main>
  );
}
