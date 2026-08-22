"""Converte os arquivos JSON de versoes/*/json/*.json para XML em versoes/*/xml/*.xml, mantendo a mesma estrutura (livro -> capitulos -> versiculos), um livro por arquivo.
"""

import argparse
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"


def build_xml(book: dict) -> str:
    chapters = book["chapters"]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<book name={quoteattr(book["name"])} abbrev={quoteattr(book["abbrev"])} chapters="{len(chapters)}">',
    ]
    for chapter in chapters:
        lines.append(f'\t<chapter number="{chapter["number"]}">')
        for verse in chapter["verses"]:
            lines.append(
                f'\t\t<verse number="{verse["number"]}">{escape(verse["text"])}</verse>'
            )
        lines.append("\t</chapter>")
    lines.append("</book>")
    return "\n".join(lines) + "\n"


def convert_file(json_path: Path, xml_dir: Path) -> Path:
    with json_path.open("r", encoding="utf-8") as f:
        book = json.load(f)
    xml_dir.mkdir(parents=True, exist_ok=True)
    xml_path = xml_dir / (json_path.stem + ".xml")
    xml_path.write_text(build_xml(book), encoding="utf-8")
    return xml_path


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
    json_dir = version_dir / "json"
    xml_dir = version_dir / "xml"

    if not json_dir.is_dir():
        print(f"erro: pasta json nao encontrada para a versao '{args.version}' ({json_dir})", file=sys.stderr)
        return 1

    if args.book.lower() == "all":
        json_files = sorted(json_dir.glob("*.json"))
    else:
        json_path = json_dir / f"{args.version}-{args.book}.json"
        if not json_path.is_file():
            print(f"erro: arquivo nao encontrado para o livro '{args.book}' ({json_path})", file=sys.stderr)
            return 1
        json_files = [json_path]

    total = 0
    print(f"{version_dir.name}: convertendo {len(json_files)} arquivo(s)...")
    for json_path in json_files:
        try:
            xml_path = convert_file(json_path, xml_dir)
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"  erro ao converter {json_path}: {exc}", file=sys.stderr)
            continue
        print(f"  {json_path.name} -> {xml_path.relative_to(REPO_ROOT)}")
        total += 1

    print(f"\nConcluido: {total} arquivo(s) convertido(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
