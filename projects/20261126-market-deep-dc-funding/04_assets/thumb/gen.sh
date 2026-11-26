#!/bin/bash
# $1 = out file, $2 = prompt
cd "$(dirname "$0")"
codex exec --skip-git-repo-check -s workspace-write -C "$(pwd)" "Use the \$imagegen skill to generate ONE image and save it exactly to $(pwd)/$1 (PNG, landscape 16:9, at least 1536x864). Do not edit any other file. Prompt: $2" > "$1.log" 2>&1
echo "done $1 $?" >> gen_done.txt
