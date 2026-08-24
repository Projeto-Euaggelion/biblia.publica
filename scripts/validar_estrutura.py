#!/usr/bin/env python3
"""Valida a estrutura dos arquivos versoes/{versao}/json/*.json.

Para cada versao verifica: contagem de livros/capitulos/versiculos e
completude declaradas em meta.json batem com os arquivos json/ atuais;
ausencia de versiculos vazios ou duplicados; ordem crescente de
capitulos e versiculos; codificacao UTF-8 valida sem caracteres de
controle indevidos.

Reaproveita o calculo de contagens/completude/hash de
scripts/gerar_meta.py para comparar com o que esta declarado no
meta.json de cada versao (ver docs/estrutura-arquivos/estrutura-meta.md).

Retorna exit code 1 se algum problema for encontrado, 0 caso contrario.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_meta import compute_completeness, compute_counts_and_hash  # noqa: E402

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")


def validate_meta(version_dir: Path, counts: dict, completeness: dict, files_hash: str) -> list[str]:
    meta_path = version_dir / "meta.json"
    if not meta_path.is_file():
        return ["meta.json nao encontrado (rode scripts/gerar_meta.py)"]

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"meta.json invalido ({exc})"]

    issues = []
    if meta.get("counts") != counts:
        issues.append(f"meta.json desatualizado: counts declarado={meta.get('counts')} atual={counts}")
    if meta.get("completeness") != completeness:
        issues.append(
            f"meta.json desatualizado: completeness declarado={meta.get('completeness')} atual={completeness}"
        )
    if meta.get("filesHash") != files_hash:
        issues.append(f"meta.json desatualizado: filesHash declarado={meta.get('filesHash')} atual={files_hash}")
    return issues


def validate_book(path: Path) -> list[str]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return [f"{path.name}: conteudo nao e UTF-8 valido ({exc})"]

    try:
        book = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{path.name}: JSON invalido ({exc})"]

    issues = []
    try:
        prev_chapter = None
        for chapter in book["chapters"]:
            cnum = chapter["number"]
            if prev_chapter is not None:
                if cnum == prev_chapter:
                    issues.append(f"{path.name}: capitulo {cnum} repetido")
                elif cnum < prev_chapter:
                    issues.append(f"{path.name}: capitulo {cnum} fora de ordem (apos {prev_chapter})")
            prev_chapter = cnum

            seen_verses: set[int] = set()
            prev_verse = None
            for verse in chapter["verses"]:
                vnum = verse["number"]
                vtext = verse["text"]

                if vnum in seen_verses:
                    issues.append(f"{path.name}: capitulo {cnum}, versiculo {vnum} duplicado")
                elif prev_verse is not None and vnum < prev_verse:
                    issues.append(f"{path.name}: capitulo {cnum}, versiculo {vnum} fora de ordem (apos {prev_verse})")
                seen_verses.add(vnum)
                prev_verse = vnum

                if not vtext.strip():
                    issues.append(f"{path.name}: capitulo {cnum}, versiculo {vnum} vazio")

                match = CONTROL_CHARS.search(vtext)
                if match:
                    issues.append(
                        f"{path.name}: capitulo {cnum}, versiculo {vnum} contem caractere de "
                        f"controle 0x{ord(match.group()):02x}"
                    )
    except (KeyError, TypeError) as exc:
        issues.append(f"{path.name}: estrutura inesperada ({exc})")

    return issues


def validate_version(version_dir: Path) -> list[str]:
    json_dir = version_dir / "json"
    if not json_dir.is_dir():
        return ["pasta json/ nao encontrada"]

    counts, files_hash, abbrevs = compute_counts_and_hash(version_dir.name, json_dir)
    completeness = compute_completeness(abbrevs)

    issues = validate_meta(version_dir, counts, completeness, files_hash)
    for path in sorted(json_dir.glob("*.json")):
        issues.extend(validate_book(path))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        dest="version",
        help="Sigla da versao a validar (ex: otb). Se omitido, valida todas as versoes em versoes/.",
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

    total_issues = 0
    versions_with_issues = 0
    for version_dir in version_dirs:
        print(f"=== {version_dir.name} ===")
        issues = validate_version(version_dir)
        if issues:
            versions_with_issues += 1
            total_issues += len(issues)
            for issue in issues:
                print(f"  ERRO: {issue}")
        else:
            print("  OK: nenhum problema encontrado.")

    print(
        f"\nResumo: {len(version_dirs)} versao(oes) verificada(s), "
        f"{versions_with_issues} com problema(s), {total_issues} problema(s) no total."
    )
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
