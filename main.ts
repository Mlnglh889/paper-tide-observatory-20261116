// Paper Tide Observatory: deterministic, dependency-free delivery.
// The committed PNG is the complete artwork; the sandbox only needs a byte copy.
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(targetDir, { recursive: true });
const source = new URL('./entry.png', import.meta.url);
const target = join(targetDir, 'entry.png');
const bytes = readFileSync(source);
if (bytes.length > 1048576 || bytes.readUInt32BE(0) !== 0x89504e47) {
  throw new Error('entry.png must be a valid PNG no larger than 1 MiB');
}
copyFileSync(source, target);
