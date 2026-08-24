#!/usr/bin/env python3
"""Gera docs/fontes.md a partir dos arquivos versoes/*/LICENSE.md.

Para cada versao com um LICENSE.md, extrai licenca/fonte/completude e
descobre o PR e o autor do ultimo commit que alterou aquele arquivo
(via `git log` + `gh api`), montando uma tabela-indice em docs/fontes.md.

Este script e pensado para rodar no workflow
.github/workflows/atualizar-fontes.yml apos um push na branch principal,
mas tambem pode ser executado localmente (sem GITHUB_REPOSITORY/gh
configurados, as colunas de PR/autor ficam em branco).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"
OUTPUT_PATH = REPO_ROOT / "docs" / "fontes.md"

FIELD_PATTERN = re.compile(r"^(?:-\s+)?\*\*(.+?):\*\*\s*(.+)$")


def parse_license_md(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FIELD_PATTERN.match(line.strip())
        if match:
            key, value = match.group(1).strip(), match.group(2).strip()
            fields[key] = value
    return fields


def last_commit_sha(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(REPO_ROOT))],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    sha = result.stdout.strip()
    return sha or None


def pr_info_for_commit(sha: str, repo_slug: str) -> dict[str, str]:
    try:
        result = subprocess.run(
            [
                "gh", "api", f"repos/{repo_slug}/commits/{sha}/pulls",
                "-H", "Accept: application/vnd.github+json",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}
    if not prs:
        return {}
    pr = prs[0]
    autor = (pr.get("user") or {}).get("login")
    return {
        "numero": str(pr.get("number", "")),
        "url": pr.get("html_url", ""),
        "autor": autor or "",
    }


def build_row(versao_dir: Path, repo_slug: str | None) -> dict[str, str]:
    license_path = versao_dir / "LICENSE.md"
    fields = parse_license_md(license_path)

    pr: dict[str, str] = {}
    if repo_slug:
        sha = last_commit_sha(license_path)
        if sha:
            pr = pr_info_for_commit(sha, repo_slug)

    pr_cell = f"[#{pr['numero']}]({pr['url']})" if pr.get("numero") else "—"
    autor_cell = f"[@{pr['autor']}](https://github.com/{pr['autor']})" if pr.get("autor") else "—"

    return {
        "versao": versao_dir.name,
        "licenca": fields.get("Licença", "—"),
        "fonte": fields.get("Fonte", "—"),
        "completude": fields.get("Completude", "—"),
        "pr": pr_cell,
        "autor": autor_cell,
    }


def render_table(rows: list[dict[str, str]]) -> str:
    header = (
        "| Versão | Licença | Fonte | Completude | PR | Contribuidor |\n"
        "|--------|---------|-------|------------|----|--------------|\n"
    )
    lines = [
        f"| `{r['versao']}` | {r['licenca']} | {r['fonte']} | {r['completude']} | {r['pr']} | {r['autor']} |"
        for r in rows
    ]
    return header + "\n".join(lines) + "\n"


def main() -> int:
    repo_slug = os.environ.get("GITHUB_REPOSITORY")

    versao_dirs = sorted(
        d for d in VERSOES_DIR.iterdir() if d.is_dir() and (d / "LICENSE.md").is_file()
    )

    rows = [build_row(d, repo_slug) for d in versao_dirs]
    body = render_table(rows) if rows else "_Nenhuma versão com `LICENSE.md` foi documentada ainda._\n"

    content = (
        "# Fontes utilizadas\n\n"
        "> Este arquivo é gerado automaticamente pelo workflow "
        "`.github/workflows/atualizar-fontes.yml` a partir dos arquivos "
        "`versoes/{versao}/LICENSE.md`, sempre que um desses arquivos muda na "
        "branch principal. **Não edite este arquivo manualmente** — para "
        "corrigir uma informação, altere o `LICENSE.md` da versão "
        "correspondente.\n\n"
        f"{body}\n"
        "Para detalhes completos de cada versão (fonte, licença, restrições de "
        "modificação e completude), veja o `LICENSE.md` da respectiva pasta em "
        "`versoes/`. Para os critérios de licenciamento exigidos de novas "
        "versões, veja [CONTRIBUTING.md](../CONTRIBUTING.md).\n"
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"docs/fontes.md atualizado com {len(rows)} versao(oes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
