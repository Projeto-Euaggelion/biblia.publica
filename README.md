# biblia.publica

[![Licença](https://img.shields.io/github/license/Projeto-Euaggelion/biblia.publica)](https://github.com/Projeto-Euaggelion/biblia.publica/blob/main/LICENSE)
[![Último commit](https://img.shields.io/github/last-commit/Projeto-Euaggelion/biblia.publica)](https://github.com/Projeto-Euaggelion/biblia.publica/commits/main)
[![Issues abertas](https://img.shields.io/github/issues/Projeto-Euaggelion/biblia.publica)](https://github.com/Projeto-Euaggelion/biblia.publica/issues)
[![Pull requests abertos](https://img.shields.io/github/issues-pr/Projeto-Euaggelion/biblia.publica)](https://github.com/Projeto-Euaggelion/biblia.publica/pulls)

[![Fase 1](https://img.shields.io/github/milestones/progress/Projeto-Euaggelion/biblia.publica/1)](https://github.com/Projeto-Euaggelion/biblia.publica/milestone/1)
[![Fase 2](https://img.shields.io/github/milestones/progress/Projeto-Euaggelion/biblia.publica/2)](https://github.com/Projeto-Euaggelion/biblia.publica/milestone/2)
[![Fase 3](https://img.shields.io/github/milestones/progress/Projeto-Euaggelion/biblia.publica/3)](https://github.com/Projeto-Euaggelion/biblia.publica/milestone/3)

Repositório dedicado à organização de traduções bíblicas, em português brasileiro, disponíveis em domínio público e em licenças Creative Commons.

## Objetivo

O objetivo principal deste repositório é organizar, de forma estruturada, todas as versões bíblicas disponíveis em lingua portuguesa sob licença de domínio público e/ou em licenças Creative Commons.

## Fontes utilizadas

A lista de versões, com licença, fonte e completude de cada uma, é gerada automaticamente a partir dos arquivos `versoes/{versao}/LICENSE.md` e fica disponível em [docs/fontes.md](docs/fontes.md).

## Canonicidade

Para saber qual cânon (protestante, católico ou outro) cada versão segue, e se inclui livros deuterocanônicos, veja [docs/canonicidade.md](docs/canonicidade.md).

## Comparação de versículos-chave

O texto de João 3:16, Gênesis 1:1 e Salmo 23:1 lado a lado entre todas as versões está em [docs/comparacao-versiculos.md](docs/comparacao-versiculos.md).

## Qualidade do texto

O esforço inicial deste projeto tem se dedicado à indexação das versões bíblicas. Revisões e correções do texto não foram realizadas (exceto quando indicado) antes do texto ser adicionado ao projeto.

## Estrutura dos arquivos

- Formato json: para mais detalhes sobre a estrutura utilizada nos arquivos `.json`, leia a documentação em [docs/estrutura-json.md](docs/estrutura-json.md);
- Formato XML: leia a documentação em [docs/estrutura-xml.md](docs/estrutura-xml.md) para mais detalhes sobre a estrututra dos arquivos no formato `.xml`.
- Metadados por versão: o formato do `meta.json` de cada versão está documentado em [docs/estrutura-arquivos/estrutura-meta.md](docs/estrutura-arquivos/estrutura-meta.md).

## Contribuições

Deseja adicionar uma nova versão bíblica ou corrigir algo? Antes de abrir um Pull Request, leia os requisitos de contribuição em [CONTRIBUTING.md](CONTRIBUTING.md). Especialmente os critérios de licenciamento (domínio público ou Creative Commons), obrigatórios para qualquer versão adicionada ao projeto.

## Uso de Inteligência Artificial

Ferramentas de IA são usadas no desenvolvimento de scripts, automações e documentação técnica do projeto, mas **nunca** para escrever, corrigir ou revisar o texto bíblico presente neste projeto. Esse trabalho é feito exclusivamente por colaboradores humanos. Veja os critérios completos em [POLITICA_IA.md](POLITICA_IA.md).

## Licenças

Cada tradução bíblica indexada neste projeto possuí sua própria licença de uso. Detalhes como: tipo de licença, fonte do conteúdo, página pública para conferência da licença, modificações permitidas e detalhes de completude da versão estão disponíveis em `versoes/{versao}/LICENSE.md`.

O projeto biblia.publica, entretanto, com seus scripts, ferramentas e recursos está licenciado sob uma licença `Creative Commons Attribution-ShareAlike 4.0 International`.

## Contribuidores

![Contribuidores](https://contrib.rocks/image?repo=Projeto-Euaggelion/biblia.publica)