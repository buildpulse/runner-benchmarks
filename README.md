# runner-benchmarks

Transparent, reproducible benchmarks comparing GitHub-hosted runners with
[BuildPulse runners](https://buildpulse.io/products/runners), on real open-source
workloads. Every number we publish links to a run in this repo's Actions tab.

## Method

- **Same jobs, two runners**: every workload runs identically on `ubuntu-latest`
  (GitHub-hosted, 4 vCPU) and `bp-ubuntu-latest-x64-4x` (BuildPulse, 4 vCPU / 16 GB).
- **Real workloads, pinned versions** (no synthetic loops):
  - `node-build`: vuejs/core at a pinned tag — install, build, unit tests
  - `go-build`: gohugoio/hugo at a pinned tag — full compile
  - `docker-build`: hugo's own multi-stage Dockerfile at the pinned tag, no cache
- **Queue time** is measured from the GitHub API (`created_at` → `started_at` per job),
  not self-reported.
- **Medians over repeated runs.** Single runs lie; we dispatch batches and report
  median and p95. The harvest script is in `scripts/`.

- **Hardware receipts** (`hardware.yml`): sysbench CPU/memory and fio disk numbers
  from the exact machines the workloads run on, same commands both sides.
- **Cache, cold vs warm** (`docker-cache.yml`): the warm build runs on a FRESH
  machine, so the speedup is the cache infrastructure, not a lingering daemon.
  GitHub gets its own recommended remote cache (buildx `gha` backend, run-scoped);
  BuildPulse uses the docker-builder pool's persistent layer cache on local NVMe.

Anyone can fork this and reproduce. If you get different numbers, open an issue.
