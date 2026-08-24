# Contribuindo com o biblia.publica

Obrigado por considerar contribuir! Toda contribuição para o projeto biblia.publica é bem-vinda.

Este é um repositório público de traduções bíblicas em português, e por isso existem critérios objetivos sobre o que será ou não aceito no projeto. Leia este documento antes de abrir um Pull Request (PR).

## Critério obrigatório: uso de IA no texto bíblico

Ferramentas de IA podem ser usadas livremente no desenvolvimento de scripts, ferramentas e documentação técnica do projeto, mas **não podem, em nenhuma hipótese, ser usadas para escrever, corrigir ou revisar o texto bíblico**, incluindo digitação inicial de fontes digitalizadas (OCR), ajustes ortográficos, "melhorias" de tradução ou decisões entre variantes de um versículo. Todo manuseio do texto bíblico é feito exclusivamente por colaboradores humanos. Critérios completos e exemplos em [docs/projeto/politica-ia.md](docs/projeto/politica-ia.md).

Todo PR que altere arquivos de texto bíblico (`versoes/{versao}/xml/**`, `versoes/{versao}/json/**`) precisa confirmar, no template de PR, que nenhuma IA foi usada no conteúdo do texto.

## Critério obrigatório: licenciamento

Toda versão bíblica adicionada ao projeto precisa estar, obrigatoriamente, sob uma das seguintes condições:

- **Domínio público**; ou
- **Qualquer licença Creative Commons** (`CC BY`, `CC BY-SA`, `CC BY-NC`, `CC BY-NC-SA`, `CC BY-ND`, `CC BY-NC-ND`).

Não existe restrição de qual variante de CC é aceita, inclusive as variantes `ND` (No Derivatives) e `NC` (Non-Commercial) podem ser usadas. Em compensação, **o contribuidor precisa declarar explicitamente, no corpo do PR, qual licença se aplica e demonstrar ciência das restrições que ela impõe**, em especial:

- **Licenças `ND` (No Derivatives):** o texto da tradução **não pode ser alterado em nenhuma hipótese**. Só é permitida **transformação técnica de formato**, ou seja, reestruturar e/ou converter o texto original em `<book>/<chapter>/<verse>` de um formato para outro, por exemplo de `.xml` para `.json` sem, no entanto, alterar o conteúdo. Corrigir digitação, unificar ortografia, "melhorar" a tradução ou mesclar com outra fonte não é permitido sob `ND`.
- **Licenças `NC` (Non-Commercial):** não impedem a entrada da versão no projeto, mas o contribuidor deve estar ciente de que isso restringe o uso comercial dos dados por terceiros que reutilizarem o repositório.
- **Domínio público:** ainda assim, é preciso indicar a fonte de onde o texto foi obtido, "domínio público" não dispensa a rastreabilidade da origem.

A licença do projeto em si (`CC BY-SA 4.0`, conforme o [README](README.md)) cobre os scripts e ferramentas do repositório, **não** substitui nem altera a licença de cada tradução individual. Cada versão mantém sua própria licença, conforme já documentado no README.

### Comprovação exigida no PR

Toda contribuição de uma nova versão precisa incluir, na descrição do PR:

1. **Link da fonte original** de onde o texto foi obtido (repositório, site oficial, etc.);
2. **Link ou indicação explícita de onde a licença está declarada** naquela fonte (arquivo `LICENSE`, página de direitos autorais, rodapé do site, etc.).

PRs que apenas afirmem "isso é domínio público" ou "isso é CC" sem apontar a fonte e a licença de forma verificável **serão recusados**.

## Documentação da licença por versão

Toda versão precisa incluir um arquivo `versoes/{versao}/LICENSE.md` descrevendo:

```markdown
# {Nome da versão}

- **Licença:** CC BY-SA 4.0 (ou domínio público, CC BY-ND, etc.)
- **Fonte:** https://... (link do repositório/site de origem)
- **Licença declarada em:** https://... (onde a licença é encontrada na fonte)
- **Modificações permitidas:** apenas estruturação técnica em XML/JSON (padrão para `ND`) | tradução pode ser adaptada livremente (quando a licença permitir)
- **Completude:** completa (66 livros) | incompleta — faltam: {lista de siglas de livros}
- **Anomalias:** (opcional, omitir se não houver nenhuma)
  - {descrição da primeira peculiaridade conhecida dos arquivos desta versão}
  - {descrição da segunda, se houver}
```

Esse arquivo é a referência oficial para revisão de licenciamento, sem ele, o PR não é aceito.

