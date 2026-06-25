from __future__ import annotations

import os
import re
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from wordpress.publicar_post import criar_post
from wordpress.upload_media import enviar_midia_por_url


def carregar_env() -> None:
    if load_dotenv:
        load_dotenv()


def extrair_campo(cabecalho: str, nome: str, padrao: str = "") -> str:
    regex = rf"^{re.escape(nome)}:\s*(.*)$"
    for linha in cabecalho.splitlines():
        achou = re.match(regex, linha.strip())
        if achou:
            return achou.group(1).strip().strip('"').strip("'")
    return padrao


def montar_url_r2(r2_key: str) -> str:
    base = os.getenv("R2_PUBLIC_BASE_URL", "").rstrip("/")
    if not base:
        raise RuntimeError("R2_PUBLIC_BASE_URL ausente")
    return f"{base}/{r2_key.lstrip('/')}"


def ler_post(caminho: str) -> dict:
    texto = Path(caminho).read_text(encoding="utf-8")

    if texto.startswith("---"):
        partes = texto.split("---", 2)
        cabecalho = partes[1]
        corpo = partes[2].strip()
    else:
        cabecalho = ""
        corpo = texto.strip()

    titulo = extrair_campo(cabecalho, "title")
    if not titulo:
        primeira_linha = corpo.splitlines()[0].strip() if corpo else "Post sem titulo"
        titulo = primeira_linha.replace("#", "").strip() or "Post sem titulo"

    return {
        "titulo": titulo,
        "conteudo": corpo,
        "excerpt": extrair_campo(cabecalho, "excerpt"),
        "status": extrair_campo(cabecalho, "status", "pending"),
        "category_ids": extrair_campo(cabecalho, "category_ids"),
        "tags": extrair_campo(cabecalho, "tags"),
        "image_url": extrair_campo(cabecalho, "image_url"),
        "r2_key": extrair_campo(cabecalho, "r2_key"),
        "image_alt": extrair_campo(cabecalho, "image_alt"),
        "image_caption": extrair_campo(cabecalho, "image_caption"),
    }


def resolver_imagem(dados: dict) -> int | None:
    url = dados.get("image_url") or ""
    r2_key = dados.get("r2_key") or ""

    if not url and r2_key:
        url = montar_url_r2(r2_key)

    if not url:
        return None

    print(f"Enviando imagem destacada: {url}")
    return enviar_midia_por_url(
        url,
        alt_text=dados.get("image_alt") or "",
        caption=dados.get("image_caption") or "",
    )


def main() -> None:
    carregar_env()
    dados = ler_post("posts/entrada.md")

    featured_media = resolver_imagem(dados)

    post = criar_post(
        titulo=dados["titulo"],
        conteudo=dados["conteudo"],
        excerpt=dados["excerpt"] or None,
        status=dados["status"] or "pending",
        category_ids=dados["category_ids"] or None,
        tags=dados["tags"] or None,
        featured_media=featured_media,
    )

    print("Post criado com sucesso")
    print(f"ID: {post.get('id')}")
    print(f"Status: {post.get('status')}")
    print(f"Link: {post.get('link')}")


if __name__ == "__main__":
    main()
