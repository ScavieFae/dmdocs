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
- **Extracted text (authoritative):** `pdfs/DND-SRD-5.2.1-CC - updated.docx.txt` — verified against PDF, use for verification
- **Extracted text (old):** `pdfs/SRD_5.2.1.txt` (24k lines, has column interleaving issues)
- **TOC reference:** `TOC.md` maps the full PDF hierarchy
- **Verification status:** `VERIFICATION-STATUS.md` — checklist of audited vs pending pages

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

See `VERIFICATION-STATUS.md` for detailed page-by-page checklist.

**Verified against SRD:** Classes (all 12), Character Creation, Origins (species + backgrounds), Feats, Level Advancement, Rules Glossary, Gameplay Toolbox

**Not yet verified:** Playing the Game, Combat, Equipment, Magic Item Rules, Spellbook, Bestiary

**Key finding:** Initial content was created from 2024 PHB, not SRD. Approach unverified sections with suspicion—they likely contain non-SRD material.

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

### Internal Link URLs

When writing links in MDX, use the **URL prefix**, not the directory name:

| Directory | URL Prefix | Example Link |
|-----------|------------|--------------|
| `content/` | `/docs` | `[Rules Glossary](/docs/rules-glossary)` |
| `spellbook/` | `/spellbook` | `[Fireball](/spellbook/evocation/fireball)` |
| `bestiary/` | `/bestiary` | `[Red Dragon](/bestiary/dragon/red-dragon)` |
| `magicitems/` | `/magicitems` | `[Bag of Holding](/magicitems/wondrous-items/bag-of-holding)` |

**Common mistake:** `/rules-glossary` (wrong) vs `/docs/rules-glossary` (correct).

Run `npm run validate-links` to catch broken internal links.

### Search

Search API at `/api/search` indexes all content with tag filtering.

- **Tags:** Rules, Spells, Monsters, Magic Items
- **Config:** `app/layout.tsx` (RootProvider search options)
- **Endpoint:** `app/api/search/route.ts`

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

## Content Verification

### Authoritative Source

**PDF screenshots are the authoritative source.** Do NOT trust:
- D&D Beyond web extracts (contaminated with 2024 PHB rules, not 5.2.1 SRD)
- Text extracted from PDF (column interleaving causes errors)
- Memory/paraphrasing (must match PDF verbatim for CC compliance)

### Dual-Column PDF Pitfalls

The SRD PDF uses two-column layout. Common transcription errors:
- **End-of-page drift**: Content at bottom of pages often missed or paraphrased
- **Column transitions**: Sections spanning columns get incomplete
- **Tables**: Can interleave incorrectly when extracted as text

When verifying, pay extra attention to page edges and column boundaries.

### Spell Naming (5.2.1 Change)

**The 5.2.1 SRD removed wizard name prefixes from spells for CC licensing.**

Old (5e) → New (5.2.1):
- Melf's Acid Arrow → Acid Arrow
- Tasha's Hideous Laughter → Hideous Laughter
- Tenser's Floating Disk → Floating Disk
- Leomund's Tiny Hut → Tiny Hut
- Leomund's Secret Chest → Secret Chest
- Bigby's Hand → Arcane Hand
- Mordenkainen's Sword → Arcane Sword
- Mordenkainen's Faithful Hound → Faithful Hound
- Mordenkainen's Private Sanctum → Private Sanctum
- Mordenkainen's Magnificent Mansion → Magnificent Mansion
- Evard's Black Tentacles → Black Tentacles
- Otiluke's Resilient Sphere → Resilient Sphere
- Otiluke's Freezing Sphere → Freezing Sphere
- Otto's Irresistible Dance → Irresistible Dance
- Rary's Telepathic Bond → Telepathic Bond
- Drawmij's Instant Summons → Instant Summons
- Nystul's Magic Aura → Arcanist's Magic Aura

**This affects ALL class spell lists**, not just Wizard. Check each spellcasting class.

### Class Verification Status

All 12 classes verified against SRD (Jan 2026). See `VERIFICATION-STATUS.md` for details.

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

## Future Work (TODO)

- [ ] **Frontmatter schema validator** — Script or pre-commit hook that validates MDX frontmatter against Zod schemas in `source.config.ts`. Would catch issues like missing required fields (e.g., `somatic: false` in spell components). Could be `npm run validate` or CI check on PRs.
- [x] **Bestiary list audit** — Monster list matches SRD (330/330). Size metadata corrected (26 Tiny creatures were marked Small).
- [x] **Lycanthrope fixes** — All 5 lycanthropes (Werebear, Wereboar, Wererat, Weretiger, Werewolf) fixed:
  - Added "(Lycanthrope)" tag to creatureType
  - Added alternate speeds for beast forms
  - Size set to "Medium" (schema limitation, see below)
- [ ] **Bestiary deep content audit** — Stat block text needs verification against SRD. Known issues found in sampling:
  - Earth Elemental was missing Thunder vulnerability (fixed)
  - Minor text simplifications in complex abilities (e.g., dragon Shapechange details)
  - Typos in action descriptions
  - Use `/audit-collection bestiary --deep` when ready for full pass
- [ ] **Headless batch processing** — Use Claude Code fan-out pattern for 500+ MDX entries:
  1. Generate file list: `claude -p "List all spellbook MDX files that need rarity metadata"`
  2. Loop with scoped tools: `for file in $(cat files.txt); do claude -p "Verify @$file against SRD" --allowedTools "Read,Grep"; done`
  3. Test on 2-3 files, refine prompt, then run at scale
  - Use cases: SRD verification, metadata fixes, content audits, bulk formatting
  - See: rnd-2026/coding/claude-code/allowed-tools.md for tool scoping
- [ ] **Mobile responsiveness** — Fumadocs horizontal nav tabs get cut off on mobile (Magic Items not visible). Need to review:
  - Nav tab overflow/scrolling behavior
  - ~~Homepage card grid on small screens~~ (fixed: descriptions now stack below titles)
- [ ] **Export builder** — Interactive UI where users select content slices and download structured data. Scope:
  - **Selection modes**: All spells, spells by class, spells by school/level, all monsters, monsters by type/CR range, all magic items, items by rarity, etc.
  - **Output formats**: JSON, YAML, TOML — user picks from a dropdown
  - **Data shape**: Frontmatter fields (typed from Zod schemas) + page content as markdown text
  - **Route**: `/export` page with a builder UI — checkboxes/dropdowns for filters, preview of selection count, download button
  - **Implementation**: API route (`/api/export`) that queries the source loaders with filters, serializes to chosen format. Client-side UI with controlled form state.
  - **Use cases**: LLM context loading, homebrew tools, VTT integration, offline reference
  - **CC-BY-4.0 note**: Export should include attribution in output metadata

### Schema Limitation: Multi-Size Creatures

The SRD has creatures marked "Medium or Small" (lycanthropes, Vampire, etc.) but our schema only supports a single size value. Current workaround: use "Medium" as the primary size. A proper fix would require schema changes to support `size: ["Medium", "Small"]` or a `sizeOptions` field.

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
