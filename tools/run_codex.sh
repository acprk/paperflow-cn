#!/usr/bin/env bash
# 用 Codex CLI 跑一轮只读审稿。
# 用法：tools/run_codex.sh <工作目录> <提示词文件> <输出文件> [超时秒数，默认2400]
#
# 要点（踩过的坑）：
# - 提示词通过标准输入传入（codex exec ... -），并且必须重定向自文件；
#   若不给提示词参数又不关闭标准输入，codex 会一直“Reading additional input from stdin...”卡住。
# - 一律用只读沙箱（-s read-only）：审稿人只能读、不能改稿。
# - -o 只保存最后一条回复（审稿结论）；完整过程写进同名 .log，便于复查审稿人的推理与检索。
set -euo pipefail
WORKDIR="$1"; PROMPT="$2"; OUT="$3"; TIMEOUT="${4:-2400}"
LOG="${OUT%.*}.log"
timeout "$TIMEOUT" codex exec -s read-only -C "$WORKDIR" -o "$OUT" - < "$PROMPT" > "$LOG" 2>&1
echo "审稿意见：$OUT"
echo "运行日志：$LOG"
