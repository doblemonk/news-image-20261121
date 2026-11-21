// News-image entry: "The World in One Image" -- 21 November 2026.
//
// The image is drawn by render.py (PIL, from the day's researched stories)
// and shipped in this repository as entry.png. This program's only job is
// to validate that file and place it where the grader looks for it:
//   <MAKEFUN_OUTPUT_DIR>/entry.png   (or /output/entry.png by default)
//
// It runs with no network and no dependencies (Node 22 standard library
// only), and it is deterministic: the same entry.png always produces the
// same output bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // the gate takes at most 1 MiB

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
// PNG IHDR chunk: width is the 4-byte big-endian value at offset 16 and
// height the one at offset 20 (after the 8-byte signature + 8-byte chunk
// header). Reading them here keeps the gate's 1024x1024 cap enforced.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

copyFileSync(source, target);
const written = statSync(target).size;
console.log(`wrote ${target} (${width}x${height}, ${written} bytes)`);
