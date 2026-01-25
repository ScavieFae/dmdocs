import { DocsLayout } from "fumadocs-ui/layout";
import type { ReactNode } from "react";
import { spellSource } from "@/lib/source";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-spellbook">
      <DocsLayout
        tree={spellSource.pageTree}
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
