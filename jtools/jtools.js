#!/usr/bin/env node

import fs from "fs";
import path from "path";

const subcommand = process.argv[2];

if (!subcommand) {
  console.log("Usage: jtools <command>");
  console.log("");
  console.log("Commands:");
  console.log("  format-pug  Format pug in ./index.html (current working dir)");
  console.log("  copy-agent  Copy ~/.claude/CLAUDE.md to ./AGENT.md");
  process.exit(0);
}

if (subcommand === "copy-agent") {
  const src = path.resolve(process.env.HOME, ".claude/CLAUDE.md");
  const dest = path.resolve(process.cwd(), "AGENT.md");
  fs.copyFileSync(src, dest);
  console.log("copied CLAUDE.md to AGENT.md");
  process.exit(0);
}

if (subcommand === "format-pug") {
  const HTML_FILE = path.resolve(process.cwd(), "index.html");
  if (!fs.existsSync(HTML_FILE)) {
    console.error("index.html not found in current directory");
    process.exit(1);
  }
  const OPEN_MARKER = "/* pug */`";

  const content = fs.readFileSync(HTML_FILE, "utf8");

  const openIdx = content.indexOf(OPEN_MARKER);
  if (openIdx === -1) throw new Error(`marker '${OPEN_MARKER}' not found`);

  const contentStart = openIdx + OPEN_MARKER.length;

  let closeIdx = contentStart;
  while (closeIdx < content.length) {
    if (content[closeIdx] === "\\") { closeIdx += 2; continue; }
    if (content[closeIdx] === "`") break;
    closeIdx++;
  }

  const rawPug = content.slice(contentStart, closeIdx);

  const trailMatch = rawPug.match(/\n(\s*)$/);
  const trailingWs = trailMatch ? "\n" + trailMatch[1] : "\n";

  const lines = rawPug.split("\n");
  const nonEmpty = lines.filter((l) => l.trim());
  if (!nonEmpty.length) process.exit(0);

  const baseIndent = Math.min(...nonEmpty.map((l) => l.match(/^(\s*)/)[1].length));
  const indent = " ".repeat(baseIndent);

  const stripped = lines
    .map((l) => l.slice(baseIndent))
    .join("\n")
    .trim();

  const { default: prettier } = await import("prettier");
  const { plugin: pugPlugin } = await import("@prettier/plugin-pug");

  const formatted = await prettier.format(stripped, {
    parser: "pug",
    plugins: [pugPlugin],
  });

  const reindented =
    "\n" +
    formatted
      .trimEnd()
      .split("\n")
      .map((l) => (l ? indent + l : ""))
      .join("\n") +
    trailingWs;

  fs.writeFileSync(
    HTML_FILE,
    content.slice(0, contentStart) + reindented + content.slice(closeIdx),
  );

  console.log("formatted pug in", path.basename(HTML_FILE));
  process.exit(0);
}

console.error(`Unknown subcommand: ${subcommand}`);
console.error("Run 'jtools' for usage.");
process.exit(1);
