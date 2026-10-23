#!/usr/bin/env bash
# 一键提交并推送 9702 讲义仓库（SSH，经 mihomo 代理）
# 用法：
#   ./deploy.sh                     # 自动生成提交信息
#   ./deploy.sh "更新第 5 章"        # 指定提交信息
#   ./deploy.sh --check             # 只做语法检查，不提交（跑 update_chapter.py validate）

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

PROXY="127.0.0.1:7890"
SSH_KEY="$HOME/.ssh/id_ed25519_github"

# ---- --check：只跑校验 ----
if [[ "${1:-}" == "--check" ]]; then
  [[ -f /tmp/ch_new.html ]] || { echo "用法：./deploy.sh --check 需配合 /tmp/ch_new.html"; exit 1; }
  python3 update_chapter.py validate /tmp/ch_new.html
  exit $?
fi

# ---- 代理连通性 ----
if ! timeout 2 bash -c "</dev/tcp/${PROXY%:*}/${PROXY##*:}" 2>/dev/null; then
  echo "❌ mihomo 代理 $PROXY 未监听 —— 请先启动 mihomo"
  exit 1
fi

# ---- GitHub SSH 认证检查 ----
# 注意：GitHub 认证成功时 ssh 仍返回 1（不提供 shell），故只检查输出
if ! ssh_out=$(timeout 20 ssh -o BatchMode=yes -o ConnectTimeout=10 -T git@github.com 2>&1); then
  :
fi
if [[ "$ssh_out" != *"successfully authenticated"* ]]; then
  echo "❌ GitHub SSH 认证失败 —— 检查 ~/.ssh/config 与密钥是否已添加到 GitHub"
  exit 1
fi

# ---- 工作区状态 ----
if git diff --quiet && git diff --cached --quiet && [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
  echo "✅ 没有需要提交的改动"
  git pull --ff-only --quiet 2>/dev/null || true
  exit 0
fi

echo "📋 变更文件："
git status --short

# ---- 提交信息 ----
msg="${1:-}"
if [[ -z "$msg" ]]; then
  changed=$(git status --short | awk '{print $NF}' | head -3 | paste -sd ', ' -)
  msg="更新内容：$changed ($(date '+%Y-%m-%d %H:%M'))"
fi

# ---- 大文件防护（GitHub 单文件上限 100 MB） ----
big=$(find . -path ./.git -prune -o -type f -size +50M -print 2>/dev/null | head -5)
if [[ -n "$big" ]]; then
  echo "⚠️  以下文件超过 50 MB，请确认是否要提交："
  echo "$big"
fi

git add -A
git commit -m "$msg"
git push

echo "✅ 已推送：$(git log -1 --oneline)"
