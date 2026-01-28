import { createSearchAPI } from "fumadocs-core/search/server";
import { source, bestiarySource, spellSource, magicItemsSource } from "@/lib/source";

export const { GET } = createSearchAPI("advanced", {
  tag: true,
  indexes: [
    ...source.getPages().map((page) => ({
      id: page.url,
      title: page.data.title,
      description: page.data.description,
      structuredData: page.data.structuredData,
      url: page.url,
      tag: "Rules",
    })),
    ...spellSource.getPages().map((page) => ({
      id: page.url,
      title: page.data.title,
      description: page.data.description,
      structuredData: page.data.structuredData,
      url: page.url,
      tag: "Spells",
    })),
    ...bestiarySource.getPages().map((page) => ({
      id: page.url,
      title: page.data.title,
      description: page.data.description,
      structuredData: page.data.structuredData,
      url: page.url,
      tag: "Monsters",
    })),
    ...magicItemsSource.getPages().map((page) => ({
      id: page.url,
      title: page.data.title,
      description: page.data.description,
      structuredData: page.data.structuredData,
      url: page.url,
      tag: "Magic Items",
    })),
  ],
});
