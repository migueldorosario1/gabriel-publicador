from __future__ import annotations

import argparse
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from wordpress.publicar_post import criar_post


def carregar_env() -> None:
    if load_dotenv:
        load_dotenv()


def ler_conteudo(args: argparse.Namespace) -> str:
    if args.content_file:
        return Path(args.content_file).read_text(encoding="utf-8")
    if args.content:
        return args.content
    raise SystemExit("Informe --content ou --content-file")


def main() -> None:
    carregar_env()

    parser = argparse.ArgumentParser(description="Publicador do Cafezinho via WordPress REST API")
    parser.add_argument("--title", required=True, help="Titulo do post")
    parser.add_argument("--content", help="Conteudo HTML ou texto do post")
    parser.add_argument("--content-file", help="Arquivo com o conteudo do post")
    parser.add_argument("--excerpt", default="", help="Resumo opcional")
    parser.add_argument("--status", default=os.getenv("CAFEZINHO_WP_DEFAULT_STATUS", "pending"), help="draft, pending, publish ou future")
    parser.add_argument("--category-ids", default="", help="IDs de categorias separados por virgula")
    parser.add_argument("--tags", default="", help="Tags separadas por virgula")

    args = parser.parse_args()
    conteudo = ler_conteudo(args)

    post = criar_post(
        titulo=args.title,
        conteudo=conteudo,
        excerpt=args.excerpt or None,
        status=args.status,
        category_ids=args.category_ids or None,
        tags=args.tags or None,
    )

    print("Post criado com sucesso")
    print(f"ID: {post.get('id')}")
    print(f"Status: {post.get('status')}")
    print(f"Link: {post.get('link')}")


if __name__ == "__main__":
    main()
