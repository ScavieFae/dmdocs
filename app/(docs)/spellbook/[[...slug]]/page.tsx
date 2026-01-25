import { spellSource } from "@/lib/source";
import {
  DocsPage,
  DocsBody,
  DocsDescription,
  DocsTitle,
} from "fumadocs-ui/page";
import { notFound } from "next/navigation";
import defaultMdxComponents from "fumadocs-ui/mdx";

// Component to display spell stats in a consistent format
function SpellStats({ data }: { data: any }) {
  const levelText = data.level === 0 ? 'Cantrip' : `Level ${data.level}`;
  const components = [
    data.components.verbal && 'V',
    data.components.somatic && 'S',
    data.components.material && `M (${data.components.material})`,
  ].filter(Boolean).join(', ');

  return (
    <div className="spell-stats mb-6 p-4 rounded-lg bg-fd-muted/50 text-sm">
      <div className="font-medium text-fd-muted-foreground mb-2">
        {levelText} {data.school}
        {data.ritual && ' (Ritual)'}
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div><strong>Casting Time:</strong> {data.castingTime}</div>
        <div><strong>Range:</strong> {data.range}</div>
        <div><strong>Components:</strong> {components}</div>
        <div><strong>Duration:</strong> {data.duration}</div>
      </div>
      <div className="mt-2 text-fd-muted-foreground">
        <strong>Classes:</strong> {data.classes.join(', ')}
      </div>
    </div>
  );
}

export default async function Page({
  params,
}: {
  params: { slug?: string[] };
}) {
  const page = spellSource.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;

  return (
    <DocsPage toc={page.data.toc}>
      <DocsTitle>{page.data.title}</DocsTitle>
      <SpellStats data={page.data} />
      <DocsBody>
        <MDX components={{ ...defaultMdxComponents }} />
        {page.data.higherLevel && (
          <p className="mt-4 text-fd-muted-foreground">
            <strong>Using a Higher-Level Spell Slot.</strong> {page.data.higherLevel}
          </p>
        )}
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return spellSource.generateParams();
}

export function generateMetadata({ params }: { params: { slug?: string[] } }) {
  const page = spellSource.getPage(params.slug);
  if (!page) notFound();

  const levelText = page.data.level === 0 ? 'Cantrip' : `Level ${page.data.level}`;

  return {
    title: page.data.title,
    description: `${levelText} ${page.data.school} spell. ${page.data.classes.join(', ')}.`,
  };
}
