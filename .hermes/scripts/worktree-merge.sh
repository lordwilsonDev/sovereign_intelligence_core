#!/usr/bin/env bash
set -euo pipefail
BRANCH="${1:?branch required}"
BASE_BRANCH="${2:-main}"
ROOT="$(git rev-parse --show-toplevel)"

cd "$ROOT"
git merge "$BASE_BRANCH" --no-ff -m "merge: $BRANCH into $BASE_BRANCH" 2>/dev/null || {
  echo "Merge conflict detected while merging $BRANCH into $BASE_BRANCH"
  echo "Resolve conflicts, then run: git commit && make worktree-merge BRANCH=$BRANCH BASE=$BASE_BRANCH"
  exit 1
}
git branch -d "$BRANCH"
echo "Merged $BRANCH into $BASE_BRANCH"
