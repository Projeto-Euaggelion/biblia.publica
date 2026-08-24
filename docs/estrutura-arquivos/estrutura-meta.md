# Estrutura do `meta.json`

Este documento descreve o formato do arquivo `meta.json`, que armazena os metadados de cada versão bíblica do repositório: identificação, base textual, completude, contagens e informações de integridade/licenciamento.

Diferente de `LICENSE.md` (texto livre voltado para a revisão humana de licenciamento, ver [CONTRIBUTING.md](../../CONTRIBUTING.md)), o `meta.json` é a representação **estruturada e legível por máquina** desses mesmos metadados, pensada para ser consumida por scripts (validação, `index.json` a ser implementado na [Fase 2](https://github.com/Projeto-Euaggelion/biblia.publica/milestone/2) de desenvolvimento do projeto, badges, etc.).

## Localização

Cada versão possui um único `meta.json` na raiz da sua pasta em `versoes/`, ao lado de `LICENSE.md` e das subpastas `json/`/`xml/`:

```
versoes/
├── otb/
│   ├── meta.json
│   ├── LICENSE.md
│   ├── json/
│   │   └── ...
│   └── xml/
│       └── ...
└── etc...
```

## Origem dos campos

Os campos se dividem em dois grupos:

- **Calculados:** derivados diretamente dos arquivos `json/` da versão (contagens, hash). Gerados/atualizados automaticamente pelo script `scripts/gerar_meta.py` ([#5](https://github.com/Projeto-Euaggelion/biblia.publica/issues/5)).
- **Manuais:** exigem julgamento e interferência humana (base textual, idioma/dialeto, anomalias, ano). Preenchidos uma vez e preservados pelo script em atualizações futuras. O script `gerar_meta.py` nunca sobrescreve um campo manual já preenchido.

A coluna **Origem** na tabela abaixo indica a qual grupo cada campo pertence.

## Objeto raiz

```json
{
  "name": "Open Translation Bible - pt-br",
  "abbrev": "otb",
  "year": 2020,
  "language": "pt-BR",
  "textualBasis": "Texto Crítico (Nestle-Aland / UBS)",
  "completeness": {
    "status": "complete",
    "missingBooks": []
  },
  "counts": {
    "books": 66,
    "chapters": 1189,
    "verses": 31082
  },
  "knownAnomalies": [
    "otb-1rs.json possui um capítulo `{ \"number\": 0, \"verses\": [] }` vazio antes do capítulo 1, herdado do XML de origem."
  ],
  "licenseCheckedAt": "2026-08-01",
  "filesHash": "sha256:9e7a46bf37e350046e994089353391882e5c436fcb593b288025d101e3bc2f95"
}
```

| Campo              | Tipo             | Origem     | Descrição                                                                                     | Exemplo                          |
|---------------------|------------------|------------|-------------------------------------------------------------------------------------------------|-----------------------------------|
| `name`              | string           | manual     | Nome oficial completo da versão                                                                | `"Open Translation Bible - pt-br"` |
| `abbrev`            | string           | manual     | Sigla da versão, igual ao nome da pasta em `versoes/` e ao prefixo `{versao}-` dos arquivos      | `"otb"`                           |
| `year`              | int ou string    | manual     | Ano (ou intervalo, como `"1990-2010"`) de publicação/revisão do texto-base; `null` se desconhecido | `2020`                          |
| `language`          | string           | manual     | Idioma/dialeto do texto, como tag [BCP 47](https://www.rfc-editor.org/rfc/rfc5646)              | `"pt-BR"`                         |
| `textualBasis`      | string ou `null` | manual     | Base textual usada na tradução (Textus Receptus, Texto Crítico, Septuaginta, etc.); `null` se não documentada pela fonte | `"Texto Crítico (Nestle-Aland / UBS)"` |
| `completeness`      | object           | —          | Ver [Objeto `completeness`](#objeto-completeness) abaixo                                        | —                                 |
| `counts`            | object           | calculado  | Ver [Objeto `counts`](#objeto-counts) abaixo                                                    | —                                 |
| `knownAnomalies`    | array de string  | manual     | Lista de peculiaridades conhecidas do texto/arquivos desta versão (ver equivalente em [estrutura-json.md](estrutura-json.md#observações-e-inconsistências-conhecidas)); lista vazia (`[]`) se não há nenhuma | ver exemplo acima |
| `licenseCheckedAt`  | string (data)    | manual     | Data (`AAAA-MM-DD`) da última verificação de que a licença declarada em `LICENSE.md` continua válida na fonte original | `"2026-08-01"`                   |
| `filesHash`         | string           | calculado  | Hash SHA-256 do conjunto de arquivos `json/` da versão, prefixado com `sha256:` (ver [cálculo do hash](#cálculo-do-filesHash)) | `"sha256:9e7a46bf..."`           |

### Objeto `completeness`

Representa, em formato estruturado, a mesma informação do campo **Completude** de `LICENSE.md`.

| Campo           | Tipo             | Origem    | Descrição                                                                 | Exemplo    |
|------------------|------------------|-----------|------------------------------------------------------------------------------|------------|
| `status`         | string (enum)    | manual    | `"complete"` (66 livros protestantes) ou `"incomplete"`                      | `"complete"` |
| `missingBooks`   | array de string  | manual    | Siglas ([tabela de livros](estrutura-xml.md#tabela-de-livros)) dos livros ausentes; `[]` quando `status` é `"complete"` | `["ap"]` |

**Importante:** versões com livros deuterocanônicos, ou cânon diferente do protestante (66 livros), são tratadas por `status`/`missingBooks` apenas quanto à completude do que a versão se propõe a conter. Ou seja, uma versão católica que possua 66 livros será considerada não completa mesmo contendo a mesma quantidade de livros de uma versão protestante.

A comparação formal entre cânones fica a cargo de `docs/canonicidade.md` ([1.8](../plano-desenvolvimento.md), [#10](https://github.com/Projeto-Euaggelion/biblia.publica/issues/10)).

### Objeto `counts`

Contagens agregadas de toda a versão, calculadas a partir dos arquivos em `versoes/{versao}/json/`.

| Campo      | Tipo | Origem    | Descrição                                             | Exemplo |
|------------|------|-----------|----------------------------------------------------------|---------|
| `books`    | int  | calculado | Número de arquivos `.json` (livros) presentes na versão   | `66`    |
| `chapters` | int  | calculado | Soma do total de capítulos de todos os livros              | `1189`  |
| `verses`   | int  | calculado | Soma do total de versículos de todos os capítulos          | `31082` |

### Cálculo do `filesHash`

Para permitir que qualquer pessoa reproduza o hash localmente e detecte alteração de conteúdo entre releases, o cálculo é fixo:

1. Listar os arquivos de `versoes/{versao}/json/*.json` em ordem alfabética pelo nome do arquivo.
2. Ler cada arquivo como bytes brutos (UTF-8, sem normalização) e concatená-los, na ordem do passo 1, em um único buffer.
3. Calcular o SHA-256 desse buffer e representar o resultado como hexadecimal minúsculo, prefixado por `sha256:`.

```python
import hashlib, glob

files = sorted(glob.glob(f"versoes/{versao}/json/*.json"))
h = hashlib.sha256()
for f in files:
    with open(f, "rb") as fh:
        h.update(fh.read())
files_hash = f"sha256:{h.hexdigest()}"
```

Qualquer alteração de conteúdo, adição ou remoção de livro muda o `filesHash`, é o mesmo valor que `scripts/validar_estrutura.py` ([1.5](../plano-desenvolvimento.md)) poderá usar para detectar divergência entre o `meta.json` declarado e os arquivos reais.

## Observações e inconsistências conhecidas

- `year`, `textualBasis` e `language` podem ser `null` quando a fonte original não documenta essa informação. Não é permitido inventar um valor para preencher o campo.
- `knownAnomalies` registra peculiaridades dos **arquivos desta versão** (ex.: capítulo `0` vazio); não deve ser usado para registrar divergências de tradução entre versões, isso é escopo de `docs/comparacao-versiculos.md` ([1.9](../plano-desenvolvimento.md)).
- `licenseCheckedAt` reflete apenas a data da última checagem manual; não expira automaticamente nem é recalculado por `gerar_meta.py`.