import { magicItemsSource } from "@/lib/source";
import {
  DocsPage,
  DocsBody,
  DocsDescription,
  DocsTitle,
} from "fumadocs-ui/page";
import { notFound } from "next/navigation";
import defaultMdxComponents from "fumadocs-ui/mdx";
import { MagicItemCard } from "@/components/magic-item-card";
import { SourceBadge } from "@/components/source-badge";

export default async function Page({
  params,
}: {
  params: { slug?: string[] };
}) {
  const page = magicItemsSource.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const isItem = page.data.rarity !== undefined;

  return (
    <DocsPage toc={page.data.toc}>
      <DocsTitle>{page.data.title}</DocsTitle>
      <DocsDescription>
        {page.data.description && !isItem && page.data.description}
        <SourceBadge source={page.data.source} />
      </DocsDescription>
      <MagicItemCard data={page.data} />
      <DocsBody>
        <MDX components={{ ...defaultMdxComponents }} />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return magicItemsSource.generateParams();
}

export function generateMetadata({ params }: { params: { slug?: string[] } }) {
  const page = magicItemsSource.getPage(params.slug);
  if (!page) notFound();

  return {
    title: page.data.title,
    description: page.data.description,
  };
}
