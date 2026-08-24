# Scripts de conversão XML ↔ JSON

Este documento descreve o uso dos scripts responsáveis por converter os textos bíblicos entre os formatos `.xml` e `.json` mantidos em `versoes/`.

- [scripts/xml_to_json.py](../../scripts/xml_to_json.py) — converte de `.xml` para `.json`.
- [scripts/json_to_xml.py](../../scripts/json_to_xml.py) — converte de `.json` para `.xml`.

Para detalhes sobre o formato de cada arquivo, veja [estrutura-xml.md](../estrutura-arquivos/estrutura-xml.md) e [estrutura-json.md](../estrutura-arquivos/estrutura-json.md).

## Requisitos

- Python 3.9 ou superior (nenhuma dependência externa é necessária, apenas a biblioteca padrão).

## Uso

Ambos os scripts seguem a mesma interface de linha de comando:

```bash
python scripts/xml_to_json.py --version [versao] --book [abreviacao|all]
python scripts/json_to_xml.py --version [versao] --book [abreviacao|all]
```

| Parâmetro   | Obrigatório | Descrição                                                                 |
|-------------|-------------|-----------------------------------------------------------------------------|
| `--version` | Sim         | Sigla da versão a converter (`blivre`, `tb`).                        |
| `--book`    | Sim         | Sigla do livro a converter (ex.: `gn`, `mt`) ou `all` para converter todos os livros da versão. |

A sigla do livro (`--book`) segue a mesma convenção usada no nome dos arquivos (`{versao}-{abbrev}.xml` / `.json`) — ver [Tabela de livros](../estrutura-arquivos/estrutura-xml.md#tabela-de-livros).

### Exemplos

Converter apenas o livro de Gênesis da versão Bíblia Livre, de XML para JSON:

```bash
python scripts/xml_to_json.py --version blivre --book gn
```

Converter todos os livros da Tradução Brasileira, de XML para JSON:

```bash
python scripts/xml_to_json.py --version tb --book all
```

Regenerar o XML de Mateus da versão Bíblia Livre a partir do JSON:

```bash
python scripts/json_to_xml.py --version blivre --book mt
```

Regenerar todos os arquivos XML da versão Bíblia Livre a partir dos JSON:

```bash
python scripts/json_to_xml.py --version blivre --book all
```

## Comportamento

- **Origem e destino**: cada script lê de `versoes/{versao}/xml/` ou `versoes/{versao}/json/` e grava na pasta irmã correspondente (`json/` ou `xml/`), sempre um arquivo por livro.
- **Nome dos arquivos**: o arquivo de saída mantém o mesmo nome base do arquivo de entrada, apenas trocando a extensão (`{versao}-{abbrev}.xml` ⇄ `{versao}-{abbrev}.json`).
- **Sobrescrita**: arquivos existentes no destino são sobrescritos sem confirmação.
- **Criação de pastas**: a pasta de destino (`json/` ou `xml/`) é criada automaticamente caso ainda não exista.
- **`--book all`**: converte todos os arquivos encontrados na pasta de origem daquela versão.
- **Ida e volta (roundtrip)**: converter um livro de XML para JSON e depois de volta para XML produz um arquivo idêntico ao original, incluindo o atributo `chapters` do elemento raiz (recalculado a partir da quantidade de capítulos) e a indentação com tabulação.

## Erros comuns

| Situação                                         | Mensagem                                                                 |
|---------------------------------------------------|---------------------------------------------------------------------------|
| Versão inexistente ou sem pasta `xml/`/`json/`     | `erro: pasta xml/json nao encontrada para a versao '{versao}' (...)`      |
| Livro inexistente para a versão informada          | `erro: arquivo nao encontrado para o livro '{book}' (...)`                |
| XML malformado (apenas em `xml_to_json.py`)        | `erro ao converter {arquivo}: {detalhe do erro de parsing}` — o script pula o arquivo e continua os demais. |
| JSON malformado ou com campos ausentes (apenas em `json_to_xml.py`) | `erro ao converter {arquivo}: {detalhe do erro}` — o script pula o arquivo e continua os demais. |

Em caso de erro de versão ou de livro não encontrado, o script encerra imediatamente com código de saída `1`. Erros de conversão em um arquivo específico (dentro de `--book all`) não interrompem a conversão dos demais arquivos.

## Quando regenerar os arquivos

Os arquivos `.json` são derivados dos `.xml` (fonte de verdade dos textos). Qualquer correção de conteúdo deve ser feita no `.xml` e em seguida `xml_to_json.py` deve ser executado para atualizar o `.json` correspondente. O script `json_to_xml.py` normalmente só é necessário em fluxos inversos, como reconstruir o `.xml` a partir de um `.json` editado ou recuperar o XML de uma versão cuja fonte original só está disponível em JSON.
