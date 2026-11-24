---
name: stories-organicos
description: Cria anúncios de STORY (9:16) com cara 100% orgânica, como se o especialista tivesse postado do celular. Cada peça é uma foto do especialista com texto nas fontes do Instagram (Classic, Modern, Editor, Poster, Squeeze, Signature), na paleta de cores do Instagram, e caixinha de pergunta no formato da original. Escreve a copy story a story pra aprovação, monta tudo no app Edits (Meta) pela automação local, revisa quadro a quadro e entrega JPG 1080×1920. Use SEMPRE que o usuário pedir "story orgânico", "anúncio de story", "anúncio com cara de story", "criativo de story", "story estático", "stories pro lançamento / Black Friday / oferta", "monta no Edits", "faz no Edits", "caixinha de pergunta", "story com a minha foto", "anúncio que não parece anúncio", ou mandar fotos pedindo anúncio pra stories, mesmo sem dizer "orgânico". Não serve pra vídeo nem pra post de feed.
---

# Stories orgânicos (copy → fotos → Edits → JPG)

**A ideia:** o anúncio de story que mais vende é o que parece story normal. Por isso cada peça leva uma foto real do especialista, texto com a fonte e a cor que o próprio Instagram oferece, e nada de layout de agência. E cada story do lote tem um visual diferente: repetir o mesmo visual em todos entrega que é anúncio.

Exemplo completo de lote: `assets/exemplo-lote.json`. As copies desse exemplo estão em `references/exemplo-copies.md`.

## O que sai

- **Uma imagem por story**, em JPG 1080 × 1920: uma foto do especialista com gancho, meio e chamada. Sem vídeo, sem fala, sem montagem de várias fotos.
- **Um projeto no Edits por story**, com o nome do código, pra ajustar à mão se quiser.
- **A copy num arquivo `.md`** na pasta do projeto do usuário.

## Antes de começar

1. **Confira se o Edits está pronto.** O app precisa estar aberto, com **Ajustes > Automação** ligada, e conectado ao Claude Code (`claude mcp list` mostra `edits … Connected`). Se não estiver, mande a pessoa seguir o README da skill: lá está o passo a passo, que leva dois minutos.
2. **Leia o contexto.** Se o projeto tiver arquivo de contexto (CLAUDE.md, briefing, página de vendas), leia. Dele saem a oferta que está no ar, a página de destino, as palavras que o especialista usa e as que ele não usa. Se não tiver, pergunte o mínimo: o que é a oferta, pra onde o anúncio leva, e se há prazo, bônus ou condição especial confirmados.
3. **Fotos na pasta Filmes.** O Edits só lê arquivos dentro de `~/Movies`. Crie `~/Movies/<nome-do-lote>/` e coloque as fotos lá, ou copie você mesmo de onde estiverem.
4. **Nome dos criativos.** Se a pessoa já tem um padrão de nome de criativo, siga e continue a numeração. Se não tem, sugira `[OFERTA]_STORY_[NUM]`: código da oferta em 3 letras e número com 3 casas (`CONF_STORY_001`). Esse nome vai no arquivo e no anúncio, e é ele que liga o criativo à métrica.

## Etapa 1 · Copy, pra aprovar antes de montar

O texto fecha antes do design. Cada story tem três partes:

- **Gancho** (no alto): diz com quem a peça fala e prende. Até 3 linhas de ~20 caracteres.
- **Meio**: a ideia da oferta numa frase. Até 3 ou 4 linhas de ~35 caracteres.
- **Chamada**: "toca em Saiba mais 👇" ou uma variação com o motivo ("e vê tudo", "garante até quarta").

Ou, no lugar do gancho, uma **caixinha de pergunta** (convite + pergunta "do seguidor") com a resposta no meio. É a melhor forma de quebrar objeção ("é por 1 ano?", "e se eu não tiver tempo?").

