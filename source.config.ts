import { defineDocs, defineConfig, frontmatterSchema } from 'fumadocs-mdx/config';
import { z } from 'zod';

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

// Bestiary (monster reference)
export const { docs: bestiaryDocs, meta: bestiaryMeta } = defineDocs({
  docs: {
    dir: 'bestiary',
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

export default defineConfig();
