// Paper Tide Observatory: deterministic, dependency-free delivery.
// The committed PNG is the complete artwork; the sandbox only needs a byte copy.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(targetDir, { recursive: true });
const source = new URL('./entry.png', import.meta.url);
const target = join(targetDir, 'entry.png');
copyFileSync(source, target);
if (!target || !dirname(target)) throw new Error('output path unavailable');
