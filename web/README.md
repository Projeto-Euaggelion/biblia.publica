# web/

Interface web simples (HTML/CSS/JS puro, sem build step nem framework) para explorar as versões e ler capítulos sem clonar o repositório. Publicada via GitHub Pages a partir desta pasta pelo workflow [`deploy-pages.yml`](../.github/workflows/deploy-pages.yml), disparado a cada push em `web/**` na branch principal.

## Como funciona

- `index.html` — casca da página (cabeçalho, breadcrumb, `<main id="app">`).
- `css/style.css` — estilos, sem framework externo.
- `js/api.js` — busca `docs/index.json` e os `.json` de cada livro direto de `raw.githubusercontent.com/Projeto-Euaggelion/biblia.publica/main/...` (nenhum dado é duplicado dentro de `web/`).
- `js/books.js` — tabela estática dos 66 livros do cânon protestante (sigla/nome/testamento), usada só para montar a navegação — o texto sempre vem do `.json` real da versão.
- `js/app.js` — roteamento por hash (`#/{versao}`, `#/{versao}/{abbrev}`, `#/{versao}/{abbrev}/{capitulo}`) e renderização das telas.

Não há chamada a nenhuma API do GitHub além do conteúdo raw — sem autenticação, sem limite de taxa relevante para uso normal.

## Rodando localmente

Como `js/app.js` é carregado como módulo ES (`<script type="module">`), abrir `index.html` direto do disco (`file://`) não funciona — o navegador bloqueia módulos por CORS nesse protocolo. Sirva a pasta por HTTP:

```bash
python -m http.server 8420 --directory web
```

E abra `http://localhost:8420`. Os dados (versões, livros) continuam vindo do `raw.githubusercontent.com` da branch `main` real — não há como testar localmente contra dados ainda não commitados/enviados sem apontar `js/api.js` para outro branch/fork temporariamente.

## Escopo atual

Navegação somente leitura: lista de versões (a partir de `docs/index.json`, ver [#15](https://github.com/Projeto-Euaggelion/biblia.publica/issues/15)) → lista de livros → capítulo com versículos. Busca por referência, comparação entre versões e outras funcionalidades ficam para issues futuras.