O campo **Anomalias** é uma lista simples (um item por linha, prefixado com `-`) de peculiaridades conhecidas dos arquivos desta versão (ex.: um capítulo vazio herdado da fonte original)

O script [`scripts/gerar_meta.py`](scripts/gerar_meta.py) lê essa lista automaticamente e a copia para `knownAnomalies` no `meta.json` da versão (ver [estrutura-meta.md](docs/estrutura-arquivos/estrutura-meta.md)).

Depois que o PR é mesclado na `main`, o workflow [`atualizar-fontes.yml`](.github/workflows/atualizar-fontes.yml) lê automaticamente todos os `versoes/{versao}/LICENSE.md` e regenera [`docs/texto-biblico/fontes.md`](docs/texto-biblico/fontes.md), incluindo o número do PR e o autor da contribuição.

**Não é necessário (e nem deve ser feito) editar `docs/texto-biblico/fontes.md` manualmente**: qualquer PR que altere esse arquivo à mão terá a alteração descartada no próximo push na `main`.

## Completude da versão

PRs com versões **incompletas** (por exemplo, apenas o Novo Testamento, ou faltando alguns livros) **são aceitos**, desde que:

- os livros faltantes estejam explicitamente listados no `LICENSE.md` da versão (campo **Completude**);
- os arquivos presentes sigam a convenção de nomes normalmente — não é necessário criar arquivos vazios para os livros ausentes.

## Formato dos arquivos

Os arquivos devem seguir a estrutura já documentada em [docs/estrutura-arquivos/estrutura-xml.md](docs/estrutura-arquivos/estrutura-xml.md) e [docs/estrutura-arquivos/estrutura-json.md](docs/estrutura-arquivos/estrutura-json.md), incluindo:

- Convenção de nomes `{versao}-{abbrev}.xml` / `{versao}-{abbrev}.json`;
- Hierarquia `book`/`chapter`/`verse` (XML) ou `chapters`/`verses` (JSON), com os atributos/campos `name`, `abbrev`, `number` e o texto do versículo;
- Uso das siglas de livro padronizadas na [tabela de livros](docs/estrutura-arquivos/estrutura-xml.md#tabela-de-livros).

**Você pode enviar o PR apenas em XML ou apenas em JSON**, não é obrigatório trazer os dois formatos prontos. O repositório disponibiliza scripts de conversão em `scripts/` (`xml_to_json.py` e o equivalente `json_to_xml.py`) para gerar o formato que faltar antes do merge.

Antes de abrir o PR, verifique se os arquivos enviados são bem formados e passam pelo script de conversão sem erros. Todo PR que altere arquivos em `versoes/**` roda automaticamente o [`scripts/validar_estrutura.py`](scripts/validar_estrutura.py) via o workflow [`validar.yml`](.github/workflows/validar.yml), verificando estrutura, ordem de capítulos/versículos, versículos vazios/duplicados e consistência entre `xml/` e `json/`. O PR não pode ser mesclado se essa checagem falhar. Você pode rodar o mesmo script localmente antes de abrir o PR: `python scripts/validar_estrutura.py --version {sigla}`.

## O que não é aceito

- Textos sob licença proprietária, "todos os direitos reservados", ou sem licença/fonte identificável;
- Declaração de domínio público ou CC sem link de comprovação;
- Modificação do texto de uma tradução sob licença `ND` além da transformação técnica de formato;
- Arquivos fora da convenção de nomes ou da estrutura documentada em `docs/estrutura-arquivos/`.

## Checklist antes de abrir o PR

- [ ] Fonte original linkada
- [ ] Licença explícita linkada/identificada
- [ ] `versoes/{versao}/LICENSE.md` criado com licença, fonte, modificações permitidas e completude
- [ ] Arquivos seguem a convenção de nomes e a estrutura em `docs/estrutura-arquivos/estrutura-xml.md` ou `docs/estrutura-arquivos/estrutura-json.md`
- [ ] Se a licença for `ND`, nenhuma alteração de texto foi feita além da conversão de formato
- [ ] Se a versão for incompleta, os livros faltantes estão listados no `LICENSE.md`
- [ ] Se o PR altera arquivos de texto bíblico (`versoes/{versao}/xml/**` ou `json/**`), confirmo que nenhuma IA foi usada para gerar, corrigir ou revisar esse conteúdo (ver [docs/projeto/politica-ia.md](docs/projeto/politica-ia.md))
- [ ] `python scripts/validar_estrutura.py` roda sem erros para a versão alterada