Princípios, e o porquê de cada um:
- **Sem preço na arte, por padrão.** Preço no story tira a cara de orgânico. E se a oferta tiver mais de um preço (cliente antigo × novo, à vista × parcelado), a pessoa chega na página e vê um número diferente. O preço fica pra página. Só põe preço se o usuário pedir.
- **Uma ideia por story, dizendo pra quem é.** Story é lido em 2 segundos.
- **Nada que não esteja confirmado.** Número de prova ("mais de 10 mil alunos"), vaga limitada, prazo e evento só entram se vierem do material do especialista. Peça que depende de confirmação leva ■ e, se tiver hora, o horário de sair do ar.
- **Ângulos que funcionam** (cardápio em `references/exemplo-copies.md`): o pacote todo, a âncora sem número ("pelo preço de um"), a lista do que vem, objeção em caixinha, garantia, data sazonal, condição de quem já é cliente, evento com vaga, prova em número.

Mostre no chat uma tabela (código · ângulo · gancho · meio · chamada), salve o `.md` e **espere a aprovação.**

## Etapa 2 · Casar fotos e stories

Abra cada foto pra ver como ela é (gere uma prévia leve com `sips -Z 900 <foto> --out <pasta-temporária>/<nome>.jpg` e leia a imagem). Anote duas coisas:
- **`topo`**: até onde vai o rosto. É a fração da altura onde o texto pode começar, logo abaixo do queixo, quase sempre entre 0,40 e 0,47. Texto em cima do rosto mata a peça.
- **Fundo atrás do texto**: claro (roupa branca, parede clara) ou escuro. A caixinha de pergunta é branca, então **só vai em foto com fundo escuro**; em cima de roupa branca ela some.

Com menos fotos do que stories, cada foto entra em no máximo dois stories, espalhados pelo lote.

## Etapa 3 · Visual de cada story

Escolha uma combinação diferente pra cada story usando `references/kits-visuais.md`. Lá estão as fontes, a paleta, as regras de combinação e 10 combinações já testadas. O resumo:
- no máximo duas fontes por story;
- uma cor dominante por story;
- texto sem caixa atrás só sobre fundo escuro;
- inclinação leve em um ou dois do lote, nunca em todos.

## Etapa 4 · Montar

1. **Escreva o lote em JSON.** O formato está em `references/formato-do-lote.md`; o jeito mais rápido é copiar `assets/exemplo-lote.json` e trocar. **Quebre as linhas à mão** (`\n`): o script calcula a altura de cada bloco pelo número de linhas.
2. **Confira:** `python3 <pasta-da-skill>/scripts/montar.py <lote>.json --checar`. Testa a conexão com o Edits, as fontes, a pasta e as fotos.
3. **Monte:** `python3 <pasta-da-skill>/scripts/montar.py <lote>.json`. Pra cada story, o script:
   - substitui o projeto de mesmo nome, se existir;
   - cria o projeto 9:16 e põe a foto;
   - empilha os blocos a partir do `topo`;
   - desenha a caixinha;
   - põe a chamada perto de 77–80% da altura;
   - exporta o JPG em `<saida>/` e uma prévia pequena em `<saida>/_previa/`.

   (A pasta da skill costuma ser `~/.claude/skills/stories-organicos`.)
4. **Se aparecer `AVISO`** (chamada encostando, texto passando da área segura): tire uma linha, diminua a fonte ou ajuste o `topo`, e refaça só aquele story com `--so <código>`.

## Etapa 5 · Revisar e entregar

- **Abra cada prévia** e confira:
  - texto fora do rosto;
  - nenhum bloco encostando no outro;
  - nada nos 13% de cima (nome do perfil) nem nos 18% de baixo (botão do anúncio);
  - cores certas;
  - emojis aparecendo (emoji composto, como 👩‍🍳, vira outro símbolo).
- **Dê zoom na caixinha**, no JPG grande: `sips -c <altura> <largura> --cropOffset <y> <x> <arquivo> --out <recorte>`. Os quatro cantos precisam estar iguais, sem emenda, com sombra suave.
- **Refaça só o que precisar**, com `--so`.
- **Abra a pasta** pro usuário (`open <saida>`) e mostre uma tabela "story · visual".
- **Atualize o `.md` da copy** com o que mudou na montagem.

## Quando algo não sair como esperado

`references/aprendizados-edits.md` tem tudo que já deu errado e como foi resolvido: cor clareada, raio de forma, texto quebrando sozinho, alinhamento à esquerda, escala da figurinha, porta do servidor. Leia antes de inventar um contorno.
