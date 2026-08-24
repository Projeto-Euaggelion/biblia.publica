# Estrutura dos arquivos JSON

Este documento descreve o formato utilizado nos arquivos `.json` do repositório, que armazenam o texto das versões bíblicas em português. 

Os arquivos `.json` são gerados a partir dos arquivos `.xml` (ver [estrutura-xml.md](estrutura-xml.md)) pelo script [scripts/xml_to_json.py](../scripts/xml_to_json.py), mantendo a mesma hierarquia de dados: livro → capítulos → versículos.

## Organização de diretórios

Cada versão bíblica possui, dentro de `versoes/`, uma subpasta `json/` com um arquivo por livro, ao lado da subpasta `xml/`:

```
versoes/
├── blivre/
│   ├── json/
│   │   ├── blivre-gn.json
│   │   ├── blivre-ex.json
│   │   └── ...
│   └── xml/
│       └── ...
├── jfaal/
│   ├── json/
│   │   ├── jfaal-gn.json
│   │   └── ...
│   └── xml/
│       └── ...
└── etc...
```

- `blivre` — Bíblia Livre
- `jfaal` — João Ferreira de Almeida Atualizada Livre
- etc...

### Convenção de nomes de arquivo

```
{versao}-{abbrev}.json
```

Onde `{versao}` é a sigla da versão (`blivre`, `jfaal`) e `{abbrev}` é a sigla do livro (ver tabela em [estrutura-xml.md](estrutura-xml.md#tabela-de-livros)). Exemplo: `jfaal-1co.json` é o livro de 1 Coríntios na versão João Ferreira de Almeida Atualizada Livre.

## Codificação

Os arquivos são salvos em UTF-8, com os caracteres acentuados e tipográficos (`á`, `ç`, `“ ” ‘ ’`, `—` etc.) gravados diretamente como caracteres Unicode, não são usadas sequências de escape (`\uXXXX`) nem entidades como na versão XML.

## Hierarquia dos elementos

Cada arquivo é um único objeto JSON representando um livro, com uma lista de capítulos, cada um com uma lista de versículos:

```json
{
  "name": "Gênesis",
  "abbrev": "gn",
  "chapters": [
    {
      "number": 1,
      "verses": [
        { "number": 1, "text": "No princípio criou Deus os céus e a terra." },
        { "number": 2, "text": "E a terra estava desordenada e vazia..." }
      ]
    },
    {
      "number": 2,
      "verses": [ ... ]
    }
  ]
}
```

### Objeto raiz (livro)

| Campo      | Tipo   | Descrição                                     | Exemplo   |
|------------|--------|------------------------------------------------|-----------|
| `name`     | string | Nome completo do livro em português             | `"Gênesis"` |
| `abbrev`   | string | Sigla do livro, também usada no nome do arquivo | `"gn"`      |
| `chapters` | array  | Lista de objetos de capítulo (ver abaixo)       | —           |

Diferente do XML, o objeto raiz não repete o número total de capítulos (`chapters` como contagem). Em JSON, `chapters` é a própria lista de capítulos, e o total pode ser obtido com o tamanho do array.

### Objeto de capítulo

| Campo    | Tipo   | Descrição                            | Exemplo |
|----------|--------|----------------------------------------|---------|
| `number` | int    | Número do capítulo (a partir de `1`)   | `1`     |
| `verses` | array  | Lista de objetos de versículo (ver abaixo) | —   |

### Objeto de versículo

| Campo    | Tipo   | Descrição                              | Exemplo |
|----------|--------|-------------------------------------------|---------|
| `number` | int    | Número do versículo (a partir de `1`)     | `1`     |
| `text`   | string | Texto do versículo                        | `"No princípio criou Deus os céus e a terra."` |

## Observações e inconsistências conhecidas

- O estilo de aspas e pontuação (retas vs. tipográficas, uso de travessão) varia entre versões, refletindo o texto original de cada tradução — a conversão para JSON não normaliza esse texto.
- Não há marcação de formatação (itálico, notas de rodapé, referências cruzadas, poesia, etc.) — cada versículo é apenas uma string de texto plano no campo `text`.
- Os arquivos JSON são gerados automaticamente a partir dos XML; qualquer correção de conteúdo deve ser feita no `.xml` correspondente e o script `scripts/xml_to_json.py` deve ser executado novamente para regenerar o `.json`.

## Tabela de livros

A tabela de siglas, nomes e número de capítulos por livro é a mesma para XML e JSON — ver [Tabela de livros em estrutura-xml.md](estrutura-xml.md#tabela-de-livros).
