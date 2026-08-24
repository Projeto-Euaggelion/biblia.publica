# Estrutura do `docs/index.json` (API estática)

Este documento descreve o formato de `docs/index.json`, um índice único de todas as versões do repositório: metadados (copiados de cada `meta.json`, ver [estrutura-meta.md](estrutura-meta.md)) e links diretos para os arquivos de cada formato, pensado para ser consumido por terceiros sem precisar clonar o repositório.

## Geração

`docs/index.json` é gerado automaticamente por [scripts/ci/gerar_index.py](../../scripts/ci/gerar_index.py), disparado pelo workflow [`atualizar-index.yml`](../../.github/workflows/atualizar-index.yml) sempre que um `versoes/{versao}/meta.json` muda na branch principal. **Não edite este arquivo manualmente** — qualquer alteração é sobrescrita na próxima execução. Para corrigir uma informação, altere o `meta.json` da versão correspondente (ou os campos manuais que o originam, ver [estrutura-meta.md](estrutura-meta.md#origem-dos-campos)) e rode `gerar_meta.py` — o índice é atualizado automaticamente no próximo push.

## Objeto raiz

```json
{
  "repository": "https://github.com/Projeto-Euaggelion/biblia.publica",
  "schemas": {
    "json": "https://raw.githubusercontent.com/.../docs/schema/biblia.schema.json",
    "xml": "https://raw.githubusercontent.com/.../docs/schema/biblia.xsd"
  },
  "versions": [ ... ]
}
```

| Campo         | Tipo   | Descrição                                                                 |
|---------------|--------|------------------------------------------------------------------------------|
| `repository`  | string | URL do repositório no GitHub.                                               |
| `schemas`     | object | Links diretos para os schemas formais dos formatos `json`/`xml` (ver [estrutura-json.md](estrutura-json.md) e [estrutura-xml.md](estrutura-xml.md)). |
| `versions`    | array  | Lista de objetos de versão (ver abaixo), uma entrada por versão com `meta.json`. |

## Objeto de versão

Cada entrada de `versions` repete os campos calculados e manuais de `versoes/{versao}/meta.json` (ver [tabela completa em estrutura-meta.md](estrutura-meta.md#objeto-raiz)) e adiciona o campo `formats`:

| Campo              | Tipo             | Descrição                                                                 |
|---------------------|------------------|------------------------------------------------------------------------------|
| `abbrev`            | string           | Sigla da versão, igual ao nome da pasta em `versoes/`.                      |
| `name`              | string ou `null` | Nome oficial completo da versão.                                            |
| `year`              | int, string ou `null` | Ano/intervalo de publicação.                                            |
| `language`          | string ou `null` | Idioma/dialeto, tag BCP 47.                                                 |
| `textualBasis`      | string ou `null` | Base textual da tradução.                                                   |
| `completeness`      | object           | `{ "status": "complete" ou "incomplete", "missingBooks": [...] }`.          |
| `counts`            | object           | `{ "books": int, "chapters": int, "verses": int }`.                         |
| `knownAnomalies`    | array de string  | Peculiaridades conhecidas dos arquivos desta versão.                        |
| `licenseCheckedAt`  | string (data) ou `null` | Data da última verificação da licença.                               |
| `filesHash`         | string           | Hash SHA-256 de `json/`, prefixado com `sha256:`.                           |
| `formats`           | object           | Links diretos para os arquivos desta versão (ver abaixo).                   |

### Objeto `formats`

| Campo     | Sempre presente | Descrição                                                                 |
|-----------|------------------|--------------------------------------------------------------------------|
| `meta`    | Sim              | Link raw para `meta.json`.                                                |
| `license` | Sim              | Link raw para `LICENSE.md`.                                               |
| `xml`     | Sim              | Link para a pasta `xml/` no GitHub (um arquivo por livro, ver [estrutura-xml.md](estrutura-xml.md)). |
| `json`    | Sim              | Link para a pasta `json/` no GitHub (um arquivo por livro, ver [estrutura-json.md](estrutura-json.md)). |
| `sql`     | Não              | Link raw para o `.sqlite` da versão (ver [estrutura-sql.md](estrutura-sql.md)); omitido se a versão ainda não tiver um `.sqlite` gerado. |

Os links de `xml`/`json` apontam para a pasta no GitHub (não para um arquivo raw único), já que cada formato tem um arquivo por livro; `meta`, `license` e `sql` são arquivo único por versão, então apontam direto para o conteúdo raw.

## Observações

- Todos os links usam a branch `main` fixa (`.../main/...`) — refletem sempre o estado mais recente da branch principal, não uma versão/tag específica.
- A ordem de `versions` segue a ordem alfabética das pastas em `versoes/`.
