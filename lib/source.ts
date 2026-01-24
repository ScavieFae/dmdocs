import { docs, meta, bestiaryDocs, bestiaryMeta } from '@/.source';
import { createMDXSource } from 'fumadocs-mdx';
import { loader } from 'fumadocs-core/source';

// Main documentation source
export const source = loader({
  baseUrl: '/docs',
  source: createMDXSource(docs, meta),
});

// Bestiary source
export const bestiarySource = loader({
  baseUrl: '/bestiary',
  source: createMDXSource(bestiaryDocs, bestiaryMeta),
});
