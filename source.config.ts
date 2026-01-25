import { defineDocs, defineConfig, frontmatterSchema } from 'fumadocs-mdx/config';
import { z } from 'zod';

// Monster schema - extends base frontmatter with monster-specific fields
const monsterSchema = frontmatterSchema.extend({
  size: z.enum(['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']).optional(),
  creatureType: z.string().optional(), // "Aberration", "Dragon (Chromatic)", "Beast", etc.
  alignment: z.string().optional(),
  ac: z.number().optional(),
  hp: z.object({
    average: z.number(),
    formula: z.string(),
  }).optional(),
  speed: z.object({
    walk: z.number().optional(),
    fly: z.number().optional(),
    swim: z.number().optional(),
    burrow: z.number().optional(),
    climb: z.number().optional(),
  }).optional(),
  abilities: z.object({
    str: z.number(),
    dex: z.number(),
    con: z.number(),
    int: z.number(),
    wis: z.number(),
    cha: z.number(),
  }).optional(),
  saves: z.object({
    str: z.number().optional(),
    dex: z.number().optional(),
    con: z.number().optional(),
    int: z.number().optional(),
    wis: z.number().optional(),
    cha: z.number().optional(),
  }).optional(),
  skills: z.array(z.string()).optional(), // ["Perception +10", "Stealth +7"]
  immunities: z.array(z.string()).optional(),
  resistances: z.array(z.string()).optional(),
  vulnerabilities: z.array(z.string()).optional(),
  conditionImmunities: z.array(z.string()).optional(),
  senses: z.array(z.string()).optional(), // ["darkvision 120 ft.", "Passive Perception 20"]
  languages: z.array(z.string()).optional(),
  cr: z.string().optional(), // "10", "1/4", "0"
  xp: z.number().optional(),
});

// Magic item schema - extends base frontmatter with item-specific fields
const magicItemSchema = frontmatterSchema.extend({
  category: z.enum(['Armor', 'Potion', 'Ring', 'Rod', 'Scroll', 'Staff', 'Wand', 'Weapon', 'Wondrous Item']).optional(),
  rarity: z.enum(['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Artifact']).optional(),
  itemType: z.string().optional(), // Subtype like "Shield", "Any Ammunition", etc.
  attunement: z.union([z.boolean(), z.string()]).optional(), // true, false, or "by a spellcaster"
  charges: z.object({
    max: z.number(),
    recharge: z.string().optional(), // "dawn", "1d6+1 at dawn", etc.
  }).optional(),
  armorType: z.string().optional(), // For armor items
  weaponType: z.string().optional(), // For weapon items
});

// Spell schema - extends base frontmatter with spell-specific fields
const spellSchema = frontmatterSchema.extend({
  level: z.number().min(0).max(9).optional(), // 0 = cantrip
  school: z.enum([
    'Abjuration',
    'Conjuration',
    'Divination',
    'Enchantment',
    'Evocation',
    'Illusion',
    'Necromancy',
    'Transmutation',
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

// Main documentation (rules, classes, origins, etc.)
export const { docs, meta } = defineDocs({
  docs: {
    dir: 'content',
  },
  meta: {
    dir: 'content',
  },
});

// Bestiary (monster reference with typed frontmatter)
export const { docs: bestiaryDocs, meta: bestiaryMeta } = defineDocs({
  docs: {
    dir: 'bestiary',
    schema: monsterSchema,
  },
  meta: {
    dir: 'bestiary',
  },
});

// Spellbook (spell reference with typed frontmatter)
export const { docs: spellDocs, meta: spellMeta } = defineDocs({
  docs: {
    dir: 'spellbook',
    schema: spellSchema,
  },
  meta: {
    dir: 'spellbook',
  },
});

// Magic Items (item reference with typed frontmatter)
export const { docs: magicItemDocs, meta: magicItemMeta } = defineDocs({
  docs: {
    dir: 'magicitems',
    schema: magicItemSchema,
  },
  meta: {
    dir: 'magicitems',
  },
});

export default defineConfig();
