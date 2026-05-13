#!/usr/bin/env node
import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const denylistPath = path.join(root, 'security', 'denylist.json');
const denylist = JSON.parse(await readFile(denylistPath, 'utf8'));

const blockedArtifacts = (denylist.blockedArtifacts || []).map((entry) => ({
  name: String(entry.name || '').toLowerCase(),
  reason: String(entry.reason || 'blocked artifact'),
})).filter((entry) => entry.name);

const allowedReferences = new Set(
  (denylist.allowedReferences || []).map((entry) => normalize(entry)),
);

const skipDirs = new Set([
  '.git',
  'node_modules',
  'dist',
  'build',
  '.next',
  'coverage',
  'temp-uploads',
  'issues',
]);

const textExtensions = new Set([
  '.c', '.cc', '.cpp', '.css', '.h', '.hpp', '.html', '.js', '.jsx',
  '.json', '.mjs', '.md', '.ts', '.tsx', '.txt', '.yaml', '.yml',
]);

function normalize(filePath) {
  return filePath.split(path.sep).join('/');
}

function relative(filePath) {
  return normalize(path.relative(root, filePath));
}

function shouldSkipDirectory(dirName) {
  return skipDirs.has(dirName) || dirName.startsWith('.cache');
}

function isTextFile(filePath) {
  return textExtensions.has(path.extname(filePath).toLowerCase());
}

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!shouldSkipDirectory(entry.name)) {
        yield* walk(fullPath);
      }
      continue;
    }
    if (entry.isFile()) {
      yield fullPath;
    }
  }
}

const violations = [];

for await (const filePath of walk(root)) {
  const rel = relative(filePath);
  const fileName = path.basename(filePath).toLowerCase();

  for (const artifact of blockedArtifacts) {
    if (fileName === artifact.name) {
      violations.push(`${rel}: blocked filename ${artifact.name} — ${artifact.reason}`);
    }
  }

  if (allowedReferences.has(rel) || !isTextFile(filePath)) {
    continue;
  }

  const info = await stat(filePath);
  if (info.size > 1024 * 1024) {
    continue;
  }

  const content = (await readFile(filePath, 'utf8')).toLowerCase();
  for (const artifact of blockedArtifacts) {
    if (content.includes(artifact.name)) {
      violations.push(`${rel}: references ${artifact.name} — ${artifact.reason}`);
    }
  }
}

if (violations.length) {
  console.error('Blocked vulnerable artifacts found:');
  for (const violation of violations) {
    console.error(`- ${violation}`);
  }
  process.exit(1);
}

console.log(`No blocked artifacts found (${blockedArtifacts.map((a) => a.name).join(', ') || 'empty denylist'}).`);
