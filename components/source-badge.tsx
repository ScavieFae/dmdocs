const labels: Record<string, { text: string; title: string }> = {
  srd: {
    text: "SRD Content",
    title: "This page contains content from the D&D 5.2.1 System Reference Document",
  },
  synthesized: {
    text: "Synthesized from SRD",
    title: "This page was derived from SRD content for quick reference",
  },
  created: {
    text: "Created Content",
    title: "This page was created for DMDocs by humans, bots, or agents",
  },
};

export function SourceBadge({ source }: { source: string }) {
  const label = labels[source];
  if (!label) return null;

  return (
    <span className="block mt-2">
      <span
        className="inline-block text-xs px-2 py-0.5 rounded border border-fd-border text-fd-muted-foreground"
        title={label.title}
      >
        {label.text}
      </span>
    </span>
  );
}
