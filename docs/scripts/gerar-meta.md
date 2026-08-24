# Script de geração de metadados (`meta.json`)

Este documento descreve o uso do script responsável por gerar/atualizar o `meta.json` de cada versão em `versoes/{versao}/meta.json`.

- [scripts/gerar_meta.py](../../scripts/gerar_meta.py) calcula os campos deriváveis dos arquivos `.json` de uma versão e escreve/atualiza o `meta.json` correspondente.

Para o schema completo (campos, tipos e origem de cada um), veja [estrutura-meta.md](../estrutura-arquivos/estrutura-meta.md).

## Requisitos

- Python 3.9 ou superior (nenhuma dependência externa é necessária, apenas a biblioteca padrão).

## Uso

```bash
python scripts/gerar_meta.py [--version <versao>]
```

| Parâmetro   | Obrigatório | Descrição                                                                                  |
|-------------|-------------|----------------------------------------------------------------------------------------------|
| `--version` | Não         | Sigla da versão a ser gerada/atualizada (ex.: `blivre`). Se for omitido, atualiza todas as versões em `versoes/` que possuam uma pasta `json/`. |

### Exemplos

Atualizar/gerar o `meta.json` de todas as versões:

```bash
python scripts/gerar_meta.py
```

Atualizar/gerar apenas a versão Bíblia Livre:

```bash
python scripts/gerar_meta.py --version blivre
```

## Comportamento

- **Campos calculados** (`abbrev`, `completeness`, `counts`, `knownAnomalies`, `filesHash`) são sempre recalculados a partir dos arquivos em `versoes/{versao}/json/` e do `LICENSE.md` da versão, sobrescrevendo qualquer valor anterior no `meta.json`.
- **Campos manuais** (`name`, `year`, `language`, `textualBasis`, `licenseCheckedAt`) são lidos do `meta.json` existente (se houver) e preservados sem alteração. Se o `meta.json` ainda não existir, esses campos são criados com valor `null` e devem ser preenchidos manualmente depois.
- **`completeness`** é calculado comparando os livros presentes com a lista canônica dos 66 livros do cânon protestante (ver [Tabela de livros](../estrutura-arquivos/estrutura-xml.md#tabela-de-livros)); versões de outros cânones ainda não são tratadas de forma diferenciada (ver [#10](https://github.com/Projeto-Euaggelion/biblia.publica/issues/10)).
- **`knownAnomalies`** é lido do campo **Anomalias** de `versoes/{versao}/LICENSE.md` — uma lista simples (`- item`) logo após a linha `**Anomalias:**` (ver [CONTRIBUTING.md](../../CONTRIBUTING.md#documentação-da-licença-por-versão)). Se o campo não existir no `LICENSE.md`, `knownAnomalies` fica `[]`.
- **Versão sem pasta `json/`**: o script emite um aviso e pula aquela versão, sem interromper as demais.
- **Arquivo `.json` de livro malformado**: o script reporta o erro daquele arquivo e continua processando os demais, mas o livro problemático não entra nas contagens nem em `completeness`.

## Quando rodar

Rode `gerar_meta.py` sempre que os arquivos `.json` de uma versão mudarem (novo livro adicionado, correção de conteúdo via `xml_to_json.py`) ou o `LICENSE.md` for atualizado (nova anomalia documentada), para manter `counts`, `completeness`, `knownAnomalies` e `filesHash` em dia. Os campos manuais só precisam ser preenchidos uma vez, editando o `meta.json` diretamente.
