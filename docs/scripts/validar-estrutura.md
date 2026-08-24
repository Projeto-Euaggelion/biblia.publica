# Script de validação de estrutura (`validar_estrutura.py`)

Este documento descreve o uso do script responsável por validar a estrutura dos arquivos `versoes/{versao}/json/*.json`, sua coerência com `meta.json`, e a fidelidade da conversão entre `xml/` e `json/` de cada versão.

- [scripts/validar_estrutura.py](../../scripts/validar_estrutura.py) roda dois modos de verificação, individualmente ou em conjunto:
  - **`estrutura`** — os arquivos `.json` de uma versão estão bem formados e `meta.json` reflete corretamente o conteúdo atual desses arquivos.
  - **`diff`** — `xml/` e `json/` de uma versão representam exatamente o mesmo texto.

## Requisitos

- Python 3.9 ou superior (nenhuma dependência externa é necessária, apenas a biblioteca padrão).

## Uso

```bash
python scripts/validar_estrutura.py [--version <versao>] [--check {estrutura,diff,tudo}]
```

| Parâmetro   | Obrigatório | Descrição                                                                                       |
|-------------|-------------|---------------------------------------------------------------------------------------------------|
| `--version` | Não         | Sigla da versão a validar (ex.: `otb`). Se for omitido, valida todas as versões em `versoes/`.    |
| `--check`   | Não         | `estrutura` roda só a validação de `json/`/`meta.json`; `diff` roda só a comparação `xml/` × `json/`; `tudo` (padrão) roda os dois. |

### Exemplos

Rodar as duas verificações sobre todas as versões (padrão):

```bash
python scripts/validar_estrutura.py
```

Validar apenas a estrutura da versão Open Translation Bible:

```bash
python scripts/validar_estrutura.py --version otb --check estrutura
```

Comparar apenas xml/ e json/ de todas as versões:

```bash
python scripts/validar_estrutura.py --check diff
```

## O que é verificado

### Modo `estrutura`

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

### Modo `diff`

Para cada versão, o script casa os arquivos de `xml/` e `json/` pelo nome (`{versao}-{abbrev}`), reaproveitando o parser de [scripts/xml_to_json.py](../../scripts/xml_to_json.py) para ler o XML, e compara:

- **Arquivo correspondente ausente:** um livro presente em `xml/` sem par em `json/`, ou vice-versa.
- **Capítulos:** mesmo conjunto de números de capítulo nos dois formatos.
- **Versículos:** mesmo conjunto de números de versículo em cada capítulo, nos dois formatos.
- **Texto:** o `text` de cada versículo é idêntico, caractere a caractere, entre `xml/` e `json/`.

Uma divergência de texto real e conhecida no momento em que este documento foi escrito: `jfaal-mt.xml` capítulo 17, versículo 14, ainda contém o texto duplicado original (ver anomalia documentada em `versoes/jfaal/LICENSE.md`), que foi corrigido apenas no `.json` — o `.xml` precisa ser atualizado e reconvertido para que a divergência desapareça.

## Relatório e exit code

O script imprime, por versão, `OK` quando nada é encontrado ou uma lista de linhas `ERRO [estrutura]:`/`ERRO [diff]:` com o problema e sua localização (arquivo, capítulo, versículo). Ao final, imprime um resumo com o total de versões verificadas, versões com problema e problemas encontrados, somando os dois modos quando `--check tudo` é usado.

Retorna exit code `0` se nenhum problema for encontrado em nenhuma versão, ou `1` caso contrário — pensado para uso em CI (ver [1.7](../plano-desenvolvimento.md#17-integrar-validação-ao-ci-9)).

## Quando rodar

Rode `validar_estrutura.py` depois de adicionar ou editar arquivos `.xml`/`.json` de uma versão (por exemplo, após corrigir um `.xml` e regenerar o `.json` com [xml_to_json.py](../../scripts/xml_to_json.py)) e depois de rodar `gerar_meta.py`, para confirmar que `meta.json` foi atualizado, que os arquivos não têm problemas estruturais e que `xml/`/`json/` continuam representando o mesmo texto, antes de abrir o PR.
