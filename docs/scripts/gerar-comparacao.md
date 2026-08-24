# Script de comparação de versículos-chave

Este documento descreve o uso do script responsável por gerar `docs/comparacao-versiculos.md`.

- [scripts/gerar_comparacao.py](../../scripts/gerar_comparacao.py) lê os arquivos `.json` de todas as versões em `versoes/` e monta uma tabela, por versículo-chave, comparando o texto entre elas.

Para o resultado, veja [docs/comparacao-versiculos.md](../comparacao-versiculos.md).

## Automação

`docs/comparacao-versiculos.md` é atualizado automaticamente pelo workflow [`atualizar-comparacao.yml`](../../.github/workflows/atualizar-comparacao.yml), que roda `gerar_comparacao.py` e faz commit do resultado a cada push na `main` que altere `versoes/**/json/**` ou `versoes/**/meta.json` — ou seja, sempre que um PR que mude o texto ou a lista de versões é mesclado. **Não é necessário (e nem deve ser feito) rodar o script manualmente antes de abrir o PR** nem editar `docs/comparacao-versiculos.md` à mão; qualquer alteração manual desse arquivo é sobrescrita no próximo push relevante na `main`.

O workflow também pode ser disparado manualmente via `workflow_dispatch` (aba Actions do GitHub), útil se o arquivo precisar ser regenerado sem um push novo em `versoes/**`.

## Uso manual (opcional)

Rodar localmente é útil apenas para conferir o resultado antes de abrir um PR:

```bash
python scripts/gerar_comparacao.py
```

O script não recebe parâmetros: sempre processa todas as pastas em `versoes/` que possuam uma subpasta `json/` e sobrescreve `docs/comparacao-versiculos.md` por completo. Descarte a mudança local (`git checkout -- docs/comparacao-versiculos.md`) antes de commitar — o CI regenera o arquivo depois do merge.

## Comportamento

- **Versículos comparados:** a lista é fixa no próprio script (`VERSICULOS_CHAVE`, em `scripts/gerar_comparacao.py`) — atualmente João 3:16, Gênesis 1:1 e Salmo 23:1. Para comparar outro versículo, adicione uma tupla `(rótulo, sigla do livro, capítulo, versículo)` a essa lista.
- **Nome de exibição da versão:** vem do campo `name` do `meta.json` da versão (ver [estrutura-meta.md](../estrutura-arquivos/estrutura-meta.md)); se o `meta.json` não existir ou `name` estiver vazio, usa a sigla da pasta em `versoes/`.
- **Versículo ausente:** se o livro não existir em `versoes/{versao}/json/` (versão incompleta, ex.: `nt-a1819a` não tem Antigo Testamento) ou o capítulo/versículo específico não existir no arquivo, a célula exibe `*(não disponível nesta versão)*` em vez de interromper a geração.
- **Versão sem pasta `json/`:** é ignorada silenciosamente na listagem de versões.

## Requisitos (para rodar localmente)

- Python 3.9 ou superior (nenhuma dependência externa é necessária, apenas a biblioteca padrão).
