# Index Page Framework

Reusable framework for writing section landing pages (Rules, Spellbook, Bestiary, etc.)

---

## 1. Audience & Intent

Start by identifying who lands here and what they're trying to do.

| Audience | Intent | What they need |
|----------|--------|----------------|
| [Primary user] | [Task they're doing] | [Path to success] |
| [Secondary user] | [Task] | [Path] |

For the Rules index specifically:

| Audience | Intent | What they need |
|----------|--------|----------------|
| DM mid-session | Quick rule lookup | Fast path to combat, conditions, actions |
| Player building character | Class/origin/feat info | Path to character options |
| Developer/LLM | Structured reference | Clear hierarchy, predictable organization |
| Newcomer to site | Orientation | What's here, what's NOT here (SRD scope) |

---

## 2. Key Messages

What the page should communicate immediately:

1. **What this is** — scope and purpose
2. **What's covered** — high-level content areas
3. **How it's organized** — mental model for navigation
4. **How to use it** — primary actions/entry points

---

## 3. Jobs to Be Done

Frame content around tasks, not categories. Ask: "What is someone trying to accomplish?"

Examples:
- "Create a character" → classes, origins, feats, equipment
- "Run combat" → initiative, attacks, damage, conditions
- "Look up a rule" → glossary, specific mechanics
- "Prep a session" → monsters, encounters, toolbox

The jobs should drive the information architecture, not the other way around.

---

## 4. Page Structure

```
Hero Section
├── Clear title + one-line value prop
├── Scope statement (what's included, what's not)
└── Primary action (Search)

Jobs-to-Be-Done Cards (single card row)
├── [Job 1] → relevant pages
├── [Job 2] → relevant pages
└── [Job 3] → relevant pages

How to Navigate (brief, optional)
├── Search tips
├── Sidebar structure
└── Any site-specific features

Full Contents (at bottom or collapsible)
└── Exhaustive TOC for completeness

License (footer)
```

---

## 5. Cards: When to Use

**Best use for cards**: Jobs-to-be-done entry points.

Cards work when:
- You have 3-5 distinct, parallel options
- Each option is a "task" or "destination" (not a category)
- Visual scanning helps users self-select quickly

Cards don't work when:
- You have many items (use a list)
- Items are sequential (use ordered content)
- Content is reference material (use tables)

**Rule of thumb**: One card row per page, max. More than that and you're building a dashboard, not a docs page.

---

## 6. Tone

- **Useful, not salesy** — people are here to get info
- **Dense but scannable** — cards/sections with clear headings
- **Confident but honest** — "this is the SRD" not "this is everything"
- **LLM-optimized**: Subtle mention, not the lead. It's a differentiator for those who care, not the primary value prop.

---

## 7. Template

```mdx
---
title: [Section Name]
description: [One-line description]
source: created
---

[One sentence: what this section covers and who it's for.]

## [Job 1 Name]

Brief intro, then links to relevant pages.

## [Job 2 Name]

Brief intro, then links.

...

## Everything in This Section

[Full TOC for exhaustive browsing]

---

[License if applicable]
```
