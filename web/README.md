# web/

Interface web simples (HTML/CSS/JS puro, sem build step nem framework) para explorar as versões e ler capítulos sem clonar o repositório. Publicada via GitHub Pages em [biblia.euaggelion.com.br](https://biblia.euaggelion.com.br/) a partir desta pasta pelo workflow [`deploy-pages.yml`](../.github/workflows/deploy-pages.yml), disparado a cada push em `web/**` na branch principal.

## Como funciona

- `CNAME` — domínio customizado (`biblia.euaggelion.com.br`). Como o deploy é feito via GitHub Actions (não a partir de uma branch), o GitHub não escreve/mantém esse arquivo sozinho — precisa estar versionado aqui dentro de `web/` pra ir junto no artefato publicado a cada deploy. Exige um registro CNAME no DNS apontando `biblia.euaggelion.com.br` para `projeto-euaggelion.github.io`, configurado fora do repositório (ver [Config do domínio customizado](#config-do-domínio-customizado) abaixo).
- `index.html` — casca da página (cabeçalho, breadcrumb, `<main id="app">`, rodapé), com o `<link>` para as fontes do Google Fonts.
- `css/style.css` — estilos, sem framework externo (variáveis de cor/tipografia no `:root`).
- `js/api.js` — busca `docs/index.json` e os `.json` de cada livro direto de `raw.githubusercontent.com/Projeto-Euaggelion/biblia.publica/main/...` (nenhum dado é duplicado dentro de `web/`).
- `js/books.js` — tabela estática dos 66 livros do cânon protestante (sigla/nome/testamento/número de capítulos), usada só para montar a navegação (posição do livro, contagem de capítulos sem precisar buscar todos os `.json` da versão) — o texto sempre vem do `.json` real da versão.
- `js/app.js` — roteamento por hash (`#/{versao}`, `#/{versao}/{abbrev}`, `#/{versao}/{abbrev}/{capitulo}`) e renderização das telas.

Não há chamada a nenhuma API do GitHub além do conteúdo raw — sem autenticação, sem limite de taxa relevante para uso normal.

A única dependência externa é a tipografia: `index.html` carrega as fontes **Fraunces** (serifa display, títulos) e **Inter** (interface) via `fonts.googleapis.com`/`fonts.gstatic.com`. Sem build step — é só um `<link>` no `<head>`.

## Rodando localmente

Como `js/app.js` é carregado como módulo ES (`<script type="module">`), abrir `index.html` direto do disco (`file://`) não funciona — o navegador bloqueia módulos por CORS nesse protocolo. Sirva a pasta por HTTP:

```bash
python -m http.server 8420 --directory web
```

E abra `http://localhost:8420`. Os dados (versões, livros) continuam vindo do `raw.githubusercontent.com` da branch `main` real — não há como testar localmente contra dados ainda não commitados/enviados sem apontar `js/api.js` para outro branch/fork temporariamente.

## Escopo atual

Navegação somente leitura: lista de versões (a partir de `docs/index.json`, ver [#15](https://github.com/Projeto-Euaggelion/biblia.publica/issues/15)) → lista de livros → capítulo com versículos. Busca por referência, comparação entre versões e outras funcionalidades ficam para issues futuras.

## Config do domínio customizado

O arquivo `CNAME` nesta pasta só resolve a metade do trabalho (diz ao GitHub Pages qual domínio aceitar). Pra `biblia.euaggelion.com.br` funcionar de verdade, quem administra o DNS de `euaggelion.com.br` precisa, fora deste repositório:

1. Criar um registro `CNAME` para o subdomínio `biblia` apontando para `projeto-euaggelion.github.io` (o apex `euaggelion.com.br` não muda).
2. Em Settings → Pages do repositório, confirmar que o campo **Custom domain** está com `biblia.euaggelion.com.br` (o GitHub detecta o arquivo `CNAME` publicado, mas pode levar um deploy pra refletir) e, depois que o DNS propagar e o certificado for emitido, marcar **Enforce HTTPS**.

Sem o registro DNS, o `CNAME` sozinho não publica nada — a URL continua resolvendo (ou falhando) conforme o domínio estiver ou não apontado.
