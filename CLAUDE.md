# DMDocs - Project Instructions

## Purpose

Transform the D&D 5.2.1 SRD (Creative Commons CC-BY-4.0) into a cleanly navigable documentation site, optimized for both human readers and LLM consumption.

## Design Philosophy

Dense but readable. Users want quick reference, not magazine layouts. Tight spacing, compact tables, minimal decorative whitespace.

## Tech Stack

- **Framework:** Next.js 14 + Fumadocs (v13.4.10)
- **Content:** MDX files with YAML frontmatter
- **Styling:** Tailwind CSS + Fumadocs UI
- **Dev:** `npm run dev` runs on localhost:3000

### Version Pinning (Important)

Fumadocs versions must stay aligned. These work together:
- fumadocs-core: 13.4.10
- fumadocs-mdx: 10.0.2
- fumadocs-ui: 13.4.10

Do NOT upgrade to v14+ without also upgrading to React 19.

### Dev Mode Note

`output: 'export'` was removed from next.config.mjs for dev mode compatibility. Add it back for production static builds.

## Source Material

- **PDF:** `pdfs/SRD_5.2.1.pdf` (official WotC release, May 2025)
- **Extracted text:** `pdfs/SRD_5.2.1.txt` (24k lines, has column interleaving issues from PDF layout)
- **TOC reference:** `TOC.md` maps the full PDF hierarchy

## Content Structure

### Navigation Pattern

Each major SRD section gets:
1. A **section header** (white text, non-clickable): `---Section Name---` in root meta.json
2. A **dropdown folder** (collapsible) containing the pages

This creates intentional duplication (header + folder with same name) for visual hierarchy.

### File Organization

```
content/
├── index.mdx                     # Site landing page
├── meta.json                     # Root navigation
├── playing-the-game/             # Dropdown folder
│   ├── meta.json                 # Lists pages in order
│   ├── rhythm-of-play.mdx
│   ├── the-six-abilities.mdx
│   └── ...
├── character-creation/
│   ├── meta.json
│   └── ...
└── [other sections]/
```

### Page Template

```mdx
---
title: Page Title
description: Brief description for SEO and LLM context
---

# Page Title

Content here. Use ## for subheadings that appear in the PDF TOC as indented items.

## Subheading

More content.
```

### Naming Conventions

- Folder names: kebab-case matching section name (`playing-the-game`)
- File names: kebab-case matching page title (`rhythm-of-play.mdx`)
- Match PDF hierarchy exactly where possible

## Current Progress

### Complete:
- [x] Playing the Game (7 pages under "Rules" header)
- [x] Combat (6 pages as separate dropdown under "Rules" header)
- [x] Spellbook (323 spells, organized by 8 schools)
- [x] Bestiary (329 monsters, organized by 14 creature types)

### Scaffolded (structure only, placeholder content):
- [x] Character Creation (6 pages)

### Not Yet Scaffolded:
- [ ] Classes (12 classes, each with subclass - use dropdown)
- [ ] Character Origins (backgrounds + species - use dropdown)
- [ ] Feats
- [ ] Equipment (consider splitting: Weapons, Armor, Gear, Services)
- [ ] Magic Items (need extraction script - follow bestiary pattern)
- [ ] Rules Glossary (keep flat - alphabetical reference)
- [ ] Gameplay Toolbox

## Multi-Docs Architecture

The site uses Fumadocs multi-docs pattern for content types with unique schemas:

```
/                     # Root
├── content/          # General docs (rules, classes, etc.)
├── spellbook/        # Spells by school
└── bestiary/         # Monsters by creature type
```

Each content source is defined in `source.config.ts` with its own Zod schema extending `frontmatterSchema`.

### Adding a New Content Type (e.g., Magic Items)

1. **Create folder structure**: `magicitems/` at root with subfolders by category
2. **Define schema** in `source.config.ts`:
   ```typescript
   const magicItemSchema = frontmatterSchema.extend({
     rarity: z.enum(['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Artifact']).optional(),
     attunement: z.boolean().optional(),
     itemType: z.string().optional(),
   });
   ```
3. **Add to sources** in `source.config.ts`
4. **Create route**: `app/(docs)/magicitems/[[...slug]]/page.tsx` (copy from bestiary)
5. **Create layout**: `app/(docs)/magicitems/layout.tsx` with theme class
6. **Add theme** in `globals.css` (optional, for distinct coloring)

### Schema Gotchas

- **Zod version**: Must use 3.23.8 (pinned in package.json)
- **CR as string**: Challenge ratings must be quoted in YAML (`cr: "17"` not `cr: 17`)
- **Optional fields**: Use `.optional()` liberally - not all monsters have all fields

### Navigation Patterns

- **Collapsed by default**: Add `"defaultOpen": false` to meta.json
- **Avoid sidebar duplication**: Don't include `"index"` in pages array if folder has index.mdx
- **Cross-references**: For items appearing in multiple categories, create stub page with meta refresh redirect

### Theming

Each content type can have its own color theme in `globals.css`:
```css
.theme-bestiary {
  --primary: 350 70% 40%;  /* HSL values */
}
```

### Cache Clearing

