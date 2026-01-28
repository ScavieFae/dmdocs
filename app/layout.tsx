import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { RootProvider } from "fumadocs-ui/provider";

const inter = Inter({ subsets: ["latin"] });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "DMDocs - D&D 5e SRD Reference",
  description: "LLM-optimized D&D 5th Edition System Reference Document",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} ${jetbrainsMono.variable}`}>
        <RootProvider
          search={{
            options: {
              api: "/api/search",
              tags: [
                { name: "Rules", value: "Rules" },
                { name: "Spells", value: "Spells" },
                { name: "Monsters", value: "Monsters" },
                { name: "Magic Items", value: "Magic Items" },
              ],
            },
          }}
        >
          {children}
        </RootProvider>
      </body>
    </html>
  );
}
