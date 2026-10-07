# docker-agent: Docker Docs migration experiment

Faithful reconstruction of Docker Docs pinned at `6cf1b1c167f032e8a6629da211602300b623b20e`. Nift itself is unchanged.

Source model: maintained rendered HTML → Nift composition → publication/search.

## Build

Prerequisites: Python (tested 3.14.4), Nift 4.7.2, and Node/npm (tested 24.21.0/11.19.0). Parallel HTML analysis uses POSIX fork. Install tools/dependencies before measuring builds:

```sh
python3 scripts/build.py --setup
python3 scripts/build.py --all
python3 scripts/build.py
nift status
```

Use `scripts/build.py` as the publication entry point: it prepares explicit Nift dependencies, downloads, metadata, feeds, redirects and fresh Pagefind search. Direct `nift build` only composes already-prepared fragments. Output is `public/`; `.generated/` and `.cache/` are disposable application state, while `.nift/` is maintained tracking/configuration.

Edit maintained HTML under `pages/` and associated typed page metadata under `data/`. Routine builds have no Markdown renderer. HTML analysis generates heading bindings and Markdown downloads from those maintained bodies.

Shared layouts live under `layouts/`; navigation and publication bindings live under `data/`. Route additions/renames/deletions require the corresponding maintained registry/metadata/navigation changes. The lifecycle harness demonstrates these operations, including retirement of old outputs. Compiled frontend assets are maintained upstream assets, preserving accepted interactions.

## Evidence

See [HANDOVER.md](HANDOVER.md), [baseline provenance](investigation/BASELINE.md), [initial C6 benchmarks](investigation/C6-BENCHMARKS.md), and [C6 optimization](investigation/C6-OPTIMIZATION.md). C7 will contain the complete comparison after fresh-checkout measurements. Initial evidence is immutable; reruns must use a new evidence output directory.
