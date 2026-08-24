#!/usr/bin/env python3
"""Gera docs/index.json a partir dos versoes/*/meta.json.

Para cada versao com um meta.json, copia os metadados (nome, ano,
idioma, completude, contagens, anomalias, filesHash) e monta links
diretos para os arquivos de cada formato (json/, xml/, sql/,
LICENSE.md, meta.json) no GitHub, alem de um bloco fixo com os links
para os schemas formais (JSON Schema e XSD, ver docs/schema/).

Pensado para rodar no workflow .github/workflows/atualizar-index.yml
apos um push na branch principal que altere algum meta.json, mas
tambem pode ser executado localmente (sem GITHUB_REPOSITORY
configurado, usa o repositorio do projeto como padrao).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"
OUTPUT_PATH = REPO_ROOT / "docs" / "index.json"
DEFAULT_REPO = "Projeto-Euaggelion/biblia.publica"
REF = "main"


def build_version_entry(version_dir: Path, repo_slug: str) -> dict:
    versao = version_dir.name
    meta = json.loads((version_dir / "meta.json").read_text(encoding="utf-8"))

    raw_base = f"https://raw.githubusercontent.com/{repo_slug}/{REF}/versoes/{versao}"
    tree_base = f"https://github.com/{repo_slug}/tree/{REF}/versoes/{versao}"

    formats = {
        "meta": f"{raw_base}/meta.json",
        "license": f"{raw_base}/LICENSE.md",
        "xml": f"{tree_base}/xml",
        "json": f"{tree_base}/json",
    }
    sqlite_path = version_dir / "sql" / f"{versao}.sqlite"
    if sqlite_path.is_file():
        formats["sql"] = f"{raw_base}/sql/{versao}.sqlite"

    return {
        "abbrev": versao,
        "name": meta.get("name"),
        "year": meta.get("year"),
        "language": meta.get("language"),
        "textualBasis": meta.get("textualBasis"),
        "completeness": meta.get("completeness"),
        "counts": meta.get("counts"),
        "knownAnomalies": meta.get("knownAnomalies"),
        "licenseCheckedAt": meta.get("licenseCheckedAt"),
        "filesHash": meta.get("filesHash"),
        "formats": formats,
    }


def main() -> int:
    repo_slug = os.environ.get("GITHUB_REPOSITORY") or DEFAULT_REPO

    version_dirs = sorted(
        d for d in VERSOES_DIR.iterdir() if d.is_dir() and (d / "meta.json").is_file()
    )
    versions = [build_version_entry(d, repo_slug) for d in version_dirs]

    index = {
        "repository": f"https://github.com/{repo_slug}",
        "schemas": {
            "json": f"https://raw.githubusercontent.com/{repo_slug}/{REF}/docs/schema/biblia.schema.json",
            "xml": f"https://raw.githubusercontent.com/{repo_slug}/{REF}/docs/schema/biblia.xsd",
        },
        "versions": versions,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"docs/index.json atualizado com {len(versions)} versao(oes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
