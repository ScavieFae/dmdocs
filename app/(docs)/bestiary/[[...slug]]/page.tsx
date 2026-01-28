import { bestiarySource } from "@/lib/source";
import {
  DocsPage,
  DocsBody,
  DocsDescription,
  DocsTitle,
} from "fumadocs-ui/page";
import { notFound } from "next/navigation";
import defaultMdxComponents from "fumadocs-ui/mdx";
import { MonsterStats } from "@/components/monster-stats";
import { SourceBadge } from "@/components/source-badge";

export default async function Page({
  params,
}: {
  params: { slug?: string[] };
}) {
  const page = bestiarySource.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const isMonster = page.data.creatureType !== undefined;

  return (
    <DocsPage toc={page.data.toc}>
      <DocsTitle>{page.data.title}</DocsTitle>
      <DocsDescription>
        {page.data.description && !isMonster && page.data.description}
        <SourceBadge source={page.data.source} />
      </DocsDescription>
      <MonsterStats data={page.data} />
      <DocsBody>
        <MDX components={{ ...defaultMdxComponents }} />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return bestiarySource.generateParams();
}

export function generateMetadata({ params }: { params: { slug?: string[] } }) {
  const page = bestiarySource.getPage(params.slug);
  if (!page) notFound();

  // For monsters, generate a richer description
  if (page.data.creatureType !== undefined) {
    return {
      title: page.data.title,
      description: `${page.data.size} ${page.data.creatureType}. CR ${page.data.cr}.`,
    };
  }

  return {
    title: page.data.title,
    description: page.data.description,
  };
}
