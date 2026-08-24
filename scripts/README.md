# Scripts

- **`scripts/`** (raiz desta pasta) — ferramentas de uso manual pelos contribuidores: conversão entre formatos, geração/atualização de metadados, validação, etc. Documentadas em [docs/scripts/](../docs/scripts/).
- **`scripts/ci/`** — scripts que só rodam automaticamente, disparados por um workflow em `.github/workflows/`. Não são pensados para uso manual (embora possam ser executados localmente para depuração).

Ao adicionar um script novo, coloque-o em `scripts/ci/` apenas se ele for exclusivamente acionado por um workflow do GitHub Actions; caso contrário, ele é uma ferramenta do projeto e fica na raiz de `scripts/`.
