# Política de uso de Inteligência Artificial

Este documento define onde ferramentas de IA (assistentes de código, LLMs, geradores de texto, etc.) podem e não podem ser usadas no projeto `biblia.publica`. Aplica-se a qualquer colaborador, humano usando IA como apoio, e a qualquer ferramenta de IA usada diretamente no repositório, incluindo assistentes de código como o usado no desenvolvimento deste próprio plano.

## Princípio geral

**IA pode ser usada para construir as ferramentas do projeto. IA não pode, em nenhuma hipótese, ser usada para escrever, corrigir ou revisar o texto bíblico.** Todo manuseio do texto bíblico, da digitação inicial à menor correção ortográfica, é feito exclusivamente por colaboradores humanos.

Essa linha existe porque o valor do projeto depende de rastreabilidade: para cada palavra no texto deve ser possível identificar uma fonte humana (a tradução original) e a uma decisão humana identificável (quem transcreveu, quem revisou, quem editou, etc.). 

Introduzir IA nesse processo quebra essa cadeia de responsabilidade, mesmo quando o resultado "parece" correto.

## Onde IA é permitida

- **Scripts, ferramentas e automações:** conversores de formato (`xml_to_json.py`, `json_to_sqlite.py` etc.), scripts de validação de estrutura, geração de metadados (`meta.json`), workflows de CI, scripts de importação de novas fontes.
- **Documentação técnica do projeto:** descrição de formatos (`docs/estrutura-arquivos/`), guias de uso para desenvolvedores, README, CONTRIBUTING, este próprio documento.
- **Extração mecânica de trechos do texto para documentação:** por exemplo, o script que gera `docs/comparacao-versiculos.md` pode copiar automaticamente um versículo já existente nos arquivos da versão, exibindo-o tal como está. Isso é tratado como parte da ferramenta (script), não como manuseio do texto.
- **Apontar possíveis problemas para revisão humana:** um script (ainda que com apoio de IA em seu desenvolvimento) pode *sinalizar* um versículo suspeito (vazio, duplicado, fora de ordem, ruído de OCR). A decisão sobre o que fazer com esse apontamento, entretanto, deve sempre humana.

## Onde IA não é permitida

- **Correção ou alteração do texto bíblico em si:** ortografia, pontuação, "melhorias" de tradução, unificação de estilo, ou qualquer edição do conteúdo de um versículo.
- **Digitação e limpeza inicial de textos digitalizados (OCR):** mesmo a correção de ruído óbvio no reconhecimento óptico (ex.: um "0" reconhecido no lugar de um "O") deve ser feita e conferida por um humano. IA pode, no máximo, apontar candidatos a erro de OCR para revisão, mas nunca aplicar a correção.
- **Decidir entre variantes de um versículo:** por exemplo, ao encontrar um versículo duplicado ou uma divergência entre XML e JSON, a escolha de qual versão manter é humana.
- **Redação de prosa interpretativa sobre o texto:** análises de estilo, tom, ou qualidade de uma tradução são uma leitura crítica do texto e devem ser escritas exclusivamente por um humano. IA pode ajudar a *organizar ou revisar a redação* desse tipo de texto depois que o conteúdo/opinião já foi definido por um humano, mas não pode originá-lo.

## Fronteira prática: scripts vs. conteúdo

A regra de bolso: **se a IA está decidindo o que o texto bíblico diz ou significa, está fora dos limites. Se a IA está movendo, formatando ou exibindo um texto que um humano já validou, está dentro dos limites.**

| Situação | Permitido? |
|---|---|
| Escrever o script que converte XML → JSON preservando o texto exatamente | Sim |
| Escrever o script que detecta um versículo vazio | Sim |
| Decidir qual texto preencher nesse versículo vazio | Não |
| Gerar `docs/comparacao-versiculos.md` copiando versículos já existentes | Sim |
| Escrever a análise de estilo de uma tradução para a seção "Por que esta versão?" | Não |
| Revisar a redação/gramática de uma análise já escrita por um humano | Sim |
| Limpar ruído de OCR na digitalização de uma nova versão | Não |

## Declaração obrigatória em Pull Requests

Todo PR que altere arquivos de texto bíblico (`versoes/{versao}/xml/**`, `versoes/{versao}/json/**`, ou qualquer outro formato de texto adicionado no futuro) deve declarar explicitamente, via checkbox no template de PR, que nenhuma ferramenta de IA foi usada para gerar, corrigir ou revisar o conteúdo do texto. Ver [CONTRIBUTING.md](CONTRIBUTING.md) e o [template de PR](.github/PULL_REQUEST_TEMPLATE.md).

PRs que alterem apenas scripts, documentação técnica ou metadados não precisam dessa declaração, o uso de IA nesses casos é normal e incentivado.
