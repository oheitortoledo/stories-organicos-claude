# Formato do lote (o JSON que o `montar.py` lê)

Exemplo completo: `assets/exemplo-lote.json`. Copie e troque.

```json
{
  "pasta_fotos": "~/Movies/<LOTE>",               // tem que estar dentro de ~/Movies (o Edits só lê lá)
  "saida": "~/Movies/<LOTE>/prontos",             // opcional; padrão = <pasta_fotos>/prontos
  "prefixo": "<OFERTA>_PACK<N>_IMG_",             // nome do projeto no Edits e do JPG = prefixo + código
  "fotos": {
    "01": {"arquivo": "01-....jpg", "topo": 0.40}  // topo = onde o texto pode começar (fração da altura, abaixo do queixo)
  },
  "stories": {
    "062": {
      "foto": "01",
      "topo": 0.445,                               // opcional: sobrescreve o topo da foto só neste story
      "gap": 0.012,                                // opcional: espaço entre blocos (padrão 0.018)
      "blocos": [ BLOCO, BLOCO ],                  // de cima pra baixo; o script empilha a partir do topo
      "cta": BLOCO_DE_TEXTO                        // a chamada; fica perto de 0.77–0.80 da altura
    }
  }
}
```

## Bloco de texto

| Campo | O que é | Padrão |
|---|---|---|
| `texto` | o texto, com `\n` onde a linha quebra. **Quebre à mão**: o script calcula a altura pelo número de linhas | obrigatório |
| `fonte` | apelido: `CLASSIC`, `CLASSIC_H`, `CLASSIC_L`, `MODERN`, `MODERN_R`, `EDITOR`, `POSTER`, `SQUEEZE`, `SIGNATURE`, `BUBBLE`, `DECO` (ou o nome PostScript) | `CLASSIC` |
| `tam` | tamanho em pontos do Edits. Gancho 25–30 · meio 18–22 · chamada 17–19 | 22 |
| `cor` | cor do texto: nome da paleta (`branco`, `preto`, `amarelo`, `verde`, `azul`, `vermelho`, `laranja`, `roxo`, `grafite`) ou hex | `branco` |
| `caixa` | cor da caixa atrás do texto (mesmos nomes). Sem `caixa` = texto solto | sem caixa |
| `estilo` | `backgroundPill` (caixa) ou `outline` (contorno na cor de `caixa`) | `backgroundPill` |
| `alinhar` | `center` ou `left` (lista) | `center` |
| `rot` | inclinação em graus (−3 a 3 dá cara de feito à mão) | 0 |
| `lh` | altura de linha forçada (fração da altura do quadro), pra fonte que foge da conta (ex.: `SIGNATURE` 26 → 0.062) | calculada |

## Bloco de caixinha de pergunta

```json
{"tipo": "pergunta", "convite": "Me faça uma pergunta", "pergunta": "serve pra quem\nnunca fez bolo?", "faixa": "grafite", "tam": 20}
```

- `convite`: o texto da faixa colorida (o que o especialista escreveu na figurinha). Curto, sem emoji com junção (👩‍🍳 vira outro símbolo).
- `pergunta`: a pergunta "do seguidor", 2 linhas de até ~20 caracteres.
- `faixa`: cor da faixa (grafite, laranja, roxo, azul...).
- `tam`: 19–20. Ocupa ~0,17 da altura com 2 linhas.

## Quanto cabe

A área útil vai do `topo` da foto (abaixo do queixo, ~0,40–0,47) até ~0,82 (o botão "Saiba mais" cobre o resto). Isso dá ~0,36–0,42 da altura pra tudo. Conta rápida, por linha: `CLASSIC` 26 ≈ 0,054 · `CLASSIC` 20 ≈ 0,042 · `MODERN` 20 ≈ 0,048 · `EDITOR` 17 ≈ 0,041 · `SQUEEZE` 28 ≈ 0,062. Se o script avisar que a chamada encostou, corte uma linha, diminua a fonte ou suba o `topo` (sem cobrir o rosto).

Larguras: em `CLASSIC` 26 cabem ~22 caracteres por linha; em `MODERN` 20, ~42; em `EDITOR` 17, ~28 (é larga, monoespaçada).
