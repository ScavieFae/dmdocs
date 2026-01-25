import { DocsLayout } from "fumadocs-ui/layout";
import type { ReactNode } from "react";
import { magicItemsSource } from "@/lib/source";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="theme-magicitems">
      <DocsLayout
        tree={magicItemsSource.pageTree}
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
