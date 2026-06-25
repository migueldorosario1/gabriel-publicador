import os
from requests.auth import HTTPBasicAuth


def env_obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"Variavel obrigatoria ausente: {nome}")
    return valor


def wp_base_url() -> str:
    return env_obrigatoria("CAFEZINHO_WP_URL").rstrip("/")


def wp_auth() -> HTTPBasicAuth:
    usuario = env_obrigatoria("CAFEZINHO_WP_USER")
    senha = env_obrigatoria("CAFEZINHO_WP_APP_PASSWORD")
    return HTTPBasicAuth(usuario, senha)


def lista_ids(valor: str | None) -> list[int]:
    if not valor:
        return []
    ids: list[int] = []
    for item in valor.split(","):
        item = item.strip()
        if item:
            ids.append(int(item))
    return ids
