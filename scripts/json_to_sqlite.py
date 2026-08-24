#!/usr/bin/env python3
"""Gera versoes/{versao}/sql/{versao}.sqlite a partir de versoes/{versao}/json/*.json.

Cria um banco SQLite por versao com o schema documentado em
docs/estrutura-arquivos/estrutura-sql.md (tabelas books/chapters/verses),
sobrescrevendo o arquivo .sqlite existente a cada execucao.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"

SCHEMA = """
CREATE TABLE books (
    id     INTEGER PRIMARY KEY,
    abbrev TEXT NOT NULL UNIQUE,
    name   TEXT NOT NULL
);

CREATE TABLE chapters (
    id      INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    number  INTEGER NOT NULL,
    UNIQUE (book_id, number)
);

CREATE TABLE verses (
    id         INTEGER PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id),
    number     INTEGER NOT NULL,
    text       TEXT NOT NULL,
    UNIQUE (chapter_id, number)
);

CREATE INDEX idx_chapters_book_id ON chapters(book_id);
CREATE INDEX idx_verses_chapter_id ON verses(chapter_id);
"""


def build_database(version_dir: Path, sqlite_path: Path) -> dict:
    json_dir = version_dir / "json"
    json_files = sorted(json_dir.glob("*.json"))

    sqlite_path.unlink(missing_ok=True)
    conn = sqlite3.connect(sqlite_path)
    try:
        conn.executescript(SCHEMA)

        counts = {"books": 0, "chapters": 0, "verses": 0}
        for path in json_files:
            book = json.loads(path.read_text(encoding="utf-8"))

            cur = conn.execute(
                "INSERT INTO books (abbrev, name) VALUES (?, ?)",
                (book["abbrev"], book["name"]),
            )
            book_id = cur.lastrowid
            counts["books"] += 1

            for chapter in book["chapters"]:
                cur = conn.execute(
                    "INSERT INTO chapters (book_id, number) VALUES (?, ?)",
                    (book_id, chapter["number"]),
                )
                chapter_id = cur.lastrowid
                counts["chapters"] += 1

                conn.executemany(
                    "INSERT INTO verses (chapter_id, number, text) VALUES (?, ?, ?)",
                    [(chapter_id, verse["number"], verse["text"]) for verse in chapter["verses"]],
                )
                counts["verses"] += len(chapter["verses"])

        conn.commit()
    finally:
        conn.close()

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        dest="version",
        help="Sigla da versao a gerar (ex: blivre). Se omitido, gera para todas as versoes com pasta json/.",
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

    generated = 0
    for version_dir in version_dirs:
        json_dir = version_dir / "json"
        if not json_dir.is_dir():
            print(f"aviso: pasta json/ nao encontrada para '{version_dir.name}', pulando.", file=sys.stderr)
            continue

        sql_dir = version_dir / "sql"
        sql_dir.mkdir(parents=True, exist_ok=True)
        sqlite_path = sql_dir / f"{version_dir.name}.sqlite"

        counts = build_database(version_dir, sqlite_path)
        print(
            f"{version_dir.name}: {sqlite_path.relative_to(REPO_ROOT)} gerado "
            f"({counts['books']} livros, {counts['chapters']} capitulos, {counts['verses']} versiculos)."
        )
        generated += 1

    print(f"\nConcluido: {generated} versao(oes) gerada(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
