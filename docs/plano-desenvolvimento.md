# Plano de desenvolvimento

Este documento estabelece o plano de desenvolvimento do projeto e o separa em tarefas pequenas, independentes e dimensionadas para trabalho solo, nas horas vagas. Cada item abaixo vira (ou já virou) uma [Issue no GitHub](https://github.com/Projeto-Euaggelion/biblia.publica/issues), agrupada por milestone de fase.

## Como usar este documento

- Cada tarefa tem **critérios de aceite**, quando todos estiverem satisfeitos, a issue pode ser fechada.
- **Depende de** aponta pré-requisitos; tarefas sem dependência podem ser feitas em qualquer ordem dentro da fase.
- O tamanho (P/M/G) é uma estimativa de esforço para uma sessão solo: P ≈ até 2h, M ≈ meio dia, G ≈ mais de uma sessão (considerar quebrar ao iniciar).
---

## Fase 1 — Metadados e confiabilidade (curto prazo)

Objetivo: toda versão passa a ter metadados estruturados e é validada automaticamente. Esta fase é pré-requisito para todas as funcionalidades que dependem da confiança nos dados (schema, releases, badges).

### 1.1 Corrigir referências antigas à versão `tb` na documentação
- **Tamanho:** P
- **Descrição:** `docs/estrutura-arquivos/estrutura-json.md` e `estrutura-xml.md` ainda citam a versão `tb` (Tradução Brasileira) como exemplo, mas ela não existe mais em `versoes/` (as versões atuais são `blivre`, `jfaal`, `nt-a1819a`, `nva`, `otb`). Atualizar os exemplos para uma versão real existente. A remoção da versão do projeto e do histórico de commits foi uma decisão motivada pela incerteza se o texto adicionado ao projeto é da versão em domínio público ou a versão atualizada.
- **Critérios de aceite:** nenhuma menção a `tb` nos docs de estrutura; exemplos de árvore de diretórios refletem versões reais.
- **Depende de:** —

### 1.2 Definir o schema do `meta.json` por versão
- **Tamanho:** P
- **Descrição:** Documentar em `docs/estrutura-arquivos/estrutura-meta.md` o formato do `meta.json` em `versoes/{versao}/meta.json`, com: nome oficial, sigla, ano, idioma/dialeto, base textual (TR, crítico, etc.), contagem de livros/capítulos/versículos, status de completude, lista de anomalias conhecidas, data da última verificação de licença, hash SHA-256 do conjunto de arquivos.
- **Critérios de aceite:** documento publicado com exemplo completo de `meta.json`; campos e tipos definidos numa tabela, no mesmo padrão de `estrutura-json.md`.
- **Depende de:** —

### 1.3 Script para gerar/atualizar `meta.json`
- **Tamanho:** M
- **Descrição:** `scripts/gerar_meta.py`, que para cada versão em `versoes/`: conta livros/capítulos/versículos a partir do JSON, calcula o hash SHA-256 do conjunto de arquivos, e escreve/atualiza `meta.json` preservando campos que exigem input humano (base textual, anomalias, idioma) já preenchidos.
- **Critérios de aceite:** script roda localmente sem erro sobre as 5 versões atuais; campos calculáveis batem com a contagem real dos arquivos.
- **Depende de:** 1.2

### 1.4 Gerar `meta.json` para as versões existentes
- **Tamanho:** P
- **Descrição:** Rodar `gerar_meta.py` e preencher manualmente os campos não-automáticos (base textual, idioma/dialeto, anomalias conhecidas) para `blivre`, `jfaal`, `nt-a1819a`, `nva`, `otb`.
- **Critérios de aceite:** as 5 pastas têm `meta.json` válido conforme o schema de 1.2.
- **Depende de:** 1.3

### 1.5 Script de validação de estrutura
- **Tamanho:** M
- **Descrição:** `scripts/validar_estrutura.py`, que verifica por versão: contagem esperada de livros (conforme completude declarada no `LICENSE.md`/`meta.json`), ausência de versículos vazios ou duplicados, ordem crescente de capítulos e versículos, codificação UTF-8 válida sem caracteres de controle indevidos.
- **Critérios de aceite:** script roda sobre as 5 versões existentes e retorna erro/exit code não-zero se encontrar problema; relatório legível no terminal.
- **Depende de:** —

### 1.6 Relatório de diferenças entre XML e JSON
- **Tamanho:** M
- **Descrição:** Script (`scripts/comparar_xml_json.py` ou opção em `validar_estrutura.py`) que compara o conteúdo convertido, garantindo que XML e JSON de uma mesma versão representam exatamente o mesmo texto (mesma contagem e mesmo texto por versículo).
- **Critérios de aceite:** rodando sobre as 5 versões, reporta divergência zero (ou lista exatamente as divergências conhecidas, como o capítulo `0` do `otb-1rs`).
- **Depende de:** —

### 1.7 Integrar validação ao CI
- **Tamanho:** P
- **Descrição:** Novo workflow `.github/workflows/validar.yml`, disparado em todo PR que altere `versoes/**`, rodando `validar_estrutura.py` (e o comparador de 1.6) e falhando o PR se houver problema.
- **Critérios de aceite:** PR de teste com um erro proposital (ex.: versículo duplicado) falha o CI; PR limpo passa.
- **Depende de:** 1.5, 1.6

### 1.8 Tabela de canonicidade
- **Tamanho:** P
- **Descrição:** `docs/canonicidade.md` documentando, por versão, se segue o cânon protestante (66 livros), católico (73) ou outro, e se há deuterocanônicos presentes.
- **Critérios de aceite:** tabela cobre as 5 versões atuais e é referenciada no README.
- **Depende de:** —

### 1.9 Página de comparação de versículos-chave
- **Tamanho:** M
- **Descrição:** `docs/comparacao-versiculos.md` (gerado por script a partir dos JSON, para não ficar desatualizado) com uma tabela mostrando João 3:16, Gênesis 1:1 e Salmo 23:1 lado a lado entre todas as versões.
- **Critérios de aceite:** documento gerado automaticamente por `scripts/gerar_comparacao.py`, cobrindo as 5 versões; referenciado no README.
- **Depende de:** —

---

## Fase 2 — Formatos e ferramentas (médio prazo)

Objetivo: dados fáceis de consumir por terceiros, com garantias formais de formato.

### 2.1 JSON Schema formal
- **Tamanho:** M
- **Descrição:** Publicar `docs/schema/biblia.schema.json` (JSON Schema Draft 2020-12) cobrindo o formato descrito em `estrutura-json.md`, e um script/step de CI que valida todos os `.json` de `versoes/` contra ele.
- **Critérios de aceite:** todos os arquivos JSON existentes validam contra o schema; schema referenciado em `estrutura-json.md`.
- **Depende de:** —

### 2.2 XSD formal
- **Tamanho:** M
- **Descrição:** Publicar `docs/schema/biblia.xsd` cobrindo o formato XML descrito em `estrutura-xml.md`, com validação equivalente à 2.1.
- **Critérios de aceite:** todos os arquivos XML existentes validam contra o XSD.
- **Depende de:** —

### 2.3 Formato SQLite
- **Tamanho:** M
- **Descrição:** `scripts/json_to_sqlite.py` gerando um `.sqlite` por versão em `versoes/{versao}/sql/` (pasta já existe, hoje vazia), com schema simples (`books`, `chapters`, `verses`) documentado em `docs/estrutura-arquivos/estrutura-sql.md`.
- **Critérios de aceite:** `.sqlite` gerado para as 5 versões, schema documentado, uma query de exemplo (buscar um versículo) funciona.
- **Depende de:** —

### 2.4 `index.json` (API estática)
- **Tamanho:** P
- **Descrição:** Script que gera `docs/index.json` (ou raiz) listando todas as versões com metadados (a partir dos `meta.json` da Fase 1) e links diretos para os arquivos em cada formato.
- **Critérios de aceite:** arquivo gerado automaticamente, atualizado em CI quando `meta.json` muda.
- **Depende de:** 1.3

### 2.5 Guia de uso para desenvolvedores
- **Tamanho:** M
- **Descrição:** `docs/guia-desenvolvedores.md` com exemplos práticos em Python, JavaScript e SQL para carregar e consultar os dados (JSON, e SQLite quando 2.3 estiver pronto), incluindo um snippet de "como citar a versão corretamente" (nome, licença, fonte).
- **Critérios de aceite:** os três exemplos rodam sem erro contra os dados reais do repositório.
- **Depende de:** 2.3 (para o exemplo em SQL)

### 2.6 Releases automatizados
- **Tamanho:** M
- **Descrição:** Workflow que, ao criar uma tag (`vX.Y.Z`), empacota `.zip`/`.tar.gz` por versão bíblica (e um consolidado com todas) e publica como GitHub Release.
- **Critérios de aceite:** criar uma tag de teste gera um Release com os artefatos esperados.
- **Depende de:** —

### 2.7 Avaliar formato USFM
- **Tamanho:** G
- **Descrição:** Investigar viabilidade de exportar para USFM (padrão da indústria de tradução bíblica); se viável, implementar `scripts/json_to_usfm.py`. Este item começa como um spike (pesquisa), não implementação direta.
- **Critérios de aceite:** decisão documentada (viável/não viável e por quê); se viável, conversor funcionando para ao menos uma versão.
- **Depende de:** —

---

## Fase 3 — Comunidade e monitoramento (longo prazo)

Objetivo: reduzir fricção de contribuição e manter o repositório saudável sem trabalho manual constante.

### 3.1 Issue templates específicos
- **Tamanho:** P
- **Descrição:** Templates em `.github/ISSUE_TEMPLATE/` para "Propor nova versão", "Reportar erro de texto / versículo faltante" e "Sugerir melhoria de formato".
- **Critérios de aceite:** os três templates aparecem ao criar uma nova issue no GitHub.
- **Depende de:** —

### 3.2 Código de conduta e processo de decisão
- **Tamanho:** P
- **Descrição:** `CODE_OF_CONDUCT.md` (ou seção dedicada em `CONTRIBUTING.md`) explicando como novas versões são aceitas, como anomalias são tratadas e quem decide em questões de licença.
- **Critérios de aceite:** documento publicado e linkado no README.
- **Depende de:** —

### 3.3 Badges no README
- **Tamanho:** P
- **Descrição:** Badges alimentados pelo CI: número de versões, status da última validação (Fase 1.7), "licença verificada".
- **Critérios de aceite:** badges visíveis no README e atualizados automaticamente (ou via workflow agendado).
- **Depende de:** 1.7

### 3.4 CHANGELOG por versão
- **Tamanho:** P
- **Descrição:** Definir e documentar em `CONTRIBUTING.md` o processo de registrar mudanças relevantes (correção de erro, nova revisão de fonte) em `versoes/{versao}/CHANGELOG.md`.
- **Critérios de aceite:** processo documentado; `CHANGELOG.md` inicial criado para as 5 versões existentes.
- **Depende de:** —

### 3.5 Monitoramento de fontes
- **Tamanho:** G
- **Descrição:** Workflow agendado (cron) que verifica periodicamente se a fonte original de cada versão (link em `LICENSE.md`) teve atualização, e abre uma issue automaticamente quando detectar mudança.
- **Critérios de aceite:** workflow roda sem erro e cria uma issue de teste ao simular uma mudança.
- **Depende de:** 1.4 (usa metadados de fonte)

### 3.6 Interface web simples (GitHub Pages)
- **Tamanho:** G
- **Descrição:** Página estática simples publicada via GitHub Pages, consumindo `index.json` (2.4), para explorar versões e ler versículos sem clonar o repositório.
- **Critérios de aceite:** página publicada, lista as versões, permite navegar até um livro/capítulo.
- **Depende de:** 2.4

### 3.7 Seção "Quem usa" no README
- **Tamanho:** P
- **Descrição:** Seção no README para projetos/apps que usam o repositório como fonte de dados (pode começar vazia, com instrução de como se adicionar via PR).
- **Critérios de aceite:** seção publicada no README.
- **Depende de:** —

---

## Expansão de versões (contínuo, fora das fases)

Adicionar novas versões bíblicas continua acontecendo em paralelo às fases acima, sempre seguindo os critérios de licença e qualidade do [CONTRIBUTING.md](../CONTRIBUTING.md). Não é uma tarefa de issue única — é fluxo recorrente via PR.

---

## Rastreamento

Cada tarefa numerada acima corresponde a uma Issue no GitHub, com label de fase (`fase-1`, `fase-2`, `fase-3`) e milestone correspondente. A lista de issues abertas/fechadas é a fonte de verdade sobre o progresso — este documento é atualizado quando o escopo de uma fase muda, não a cada issue fechada.
