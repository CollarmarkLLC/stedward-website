import assert from "node:assert/strict";
import { readdir, readFile, stat } from "node:fs/promises";
import { dirname, extname, join, relative, resolve, sep } from "node:path";
import test from "node:test";

const projectRoot = resolve(import.meta.dirname, "..");
const outputRoot = join(projectRoot, "_site");

async function filesBelow(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesBelow(path) : [path];
  }));
  return nested.flat();
}

function localReferences(html) {
  const references = [];
  for (const match of html.matchAll(/\b(?:href|src)=["']([^"']+)["']/gi)) {
    references.push(match[1]);
  }
  for (const match of html.matchAll(/\bsrcset=["']([^"']+)["']/gi)) {
    references.push(...match[1].split(",").map((candidate) => candidate.trim().split(/\s+/)[0]));
  }
  return references.filter((value) => value && !/^(?:[a-z]+:|\/\/|#)/i.test(value));
}

async function resolveReference(htmlPath, reference) {
  const pathname = decodeURIComponent(reference.split(/[?#]/, 1)[0]);
  if (!pathname) return null;
  let target = pathname.startsWith("/")
    ? join(outputRoot, pathname.slice(1))
    : resolve(dirname(htmlPath), pathname);
  assert.ok(target === outputRoot || target.startsWith(`${outputRoot}${sep}`), `reference escapes output: ${reference}`);
  if (pathname.endsWith("/")) target = join(target, "index.html");
  if (!extname(target)) {
    try {
      if ((await stat(target)).isDirectory()) target = join(target, "index.html");
    } catch {
      target = join(target, "index.html");
    }
  }
  return target;
}

test("generated pages have essential document metadata", async () => {
  const htmlFiles = (await filesBelow(outputRoot)).filter((path) => path.endsWith(".html"));
  assert.ok(htmlFiles.length > 300, `expected the bulletin archive, found ${htmlFiles.length} HTML files`);
  for (const path of htmlFiles) {
    const html = await readFile(path, "utf8");
    const label = relative(outputRoot, path);
    assert.match(html, /<html\b[^>]*\blang=["'][^"']+/i, `${label}: missing language`);
    assert.match(html, /<title>[^<]+<\/title>/i, `${label}: missing title`);
    assert.match(html, /<meta\b[^>]*\bname=["']viewport["']/i, `${label}: missing viewport`);
  }
});

test("all generated local links and assets resolve", async () => {
  const htmlFiles = (await filesBelow(outputRoot)).filter((path) => path.endsWith(".html"));
  const missing = [];
  for (const htmlPath of htmlFiles) {
    const html = await readFile(htmlPath, "utf8");
    for (const reference of localReferences(html)) {
      const target = await resolveReference(htmlPath, reference);
      if (!target) continue;
      try { await stat(target); } catch { missing.push(`${relative(outputRoot, htmlPath)} -> ${reference}`); }
    }
  }
  assert.deepEqual(missing, []);
});

test("production CSS is compiled and both Netlify forms are present", async () => {
  const css = await readFile(join(outputRoot, "assets/css/tailwind.css"), "utf8");
  assert.doesNotMatch(css, /@tailwind\b/);
  const homepage = await readFile(join(outputRoot, "index.html"), "utf8");
  for (const name of ["bulletin-subscribe", "contact"]) {
    assert.match(homepage, new RegExp(`<form[^>]+name=["']${name}["'][^>]+data-netlify=["']true["']`, "i"));
    assert.match(homepage, new RegExp(`name=["']form-name["'][^>]+value=["']${name}["']`, "i"));
  }
});

test("Atom feed publishes the newest twenty bulletins with canonical URLs", async () => {
  const feed = await readFile(join(outputRoot, "feed.xml"), "utf8");
  assert.match(feed, /^<\?xml version="1\.0" encoding="utf-8"\?>/);
  assert.match(feed, /<feed xmlns="http:\/\/www\.w3\.org\/2005\/Atom"/);
  assert.match(feed, /<title>St\. Edward Parish Bulletins<\/title>/);
  assert.match(feed, /https:\/\/saintedwardtallulah\.church\/posts\/2026-08-16\//);
  assert.match(feed, /<title>Twentieth Sunday in Ordinary Time<\/title>/);
  assert.equal((feed.match(/<entry>/g) || []).length, 20);
  assert.doesNotMatch(feed, /https:\/\/stedwardtallulah\.church/);

  const homepage = await readFile(join(outputRoot, "index.html"), "utf8");
  assert.match(
    homepage,
    /<link rel="alternate" type="application\/atom\+xml" title="St\. Edward Parish Bulletins" href="\/feed\.xml">/
  );
});
