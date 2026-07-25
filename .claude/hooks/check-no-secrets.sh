#!/bin/bash
# PreToolUse hook (matcher: Bash) — bloqueia `git commit` quando o diff staged
# contém um padrão de segredo em texto plano.
#
# Recupera mecanicamente, para o caminho de commit, a garantia que
# nr.no-hardcoded-secrets (MUST_NOT, core/standard.code-quality.review-baseline@1.0.0)
# perdeu ao virar só instrução textual em .claude/skills/code-review/SKILL.md.
# A skill continua sendo "pedir ao modelo"; este hook é a barreira mecânica que
# não depende do modelo ter seguido a instrução.
#
# Conjunto de padrões deliberadamente pequeno e ilustrativo — não substitui uma
# ferramenta dedicada (gitleaks, trufflehog) contra um banco de padrões completo
# e atualizado. Mesma ressalva de não-exaustividade já registrada para a skill
# `dependency-audit` (docs/claude-code-translation.md).

set -uo pipefail

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"

# Só age sobre comandos que contêm `git commit`; qualquer outro Bash passa direto.
if ! printf '%s' "$COMMAND" | grep -qE '(^|[;&|]|\s)git\s+commit(\s|$)'; then
  exit 0
fi

STAGED_DIFF="$(git diff --cached -- . 2>/dev/null)"
if [ -z "$STAGED_DIFF" ]; then
  exit 0
fi

PATTERNS='sk_live_[0-9a-zA-Z]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[0-9a-zA-Z]{36}|AIza[0-9A-Za-z_-]{35}|-----BEGIN[ A-Z]*PRIVATE KEY-----'

CURRENT_FILE="(arquivo desconhecido)"
FINDINGS=""
while IFS= read -r line; do
  case "$line" in
    "+++ "*)
      CURRENT_FILE="${line#+++ b/}"
      ;;
    "+++"*) ;;
    "+"*)
      CONTENT="${line:1}"
      if printf '%s' "$CONTENT" | grep -qE "$PATTERNS"; then
        SNIPPET="${CONTENT:0:100}"
        FINDINGS="${FINDINGS}  - ${CURRENT_FILE}: ${SNIPPET}"$'\n'
      fi
      ;;
  esac
done <<< "$STAGED_DIFF"

if [ -n "$FINDINGS" ]; then
  {
    echo "BLOQUEADO por .claude/hooks/check-no-secrets.sh"
    echo ""
    echo "Padrão de segredo em texto plano detectado no diff staged:"
    echo "$FINDINGS"
    echo "Corresponde a nr.no-hardcoded-secrets (MUST_NOT, core/standard.code-quality.review-baseline@1.0.0)."
    echo "Remova o valor do código-fonte (variável de ambiente / gerenciador de segredos)"
    echo "e revogue a credencial se ela já tiver sido exposta em algum commit ou diff."
    echo "Se for um valor de teste/fixture deliberado, ajuste o padrão do fixture"
    echo "para não corresponder à assinatura de uma credencial real, ou peça revisão"
    echo "humana explícita antes de tentar de novo."
  } >&2
  exit 2
fi

exit 0
