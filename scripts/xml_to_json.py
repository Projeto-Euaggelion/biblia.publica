"""Converte os arquivos XML de versoes/*/xml/*.xml para JSON em versoes/*/json/*.json, mantendo a mesma estrutura (livro -> capitulos -> versiculos), um livro por arquivo.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"


def parse_book(xml_path: Path) -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    chapters = []
    for chapter_el in root.findall("chapter"):
        verses = [
            {
                "number": int(verse_el.get("number")),
                "text": verse_el.text or "",
            }
            for verse_el in chapter_el.findall("verse")
        ]
        chapters.append({
            "number": int(chapter_el.get("number")),
            "verses": verses,
        })

    return {
        "name": root.get("name"),
        "abbrev": root.get("abbrev"),
        "chapters": chapters,
    }


def convert_file(xml_path: Path, json_dir: Path) -> Path:
    book = parse_book(xml_path)
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir / (xml_path.stem + ".json")
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return json_path


def find_versions(versoes_dir: Path) -> list[Path]:
    return sorted(p for p in versoes_dir.iterdir() if p.is_dir() and (p / "xml").is_dir())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--versao",
        action="append",
        dest="versoes",
        help="Nome da versao a converter (ex: blivre, otb, tb). Pode ser usado varias vezes. "
             "Se omitido, converte todas as versoes encontradas em versoes/.",
    )
    args = parser.parse_args()

    if args.versoes:
        version_dirs = [VERSOES_DIR / v for v in args.versoes]
        for v in version_dirs:
            if not (v / "xml").is_dir():
                print(f"erro: pasta xml nao encontrada para a versao '{v.name}' ({v / 'xml'})", file=sys.stderr)
                return 1
    else:
        version_dirs = find_versions(VERSOES_DIR)

    total = 0
    for version_dir in version_dirs:
        xml_dir = version_dir / "xml"
        json_dir = version_dir / "json"
        xml_files = sorted(xml_dir.glob("*.xml"))
        print(f"{version_dir.name}: convertendo {len(xml_files)} arquivo(s)...")
        for xml_path in xml_files:
            try:
                json_path = convert_file(xml_path, json_dir)
            except ET.ParseError as exc:
                print(f"  erro ao converter {xml_path}: {exc}", file=sys.stderr)
                continue
            print(f"  {xml_path.name} -> {json_path.relative_to(REPO_ROOT)}")
            total += 1

    print(f"\nConcluido: {total} arquivo(s) convertido(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
