import { docs, meta, bestiaryDocs, bestiaryMeta, spells } from '@/.source';
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

// Spellbook source - uses collection (no meta file needed)
export const spellSource = loader({
  baseUrl: '/spellbook',
  source: createMDXSource(spells, []),
});

// Helper to get all spells with their typed data
export function getAllSpells() {
  return spellSource.getPages();
}

// Helper to filter spells by level
export function getSpellsByLevel(level: number) {
  return getAllSpells().filter(spell => spell.data.level === level);
}

// Helper to filter spells by school
export function getSpellsBySchool(school: string) {
  return getAllSpells().filter(spell => spell.data.school === school);
}

// Helper to filter spells by class
export function getSpellsByClass(className: string) {
  return getAllSpells().filter(spell =>
    spell.data.classes.includes(className)
  );
}
