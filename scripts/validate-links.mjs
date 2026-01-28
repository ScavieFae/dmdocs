#!/usr/bin/env node

/**
 * Internal link validator for DMDocs.
 *
 * Scans all MDX files for internal links (markdown + JSX href) and checks
 * that each one resolves to an actual content page.
 *
 * Usage: node scripts/validate-links.mjs
 */

import { readdir, readFile } from "node:fs/promises";
import { join, dirname, posix } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");

// Content directories and their URL prefixes
const SOURCES = [
  { dir: "content", prefix: "/docs" },
  { dir: "spellbook", prefix: "/spellbook" },
  { dir: "bestiary", prefix: "/bestiary" },
  { dir: "magicitems", prefix: "/magicitems" },
];

// ---------------------------------------------------------------------------
// Step 1 — Build the set of valid routes
// ---------------------------------------------------------------------------

async function collectMdxFiles(dir) {
  const files = [];
  const entries = await readdir(dir, { withFileTypes: true, recursive: true });
  for (const entry of entries) {
    if (entry.isFile() && entry.name.endsWith(".mdx")) {
      // Node 18 recursive readdir gives parentPath (or path in older builds)
      const parent = entry.parentPath ?? entry.path;
      files.push(join(parent, entry.name));
    }
  }
  return files;
}

function fileToRoute(filePath, sourceDir, prefix) {
  let rel = filePath.slice(sourceDir.length); // e.g. /combat/attacks.mdx
  rel = rel.replace(/\.mdx$/, "");
  rel = rel.replace(/\/index$/, "");
  if (rel === "") return prefix || "/";
  return prefix + rel;
}

async function buildValidRoutes() {
  const routes = new Set();

  for (const { dir, prefix } of SOURCES) {
    const absDir = join(ROOT, dir);
    let files;
    try {
      files = await collectMdxFiles(absDir);
    } catch {
      // Directory may not exist yet
      continue;
    }
    for (const f of files) {
      routes.add(fileToRoute(f, absDir, prefix));
    }
  }

  return routes;
}

// ---------------------------------------------------------------------------
// Step 2 — Extract internal links from MDX content
// ---------------------------------------------------------------------------

// Matches markdown links: [text](/path) — captures the path
const MD_LINK_RE = /\]\(([^)#"?\s]+)\)/g;
// Matches JSX href props: href="/path" — captures the path
const JSX_HREF_RE = /href="([^"#?]+)"/g;

function extractLinks(content) {
  const links = [];

  for (const m of content.matchAll(MD_LINK_RE)) {
    const href = m[1];
    if (isInternal(href)) links.push(href);
  }
  for (const m of content.matchAll(JSX_HREF_RE)) {
    const href = m[1];
    if (isInternal(href)) links.push(href);
  }

  return [...new Set(links)]; // dedupe per file
}

function isInternal(href) {
  if (href.startsWith("http://") || href.startsWith("https://")) return false;
  if (href.startsWith("mailto:")) return false;
  if (href.startsWith("#")) return false;
  // Skip image/asset references
  if (/\.(png|jpg|jpeg|gif|svg|webp|ico|pdf|css|js)$/i.test(href)) return false;
  return true;
}

// ---------------------------------------------------------------------------
// Step 3 — Resolve relative links
// ---------------------------------------------------------------------------

function resolveLink(href, filePath) {
  if (href.startsWith("/")) {
    // Already absolute — strip trailing slash for consistency
    return href.replace(/\/$/, "") || "/";
  }

  // Relative link — resolve against the file's directory route
  const source = SOURCES.find((s) => filePath.startsWith(join(ROOT, s.dir)));
  if (!source) return null; // shouldn't happen

  const absDir = join(ROOT, source.dir);
  const fileDir = dirname(filePath);
  const relDir = fileDir.slice(absDir.length); // e.g. /fey/hobgoblins

  // If the file is an index, the "directory" is its own route folder
  const isIndex = filePath.endsWith("/index.mdx");
  const routeDir = isIndex
    ? source.prefix + relDir
    : source.prefix + relDir; // same either way — link resolves from directory

  // posix.resolve handles ./ and ../ correctly
  const resolved = posix.resolve(routeDir, href);
  return resolved;
}

// ---------------------------------------------------------------------------
// Step 4 — Run validation and report
// ---------------------------------------------------------------------------

async function main() {
  const routes = await buildValidRoutes();
  const broken = []; // { file, href, resolved }

  for (const { dir } of SOURCES) {
    const absDir = join(ROOT, dir);
    let files;
    try {
      files = await collectMdxFiles(absDir);
    } catch {
      continue;
    }

    for (const filePath of files) {
      const content = await readFile(filePath, "utf-8");
      const links = extractLinks(content);

      for (const href of links) {
        const resolved = resolveLink(href, filePath);
        if (resolved === null) continue;

        if (!routes.has(resolved)) {
          const relFile = filePath.slice(ROOT.length + 1);
          broken.push({ file: relFile, href, resolved });
        }
      }
    }
  }

  if (broken.length === 0) {
    console.log(`\u2713 All internal links valid (${routes.size} routes checked)`);
    process.exit(0);
  }

  // Group by file
  const grouped = new Map();
  for (const { file, href, resolved } of broken) {
    if (!grouped.has(file)) grouped.set(file, []);
    grouped.get(file).push({ href, resolved });
  }

  for (const [file, links] of grouped) {
    console.log(`\n${file}:`);
    for (const { href, resolved } of links) {
      const extra = href !== resolved ? ` (resolved: ${resolved})` : "";
      console.log(`  ${href} \u2192 NOT FOUND${extra}`);
    }
  }

  console.log(`\n\u2717 ${broken.length} broken link${broken.length === 1 ? "" : "s"} found`);
  process.exit(1);
}

main();
