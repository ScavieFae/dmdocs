import { DocsLayout } from "fumadocs-ui/layout";
import type { ReactNode } from "react";
import { source } from "@/lib/source";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-rules">
      <DocsLayout
        tree={source.pageTree}
        nav={{ enabled: false }}
        sidebar={{
          defaultOpenLevel: 0,
          hideSearch: true,
        }}
      >
        {children}
      </DocsLayout>
    </div>
  );
}