When navigation breaks or files aren't found:
```bash
rm -rf .next .source && npm run dev
```

Note: `.source` is Fumadocs' cache for MDX processing.

## Lessons Learned (Jan 2026)

### Navigation Architecture
- White section headers (`---Name---`) group related dropdowns conceptually
- A folder with `meta.json` automatically becomes a dropdown
- Beefy sections deserve their own dropdown, not just a long single page
- Related content should nest together (e.g., Damage & Healing under Combat)

### The PDF TOC Isn't Sacred
- Reorganize away from PDF hierarchy where it improves browsing UX
- "Playing the Game" → "Rules" is a cleaner mental model for the section header
- Combat as a peer to Playing the Game (not nested) reflects how people look things up
- Think about what people search for—that's likely dropdown-worthy

### Technical Workflow
- `rm -rf .next` when navigation gets weird after restructuring
- Update multiple meta.json files when moving things (root + section-level)
- Hot reload doesn't always catch folder moves—restart sometimes needed
- When moving a page to a folder, delete the old .mdx file

### Content Extraction
- Despite column interleaving in PDF text, content is extractable with manual cleanup
- Tables need markdown reformatting
- PDF sidebars become `##` sections or callouts
- Use `&` in titles where it reads better (Damage & Healing)

### Future Section Predictions
- Classes, Spells, Monsters will each need their own dropdowns (high volume)
- Equipment might benefit from splitting (Weapons, Armor, Gear, Services)
- Rules Glossary should stay flat since it's alphabetical reference

### Class Page Structure
Each class page follows this pattern:
1. **Frontmatter**: title (class name), description (flavor + primary ability + hit die)
2. **Import**: `import { Tab, Tabs } from 'fumadocs-ui/components/tabs';`
3. **Core Traits Table**: Primary ability, hit die, saves, skills, weapons, armor, starting equipment
4. **Becoming a [Class]**: Level 1 and multiclass entry requirements
5. **Class Features Table**: Level progression with proficiency bonus, features, class-specific columns
6. **Features by Tier (Tabs)**:
   - Tier 1 (Levels 1-4): Foundation abilities
   - Tier 2 (Levels 5-10): Core power spike (Extra Attack, etc.)
   - Tier 3 (Levels 11-16): Advanced abilities
   - Tier 4 (Levels 17-20): Capstone abilities
7. **Subclass Section**: After the tabs, with its own level-based features (#### headings)
8. **Spell List** (if applicable): After subclass, table of spells by level

Spellcasting classes: Bard, Cleric, Druid, Paladin, Ranger, Sorcerer, Warlock, Wizard

## Content Extraction

### Source Material

- **PDF**: Has column interleaving issues, not ideal for bulk extraction
- **GitHub markdown**: https://github.com/springbov/dndsrd5.2_markdown - clean 5.2.1 markdown, used for spells and monsters

### Import Scripts

Located in `scripts/`:
- `import-spells.py` - Parses spell markdown, generates MDX with typed frontmatter
- `import-monsters.py` - Parses monster markdown, generates MDX with stat block data
- `reorganize-*.py` - Group related creatures (dragons, fiends, goblinoids, etc.)

### Creature Grouping Pattern

Related creatures get subfolders with comparison tables:
```
bestiary/dragon/
├── index.mdx           # Overview of all dragons
├── red-dragon/
│   ├── index.mdx       # Red dragon comparison table (wyrmling → ancient)
│   ├── wyrmling.mdx
│   ├── young.mdx
│   ├── adult.mdx
│   └── ancient.mdx
└── [other colors]/
```

Applied to: dragons (by color), devils/demons (by CR), goblins/hobgoblins/bugbears, elementals/mephits, golems, sphinxes, hags.

### Cross-Type References

When a creature logically belongs in multiple places (e.g., Night Hag is a Fiend but grouped with Hags under Fey):
1. Keep canonical page in correct type folder (`fiend/night-hag.mdx`)
2. Create stub in related folder (`fey/hags/night-hag.mdx`) with:
   - Title including type hint: "Night Hag (Fiend)"
   - Meta refresh redirect to canonical page
   - Fallback link for accessibility

## LLM Optimization (TODO)

Based on docs-ai-era research:
- [ ] Add `llms.txt` at root with site structure
- [ ] Ensure consistent frontmatter across all pages
- [ ] Add structured data (JSON-LD) for stat blocks
- [ ] Cross-reference related content

## Attribution (Required)

Every page should include or link to:

> This work includes material from the System Reference Document 5.2.1 by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. Licensed under CC-BY-4.0.

## Common Tasks

### Add a new flat section
1. Create folder: `content/section-name/`
2. Add `meta.json` with `{"title": "Section Name", "pages": [...]}`
3. Create page files
4. Add to root `meta.json`: `"---Section Name---"` then `"section-name"`

### Run dev server
```bash
npm run dev
```

### Build for production
```bash
# Add output: 'export' to next.config.mjs first
npm run build
```

### Clear cache if errors
```bash
rm -rf .next .source && npm run dev
```

### Force restart (turbopack corruption)
```bash
pkill -9 -f "next"; rm -rf .next .source; npm run dev
```
