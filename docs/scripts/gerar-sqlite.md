# Script de geração do banco SQLite (`json_to_sqlite.py`)

Este documento descreve o uso do script responsável por gerar o banco `versoes/{versao}/sql/{versao}.sqlite` de cada versão, a partir dos arquivos `versoes/{versao}/json/*.json`.

- [scripts/json_to_sqlite.py](../../scripts/json_to_sqlite.py) lê todos os livros `.json` de uma versão e (re)cria o `.sqlite` correspondente, do zero, com o schema `books`/`chapters`/`verses`.

Para o schema completo (tabelas, colunas e uma query de exemplo), veja [estrutura-sql.md](../estrutura-arquivos/estrutura-sql.md).

## Requisitos

- Python 3.9 ou superior (nenhuma dependência externa é necessária — usa o módulo `sqlite3` da biblioteca padrão).

## Uso

```bash
python scripts/json_to_sqlite.py [--version <versao>]
```

| Parâmetro   | Obrigatório | Descrição                                                                                  |
|-------------|-------------|----------------------------------------------------------------------------------------------|
| `--version` | Não         | Sigla da versão a gerar (ex.: `blivre`). Se for omitido, gera para todas as versões em `versoes/` que possuam uma pasta `json/`. |

### Exemplos

Gerar/atualizar o `.sqlite` de todas as versões:

```bash
python scripts/json_to_sqlite.py
```

Gerar/atualizar apenas a versão Bíblia Livre:

```bash
python scripts/json_to_sqlite.py --version blivre
```

## Comportamento

- O arquivo `versoes/{versao}/sql/{versao}.sqlite` é apagado e recriado do zero a cada execução — não há atualização incremental, o banco sempre reflete o estado atual de `json/` no momento em que o script roda.
- A pasta `versoes/{versao}/sql/` é criada automaticamente se ainda não existir.
- Os livros são inseridos na ordem alfabética dos arquivos `.json` (mesma ordem usada pelos demais scripts, como [gerar_meta.py](gerar-meta.md)), não necessariamente a ordem canônica do cânon.
- **Versão sem pasta `json/`**: o script emite um aviso e pula aquela versão, sem interromper as demais.

## Quando rodar

Rode `json_to_sqlite.py` sempre que os arquivos `.json` de uma versão mudarem (novo livro adicionado, correção de conteúdo via `xml_to_json.py`), para manter o `.sqlite` em dia com o texto atual — assim como `meta.json` (ver [gerar-meta.md](gerar-meta.md)), o `.sqlite` é um artefato gerado e deve ser commitado junto da mudança que o originou.
