# Debugging & Codebase Notes

A structured guide for future Claudes, contributors, and anyone working on DMDocs. This covers the non-obvious stuff — the things that cost us hours and shouldn't cost you the same.

---

## Tailwind + Fumadocs Responsive Classes

**The biggest gotcha in this codebase.**

Fumadocs uses a Tailwind preset (`fumadocs-ui/tailwind-plugin`) that conflicts with standard responsive class patterns. Specifically:

- `hidden md:flex` — **does not work**. The `md:flex` never overrides `hidden`.
- `sm:grid-cols-3` — **does not work**. Fumadocs' `sm:grid-cols-2` on the Cards component wins.

**What works instead:**

| Broken | Fix |
|--------|-----|
| `hidden md:flex` | `max-md:hidden flex` |
| `md:hidden` | Works fine (hiding at breakpoint is OK) |
| `sm:grid-cols-3` on Cards | `grid-cols-3` (no breakpoint) + `!important` CSS override |

The pattern: **invert the logic**. Instead of "hidden by default, shown at md", use "shown by default, hidden below md" (`max-md:hidden`).

For the Cards grid specifically, we added a CSS override in `globals.css`:
```css
.grid.grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}
```

This is needed because Fumadocs' Card component uses `twMerge` internally, and the baked-in `sm:grid-cols-2` class takes priority over a passed `grid-cols-3`.

---

## Cache Corruption

When things look wrong after restructuring files, moving folders, or changing navigation:

```bash
rm -rf .next .source && npm run dev
```

`.source` is Fumadocs' MDX processing cache. `.next` is Next.js build cache. Both can get stale.

**Symptoms:** Navigation shows old structure, pages 404 that shouldn't, MDX changes not reflecting.

---

## Fumadocs Component Reference

Components we use from `fumadocs-ui`:

| Component | Import | Notes |
|-----------|--------|-------|
| `Card`, `Cards` | `fumadocs-ui/components/card` | Cards takes `className`, Card takes `icon`, `title`, `description`, `href` |
| `Callout` | `fumadocs-ui/components/callout` | Types: `info`, `warn`, `error` |
| `Tab`, `Tabs` | `fumadocs-ui/components/tabs` | Used in class pages for tier grouping |
| `DocsLayout` | `fumadocs-ui/layout` | Section layouts; set `nav={{ enabled: false }}` since we have custom navbar |
| `DocsPage`, `DocsBody`, `DocsTitle`, `DocsDescription` | `fumadocs-ui/page` | Page rendering; badge/metadata goes inside `DocsDescription` to sit near the title |

### DocsPage Layout Slots

Content inside `DocsPage` renders in distinct sections with their own spacing. If you need something visually close to the title/description, put it *inside* `DocsDescription`, not as a sibling after it. Siblings get the body content gap.

---

## Custom Navbar

The navbar is fully custom (`components/navbar.tsx`), not Fumadocs' built-in nav.

**Structure:**
- Top row: hamburger (mobile only) + logo + search + AI search + theme toggle
- Bottom row: pill tab navigation (desktop only, hidden on mobile via `max-md:hidden`)

**Mobile:** Hamburger opens a dropdown with all section links. Closes on route change, outside click, or toggle.

**Alignment:** Both rows use `paddingLeft: var(--fd-layout-offset)` to align with the Fumadocs sidebar. The pill row has additional `px-4`. The offset is defined in `globals.css` and scales with viewport width:
- Default: 0px
- 1280px+: 3rem
- 1536px+: 6rem
- 1800px+: 10rem

---

## Multi-Docs Architecture

Four separate content sources, each with its own schema:

| Source | Dir | Schema | Base URL |
|--------|-----|--------|----------|
| docs | `content/` | `baseSchema` | `/docs` |
| bestiary | `bestiary/` | `monsterSchema` | `/bestiary` |
| spellbook | `spellbook/` | `spellSchema` | `/spellbook` |
| magicitems | `magicitems/` | `magicItemSchema` | `/magicitems` |

All schemas extend `baseSchema` which extends Fumadocs' `frontmatterSchema` with a `source` field (`srd` | `synthesized` | `created`, defaults to `srd`).

**Adding a field to all content types:** Add it to `baseSchema` in `source.config.ts`.

**Adding a field to one content type:** Add it to that type's schema (e.g., `monsterSchema`).

---

## Content Source Tags

Every page has a `source` frontmatter field:

| Value | Meaning | Example |
|-------|---------|---------|
| `srd` (default) | Direct SRD content | Class pages, spell descriptions |
| `synthesized` | Derived from SRD data | Conditions quick ref |
| `created` | Original DMDocs content | Index pages, style guide, contribute |

You don't need to add `source: srd` — it's the default. Only add it when the value is `synthesized` or `created`.

---

## Zod Schema Constraints

- **Zod version must be 3.23.8** (pinned in package.json)
- Challenge ratings must be strings in YAML: `cr: "17"` not `cr: 17`
- Use `.optional()` for fields not all entries have
- `source` field has `.default('srd')` so it never needs explicit setting for SRD content

---

## SRD Content Verification

**The initial content was created from the 2024 PHB, not the SRD.** Treat unverified sections with suspicion.

Authoritative source: `pdfs/DND-SRD-5.2.1-CC - updated.docx.txt`

Key differences from PHB:
- Only 17 feats (not 74)
- Only one subclass per class
- Wizard name prefixes removed from spells (Melf's Acid Arrow → Acid Arrow)
- No Gem dragons for Dragonborn
- Limited species, backgrounds, equipment

See `VERIFICATION-STATUS.md` for what's been audited.

---

## Build & Deploy

**Dev:**
```bash
npm run dev          # localhost:3000, turbopack
```

**Production build:**
```bash
npm run build        # TypeScript strict — catches things dev mode doesn't
```

**Deploy to Vercel:**
```bash
vercel --prod
```

**Common build failures:**
- Unused variables (ESLint strict mode) — `@typescript-eslint/no-unused-vars`
- Missing type annotations that turbopack ignores
- `output: 'export'` was removed from `next.config.mjs` for dev compatibility; don't re-add unless doing static builds

---

## Port Conflicts

`npm run dev` defaults to port 3000. If it's in use, Next.js auto-picks 3001+. After `pkill -f "next"`, the next restart will go back to 3000.

---

## File Naming

- Folders: kebab-case (`playing-the-game/`)
- MDX files: kebab-case (`rhythm-of-play.mdx`)
- Navigation: defined in `meta.json` per folder
- Section headers in root meta.json: `"---Section Name---"`
