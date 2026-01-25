# DNDocs: Project Approach

This document captures how we approached building a D&D 5.2.1 SRD documentation site, with particular focus on treating spell data as structured, queryable content rather than static pages.

## The Goal

Transform the D&D 5.2.1 System Reference Document (Creative Commons CC-BY-4.0) into a cleanly navigable documentation site optimized for both human readers and LLM consumption. The key insight: reference data like spells, monsters, and magic items should be **structured data first**, with documentation pages generated from that structure.

## Tech Stack

- **Framework:** Next.js 14 + Fumadocs (v13.4.10)
- **Content:** MDX files with YAML frontmatter
- **Schema Validation:** Zod (v3.23.8 - must match fumadocs-mdx's internal version)
- **Styling:** Tailwind CSS + Fumadocs UI

### Version Pinning Note

Fumadocs and Zod versions must stay aligned. We hit a breaking issue with Zod v4 vs v3 incompatibility—fumadocs-mdx internally uses Zod v3, so our schema definitions must use the same version or `frontmatterSchema.extend()` fails with cryptic errors like `keyValidator._parse is not a function`.

## Architecture: Multi-Docs Pattern

The site uses Fumadocs' multi-docs architecture with separate content sources:

```
content/          → /docs      (rules, classes, equipment)
bestiary/         → /bestiary  (monster stat blocks)
spellbook/        → /spellbook (spell reference)
```

Each source has its own:
- Directory of MDX files
- `meta.json` files for navigation structure
- Optional schema for typed frontmatter
- Dedicated layout and page components

This separation allows each content type to have its own schema, styling (via CSS custom properties), and navigation structure.

## The Spellbook: Treating Spells as Structured Data

### The Problem with Static Spell Pages

The SRD contains 70+ spells. If each is a static MDX page with prose content, you get:
- Alphabetical listing only (like Wizards does)
- No easy filtering by level, school, class
- Hard for LLMs to query programmatically
- Duplication if you want multiple views

### The Solution: Schema-Validated Frontmatter

Instead of treating spells as prose, we treat them as **structured data with a description field**. Each spell is an MDX file where:
- Frontmatter contains all queryable fields (level, school, components, etc.)
- Body contains the spell description (can include markdown formatting)
- Fumadocs validates the frontmatter against a Zod schema at build time

### The Spell Schema

```typescript
// source.config.ts
import { frontmatterSchema } from 'fumadocs-mdx/config';
import { z } from 'zod';

const spellSchema = frontmatterSchema.extend({
  level: z.number().min(0).max(9).optional(),  // 0 = cantrip
  school: z.enum([
    'Abjuration', 'Conjuration', 'Divination', 'Enchantment',
    'Evocation', 'Illusion', 'Necromancy', 'Transmutation',
  ]).optional(),
  castingTime: z.string().optional(),
  range: z.string().optional(),
  components: z.object({
    verbal: z.boolean(),
    somatic: z.boolean(),
    material: z.string().optional(),
  }).optional(),
  duration: z.string().optional(),
  concentration: z.boolean().default(false),
  ritual: z.boolean().default(false),
  classes: z.array(z.string()).optional(),
  higherLevel: z.string().optional(),
});
```

Fields are optional so non-spell pages (like the index) can exist in the same collection without all fields.

### Example Spell MDX File

```mdx
---
title: Fireball
level: 3
school: Evocation
castingTime: Action
range: 150 feet
components:
  verbal: true
  somatic: true
  material: a ball of bat guano and sulfur
duration: Instantaneous
concentration: false
ritual: false
classes:
  - Sorcerer
  - Wizard
higherLevel: The damage increases by 1d6 for each spell slot level above 3.
---

A bright streak flashes from you to a point you choose within range and then blossoms with a low roar into a fiery explosion. Each creature in a 20-foot-radius Sphere centered on that point makes a Dexterity saving throw, taking 8d6 Fire damage on a failed save or half as much damage on a successful one.

Flammable objects in the area that aren't being worn or carried start burning.
```

### Querying Spells

With this structure, filtering is straightforward:

```typescript
// lib/source.ts
export function getAllSpells() {
  return spellSource.getPages();
}

export function getSpellsByLevel(level: number) {
  return getAllSpells().filter(spell => spell.data.level === level);
}

export function getSpellsBySchool(school: string) {
  return getAllSpells().filter(spell => spell.data.school === school);
}

export function getSpellsByClass(className: string) {
  return getAllSpells().filter(spell =>
    spell.data.classes?.includes(className)
  );
}
```

### Rendering the Spell Stats Card

The page component checks if `level` exists to determine if a page is a spell, then renders a stats card:

```tsx
function SpellStats({ data }: { data: any }) {
  if (data.level === undefined) return null;

  const levelText = data.level === 0 ? 'Cantrip' : `Level ${data.level}`;
  const components = [
    data.components?.verbal && 'V',
    data.components?.somatic && 'S',
    data.components?.material && `M (${data.components.material})`,
  ].filter(Boolean).join(', ');

  return (
    <div className="spell-stats mb-6 p-4 rounded-lg bg-fd-muted/50 text-sm">
      <div className="font-medium text-fd-muted-foreground mb-2">
        {levelText} {data.school}
        {data.ritual && ' (Ritual)'}
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div><strong>Casting Time:</strong> {data.castingTime}</div>
        <div><strong>Range:</strong> {data.range}</div>
        <div><strong>Components:</strong> {components}</div>
        <div><strong>Duration:</strong> {data.duration}</div>
      </div>
      {data.classes && (
        <div className="mt-2 text-fd-muted-foreground">
          <strong>Classes:</strong> {data.classes.join(', ')}
        </div>
      )}
    </div>
  );
}
```

## Sidebar Organization

We organized spells by school (8 folders) rather than alphabetically or by level:

```
spellbook/
├── index.mdx
├── meta.json
├── abjuration/
├── conjuration/
├── divination/
├── enchantment/
├── evocation/
├── illusion/
├── necromancy/
└── transmutation/
```

Each school folder has its own `meta.json` listing its spells. This keeps the sidebar manageable (8 collapsible sections) while still allowing direct navigation.

## Extracting Spells from the SRD PDF

### The Challenge

The official SRD PDF (`pdfs/SRD_5.2.1.pdf`) was converted to text, but the two-column layout caused **line interleaving**—left and right column content alternates line by line:

```
Acid Arrow                                                (right column text)
Level 2 Evocation (Wizard)                                (right column text)
Casting Time: Action                                      Audible Alarm...
```

This makes automated extraction difficult.

### Extraction Approach

We wrote a Python script (`scripts/extract-spells.py`) that:
1. Scans for spell header patterns: `Level X School (Classes)` or `School Cantrip (Classes)`
2. Extracts the preceding spell name
3. Parses Casting Time, Range, Components, Duration from subsequent lines
4. Captures the description text
5. Generates MDX files with proper YAML frontmatter

Due to column interleaving, the script only catches ~10% of spells. The remaining spells need manual entry or a cleaner data source.

### Manual Entry Approach

For manual entry, we use the sample spells as templates. The pattern:
1. Copy spell name and metadata from PDF
2. Create MDX file in appropriate school folder
3. Fill in frontmatter fields
4. Paste and clean up description
5. Add file to school's `meta.json`

## Future: JSON API Endpoint

The structured frontmatter enables a future JSON API endpoint that exposes all spell data programmatically—useful for:
- LLM tool use (query spells by criteria)
- Third-party apps
- Search indexes

This would be a simple API route that calls `getAllSpells()` and returns the data as JSON.

## Key Learnings

1. **Frontmatter is your friend** - Fumadocs' schema validation turns MDX frontmatter into typed, queryable data
2. **Version alignment matters** - Zod v3 vs v4 caused silent failures; always check peer dependency versions
3. **PDF extraction is hard** - Multi-column PDFs don't convert cleanly to text; sometimes manual entry is faster
4. **Organize for humans** - Schools as top-level folders keeps sidebar navigable; levels can be a filter
5. **Schema fields should be optional** - Allows non-spell pages (indexes) to coexist in the same collection

## Status

- [x] Spellbook architecture and schema
- [x] Sample spells (Fire Bolt, Magic Missile, Detect Magic, Fireball)
- [x] Spell stats card component
- [x] School-based sidebar organization
- [ ] Extract remaining ~70 spells from SRD
- [ ] Build spell index pages with filtering
- [ ] Add JSON API endpoint
