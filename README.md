# Paper Tide Observatory

A deterministic Node 22 image entry for make.fun's **ai-excited-01** competition. It depicts a luminous origami dragon erupting from a tiny paper boat, with its tail turning into a galaxy and a cyan orbital lens framing the storm.

[![make.fun competition](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/c/ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/Mlnglh889/paper-tide-observatory-20261116/rank.svg)](https://make.fun/c/ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/Mlnglh889/paper-tide-observatory-20261116/reward.svg)](https://make.fun/c/ai-excited-01)

## Run

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The runtime uses only Node's standard library and copies the committed `entry.png` to the output directory. `build_art.py` is a build-time Pillow generator for the original artwork; the competition runtime does not install or import it.

## License

MIT
