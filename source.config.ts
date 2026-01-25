import { defineDocs, defineCollections, defineConfig } from 'fumadocs-mdx/config';
import { z } from 'zod';

// Spell schema - structured data for the spellbook
const spellSchema = z.object({
  title: z.string(),
  level: z.number().min(0).max(9), // 0 = cantrip
  school: z.enum([
    'Abjuration',
    'Conjuration',
    'Divination',
    'Enchantment',
    'Evocation',
    'Illusion',
    'Necromancy',
    'Transmutation',
  ]),
  castingTime: z.string(),
  range: z.string(),
  components: z.object({
    verbal: z.boolean(),
    somatic: z.boolean(),
    material: z.string().optional(),
  }),
  duration: z.string(),
  concentration: z.boolean().default(false),
  ritual: z.boolean().default(false),
  classes: z.array(z.string()),
  // Optional: description of higher-level casting
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
export const spells = defineCollections({
  type: 'doc',
  dir: 'spellbook',
  schema: spellSchema,
});

export default defineConfig();
