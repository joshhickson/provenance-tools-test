#!/usr/bin/env bash
# Step 1 of a tool run: create the demo repo from the seed. Tool setup happens
# next, by hand via `docker exec`, and is recorded in phase2-notes.md.
set -euo pipefail
git config --global user.name "demo"
git config --global user.email "demo@example.com"
git config --global init.defaultBranch main
rm -rf /work/repo
cp -r /scenario/seed /work/repo
cd /work/repo
git init -q && git add -A && git commit -qm "seed: provider stub"
echo "seeded /work/repo"
