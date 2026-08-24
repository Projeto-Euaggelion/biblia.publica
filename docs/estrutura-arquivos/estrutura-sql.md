# Estrutura do banco SQLite (`estrutura-sql.md`)

Este documento descreve o schema do banco `.sqlite` gerado por versão bíblica, formato alternativo ao par `xml`/`json` (ver [estrutura-xml.md](estrutura-xml.md) e [estrutura-json.md](estrutura-json.md)) pensado para consulta direta via SQL, sem necessidade de carregar e percorrer os arquivos manualmente.

## Localização

Cada versão possui um único arquivo `.sqlite`, gerado por [scripts/json_to_sqlite.py](../../scripts/json_to_sqlite.py) (ver [docs/scripts/gerar-sqlite.md](../scripts/gerar-sqlite.md)), dentro da sua pasta em `versoes/`:

```
versoes/
├── blivre/
│   ├── meta.json
│   ├── LICENSE.md
│   ├── json/
│   ├── xml/
│   └── sql/
│       └── blivre.sqlite
└── etc...
```

## Schema

Três tabelas, refletindo a mesma hierarquia livro → capítulo → versículo dos formatos `xml`/`json`, relacionadas por chave estrangeira:

```sql
CREATE TABLE books (
    id     INTEGER PRIMARY KEY,
    abbrev TEXT NOT NULL UNIQUE,
    name   TEXT NOT NULL
);

CREATE TABLE chapters (
    id      INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    number  INTEGER NOT NULL,
    UNIQUE (book_id, number)
);

CREATE TABLE verses (
    id         INTEGER PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id),
    number     INTEGER NOT NULL,
    text       TEXT NOT NULL,
    UNIQUE (chapter_id, number)
);

CREATE INDEX idx_chapters_book_id ON chapters(book_id);
CREATE INDEX idx_verses_chapter_id ON verses(chapter_id);
```

### Tabela `books`

Um livro por linha, na ordem em que os arquivos `json/` aparecem em ordem alfabética (não necessariamente a ordem canônica do cânon).

| Coluna   | Tipo    | Descrição                                                        |
|----------|---------|--------------------------------------------------------------------|
| `id`     | INTEGER | Chave primária, autoincrementada pelo SQLite.                     |
| `abbrev` | TEXT    | Sigla do livro (ver [tabela de livros](estrutura-xml.md#tabela-de-livros)), única na versão. |
| `name`   | TEXT    | Nome completo do livro em português.                              |

### Tabela `chapters`

| Coluna    | Tipo    | Descrição                                                  |
|-----------|---------|----------------------------------------------------------------|
| `id`      | INTEGER | Chave primária, autoincrementada pelo SQLite.                 |
| `book_id` | INTEGER | Referência a `books.id`.                                       |
| `number`  | INTEGER | Número do capítulo, a partir de `1`; único por `book_id`.      |

### Tabela `verses`

| Coluna       | Tipo    | Descrição                                                     |
|--------------|---------|--------------------------------------------------------------------|
| `id`         | INTEGER | Chave primária, autoincrementada pelo SQLite.                     |
| `chapter_id` | INTEGER | Referência a `chapters.id`.                                        |
| `number`     | INTEGER | Número do versículo, a partir de `1`; único por `chapter_id`.     |
| `text`       | TEXT    | Texto do versículo, em texto plano — mesmo conteúdo do campo `text` de [estrutura-json.md](estrutura-json.md#objeto-de-versículo). |

## Query de exemplo

Buscar o texto de um versículo específico (Gênesis 1:1), a partir da sigla do livro, número do capítulo e número do versículo:

```sql
SELECT v.text
FROM verses v
JOIN chapters c ON c.id = v.chapter_id
JOIN books b ON b.id = c.book_id
WHERE b.abbrev = 'gn' AND c.number = 1 AND v.number = 1;
```

## Observações

- O banco é gerado inteiramente a partir de `versoes/{versao}/json/*.json` — qualquer correção de conteúdo deve ser feita no `.xml`/`.json` correspondente (ver [estrutura-json.md](estrutura-json.md#observações-e-inconsistências-conhecidas)) e o `.sqlite` regenerado com `scripts/json_to_sqlite.py`, nunca editado diretamente.
- `scripts/json_to_sqlite.py` sobrescreve o arquivo `.sqlite` inteiro a cada execução (não faz atualização incremental), garantindo que ele sempre reflita o estado atual de `json/`.
- Não há tabela ou coluna para `meta.json` (contagens, completude, licenciamento, etc.) — o `.sqlite` cobre apenas o texto bíblico; para metadados, consulte `versoes/{versao}/meta.json` (ver [estrutura-meta.md](estrutura-meta.md)).
