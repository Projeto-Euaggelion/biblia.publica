# biblia.publica
Repositório dedicado à organização de traduções bíblicas, em português brasileiro, disponíveis em domínio público e em licenças Creative Commons.

## Objetivo

O objetivo principal deste repositório é organizar, de forma estruturada, todas as versões bíblicas disponíveis em lingua portuguesa sob licença de domínio público e/ou em licenças Creative Commons.

## Fontes utilizadas

A lista de versões, com licença, fonte e completude de cada uma, é gerada automaticamente a partir dos arquivos `versoes/{versao}/LICENSE.md` e fica disponível em [docs/fontes.md](docs/fontes.md).

## Qualidade do texto

O esforço inicial deste projeto tem se dedicado à indexação das versões bíblicas. Revisões e correções do texto não foram realizadas (exceto quando indicado) antes do texto ser adicionado ao projeto.

## Estrutura dos arquivos

- Formato json: para mais detalhes sobre a estrutura utilizada nos arquivos `.json`, leia a documentação em [docs/estrutura-json.md](docs/estrutura-json.md);
- Formato XML: leia a documentação em [docs/estrutura-xml.md](docs/estrutura-xml.md) para mais detalhes sobre a estrututra dos arquivos no formato `.xml`.
- Metadados por versão: o formato do `meta.json` de cada versão está documentado em [docs/estrutura-arquivos/estrutura-meta.md](docs/estrutura-arquivos/estrutura-meta.md).

## Contribuições

Deseja adicionar uma nova versão bíblica ou corrigir algo? Antes de abrir um Pull Request, leia os requisitos de contribuição em [CONTRIBUTING.md](CONTRIBUTING.md). Especialmente os critérios de licenciamento (domínio público ou Creative Commons), obrigatórios para qualquer versão adicionada ao projeto.

## Licenças

Cada tradução bíblica indexada neste projeto possuí sua própria licença de uso. Detalhes como: tipo de licença, fonte do conteúdo, página pública para conferência da licença, modificações permitidas e detalhes de completude da versão estão disponíveis em `versoes/{versao}/LICENSE.md`.

O projeto biblia.publica, entretanto, com seus scripts, ferramentas e recursos está licenciado sob uma licença `Creative Commons Attribution-ShareAlike 4.0 International`.