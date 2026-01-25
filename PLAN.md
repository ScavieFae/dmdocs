# DMDocs: LLM-Optimized D&D 5e SRD Documentation

## Project Goal

Transform the D&D 5.2.1 SRD (CC-BY-4.0) into a cleanly navigable documentation site optimized for both human readers and LLM consumption.

## Source Material

- **SRD 5.2.1** (May 2025) - Official Wizards of the Coast release under CC-BY-4.0
- PDF: `pdfs/SRD_5.2.1.pdf`
- Extracted text: `pdfs/SRD_5.2.1.txt` (24,074 lines)

## Tech Stack

- **Framework**: Next.js 14 + Fumadocs
- **Content**: MDX files with structured frontmatter
- **Styling**: Tailwind CSS + Fumadocs UI
- **Deployment**: Static export to Vercel

## Content Structure

```
content/
├── index.mdx                    # Landing page
├── rules/                       # Core mechanics
├── classes/                     # 12 character classes
├── spells/                      # ~300 spells (individual files)
├── monsters/                    # ~200 creatures (individual files)
├── equipment/                   # Weapons, armor, gear
└── magic-items/                 # Magical treasures
```

## LLM Optimization

Based on docs-ai-era learnings:

1. **Consistent Frontmatter** - Every page has structured metadata
2. **llms.txt** - Machine-readable navigation at root
3. **Cross-References** - Explicit links between related content
4. **Structured Data** - JSON-LD for stat blocks

## Processing Pipeline

### Phase 1: Framework Setup ✅
- [x] Initialize Next.js + Fumadocs
- [x] Configure MDX processing
- [x] Create basic navigation structure
- [x] Test build

### Phase 2: Content Extraction (Current)
Order by structure cleanliness:

1. **Spells** - Most consistent format
   - Script: `scripts/extract-spells.py`
   - Pattern: Name, Level+School, Casting Time, Range, Components, Duration, Description

2. **Monsters** - Structured stat blocks
   - Script: `scripts/extract-monsters.py`
   - Pattern: Name, Type/Size/Alignment, Stats, Traits, Actions

3. **Magic Items** - Variable format
   - Script: `scripts/extract-magic-items.py`

4. **Classes** - Complex, needs manual cleanup
5. **Rules** - Prose-heavy, manual extraction

### Phase 3: Enhancement
- Add cross-references
- Build index pages with filters
- Generate llms.txt

### Phase 4: Polish
- Stat block styling
- Mobile responsiveness
- Deploy

## Extraction Patterns from PDF

### Spell Format (lines 8171-8195):
```
Fireball
Level 3 Evocation (Sorcerer, Wizard)
Casting Time: Action
Range: 150 feet
Components: V, S, M (a ball of bat guano and sulfur)
Duration: Instantaneous

[Description paragraphs]

Using a Higher-Level Spell Slot. [Upcasting text]
```

### Monster Format (lines 16732-16784):
```
Aboleth
Large Aberration, Lawful Evil
AC 17                    Initiative +7 (17)
HP 150 (20d10 + 40)
Speed 10 ft., Swim 40 ft.
[Ability scores table]
Skills History +12, Perception +10
Senses Darkvision 120 ft.; Passive Perception 20
Languages Deep Speech; telepathy 120 ft.
CR 10 (XP 5,900, or 7,200 in lair; PB +4)

Traits
[Trait descriptions]

Actions
[Action descriptions]
```

## Attribution (Required)

> This work includes material from the System Reference Document 5.2.1 by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. Licensed under CC-BY-4.0.

---

# Origins Section Plan

## Overview

**Content to create:**
- 4 Backgrounds: Acolyte, Criminal, Sage, Soldier
- 9 Species: Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling

**Structure already exists:** meta.json files and index.mdx with links are in place.

---

## Background Page Template

Each background is compact in 5.2.1. Consistent structure:

```mdx
---
title: [Background Name]
description: [One-line flavor]
---

# [Background Name]

[1-2 sentence flavor text]

| Trait | Value |
|-------|-------|
| Ability Scores | [Options] |
| Skill Proficiencies | [Skills] |
| Tool Proficiency | [Tool] |
| Equipment | [Gear] |
| Origin Feat | [Feat Name] |

## [Origin Feat Name]

[Feat description - full text so readers don't have to navigate away]
```

**Rationale:** Backgrounds are simple enough that a single table + feat description covers everything. No need for tabs or accordions—clean and scannable.

---

## Species Page Template

Species have more variety. Two patterns:

### Pattern A: Simple Species (Human, Halfling, Orc, Gnome, Goliath)

```mdx
---
title: [Species]
description: [Flavor + key trait hint]
---

# [Species]

[2-3 sentence flavor]

## [Species] Traits

| Trait | Value |
|-------|-------|
| Creature Type | Humanoid |
| Size | [Size] |
| Speed | [Speed] |
| Life Span | [Years] |

## Special Traits

### [Trait Name]
[Description]
```

### Pattern B: Species with Lineages/Ancestries (Dragonborn, Dwarf, Elf, Tiefling)

Use **Tabs** for the variant options:

```mdx
import { Tab, Tabs } from 'fumadocs-ui/components/tabs';

# Dragonborn

[Flavor]

## Dragonborn Traits
[Core traits table]

## Draconic Ancestry

<Tabs items={['Chromatic', 'Gem', 'Metallic']}>
<Tab value="Chromatic">
[Chromatic options table + breath weapon details]
</Tab>
...
</Tabs>
```

**Where tabs make sense:**
- **Dragonborn** — 3 ancestry categories (Chromatic, Gem, Metallic) with different damage types
- **Elf** — 3 lineages (Drow, High Elf, Wood Elf)
- **Tiefling** — 3 fiendish legacies (Abyssal, Chthonic, Infernal)

**Where tables shine:**
- Dragonborn breath weapon damage by level
- Goliath's Large Form details

---

## Fumadocs Components

| Component | Use Case |
|-----------|----------|
| `Tabs` | Species with lineage/ancestry choices |
| Markdown tables | Trait summaries, damage progression |
| Standard headings | Feature descriptions |

**Not using:** Callouts, Accordions, Steps, Cards — content isn't procedural or long enough to warrant them.

---

## Execution Order

1. **Backgrounds** (4 files) — simpler, establishes rhythm
2. **Simple species** (5 files) — Human, Halfling, Orc, Gnome, Goliath
3. **Complex species** (4 files) — Dragonborn, Dwarf, Elf, Tiefling (with tabs)

Total: 13 files
