#!/usr/bin/env bash
set -euo pipefail
TASK="${1:-}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
WORKTREE_DIR="$REPO_ROOT/.worktrees/agent-$$"
BRANCH="agent/$$-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$REPO_ROOT/.worktrees"
git worktree add "$WORKTREE_DIR" -b "$BRANCH" >/dev/null 2>&1 || {
  echo "Worktree creation failed. Cleaning up..."
  git worktree remove "$WORKTREE_DIR" 2>/dev/null || true
  git branch -D "$BRANCH" 2>/dev/null || true
  exit 1
}

echo "WORKTREE=$WORKTREE_DIR"
echo "BRANCH=$BRANCH"
echo "---"
echo "Agent checkout: $WORKTREE_DIR"
echo "Task: $TASK"
echo ""
echo "Next:"
echo "  1. cd $WORKTREE_DIR"
echo "  2. Do the work"
echo "  3. Run: make verify"
echo "  4. Run: make worktree-merge BRANCH=$BRANCH"
