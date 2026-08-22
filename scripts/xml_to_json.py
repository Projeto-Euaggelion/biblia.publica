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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        required=True,
        dest="version",
        help="Nome da versao a converter (ex: blivre, otb, tb).",
    )
    parser.add_argument(
        "--book",
        required=True,
        dest="book",
        help="Abreviacao do livro a converter (ex: gn, mt) ou 'all' para converter todos os livros da versao.",
    )
    args = parser.parse_args()

    version_dir = VERSOES_DIR / args.version
    xml_dir = version_dir / "xml"
    json_dir = version_dir / "json"

    if not xml_dir.is_dir():
        print(f"erro: pasta xml nao encontrada para a versao '{args.version}' ({xml_dir})", file=sys.stderr)
        return 1

    if args.book.lower() == "all":
        xml_files = sorted(xml_dir.glob("*.xml"))
    else:
        xml_path = xml_dir / f"{args.version}-{args.book}.xml"
        if not xml_path.is_file():
            print(f"erro: arquivo nao encontrado para o livro '{args.book}' ({xml_path})", file=sys.stderr)
            return 1
        xml_files = [xml_path]

    total = 0
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
