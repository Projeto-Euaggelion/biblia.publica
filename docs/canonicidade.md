# Canonicidade por versão

Este documento indica, para cada versão bíblica do repositório, qual cânon ela segue e se inclui livros deuterocanônicos. Ele existe porque `completeness`/`missingBooks` do `meta.json` ([estrutura-meta.md](estrutura-arquivos/estrutura-meta.md#objeto-completeness)) só comparam os arquivos da versão contra o cânon protestante de 66 livros — não distinguem "faltam livros" de "a versão segue outro cânon". Esta tabela é a referência manual para essa distinção.

## Cânones de referência

| Cânon | Livros | Descrição |
|-------|--------|-----------|
| **Protestante** | 66 (39 AT + 27 NT) | Sem deuterocanônicos. É o cânon usado pela [tabela de livros](estrutura-arquivos/estrutura-xml.md#tabela-de-livros) e pelas siglas padronizadas do projeto. |
| **Católico** | 73 (46 AT + 27 NT) | Acrescenta 7 livros deuterocanônicos ao Antigo Testamento — Tobias, Judite, 1 Macabeus, 2 Macabeus, Sabedoria, Eclesiástico (Sirácida) e Baruque — além de trechos adicionais em Ester e Daniel. |
| **Outro** | variável | Cânones ortodoxos e demais tradições incluem ainda outros livros (ex.: 1 Esdras, 3 Macabeus, Salmo 151); nenhuma versão do repositório se enquadra aqui até o momento. |

## Tabela de canonicidade

| Versão | Cânon | Livros presentes | Deuterocanônicos | Observação |
|--------|-------|-------------------|-------------------|------------|
| `alm1911` | Protestante | 66/66 | Nenhum | — |
| `blivre` | Protestante | 66/66 | Nenhum | — |
| `nt-a1819a` | Protestante | 27/66 | Nenhum | Apenas o Novo Testamento disponível na fonte; os 39 livros do Antigo Testamento estão ausentes por completude, não por diferença de cânon (ver `missingBooks` no [`meta.json`](../versoes/nt-a1819a/meta.json)). |
| `nva` | Protestante | 66/66 | Nenhum | — |

A coluna **Livros presentes** reflete `counts.books` do `meta.json` de cada versão sobre o total do cânon protestante (66); para versões incompletas, os livros ausentes específicos estão em `completeness.missingBooks` do respectivo `meta.json`.

## Observações

- Todas as versões atuais do repositório seguem o cânon protestante — nenhuma inclui deuterocanônicos até o momento.
- A [tabela de livros](estrutura-arquivos/estrutura-xml.md#tabela-de-livros) e as siglas padronizadas do projeto cobrem apenas os 66 livros do cânon protestante. Uma futura versão católica ou de outro cânon exigiria estender essa tabela (novas siglas para os deuterocanônicos) antes de ser adicionada — isso ainda não foi implementado.
- Ao adicionar uma nova versão bíblica, atualize esta tabela como parte do PR se o cânon dela divergir do protestante ou incluir deuterocanônicos.
