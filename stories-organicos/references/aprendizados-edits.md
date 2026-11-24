# O que se aprendeu montando no Edits

Tudo aqui foi descoberto na prática, montando um lote real de stories de venda (testado no Edits 457 para Mac, nov/2026). O `montar.py` já resolve cada ponto; isto é pra quando algo sair do esperado, ou se uma versão nova do Edits mudar o comportamento.

## Conexão

- O Edits (app de vídeo da Meta) tem servidor MCP próprio: **Ajustes > Automação** liga o servidor e mostra a chave de acesso e o botão "Add Edits to Claude Code". O comando que ele copia é `claude mcp add --transport http --scope user edits http://127.0.0.1:<porta>/mcp --header "Authorization: Bearer <chave>"`. Fica salvo no `~/.claude.json` (`mcpServers.edits`), de onde o script lê.
- O servidor só existe com o app aberto e a automação ligada. **A porta pode mudar ao reabrir o app**: se o script não conectar, compare a porta da aba Automação com a do cadastro e refaça (`claude mcp remove edits -s user` + o comando novo).
- As ferramentas mudam com a tela: na tela inicial só aparecem as de projeto (abrir, criar, apagar); as de edição (texto, figurinha, exportar) só com um projeto aberto. Por isso o script abre o projeto antes de editar.
- A chave dá controle dos projetos do Edits, mas o servidor só aceita conexão do próprio computador (127.0.0.1). Não compartilhe a chave.

## Arquivos

- **O Edits só lê arquivos dentro de `~/Movies` (Filmes)**, ou escolhidos à mão no app. Foto e figurinha PNG vão pra `~/Movies/<lote>/`. Não use a pasta `~/Movies/Edits/`, que é a biblioteca do app.
- Foto com rotação no EXIF (6000 × 4000 deitada, mas vertical de verdade) entra na orientação certa.
- `addMedia` coloca a foto com 3 s; `setTransform fitMode=fill` preenche o 9:16 cortando as laterais (foto 2:3 vira 9:16 sem cortar em cima nem embaixo).
- O quadro 9:16 do Edits é 1440 × 2560. `captureFrame maxWidth=1080` devolve o JPG 1080 × 1920 da composição exata: é assim que a imagem é "exportada" (o `export` do Edits só faz vídeo).

## Texto

- `setTextPosition` posiciona o **centro da caixa de texto**. Pra alinhar à esquerda, deixe x = 0,5 e estreite a caixa (`boxWidth` 0,80); mover o x pra esquerda joga o texto pra fora da tela.
- Quebre as linhas à mão (`\n`) e use `boxWidth` 0,95: com a largura padrão (0,835) o Edits quebra sozinho no meio da frase e o texto invade o bloco de baixo.
- Caixa atrás do texto = `setEmphasis backgroundPill` com a cor; contorno = `outline`. `invertedBackgroundPill` troca texto e caixa.
- Emoji composto (👩‍🍳, 🧑‍🍳) aparece como outro símbolo. Emoji simples (🖤 🎄 😉 🥹 👇 🍰 🎂 🍫) funciona.

## Cor

- **O Edits clareia a cor de caixa, de forma e de PNG** (trata o hex como linear): vermelho #ED4956 sai salmão, grafite #262626 sai cinza. A compensação que funcionou é elevar cada canal a 2,2 antes de mandar (`comp()` no script). Branco e preto não mudam. Contorno (`outline`) não precisa.
- A foto não é afetada.
- O rosa (#D10869) sai puxado pro vermelho mesmo compensado.

## Formas e caixinha de pergunta

- `addShape` gera um PNG e põe como figurinha. **O raio do canto cresce com a altura da forma**, e não há como arredondar só alguns cantos nem desfocar sombra. Uma caixinha montada com três formas empilhadas sai com a parte branca oval, emenda na faixa e sombra dura (foi reprovada no primeiro teste).
- Solução: o fundo da caixinha é um PNG desenhado em Python puro (`scripts/caixinha.py`, sem instalar nada), com cartão único, os quatro cantos iguais, faixa recortada e sombra desfocada. Entra com `addSticker`, e os textos vão por cima no Edits, com a fonte do Instagram.
- `addSticker` aceita PNG, WebP ou GIF (JPEG não). Na escala 1 a figurinha fica pequena: com o PNG de 1090 px de largura, **escala 2,458 = 1 px do PNG por 1 px do quadro**. Se mudar a largura do PNG, refaça a conta (na escala 1, a largura exibida é ~0,308 da largura do quadro pra 1090 px).
- A caixinha é uma réplica. A figurinha nativa do Instagram só existe postando pelo app. Se alguém quiser a 100% oficial: o especialista posta a caixinha, responde, compartilha e manda o print.

## Projetos

- Um projeto por story, com o nome do código (`setTitle`). Ao refazer, apague o projeto de mesmo nome antes (`deleteProject`), senão a biblioteca fica com duplicatas. O script faz isso.
- `saveProject` antes de `closeProject`.
