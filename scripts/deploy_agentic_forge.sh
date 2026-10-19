#!/usr/bin/env bash
# Deploy a pinned Agentic Forge version into a consuming repository.
#
# Usage:
#   scripts/deploy_agentic_forge.sh <repo>            # dry-run
#   scripts/deploy_agentic_forge.sh <repo> --apply    # update, validate, commit
#
# The target must be clean and have a .agent submodule and a forge.toml.
# On validation failure the script restores the previous submodule commit.
set -euo pipefail

usage() {
    sed -n '2,8p' "$0"
}

target="${1:-}"
mode="${2:-}"
if [[ -z "$target" || "$target" == "-h" || "$target" == "--help" ]]; then
    usage
    exit 2
fi
if [[ -n "$mode" && "$mode" != "--apply" ]]; then
    usage
    exit 2
fi

repo="$(cd "$target" && pwd)"
agent="$repo/.agent"
if [[ ! -e "$agent/.git" ]]; then
    echo "❌ $repo has no .agent submodule." >&2
    exit 2
fi
if [[ ! -f "$repo/forge.toml" ]]; then
    echo "❌ $repo has no forge.toml; this is not an Agentic Forge consumer." >&2
    exit 2
fi

version="${AGENTIC_FORGE_VERSION:-v1.4.2}"

cd "$repo"
if [[ -n "$(git status --porcelain)" ]]; then
    echo "❌ Working tree is dirty; commit or stash changes first:" >&2
    git status --short >&2
    exit 1
fi

current_commit="$(git -C .agent rev-parse HEAD)"
current_label="$(git -C .agent describe --tags --always 2>/dev/null || echo "$current_commit")"
echo "Repo:              $repo"
echo "Current framework: $current_label"
echo "Desired framework: $version"

if [[ "$mode" != "--apply" ]]; then
    echo "Dry-run only. Re-run with --apply to update the submodule."
    exit 0
fi

restore() {
    echo "↩️  Restoring .agent to $current_commit" >&2
    git -C .agent checkout -q "$current_commit" || true
    git reset -q -- .agent || true
}
trap restore ERR

echo "Fetching tags..."
git -C .agent fetch --tags origin
git -C .agent checkout "$version"

export PYTHONDONTWRITEBYTECODE=1
python .agent/tools/forge.py validate
python .agent/tools/forge.py validate --graph
python .agent/tools/forge.py validate --conflicts
python .agent/tools/forge.py metrics validate
python .agent/tools/forge.py memory check
python .agent/tools/forge.py memory prune

trap - ERR
git add .agent
git commit -m "chore(agent): bump agentic-forge to $version"
echo "✅ Updated $repo to $version."
echo "Push with: git push origin HEAD"
