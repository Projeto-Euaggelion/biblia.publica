#!/usr/bin/env python3
"""Gera/atualiza versoes/{versao}/meta.json a partir de versoes/{versao}/json/*.json
e do campo Anomalias de versoes/{versao}/LICENSE.md.

Calcula os campos derivaveis diretamente dos arquivos (contagens de
livros/capitulos/versiculos, completude, lista de anomalias e hash
SHA-256) e preserva os campos que exigem preenchimento manual (name,
year, language, textualBasis, licenseCheckedAt) ja existentes em um
meta.json anterior, sem sobrescreve-los.

Ver docs/estrutura-arquivos/estrutura-meta.md para o schema completo e o
significado de cada campo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"

# Ordem canonica dos 66 livros do canon protestante (ver tabela de livros em
# docs/estrutura-arquivos/estrutura-xml.md). Usada apenas para calcular
# completeness/missingBooks; nao reflete outros canones (ver #10).
CANONICAL_BOOKS = [
    "gn", "ex", "lv", "nm", "dt", "js", "jz", "rt", "1sm", "2sm", "1rs", "2rs",
    "1cr", "2cr", "ed", "ne", "et", "job", "sl", "pv", "ec", "ct", "is", "jr",
    "lm", "ez", "dn", "os", "jl", "am", "ob", "jn", "mq", "na", "hc", "sf",
    "ag", "zc", "ml",
    "mt", "mc", "lc", "jo", "at", "rm", "1co", "2co", "gl", "ef", "fp", "cl",
    "1ts", "2ts", "1tm", "2tm", "tt", "fm", "hb", "tg", "1pe", "2pe", "1jo",
    "2jo", "3jo", "jd", "ap",
]

MANUAL_DEFAULTS = {
    "name": None,
    "year": None,
    "language": None,
    "textualBasis": None,
    "licenseCheckedAt": None,
}

ANOMALIES_HEADER = re.compile(r"^\*\*Anomalias:\*\*")
LIST_ITEM = re.compile(r"^-\s+(.+)$")


def book_abbrev_from_filename(version: str, json_path: Path) -> str:
    prefix = f"{version}-"
    stem = json_path.stem
    if not stem.startswith(prefix):
        raise ValueError(f"nome de arquivo fora do padrao '{prefix}*.json': {json_path.name}")
    return stem[len(prefix):]


def compute_counts_and_hash(version: str, json_dir: Path) -> tuple[dict, str, set[str]]:
    json_files = sorted(json_dir.glob("*.json"))
    chapters = 0
    verses = 0
    abbrevs: set[str] = set()
    h = hashlib.sha256()

    for path in json_files:
        data = path.read_bytes()
        h.update(data)
        try:
            book = json.loads(data)
            chapters += len(book["chapters"])
            verses += sum(len(c["verses"]) for c in book["chapters"])
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"  erro ao ler {path.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr)
            continue
        abbrevs.add(book_abbrev_from_filename(version, path))

    counts = {"books": len(json_files), "chapters": chapters, "verses": verses}
    files_hash = f"sha256:{h.hexdigest()}"
    return counts, files_hash, abbrevs


def compute_completeness(abbrevs: set[str]) -> dict:
    missing = [b for b in CANONICAL_BOOKS if b not in abbrevs]
    status = "complete" if not missing else "incomplete"
    return {"status": status, "missingBooks": missing}


def parse_anomalies(license_path: Path) -> list[str]:
    """Le a lista simples sob '**Anomalias:**' em LICENSE.md (ver CONTRIBUTING.md)."""
    if not license_path.is_file():
        return []

    anomalies: list[str] = []
    in_list = False
    for line in license_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not in_list:
            if ANOMALIES_HEADER.match(stripped):
                in_list = True
            continue
        if not stripped:
            continue
        match = LIST_ITEM.match(stripped)
        if not match:
            break
        anomalies.append(match.group(1).strip())

    return anomalies


def load_manual_fields(meta_path: Path) -> dict:
    if not meta_path.is_file():
        return dict(MANUAL_DEFAULTS)
    existing = json.loads(meta_path.read_text(encoding="utf-8"))
    return {field: existing.get(field, default) for field, default in MANUAL_DEFAULTS.items()}


def build_meta(version_dir: Path) -> dict:
    version = version_dir.name
    counts, files_hash, abbrevs = compute_counts_and_hash(version, version_dir / "json")
    manual = load_manual_fields(version_dir / "meta.json")

    return {
        "name": manual["name"],
        "abbrev": version,
        "year": manual["year"],
        "language": manual["language"],
        "textualBasis": manual["textualBasis"],
        "completeness": compute_completeness(abbrevs),
        "counts": counts,
        "knownAnomalies": parse_anomalies(version_dir / "LICENSE.md"),
        "licenseCheckedAt": manual["licenseCheckedAt"],
        "filesHash": files_hash,
    }


def write_meta(version_dir: Path, meta: dict) -> Path:
    meta_path = version_dir / "meta.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return meta_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        dest="version",
        help="Sigla da versao a atualizar (ex: blivre). Se omitido, atualiza todas as versoes com pasta json/.",
    )
    args = parser.parse_args()

    if args.version:
        version_dir = VERSOES_DIR / args.version
        if not version_dir.is_dir():
            print(f"erro: versao '{args.version}' nao encontrada ({version_dir})", file=sys.stderr)
            return 1
        version_dirs = [version_dir]
    else:
        version_dirs = sorted(d for d in VERSOES_DIR.iterdir() if d.is_dir())

    updated = 0
    for version_dir in version_dirs:
        json_dir = version_dir / "json"
        if not json_dir.is_dir():
            print(f"aviso: pasta json/ nao encontrada para '{version_dir.name}', pulando.", file=sys.stderr)
            continue

        meta = build_meta(version_dir)
        meta_path = write_meta(version_dir, meta)
        print(
            f"{version_dir.name}: {meta_path.relative_to(REPO_ROOT)} atualizado "
            f"({meta['counts']['books']} livros, {meta['counts']['chapters']} capitulos, "
            f"{meta['counts']['verses']} versiculos, completude={meta['completeness']['status']})."
        )
        updated += 1

    print(f"\nConcluido: {updated} versao(oes) atualizada(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
