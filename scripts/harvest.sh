#!/usr/bin/env bash
# Collects queue + duration stats for all bench runs.
#   ./scripts/harvest.sh > results.csv
set -euo pipefail
echo "run_id,job,runner,queued_s,duration_s,conclusion"
gh run list --workflow bench --limit 50 --json databaseId --jq '.[].databaseId' | while read -r id; do
  gh api "repos/{owner}/{repo}/actions/runs/$id/jobs" --jq '.jobs[] | [
    .run_id, .name, (.labels[0] // "?"),
    ((.started_at | fromdate) - (.created_at | fromdate)),
    ((.completed_at | fromdate) - (.started_at | fromdate)),
    .conclusion] | @csv'
done
