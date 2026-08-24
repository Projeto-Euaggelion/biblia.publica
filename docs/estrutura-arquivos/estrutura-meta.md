# Estrutura do `meta.json`

Este documento descreve o formato do arquivo `meta.json`, que armazena os metadados de cada versão bíblica do repositório: identificação, base textual, completude, contagens e informações de integridade/licenciamento.

Diferente de `LICENSE.md` (texto livre voltado para a revisão humana de licenciamento, ver [CONTRIBUTING.md](../../CONTRIBUTING.md)), o `meta.json` é a representação **estruturada e legível por máquina** desses mesmos metadados, pensada para ser consumida por scripts (validação, [docs/index.json](../../docs/index.json) — ver [estrutura-index.md](estrutura-index.md) —, badges, etc.).

## Localização

Cada versão possui um único `meta.json` na raiz da sua pasta em `versoes/`, ao lado de `LICENSE.md` e das subpastas `json/`/`xml/`:

```
versoes/
├── blivre/
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

- **Calculados:** derivados diretamente dos arquivos `json/` e do `LICENSE.md` da versão (sigla, contagens, completude, anomalias, hash). Recalculados a cada execução do script [scripts/gerar_meta.py](../../scripts/gerar_meta.py) ([#5](https://github.com/Projeto-Euaggelion/biblia.publica/issues/5), uso documentado em [docs/scripts/gerar-meta.md](../scripts/gerar-meta.md)), sobrescrevendo o valor anterior.
- **Manuais:** exigem julgamento e interferência humana (nome oficial, base textual, idioma/dialeto, ano, data de verificação de licença). Preenchidos uma vez, diretamente no `meta.json`, e preservados pelo script em atualizações futuras — `gerar_meta.py` nunca sobrescreve um campo manual já preenchido.

A coluna **Origem** na tabela abaixo indica a qual grupo cada campo pertence.

## Objeto raiz

```json
{
  "name": "Bíblia Livre",
  "abbrev": "blivre",
  "year": 2018,
  "language": "pt-BR",
  "textualBasis": null,
  "completeness": {
    "status": "complete",
    "missingBooks": []
  },
  "counts": {
    "books": 66,
    "chapters": 1189,
    "verses": 31101
  },
  "knownAnomalies": [],
  "licenseCheckedAt": "2026-08-23",
  "filesHash": "sha256:b9e123a5d5b5443be155a03130fe5eba1ac31155f4ae37a1df01162f1abba30b"
}
```

| Campo              | Tipo             | Origem     | Descrição                                                                                     | Exemplo                          |
|---------------------|------------------|------------|-------------------------------------------------------------------------------------------------|-----------------------------------|
| `name`              | string           | manual     | Nome oficial completo da versão                                                                | `"Bíblia Livre"` |
| `abbrev`            | string           | calculado  | Sigla da versão, igual ao nome da pasta em `versoes/` e ao prefixo `{versao}-` dos arquivos      | `"blivre"`                           |
| `year`              | int ou string    | manual     | Ano (ou intervalo, como `"1990-2010"`) de publicação/revisão do texto-base; `null` se desconhecido | `2018`                          |
| `language`          | string           | manual     | Idioma/dialeto do texto, como tag [BCP 47](https://www.rfc-editor.org/rfc/rfc5646)              | `"pt-BR"`                         |
| `textualBasis`      | string ou `null` | manual     | Base textual usada na tradução (Textus Receptus, Texto Crítico, Septuaginta, etc.); `null` se não documentada pela fonte | `null` |
| `completeness`      | object           | calculado  | Ver [Objeto `completeness`](#objeto-completeness) abaixo                                        | —                                 |
| `counts`            | object           | calculado  | Ver [Objeto `counts`](#objeto-counts) abaixo                                                    | —                                 |
| `knownAnomalies`    | array de string  | calculado  | Lista de peculiaridades conhecidas do texto/arquivos desta versão, copiada do campo **Anomalias** de `LICENSE.md` ([formato](../../CONTRIBUTING.md#documentação-da-licença-por-versão); ver equivalente em [estrutura-json.md](estrutura-json.md#observações-e-inconsistências-conhecidas)); lista vazia (`[]`) se `LICENSE.md` não declarar nenhuma | ver exemplo acima |
| `licenseCheckedAt`  | string (data)    | manual     | Data (`AAAA-MM-DD`) da última verificação de que a licença declarada em `LICENSE.md` continua válida na fonte original | `"2026-08-01"`                   |
| `filesHash`         | string           | calculado  | Hash SHA-256 do conjunto de arquivos `json/` da versão, prefixado com `sha256:` (ver [cálculo do hash](#cálculo-do-filesHash)) | `"sha256:9e7a46bf..."`           |

### Objeto `completeness`

Representa, em formato estruturado, a mesma informação do campo **Completude** de `LICENSE.md`. É calculado automaticamente comparando os arquivos presentes em `json/` com a lista canônica dos 66 livros do cânon protestante ([tabela de livros](estrutura-xml.md#tabela-de-livros)) — não é editado manualmente.

| Campo           | Tipo             | Origem    | Descrição                                                                 | Exemplo    |
|------------------|------------------|-----------|------------------------------------------------------------------------------|------------|
| `status`         | string (enum)    | calculado | `"complete"` (todos os 66 livros protestantes presentes) ou `"incomplete"`   | `"complete"` |
| `missingBooks`   | array de string  | calculado | Siglas ([tabela de livros](estrutura-xml.md#tabela-de-livros)) dos livros da lista canônica ausentes em `json/`; `[]` quando `status` é `"complete"` | `["ap"]` |

**Importante:** por só comparar contra o cânon protestante de 66 livros, `status`/`missingBooks` ainda não distinguem "faltam livros" de "cânon diferente" — uma versão católica com todos os deuterocanônicos, mas sem repetir o mesmo agrupamento dos 66 protestantes, pode aparecer como `"incomplete"`. O cânon de cada versão está documentado em [docs/texto-biblico/canonicidade.md](../texto-biblico/canonicidade.md); como todas as versões atuais do repositório seguem o cânon protestante, o cálculo é correto para todas elas por ora, mas ainda não considera essa informação automaticamente — isso fica para quando uma versão de outro cânon for adicionada.

### Objeto `counts`

Contagens agregadas de toda a versão, calculadas a partir dos arquivos em `versoes/{versao}/json/`.

| Campo      | Tipo | Origem    | Descrição                                             | Exemplo |
|------------|------|-----------|----------------------------------------------------------|---------|
| `books`    | int  | calculado | Número de arquivos `.json` (livros) presentes na versão   | `66`    |
| `chapters` | int  | calculado | Soma do total de capítulos de todos os livros              | `1189`  |
| `verses`   | int  | calculado | Soma do total de versículos de todos os capítulos          | `31101` |

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

Qualquer alteração de conteúdo, adição ou remoção de livro muda o `filesHash`, é o mesmo valor que `scripts/validar_estrutura.py` ([1.5](../projeto/plano-desenvolvimento.md)) poderá usar para detectar divergência entre o `meta.json` declarado e os arquivos reais.

## Observações e inconsistências conhecidas

- `year`, `textualBasis` e `language` podem ser `null` quando a fonte original não documenta essa informação. Não é permitido inventar um valor para preencher o campo.
- `knownAnomalies` registra peculiaridades dos **arquivos desta versão** (ex.: capítulo `0` vazio); não deve ser usado para registrar divergências de tradução entre versões, isso é escopo de `docs/texto-biblico/comparacao-versiculos.md` ([1.9](../projeto/plano-desenvolvimento.md)). Para corrigir esse campo, edite o **Anomalias** do `LICENSE.md` da versão e rode `gerar_meta.py` novamente — editar `meta.json` diretamente é sobrescrito na próxima execução.
- `licenseCheckedAt` reflete apenas a data da última checagem manual; não expira automaticamente nem é recalculado por `gerar_meta.py`.