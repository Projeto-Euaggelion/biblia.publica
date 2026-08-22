# Estrutura dos arquivos XML

Este documento descreve o formato utilizado nos arquivos `.xml` do repositório, que armazenam o texto das versões bíblicas em português.

## Organização de diretórios

Cada versão bíblica possui sua própria pasta dentro de `versoes/`, contendo uma subpasta `xml/` com um arquivo por livro:

```
versoes/
├── blivre/
│   └── xml/
│       ├── blivre-gn.xml
│       ├── blivre-ex.xml
│       └── ...
├── otb/
│   └── xml/
│       ├── otb-gn.xml
│       └── ...
└── tb/
    └── xml/
        ├── tb-gn.xml
        └── ...
```

- `blivre` — Bíblia Livre
- `otb` — Open Translate Bible
- `tb` — Tradução Brasileira

As três versões contêm exatamente os mesmos 66 arquivos (um por livro), diferindo apenas no prefixo do nome do arquivo e no texto traduzido.

### Convenção de nomes de arquivo

```
{versao}-{abbrev}.xml
```

Onde `{versao}` é a sigla da versão (`blivre`, `otb`, `tb`) e `{abbrev}` é a sigla do livro (ver tabela abaixo). Exemplo: `tb-1co.xml` é o livro de 1 Coríntios na versão Tradução Brasileira.

## Codificação

Todos os arquivos começam com a declaração:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

Aspas retas (`"`) dentro do texto dos versículos aparecem, em alguns arquivos, como entidade `&quot;`; em outros (principalmente na versão `otb`) o texto usa aspas tipográficas (`“ ” ‘ ’`) e travessão (`—`) diretamente como caracteres Unicode. O sinal `>` também pode aparecer escapado como `&gt;`.

## Hierarquia dos elementos

Cada arquivo tem um único elemento raiz `<book>`, contendo um ou mais elementos `<chapter>`, que por sua vez contêm um ou mais elementos `<verse>` com o texto do versículo.

```xml
<book name="Gênesis" abbrev="gn" chapters="50">
    <chapter number="1">
        <verse number="1">No princípio criou Deus os céus e a terra.</verse>
        <verse number="2">E a terra estava desordenada e vazia...</verse>
        ...
    </chapter>
    <chapter number="2">
        ...
    </chapter>
</book>
```

### `<book>`

Elemento raiz do arquivo. Atributos:

| Atributo   | Descrição                                              | Exemplo      |
|------------|----------------------------------------------------------|--------------|
| `name`     | Nome completo do livro em português                     | `Gênesis`    |
| `abbrev`   | Sigla do livro, também usada no nome do arquivo          | `gn`         |
| `chapters` | Número total de capítulos do livro                       | `50`         |

### `<chapter>`

Um capítulo do livro. Atributo:

| Atributo | Descrição                  | Exemplo |
|----------|-----------------------------|---------|
| `number` | Número do capítulo (a partir de `1`) | `1` |

### `<verse>`

Um versículo do capítulo. O texto do versículo é o conteúdo textual do elemento. Atributo:

| Atributo | Descrição                    | Exemplo |
|----------|-------------------------------|---------|
| `number` | Número do versículo (a partir de `1`) | `1` |

## Observações e inconsistências conhecidas

- O arquivo `versoes/otb/xml/otb-1rs.xml` possui um `<chapter number="0">` vazio (sem versículos) antes do capítulo `1`. Trata-se de uma particularidade herdada da fonte original, não um padrão do formato.
- O estilo de aspas e pontuação (retas vs. tipográficas, uso de travessão) varia entre versões, refletindo o texto original de cada tradução — não há normalização entre elas.
- Não há marcação de formatação (itálico, notas de rodapé, referências cruzadas, poesia, etc.) — cada `<verse>` contém apenas texto plano.

## Tabela de livros

| Sigla  | Livro                        | Capítulos | Testamento |
|--------|-------------------------------|-----------|------------|
| gn     | Gênesis                       | 50        | AT |
| ex     | Êxodo                          | 40        | AT |
| lv     | Levítico                       | 27        | AT |
| nm     | Números                        | 36        | AT |
| dt     | Deuteronômio                   | 34        | AT |
| js     | Josué                          | 24        | AT |
| jz     | Juízes                         | 21        | AT |
| rt     | Rute                            | 4         | AT |
| 1sm    | 1 Samuel                        | 31        | AT |
| 2sm    | 2 Samuel                        | 24        | AT |
| 1rs    | 1 Reis                          | 22        | AT |
| 2rs    | 2 Reis                          | 25        | AT |
| 1cr    | 1 Crônicas                      | 29        | AT |
| 2cr    | 2 Crônicas                      | 36        | AT |
| ed     | Esdras                          | 10        | AT |
| ne     | Neemias                         | 13        | AT |
| et     | Ester                           | 10        | AT |
| job    | Jó                              | 42        | AT |
| sl     | Salmos                          | 150       | AT |
| pv     | Provérbios                      | 31        | AT |
| ec     | Eclesiastes                     | 12        | AT |
| ct     | Cânticos                        | 8         | AT |
| is     | Isaías                          | 66        | AT |
| jr     | Jeremias                        | 52        | AT |
| lm     | Lamentações de Jeremias          | 5         | AT |
| ez     | Ezequiel                        | 48        | AT |
| dn     | Daniel                          | 12        | AT |
| os     | Oséias                          | 14        | AT |
| jl     | Joel                            | 3         | AT |
| am     | Amós                            | 9         | AT |
| ob     | Obadias                         | 1         | AT |
| jn     | Jonas                           | 4         | AT |
| mq     | Miquéias                        | 7         | AT |
| na     | Naum                            | 3         | AT |
| hc     | Habacuque                       | 3         | AT |
| sf     | Sofonias                        | 3         | AT |
| ag     | Ageu                            | 2         | AT |
| zc     | Zacarias                        | 14        | AT |
| ml     | Malaquias                       | 4         | AT |
| mt     | Mateus                          | 28        | NT |
| mc     | Marcos                          | 16        | NT |
| lc     | Lucas                           | 24        | NT |
| jo     | João                            | 21        | NT |
| at     | Atos                            | 28        | NT |
| rm     | Romanos                         | 16        | NT |
| 1co    | 1 Coríntios                     | 16        | NT |
| 2co    | 2 Coríntios                     | 13        | NT |
| gl     | Gálatas                         | 6         | NT |
| ef     | Efésios                         | 6         | NT |
| fp     | Filipenses                      | 4         | NT |
| cl     | Colossenses                     | 4         | NT |
| 1ts    | 1 Tessalonicenses               | 5         | NT |
| 2ts    | 2 Tessalonicenses               | 3         | NT |
| 1tm    | 1 Timóteo                       | 6         | NT |
| 2tm    | 2 Timóteo                       | 4         | NT |
| tt     | Tito                            | 3         | NT |
| fm     | Filemom                         | 1         | NT |
| hb     | Hebreus                         | 13        | NT |
| tg     | Tiago                           | 5         | NT |
| 1pe    | 1 Pedro                         | 5         | NT |
| 2pe    | 2 Pedro                         | 3         | NT |
| 1jo    | 1 João                          | 5         | NT |
| 2jo    | 2 João                          | 1         | NT |
| 3jo    | 3 João                          | 1         | NT |
| jd     | Judas                           | 1         | NT |
| ap     | Apocalipse                      | 22        | NT |
