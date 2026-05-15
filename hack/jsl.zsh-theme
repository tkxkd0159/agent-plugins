function _git_custom_prompt() {
  git rev-parse --is-inside-work-tree &>/dev/null || return

  local branch
  branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
  [[ -z "$branch" ]] && return

  local result="%F{magenta}⎇ ${branch//\%/%%}%f"

  local counts
  counts=$(git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null)
  if [[ -n "$counts" ]]; then
    local ahead=${counts%%$'\t'*}
    local behind=${counts##*$'\t'}
    local sync=""
    [[ "$ahead" -gt 0 ]] && sync+="⇡$ahead"
    [[ "$ahead" -gt 0 && "$behind" -gt 0 ]] && sync+=" "
    [[ "$behind" -gt 0 ]] && sync+="⇣$behind"
    [[ -n "$sync" ]] && result+=" %F{blue}[$sync]%f"
  fi

  local porcelain
  porcelain=$(git status --porcelain -uall 2>/dev/null)
  if [[ -n "$porcelain" ]]; then
    local deleted=0 changed=0
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      if [[ "${line[1]}" == "D" || "${line[2]}" == "D" ]]; then
        ((deleted++))
      else
        ((changed++))
      fi
    done <<< "$porcelain"
    [[ "$deleted" -gt 0 ]] && result+=" %F{red}✘$deleted%f"
    [[ "$changed" -gt 0 ]] && result+=" %F{yellow}✚$changed%f"
  else
    result+=" %F{green}✔%f"
  fi

  echo -n "$result"
}

function _k8s_prompt() {
  command -v kubectl >/dev/null 2>&1 || return
  local context
  context=$(kubectl config current-context 2>/dev/null)
  [[ -z "$context" ]] && return
  local namespace
  namespace=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}' 2>/dev/null)
  [[ -z "$namespace" ]] && namespace="default"
  echo -n " ⚓️%F{#ffdfba}${context}(${namespace})%f"
}

PROMPT=" %{$fg[cyan]%}%~%{$reset_color%}"
PROMPT+=' $(_git_custom_prompt)$(_k8s_prompt)'
PROMPT+=$'\n''%(?:%{$fg_bold[green]%}%1{➜%} :%{$fg_bold[red]%}%1{➜%} )%{$reset_color%}'
RPROMPT='%F{yellow}%D %*%f'
