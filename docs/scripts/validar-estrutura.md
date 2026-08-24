# Script de validação de estrutura (`validar_estrutura.py`)

Este documento descreve o uso do script responsável por validar a estrutura dos arquivos `versoes/{versao}/json/*.json` e sua coerência com `meta.json`.

- [scripts/validar_estrutura.py](../../scripts/validar_estrutura.py) verifica, para cada versão em `versoes/`, se os arquivos `.json` estão bem formados e se `meta.json` reflete corretamente o conteúdo atual desses arquivos.

## Requisitos

- Python 3.9 ou superior (nenhuma dependência externa é necessária, apenas a biblioteca padrão).

## Uso

```bash
python scripts/validar_estrutura.py [--version <versao>]
```

| Parâmetro   | Obrigatório | Descrição                                                                                  |
|-------------|-------------|------------------------------------------------------------------------------------------------|
| `--version` | Não         | Sigla da versão a validar (ex.: `otb`). Se for omitido, valida todas as versões em `versoes/`. |

### Exemplos

Validar todas as versões:

```bash
python scripts/validar_estrutura.py
```

Validar apenas a versão Open Translation Bible:

```bash
python scripts/validar_estrutura.py --version otb
```

## O que é verificado

Para cada versão, o script reaproveita o cálculo de contagens/completude/hash de [scripts/gerar_meta.py](../../scripts/gerar_meta.py) para comparar o estado atual dos arquivos `json/` com o que está declarado em `meta.json` (ver [estrutura-meta.md](../estrutura-arquivos/estrutura-meta.md)):

- **`counts`** (livros/capítulos/versículos) declarado em `meta.json` bate com a contagem real dos arquivos `json/`.
- **`completeness`** (status/livros faltantes) declarado bate com o cálculo atual contra o cânon protestante de 66 livros.
- **`filesHash`** declarado bate com o hash SHA-256 recalculado do conteúdo atual de `json/`.

Em seguida, cada arquivo `versoes/{versao}/json/*.json` é validado individualmente:

- **Codificação:** os bytes do arquivo devem ser UTF-8 válido.
- **JSON:** o conteúdo deve ser um JSON bem formado, seguindo a estrutura de [estrutura-json.md](../estrutura-arquivos/estrutura-json.md).
- **Versículos vazios:** nenhum `text` de versículo pode ser vazio ou conter apenas espaços em branco.
- **Versículos duplicados:** nenhum número de versículo pode se repetir dentro do mesmo capítulo.
- **Ordem crescente:** os números de capítulo (dentro do livro) e de versículo (dentro de cada capítulo) devem ser estritamente crescentes.
- **Caracteres de controle:** nenhum `text` de versículo pode conter caracteres de controle (`\x00`–`\x1F`, exceto tabulação/quebra de linha, e `\x7F`).

## Relatório e exit code

O script imprime, por versão, `OK` quando nada é encontrado ou uma lista de linhas `ERRO:` com o problema e sua localização (arquivo, capítulo, versículo). Ao final, imprime um resumo com o total de versões verificadas, versões com problema e problemas encontrados.

Retorna exit code `0` se nenhum problema for encontrado em nenhuma versão, ou `1` caso contrário — pensado para uso em CI (ver [1.7](../plano-desenvolvimento.md#17-integrar-validação-ao-ci-9)).

## Quando rodar

Rode `validar_estrutura.py` depois de adicionar ou editar arquivos `.json` de uma versão (por exemplo, após corrigir um `.xml` e regenerar o `.json` com [xml_to_json.py](../../scripts/xml_to_json.py)) e depois de rodar `gerar_meta.py`, para confirmar que `meta.json` foi atualizado e que os arquivos não têm problemas estruturais antes de abrir o PR.
