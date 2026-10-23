#!/usr/bin/env python3
"""Median job time per runner for one run of rust.yml, typescript.yml or docker-build.yml.

A job's time is the sum of its "phase: ..." steps, as GitHub records them
(started_at to completed_at). Only jobs whose phases all succeeded count.

    python3 scripts/medians.py <run id>
"""
import datetime
import json
import re
import statistics
import subprocess
import sys

REPO = "buildpulse/runner-benchmarks"


def seconds(step):
    parse = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (parse(step["completed_at"]) - parse(step["started_at"])).total_seconds()


def main(run_id):
    out = subprocess.check_output(
        ["gh", "api", "--paginate", f"repos/{REPO}/actions/runs/{run_id}/jobs?per_page=100", "--jq", ".jobs[]"]
    )
    by_runner = {}
    for line in out.decode().splitlines():
        job = json.loads(line)
        phases = [s for s in job["steps"] if s["name"].startswith("phase:") and s["conclusion"] != "skipped"]
        if not phases or any(s["conclusion"] != "success" for s in phases):
            print(f"skipped {job['name']}: {job['conclusion']}", file=sys.stderr)
            continue
        runner = re.sub(r" \d+$", "", job["name"]).split(" ", 1)[1]
        by_runner.setdefault(runner, []).append(sum(seconds(s) for s in phases))
    for runner, times in sorted(by_runner.items()):
        print(f"{runner}: n={len(times)} median={statistics.median(times):.0f}s runs={sorted(round(t) for t in times)}")


if __name__ == "__main__":
    main(sys.argv[1])
