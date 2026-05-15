#!/bin/bash

input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir')
session_name=$(echo "$input" | jq -r '.session_name // empty')
model_name=$(echo "$input" | jq -r '.model.display_name')
effort_level=$(echo "$input" | jq -r '.effort.level // empty')

# ── Git info (mirrors jsl.zsh-theme logic) ──────────────────────────────────
git_line=""
if git -C "$cwd" rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null \
             || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        git_line="\033[35m⎇ ${branch}\033[0m"

        counts=$(git -C "$cwd" rev-list --left-right --count 'HEAD...@{upstream}' 2>/dev/null)
        if [ -n "$counts" ]; then
            ahead="${counts%%$'\t'*}"
            behind="${counts##*$'\t'}"
            sync=""
            [ "$ahead" -gt 0 ] && sync="${sync}⇡${ahead}"
            [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ] && sync="${sync} "
            [ "$behind" -gt 0 ] && sync="${sync}⇣${behind}"
            [ -n "$sync" ] && git_line="${git_line} \033[34m[${sync}]\033[0m"
        fi

        porcelain=$(git -C "$cwd" status --porcelain -uall 2>/dev/null)
        if [ -n "$porcelain" ]; then
            deleted=0; changed=0
            while IFS= read -r line; do
                [ -z "$line" ] && continue
                xy="${line:0:2}"
                if [[ "$xy" == *D* ]]; then
                    ((deleted++))
                else
                    ((changed++))
                fi
            done <<< "$porcelain"
            [ "$deleted" -gt 0 ] && git_line="${git_line} \033[31m✘${deleted}\033[0m"
            [ "$changed" -gt 0 ] && git_line="${git_line} \033[33m✚${changed}\033[0m"
        else
            git_line="${git_line} \033[32m✔\033[0m"
        fi
    fi
fi

# ── Kubernetes context ───────────────────────────────────────────────────────
k8s_context=""
k8s_namespace=""
if command -v kubectl > /dev/null 2>&1; then
    k8s_context=$(kubectl config current-context 2>/dev/null)
    if [ -n "$k8s_context" ]; then
        k8s_namespace=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}' 2>/dev/null)
        [ -z "$k8s_namespace" ] && k8s_namespace="default"
    fi
fi

# ── Claude.ai rate limit cache ───────────────────────────────────────────────
context_used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
rate_5h=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
rate_7d=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

RATE_CACHE="$HOME/.claude/rate-limits-cache.json"
rate_5h_stale=false
rate_7d_stale=false

if [ -n "$rate_5h" ] || [ -n "$rate_7d" ]; then
    cached_5h="${rate_5h:-null}"
    cached_7d="${rate_7d:-null}"
    if [ -f "$RATE_CACHE" ]; then
        [ -z "$rate_5h" ] && cached_5h=$(jq -r '.five_hour // "null"' "$RATE_CACHE" 2>/dev/null || echo "null")
        [ -z "$rate_7d" ] && cached_7d=$(jq -r '.seven_day // "null"' "$RATE_CACHE" 2>/dev/null || echo "null")
    fi
    printf '{"five_hour":%s,"seven_day":%s}' "$cached_5h" "$cached_7d" > "$RATE_CACHE" 2>/dev/null
else
    if [ -f "$RATE_CACHE" ]; then
        cached_5h=$(jq -r '.five_hour // empty' "$RATE_CACHE" 2>/dev/null)
        cached_7d=$(jq -r '.seven_day // empty' "$RATE_CACHE" 2>/dev/null)
        [ -n "$cached_5h" ] && rate_5h="$cached_5h" && rate_5h_stale=true
        [ -n "$cached_7d" ] && rate_7d="$cached_7d" && rate_7d_stale=true
    fi
fi

# ── Session duration ────────────────────────────────────────────────────────
# Claude Code does not expose a session-start timestamp in the JSON, so we
# derive it from the transcript file's creation time (birthtime on macOS /
# ctime fallback on Linux). The transcript file is created when the session
# opens and its path is stable for the lifetime of the session.
session_duration=""
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
    # macOS: stat -f %SB (birthtime); Linux fallback: stat -c %Z (ctime)
    if stat -f "%SB" "$transcript_path" > /dev/null 2>&1; then
        birth_epoch=$(stat -f "%B" "$transcript_path" 2>/dev/null)
    else
        birth_epoch=$(stat -c "%Z" "$transcript_path" 2>/dev/null)
    fi
    if [ -n "$birth_epoch" ]; then
        now_epoch=$(date +%s)
        elapsed=$(( now_epoch - birth_epoch ))
        if [ "$elapsed" -ge 3600 ]; then
            hours=$(( elapsed / 3600 ))
            minutes=$(( (elapsed % 3600) / 60 ))
            if [ "$minutes" -gt 0 ]; then
                session_duration="${hours}h${minutes}m"
            else
                session_duration="${hours}h"
            fi
        else
            minutes=$(( elapsed / 60 ))
            session_duration="${minutes}m"
        fi
    fi
fi

# ── Line 1: Claude metadata ──────────────────────────────────────────────────
# Model name: magenta
line1="\033[35m${model_name}\033[0m"

# Effort level: yellow-orange
[ -n "$effort_level" ] && line1="${line1} \033[33m[${effort_level}]\033[0m"

# Context used percentage: green
[ -n "$context_used" ] && line1="${line1} \033[32mctx:$(printf '%.0f' "$context_used")%\033[0m"

# Rate limit usage: 5h (orange) and 7d (red)
if [ -n "$rate_5h" ]; then
    if $rate_5h_stale; then
        line1="${line1} \033[38;5;214m~5h:$(printf '%.0f' "$rate_5h")%\033[0m"
    else
        line1="${line1} \033[38;5;214m5h:$(printf '%.0f' "$rate_5h")%\033[0m"
    fi
fi
if [ -n "$rate_7d" ]; then
    if $rate_7d_stale; then
        line1="${line1} \033[31m~7d:$(printf '%.0f' "$rate_7d")%\033[0m"
    else
        line1="${line1} \033[31m7d:$(printf '%.0f' "$rate_7d")%\033[0m"
    fi
fi

# Session duration: fire emoji + dim white
[ -n "$session_duration" ] && line1="${line1} 🔥${session_duration}"

# Session name
[ -n "$session_name" ] && line1="${line1} \033[35m[${session_name}]\033[0m"

# ── Line 2: theme metadata ───────────────────────────────────────────────────
# Cyan path (~ for home)
short_cwd="${cwd/#$HOME/~}"
line2="\033[36m${short_cwd}\033[0m"

# Git info
[ -n "$git_line" ] && line2="${line2} ${git_line}"

# kubectl context/namespace with anchor and cream/peach colour (#ffdfba = 256-colour approximation 223)
if [ -n "$k8s_context" ]; then
    line2="${line2} ⚓️\033[38;5;223m${k8s_context}(${k8s_namespace})\033[0m"
fi

# Date/time (yellow, mirrors RPROMPT)
line2="${line2} ⏳\033[33m$(date '+%y-%m-%d %H:%M:%S')\033[0m"

printf '%b\n%b' "$line1" "$line2"
