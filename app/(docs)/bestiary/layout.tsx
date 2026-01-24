import { DocsLayout } from "fumadocs-ui/layout";
import type { ReactNode } from "react";
import { bestiarySource } from "@/lib/source";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-bestiary">
      <DocsLayout
        tree={bestiarySource.pageTree}
        nav={{ enabled: false }}
        sidebar={{
          defaultOpenLevel: 1,
          hideSearch: true,
        }}
      >
        {children}
      </DocsLayout>
    </div>
  );
}
