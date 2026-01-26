import Link from "next/link";
import { BookOpen, Skull, Sparkles, Gem } from "lucide-react";
import { Button } from "@/components/ui/button";

const sections = [
  {
    title: "Rules",
    description:
      "Core mechanics, classes, character creation, combat, and gameplay. Everything you need to play.",
    href: "/docs",
    icon: BookOpen,
    color: "hsl(48, 85%, 48%)",
  },
  {
    title: "Bestiary",
    description:
      "330 monsters from Aboleth to Zombie. Stats, abilities, and lore for every creature in the SRD.",
    href: "/bestiary",
    icon: Skull,
    color: "hsl(350, 70%, 45%)",
  },
  {
    title: "Spellbook",
    description:
      "All 339 spells organized by school. Quick reference for casting times, ranges, and effects.",
    href: "/spellbook",
    icon: Sparkles,
    color: "hsl(182, 70%, 40%)",
  },
  {
    title: "Magic Items",
    description:
      "257 wondrous items, weapons, armor, and artifacts. Rarity, attunement, and properties.",
    href: "/magicitems",
    icon: Gem,
    color: "hsl(270, 35%, 55%)",
  },
];

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 md:p-24">
      <h1 className="text-4xl font-bold mb-2">DMDocs</h1>
      <p className="text-lg text-fd-muted-foreground mb-8 text-center max-w-lg">
        The complete D&D 5e System Reference Document, optimized for quick lookup
      </p>

      <Button asChild size="lg" className="mb-12">
        <Link href="/docs">Enter the SRD</Link>
      </Button>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-3xl w-full mb-12">
        {sections.map((section) => (
          <Link
            key={section.title}
            href={section.href}
            className="group p-6 rounded-xl border border-fd-border bg-fd-card hover:border-fd-primary/50 transition-colors"
          >
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center mb-4"
              style={{ backgroundColor: `${section.color}20` }}
            >
              <section.icon
                className="w-5 h-5"
                style={{ color: section.color }}
              />
            </div>
            <h2 className="font-semibold text-lg mb-2 group-hover:text-fd-primary transition-colors">
              {section.title}
            </h2>
            <p className="text-sm text-fd-muted-foreground leading-relaxed">
              {section.description}
            </p>
          </Link>
        ))}
      </div>

      <p className="text-xs text-fd-muted-foreground max-w-md text-center">
        Based on SRD 5.2.1 by Wizards of the Coast LLC, licensed under CC-BY-4.0
      </p>
    </main>
  );
}
