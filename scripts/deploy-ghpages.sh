#!/usr/bin/env bash
# Rebuild the site and update the gh-pages branch in one command.
# Usage: scripts/deploy-ghpages.sh [--push]
#   --push : also push master + gh-pages to origin (requires remote set)
set -euo pipefail
cd "$(dirname "$0")/.."

echo "· building site/ from content/…"
python3 scripts/build.py

echo "· updating gh-pages branch…"
BRANCH=$(git branch --show-current)
git checkout gh-pages
# wipe tracked files except .git, then copy fresh build
git rm -rq --cached . 2>/dev/null || true
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r site/* .
[ -f CNAME ] || echo "shihabarch.tech" > CNAME
touch .nojekyll   # critical: stops GitHub Jekyll from converting the .md twins
git add -A
if git diff --cached --quiet; then
  echo "· no changes — nothing to commit"
else
  git -c user.name="Mohammad Shahabuddin" -c user.email="mohammad.sahab.97@gmail.com" \
    commit -m "gh-pages: rebuild $(date +%F)"
fi
git checkout "$BRANCH"

if [ "${1:-}" = "--push" ]; then
  echo "· pushing…"
  git push origin master gh-pages
else
  echo "· done. Push with: git push origin master gh-pages  (or rerun with --push)"
fi
