#!/usr/bin/env python3
"""Desenha o FUNDO da caixinha de pergunta (sem texto) como PNG transparente, só com Python (sem instalar nada).

Cartão único com os quatro cantos iguais, faixa colorida recortada no topo e sombra suave. O Edits não consegue
fazer isso com as formas dele (o raio cresce com a altura e não há desfoque), por isso o fundo vem pronto em PNG
e entra como figurinha; os textos vão por cima no Edits, com a fonte do Instagram.

Uso direto:  python3 caixinha.py saida.png "#262626" 950 112 300 [34]
(largura, altura da faixa, altura do corpo e raio em pixels do quadro do Edits, 1440 x 2560)
"""
import math, struct, sys, zlib

PAD = 70  # folga em volta pra sombra


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _sdf(px, py, cx, cy, hw, hh, r):
    """Distância com sinal até um retângulo de cantos arredondados (negativa = dentro)."""
    qx = abs(px - cx) - (hw - r)
    qy = abs(py - cy) - (hh - r)
    fora = math.hypot(max(qx, 0.0), max(qy, 0.0))
    return fora + min(max(qx, qy), 0.0) - r


def _sombra(d, sigma):
    """Borda desfocada por uma gaussiana (como o box-shadow do navegador): 50% em cima da borda, some pra fora."""
    return 0.5 * math.erfc(d / (sigma * math.sqrt(2)))


def desenhar(saida, cor_faixa, w, hf, hc, raio=34):
    W, H = w + 2 * PAD, hf + hc + 2 * PAD
    cx, cy, hw, hh = W / 2, H / 2, w / 2, (hf + hc) / 2
    fr, fg, fb = _hex(cor_faixa)
    topo_corpo = PAD + hf
    linhas = []
    for y in range(H):
        py = y + 0.5
        linha = bytearray([0])  # filtro PNG "none"
        for x in range(W):
            px = x + 0.5
            d = _sdf(px, py, cx, cy, hw, hh, raio)
            a_card = min(max(0.5 - d, 0.0), 1.0)
            # sombra: uma larga e difusa + uma curta e mais escura (desfoque aproximado pela distância)
            s1 = 0.28 * _sombra(_sdf(px, py - 10, cx, cy, hw, hh, raio), 18.0)
            s2 = 0.12 * _sombra(_sdf(px, py - 2, cx, cy, hw, hh, raio), 3.0)
            a_s = 1 - (1 - s1) * (1 - s2)
            if a_card >= 1.0:
                r, g, b = (fr, fg, fb) if py < topo_corpo else (255, 255, 255)
                linha += bytes((r, g, b, 255))
                continue
            a = a_card + a_s * (1 - a_card)
            if a <= 0:
                linha += b"\x00\x00\x00\x00"
                continue
            r, g, b = (fr, fg, fb) if py < topo_corpo else (255, 255, 255)
            k = a_card / a  # sombra é preta: só o cartão contribui com cor
            linha += bytes((round(r * k), round(g * k), round(b * k), round(a * 255)))
        linhas.append(bytes(linha))

    def bloco(tipo, dados):
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + bloco(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
    png += bloco(b"IDAT", zlib.compress(b"".join(linhas), 9)) + bloco(b"IEND", b"")
    with open(saida, "wb") as fh:
        fh.write(png)
    return W, H


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 5:
        sys.exit(__doc__)
    print(desenhar(a[0], a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]) if len(a) > 5 else 34))
