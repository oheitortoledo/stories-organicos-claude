#!/usr/bin/env python3
"""Monta anúncios de story com cara orgânica no Edits (app de vídeo da Meta) a partir de um lote em JSON.

Cada story vira um projeto 9:16 no Edits (nome = código do criativo) e um JPG 1080 x 1920.
Fala só com o servidor local do Edits (127.0.0.1): nada sai do seu computador.
Não precisa instalar nada além do Python 3 que já vem no Mac.

Uso:
  python3 montar.py lote.json                 # monta todos
  python3 montar.py lote.json --so 03 07      # só esses (refaz: substitui o projeto de mesmo nome)
  python3 montar.py lote.json --checar        # confere conexão, fontes, pasta e fotos sem montar

Conexão com o Edits, nesta ordem:
  1. variáveis EDITS_MCP_URL e EDITS_MCP_TOKEN
  2. o cadastro "edits" do Claude Code em ~/.claude.json (feito pelo botão "Add Edits to Claude Code")
  3. um .mcp.json na pasta atual
"""
import argparse, base64, json, os, sys, time, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import caixinha  # noqa: E402

FONTES = {
    "CLASSIC": "IGUIBetav9-Bold",               # Classic Medium: o texto padrão de story
    "CLASSIC_H": "IGUIBetav9-Heavy",            # Classic: mais grosso, pra gancho
    "CLASSIC_L": "IGUIBetav9-Regular",          # Classic Light
    "MODERN": "InstagramSansCondensed-Bold",    # Modern Bold: condensada
    "MODERN_R": "IGSansCondensedGlobal-Regular",
    "EDITOR": "InstagramEditor-Regular",        # máquina de escrever (larga)
    "POSTER": "InstagramPoster-Black",          # serifa pesada
    "SQUEEZE": "InstagramSqueeze-Black",        # caixa alta condensada
    "SIGNATURE": "InstagramSignature-Regular",  # manuscrita
    "BUBBLE": "InstagramBubble-Black",
    "DECO": "InstagramDeco-Regular",
}
CORES = {
    "branco": "#FFFFFF", "preto": "#000000", "grafite": "#262626",
    "amarelo": "#FDCB5C", "verde": "#70C050", "azul": "#3897F0", "vermelho": "#ED4956",
    "laranja": "#FD8D32", "roxo": "#A307BA", "rosa": "#D10869",
}
# altura de uma linha por ponto de fonte, em fração da altura do quadro (medida no Edits, quadro 1440 x 2560)
FATOR_LINHA = {"MODERN": 0.0024, "MODERN_R": 0.0024, "SQUEEZE": 0.0022, "POSTER": 0.0023, "EDITOR": 0.0024}
FATOR_PADRAO = 0.00208
QW, QH = 1440, 2560
AREA_FIM = 0.80   # centro máximo da chamada; o botão "Saiba mais" do anúncio cobre os ~18% de baixo
GAP = 0.018


# ---------------------------------------------------------------- conexão
def _de_mcp(e):
    if e and e.get("url"):
        return e["url"], (e.get("headers") or {}).get("Authorization", "")
    return None


