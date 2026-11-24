#!/bin/bash
# Instala a skill stories-organicos no Claude Code (~/.claude/skills/).
set -e
DESTINO="$HOME/.claude/skills/stories-organicos"
ORIGEM="$(cd "$(dirname "$0")" && pwd)/stories-organicos"

if [ -d "$DESTINO" ]; then
  echo "Já existe uma versão em $DESTINO. Substituindo pela desta pasta..."
  rm -rf "$DESTINO"
fi
mkdir -p "$HOME/.claude/skills"
cp -R "$ORIGEM" "$DESTINO"
echo "Pronto: skill instalada em $DESTINO"
echo
if command -v claude >/dev/null 2>&1 && claude mcp list 2>/dev/null | grep -q "^edits"; then
  echo "O Edits já está conectado ao Claude Code."
else
  echo "Falta conectar o Edits: abra o app, vá em Ajustes > Automação, ligue e use o botão"
  echo "\"Add Edits to Claude Code\" (passo a passo no README, Passo 1)."
fi
echo "Abra uma conversa nova no Claude Code e peça: \"cria anúncios de story orgânico com as minhas fotos\"."
