#!/usr/bin/env python3
"""Valida a estrutura dos arquivos versoes/{versao}/json/*.json e/ou
compara o conteudo convertido entre xml/ e json/ de cada versao.

Modo "estrutura" verifica: contagem de livros/capitulos/versiculos e
completude declaradas em meta.json batem com os arquivos json/ atuais;
ausencia de versiculos vazios ou duplicados; ordem crescente de
capitulos e versiculos; codificacao UTF-8 valida sem caracteres de
controle indevidos.

Modo "diff" verifica, por livro, se xml/ e json/ representam
exatamente o mesmo texto (mesmos capitulos, mesmos versiculos, mesmo
texto por versiculo).

Modo "schema" verifica, por livro, se o .json valida contra
docs/schema/biblia.schema.json (JSON Schema Draft 2020-12), e requer o
pacote jsonschema (ver scripts/requirements.txt).

Modo "xsd" verifica, por livro, se o .xml valida contra
docs/schema/biblia.xsd, e requer o pacote lxml (ver
scripts/requirements.txt).

Reaproveita o calculo de contagens/completude/hash de
scripts/gerar_meta.py e o parser de XML de scripts/xml_to_json.py (ver
docs/estrutura-arquivos/estrutura-meta.md e estrutura-xml.md).

Retorna exit code 1 se algum problema for encontrado, 0 caso contrario.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"
SCHEMA_PATH = REPO_ROOT / "docs" / "schema" / "biblia.schema.json"
XSD_PATH = REPO_ROOT / "docs" / "schema" / "biblia.xsd"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_meta import compute_completeness, compute_counts_and_hash  # noqa: E402
from xml_to_json import parse_book  # noqa: E402

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


def load_schema_validator():
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit(
            "erro: o modo 'schema' requer o pacote jsonschema "
            "(pip install -r scripts/requirements.txt)"
        ) from exc

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    return validator_cls(schema)


def validate_book_schema(path: Path, validator) -> list[str]:
    try:
        book = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: JSON invalido ({exc})"]

    issues = []
    for error in sorted(validator.iter_errors(book), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(p) for p in error.absolute_path) or "(raiz)"
        issues.append(f"{path.name}: {location}: {error.message}")
    return issues


def validate_version_schema(version_dir: Path, validator) -> list[str]:
    json_dir = version_dir / "json"
    if not json_dir.is_dir():
        return ["pasta json/ nao encontrada"]

    issues = []
    for path in sorted(json_dir.glob("*.json")):
        issues.extend(validate_book_schema(path, validator))
    return issues


def load_xsd_validator():
    try:
        from lxml import etree
    except ImportError as exc:
        raise SystemExit(
            "erro: o modo 'xsd' requer o pacote lxml "
            "(pip install -r scripts/requirements.txt)"
        ) from exc

    return etree.XMLSchema(etree.parse(str(XSD_PATH)))


def validate_book_xsd(path: Path, validator) -> list[str]:
    from lxml import etree

    try:
        doc = etree.parse(str(path))
    except etree.XMLSyntaxError as exc:
        return [f"{path.name}: XML invalido ({exc})"]

    if validator.validate(doc):
        return []
    return [f"{path.name}: {error.message} (linha {error.line})" for error in validator.error_log]


def validate_version_xsd(version_dir: Path, validator) -> list[str]:
    xml_dir = version_dir / "xml"
    if not xml_dir.is_dir():
        return ["pasta xml/ nao encontrada"]

    issues = []
    for path in sorted(xml_dir.glob("*.xml")):
        issues.extend(validate_book_xsd(path, validator))
    return issues


def compare_book(xml_path: Path, json_path: Path) -> list[str]:
    if not xml_path.is_file():
        return [f"{json_path.name}: xml correspondente nao encontrado ({xml_path.name})"]
    if not json_path.is_file():
        return [f"{xml_path.name}: json correspondente nao encontrado ({json_path.name})"]

    try:
        xml_book = parse_book(xml_path)
    except ET.ParseError as exc:
        return [f"{xml_path.name}: XML invalido ({exc})"]

    try:
        json_book = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{json_path.name}: JSON invalido ({exc})"]

    label = xml_path.stem
    issues = []

    xml_chapters = {c["number"]: c for c in xml_book["chapters"]}
    json_chapters = {c["number"]: c for c in json_book["chapters"]}

    for cnum in sorted(xml_chapters.keys() - json_chapters.keys()):
        issues.append(f"{label}: capitulo {cnum} presente no xml mas ausente no json")
    for cnum in sorted(json_chapters.keys() - xml_chapters.keys()):
        issues.append(f"{label}: capitulo {cnum} presente no json mas ausente no xml")

    for cnum in sorted(xml_chapters.keys() & json_chapters.keys()):
        xml_verses = {v["number"]: v["text"] for v in xml_chapters[cnum]["verses"]}
        json_verses = {v["number"]: v["text"] for v in json_chapters[cnum]["verses"]}

        for vnum in sorted(xml_verses.keys() - json_verses.keys()):
            issues.append(f"{label}: capitulo {cnum}, versiculo {vnum} presente no xml mas ausente no json")
        for vnum in sorted(json_verses.keys() - xml_verses.keys()):
            issues.append(f"{label}: capitulo {cnum}, versiculo {vnum} presente no json mas ausente no xml")

        for vnum in sorted(xml_verses.keys() & json_verses.keys()):
            if xml_verses[vnum] != json_verses[vnum]:
                issues.append(f"{label}: capitulo {cnum}, versiculo {vnum} texto diverge entre xml e json")

    return issues


def compare_version(version_dir: Path) -> list[str]:
    xml_dir = version_dir / "xml"
    json_dir = version_dir / "json"
    if not xml_dir.is_dir():
        return ["pasta xml/ nao encontrada"]
    if not json_dir.is_dir():
        return ["pasta json/ nao encontrada"]

    stems = {p.stem for p in xml_dir.glob("*.xml")} | {p.stem for p in json_dir.glob("*.json")}

    issues = []
    for stem in sorted(stems):
        issues.extend(compare_book(xml_dir / f"{stem}.xml", json_dir / f"{stem}.json"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        dest="version",
        help="Sigla da versao a validar (ex: blivre). Se omitido, valida todas as versoes em versoes/.",
    )
    parser.add_argument(
        "--check",
        dest="check",
        choices=["estrutura", "diff", "schema", "xsd", "tudo"],
        default="tudo",
        help=(
            "'estrutura' valida apenas os arquivos json/ e o meta.json; 'diff' apenas compara "
            "xml/ com json/; 'schema' valida json/ contra docs/schema/biblia.schema.json; "
            "'xsd' valida xml/ contra docs/schema/biblia.xsd; 'tudo' (padrao) executa os quatro."
        ),
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

    schema_validator = load_schema_validator() if args.check in ("schema", "tudo") else None
    xsd_validator = load_xsd_validator() if args.check in ("xsd", "tudo") else None

    total_issues = 0
    versions_with_issues = 0
    for version_dir in version_dirs:
        print(f"=== {version_dir.name} ===")
        issues: list[tuple[str, str]] = []
        if args.check in ("estrutura", "tudo"):
            issues.extend(("estrutura", issue) for issue in validate_version(version_dir))
        if args.check in ("diff", "tudo"):
            issues.extend(("diff", issue) for issue in compare_version(version_dir))
        if args.check in ("schema", "tudo"):
            issues.extend(("schema", issue) for issue in validate_version_schema(version_dir, schema_validator))
        if args.check in ("xsd", "tudo"):
            issues.extend(("xsd", issue) for issue in validate_version_xsd(version_dir, xsd_validator))

        if issues:
            versions_with_issues += 1
            total_issues += len(issues)
            for check, issue in issues:
                print(f"  ERRO [{check}]: {issue}")
        else:
            print("  OK: nenhum problema encontrado.")

    print(
        f"\nResumo: {len(version_dirs)} versao(oes) verificada(s), "
        f"{versions_with_issues} com problema(s), {total_issues} problema(s) no total."
    )
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
