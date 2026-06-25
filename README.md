# Publicador Cafezinho

Publicador simples do portal O Cafezinho via WordPress REST API e GitHub Actions.

O objetivo é permitir que Miguel ou Gabriel criem posts pendentes no WordPress do Cafezinho sem expor senhas em chat, código ou tutorial.

## Regra de segurança

Nunca coloque senhas reais no repositório.

As credenciais ficam apenas em GitHub Secrets ou em um arquivo `.env` local que nunca deve ser enviado ao GitHub.

## GitHub Secrets obrigatórios

WordPress:

```text
CAFEZINHO_WP_URL
CAFEZINHO_WP_USER
CAFEZINHO_WP_APP_PASSWORD
CAFEZINHO_WP_AUTHOR_ID
```

Cloudflare R2, para etapa de imagens:

```text
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET
R2_PUBLIC_BASE_URL
```

## Status padrão

O publicador cria posts como `pending`, para revisão antes da publicação final.

## Como testar pelo GitHub Actions

1. Abra o repositório no GitHub.
2. Clique em `Actions`.
3. Escolha o workflow `Publicar no Cafezinho`.
4. Clique em `Run workflow`.
5. Preencha título e conteúdo.
6. Execute.

O workflow deve criar um post pendente no WordPress e mostrar o link no log da execução.

## Padrão editorial

Títulos usam maiúscula apenas na primeira letra e em nomes próprios.

Os textos devem ter parágrafos curtos.

Posts preparados para o Cafezinho devem terminar com:

```text
Categoria (sugestão):
Autor:
Tags:
```

Autor padrão para Gabriel:

```text
5784
```

## Próximas etapas

1. Testar criação de post pendente.
2. Adicionar upload de imagem para o WordPress.
3. Adicionar busca e download de imagens no Cloudflare R2.
4. Criar tutorial final para Gabriel.
