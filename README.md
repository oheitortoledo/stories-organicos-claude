# Stories orgânicos com Claude + Edits

Uma skill pro **Claude Code** que cria anúncios de story com **cara 100% orgânica**: a sua foto, com o texto nas **fontes e cores do próprio Instagram** e a **caixinha de pergunta** no formato da original. Tudo montado sozinho no **Edits**, o app de edição da Meta, e entregue em JPG 1080 × 1920 pronto pra subir.

Você conta a oferta e manda as fotos. O Claude:
1. escreve a copy de cada story (gancho, meio e chamada) e espera você aprovar;
2. olha cada foto pra não pôr texto em cima do rosto;
3. escolhe um visual diferente pra cada story, porque lote com tudo igual entrega que é anúncio;
4. monta tudo no Edits, confere quadro a quadro e entrega as imagens.

Criado por [@oheitortoledo](https://instagram.com/oheitortoledo).

---

## O que você precisa

- **Um Mac** (foi testado no macOS, com o Edits 457).
- **O app Edits** instalado (é gratuito, da Meta).
- **O Claude Code** instalado (terminal, app desktop ou extensão do VS Code).
- **Python 3**, que já vem no Mac. Não precisa instalar mais nada.

## Passo 1 · Conectar o Claude ao Edits (2 minutos)

1. Abra o **Edits**.
2. Vá em **Ajustes** (⌘ + vírgula) e abra a aba **Automação**.
3. **Ligue** a automação. Vão aparecer a chave de acesso e o botão **"Add Edits to Claude Code"**.
4. Clique no botão. Ele copia um comando que começa com `claude mcp add`.
5. Abra o **Terminal** (⌘ + espaço, digite "Terminal"), cole o comando (⌘ + V) e aperte Enter. Deve aparecer *"Added HTTP MCP server edits"*.
6. **Reinicie o Claude Code** (feche e abra uma conversa nova). Digite `/mcp`: o **edits** tem que aparecer conectado.

> A chave de acesso funciona como senha: ela dá controle dos seus projetos no Edits. Não mande ela pra ninguém nem cole em lugar público. O servidor só aceita conexão do seu próprio computador.

## Passo 2 · Instalar a skill

No Terminal:

```bash
git clone https://github.com/oheitortoledo/stories-organicos-claude.git
cd stories-organicos-claude
./instalar.sh
```

Ou copie a pasta `stories-organicos` pra `~/.claude/skills/` à mão. Depois, abra uma conversa nova no Claude Code.

## Passo 3 · Usar

1. Coloque as suas fotos numa pasta dentro de **Filmes** (`~/Movies/minhas-fotos/`). O Edits só consegue ler arquivos dessa pasta.
2. Peça pro Claude, do seu jeito. Exemplos:
   - *"Cria 6 anúncios de story orgânico pro meu curso de confeitaria. As fotos estão em Filmes/fotos-curso. A página é meusite.com/curso."*
   - *"Quero stories com cara de orgânico pra Black Friday da minha mentoria, sem preço na arte."*
   - *"Faz um story com caixinha de pergunta respondendo 'serve pra iniciante?'."*
3. Aprove a copy. O Claude monta, revisa e abre a pasta com as imagens prontas.

Cada story também fica salvo como projeto no Edits, com o nome do criativo. Se quiser mexer em alguma coisa à mão, é só abrir o projeto no app.

## Problemas comuns

| O que aconteceu | O que fazer |
|---|---|
| "O Edits não respondeu" | Abra o Edits e confira se a Automação está ligada. Se você fechou e abriu o app, a porta pode ter mudado: refaça o Passo 1 (antes, rode `claude mcp remove edits -s user`). |
| "a pasta das fotos precisa estar dentro de ~/Movies" | Mova as fotos pra uma pasta dentro de Filmes. |
| Alguma fonte faltando | Atualize o Edits. As fontes do Instagram vêm dentro do app. |
| Texto encostando em outro | O Claude avisa e refaz. Se quiser, peça uma linha a menos ou uma fonte menor. |

## O que ela não faz

- **Não posta** no Instagram nem sobe anúncio: entrega as imagens pra você subir.
- **Não usa a figurinha oficial** de pergunta do Instagram. Essa só existe postando pelo app. A caixinha aqui é uma réplica fiel, com a fonte do Instagram.
- **Não faz vídeo.** É story estático: foto + texto.

## Como funciona por dentro

A skill (`stories-organicos/SKILL.md`) guia o Claude pelas etapas. A montagem é feita pelo `scripts/montar.py`, que conversa direto com a automação local do Edits (só no seu computador). O fundo da caixinha de pergunta é desenhado pelo `scripts/caixinha.py`, em Python puro. O `references/` tem as fontes, as cores, as combinações testadas e tudo que já deu errado e como foi resolvido.

## Licença

MIT. Use, adapte e compartilhe à vontade.
