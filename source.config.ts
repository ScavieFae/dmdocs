import { defineDocs, defineConfig } from 'fumadocs-mdx/config';

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

export default defineConfig();