def _conexao():
    if os.environ.get("EDITS_MCP_URL"):
        tok = os.environ.get("EDITS_MCP_TOKEN", "")
        return os.environ["EDITS_MCP_URL"], ("" if not tok else tok if tok.startswith("Bearer ") else "Bearer " + tok)
    cfg_path = os.path.expanduser("~/.claude.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path))
        achou = _de_mcp((cfg.get("mcpServers") or {}).get("edits"))
        if achou:
            return achou
        for proj in (cfg.get("projects") or {}).values():
            achou = _de_mcp((proj.get("mcpServers") or {}).get("edits"))
            if achou:
                return achou
    if os.path.exists(".mcp.json"):
        achou = _de_mcp((json.load(open(".mcp.json")).get("mcpServers") or {}).get("edits"))
        if achou:
            return achou
    sys.exit("Não achei a conexão com o Edits. No app: Ajustes > Automação > ligar, e rodar no Terminal o comando do "
             "botão \"Add Edits to Claude Code\" (passo a passo no README).")


URL, AUTH = None, None
_id = [0]


def call(nome, args=None):
    global URL, AUTH
    if URL is None:
        URL, AUTH = _conexao()
    _id[0] += 1
    corpo = json.dumps({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
                        "params": {"name": nome, "arguments": args or {}}}).encode()
    req = urllib.request.Request(URL, data=corpo, headers={
        "Authorization": AUTH, "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2025-06-18"})
    try:
        bruto = urllib.request.urlopen(req, timeout=120).read().decode()
    except Exception as ex:
        sys.exit(f"O Edits não respondeu em {URL} ({ex}). O app está aberto e com Ajustes > Automação ligada? "
                 "Se você fechou e abriu o app, a porta pode ter mudado: refaça o cadastro (README).")
    if bruto.startswith(("event:", "data:")):
        bruto = "\n".join(l[5:].strip() for l in bruto.splitlines() if l.startswith("data:"))
    msg = json.loads(bruto)
    if "error" in msg:
        raise RuntimeError(f"{nome}: {msg['error']}")
    res = msg["result"]
    texto, imagens = {}, []
    for c in res.get("content", []):
        if c.get("type") == "text":
            try:
                texto = json.loads(c["text"])
            except ValueError:
                texto = {"raw": c["text"]}
        elif c.get("type") == "image":
            imagens.append(base64.b64decode(c["data"]))
    if res.get("isError") or texto.get("ok") is False:
        raise RuntimeError(f"{nome}: {texto}")
    return texto, imagens


def esperar_editor():
    for _ in range(40):
        st, _ = call("appState")
        if st.get("screen") == "editor":
            return
        time.sleep(0.5)
    raise RuntimeError("o editor do Edits não abriu")


def ir_pra_home():
    st, _ = call("appState")
    if st.get("screen") == "editor":
        call("closeProject")


# ---------------------------------------------------------------- utilidades
def cor(v):
    return CORES.get(str(v).lower(), v)


def comp(h, g=2.2):
    """O Edits clareia a cor de caixa, forma e PNG. Escurece na entrada pra sair a cor pedida."""
    h = cor(h).lstrip("#")
    v = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return "#" + "".join(f"{round((c ** g) * 255):02X}" for c in v)


def fonte(apelido):
    return FONTES.get(apelido, apelido)


def altura_texto(b):
    n = b["texto"].count("\n") + 1
    return n * (b.get("lh") or b.get("tam", 22) * FATOR_LINHA.get(b.get("fonte", "CLASSIC"), FATOR_PADRAO))


# ---------------------------------------------------------------- blocos
def por_texto(b, y_centro):
    r, _ = call("addText", {"text": b["texto"], "atSeconds": 0, "duration": 3})
    i = r["id"]
    call("setTextFont", {"id": i, "family": fonte(b.get("fonte", "CLASSIC"))})
    estilo = b.get("estilo", "backgroundPill") if b.get("caixa") else "none"
    if estilo != "none":
        c = cor(b["caixa"]) if estilo in ("outline", "invertedOutline") else comp(b["caixa"])
        call("setEmphasis", {"id": i, "style": estilo, "color": c})
    alinhar = b.get("alinhar", "center")
    call("setTextStyle", {"id": i, "color": cor(b.get("cor", "branco")), "size": b.get("tam", 22),
                          "alignment": alinhar, "boxWidth": 0.95 if alinhar == "center" else 0.80})
    call("setTextPosition", {"id": i, "x": 0.5, "y": round(y_centro, 4)})  # posição = centro da caixa de texto
    if b.get("rot"):
        call("setTransform", {"id": i, "rotationDegrees": b["rot"]})
    return i


def por_pergunta(b, y0, cod, pasta_stickers):
    """Resposta da caixinha de pergunta compartilhada no story: fundo em PNG (figurinha) + textos no Edits."""
    W, HF, PADV, RAIO = 950, 112, 58, 34     # px do quadro 1440 x 2560; cartão = 66% da largura
    ESCALA = 2.458                           # PNG de 1090 px de largura: 1 px do PNG = 1 px do quadro
    tam = b.get("tam", 20)
    linha = round(tam * FATOR_PADRAO * QH)
    n = b["pergunta"].count("\n") + 1
    HC = n * linha + 2 * PADV
    os.makedirs(pasta_stickers, exist_ok=True)
    png = os.path.join(pasta_stickers, f"caixinha-{cod}.png")
    caixinha.desenhar(png, comp(b.get("faixa", "grafite")), W, HF, HC, RAIO)
    h = (HF + HC) / QH
    r, _ = call("addSticker", {"path": png, "sticker": f"caixinha-{cod}", "atSeconds": 0, "duration": 3})
    call("setTransform", {"id": r["id"], "x": 0.5, "y": round(y0 + h / 2, 4), "scale": ESCALA})
    r, _ = call("addText", {"text": b["convite"], "atSeconds": 0, "duration": 3})
    call("setTextFont", {"id": r["id"], "family": FONTES["CLASSIC"]})
    call("setTextStyle", {"id": r["id"], "color": "#FFFFFF", "size": 15})
    call("setTextPosition", {"id": r["id"], "x": 0.5, "y": round(y0 + HF / 2 / QH, 4)})
    r, _ = call("addText", {"text": b["pergunta"], "atSeconds": 0, "duration": 3})
    call("setTextFont", {"id": r["id"], "family": FONTES["CLASSIC"]})
    call("setTextStyle", {"id": r["id"], "color": "#000000", "size": tam})
    call("setTextPosition", {"id": r["id"], "x": 0.5, "y": round(y0 + (HF + HC / 2) / QH, 4)})
    return h


# ---------------------------------------------------------------- montagem
def apagar_projeto(nome):
    p, _ = call("projects")
    for pr in p.get("projects", []):
        if pr["name"] == nome:
            call("deleteProject", {"id": pr["id"]})


def montar(lote, cod, base):
    s = lote["stories"][cod]
    foto = lote["fotos"][s["foto"]]
    nome = f'{lote.get("prefixo", "STORY_")}{cod}'
    saida = os.path.expanduser(lote.get("saida", os.path.join(base, "prontos")))
    previa = os.path.join(saida, "_previa")
    os.makedirs(previa, exist_ok=True)

    ir_pra_home()
    apagar_projeto(nome)                    # refazer substitui, nunca duplica
    call("newProject")
    esperar_editor()
    call("setTitle", {"name": nome})
    call("setAspectRatio", {"ratio": "9:16"})
    m, _ = call("addMedia", {"path": os.path.join(base, foto["arquivo"])})
    call("setTransform", {"id": m["id"], "fitMode": "fill"})

    y = s.get("topo", foto.get("topo", 0.42))
    gap = s.get("gap", GAP)
    for b in s["blocos"]:
        if b.get("tipo") == "pergunta":
            y += por_pergunta(b, y, cod, os.path.join(base, "stickers")) + gap
        else:
            h = altura_texto(b)
            por_texto(b, y + h / 2)
            y += h + gap
    avisos = []
    c = s.get("cta")
    if c:
        h = altura_texto(c)
        yc = min(max(0.77, y + 0.03 + h / 2), AREA_FIM)
        if yc - h / 2 < y - gap + 0.004:
            avisos.append("a chamada encosta no bloco de cima: tire uma linha, diminua a fonte ou suba o 'topo'")
        por_texto(c, yc)
    elif y > AREA_FIM + 0.02:
        avisos.append("o texto passa da área segura de baixo")

    _, imgs = call("captureFrame", {"atSeconds": 1, "maxWidth": 1080})
    arq = os.path.join(saida, f"{nome}.jpg")
    with open(arq, "wb") as fh:
        fh.write(imgs[0])
    _, prev = call("captureFrame", {"atSeconds": 1, "maxWidth": 360})
    with open(os.path.join(previa, f"{cod}.jpg"), "wb") as fh:
        fh.write(prev[0])
    call("saveProject")
    call("closeProject")
    print(f"{cod} ok  {arq}" + "".join(f"\n   AVISO: {a}" for a in avisos), flush=True)


def checar(lote, base):
    st, _ = call("appState")
    print("ok  Edits respondendo (tela:", st.get("screen") + ")")
    faltam = []
    for apelido, nome in FONTES.items():
        r, _ = call("listFonts", {"query": nome, "limit": 5})
        if not any(f.get("name") == nome for f in r.get("fonts", [])):
            faltam.append(f"{apelido} ({nome})")
    print("ok  fontes do Instagram" if not faltam else "AVISO: fontes que esta versão do Edits não tem: " + ", ".join(faltam))
    if not os.path.realpath(base).startswith(os.path.realpath(os.path.expanduser("~/Movies"))):
        print("ERRO: a pasta das fotos precisa estar dentro de ~/Movies (Filmes); o Edits não lê fora dela")
    for k, f in lote["fotos"].items():
        p = os.path.join(base, f["arquivo"])
        print(("ok  " if os.path.exists(p) else "FALTA ") + f"foto {k}: {p}")
    for cod, s in lote["stories"].items():
        if s["foto"] not in lote["fotos"]:
            print(f"FALTA: o story {cod} usa a foto {s['foto']}, que não está em 'fotos'")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Monta stories orgânicos no Edits a partir de um lote em JSON.")
    ap.add_argument("lote")
    ap.add_argument("--so", nargs="*", help="só estes códigos")
    ap.add_argument("--checar", action="store_true", help="só confere, não monta")
    a = ap.parse_args()
    lote = json.load(open(a.lote, encoding="utf-8"))
    base = os.path.expanduser(lote["pasta_fotos"])
    if a.checar:
        checar(lote, base)
        sys.exit(0)
    for cod in (a.so or list(lote["stories"])):
        montar(lote, cod, base)
    ir_pra_home()
