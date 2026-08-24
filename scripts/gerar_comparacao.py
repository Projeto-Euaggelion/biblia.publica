#!/usr/bin/env python3
"""Gera docs/texto-biblico/comparacao-versiculos.md a partir de versoes/{versao}/json/*.json,
comparando o texto de versiculos-chave (Joao 3:16, Genesis 1:1, Salmo 23:1)
lado a lado entre todas as versoes do repositorio.

O arquivo gerado nao deve ser editado manualmente - rode este script
novamente apos qualquer mudanca no texto de uma versao. Ver
docs/scripts/gerar-comparacao.md para o uso.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSOES_DIR = REPO_ROOT / "versoes"
OUTPUT_PATH = REPO_ROOT / "docs" / "texto-biblico" / "comparacao-versiculos.md"

# (rotulo de exibicao, sigla do livro, capitulo, versiculo). Siglas conforme a
# tabela de livros em docs/estrutura-arquivos/estrutura-xml.md.
VERSICULOS_CHAVE = [
    ("João 3:16", "jo", 3, 16),
    ("Gênesis 1:1", "gn", 1, 1),
    ("Salmo 23:1", "sl", 23, 1),
]


def load_meta(version_dir: Path) -> dict:
    meta_path = version_dir / "meta.json"
    if not meta_path.is_file():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))


def find_verse_text(version_dir: Path, version: str, abbrev: str, chapter: int, verse: int) -> str | None:
    book_path = version_dir / "json" / f"{version}-{abbrev}.json"
    if not book_path.is_file():
        return None
    book = json.loads(book_path.read_text(encoding="utf-8"))
    for capitulo in book["chapters"]:
        if capitulo["number"] != chapter:
            continue
        for versiculo in capitulo["verses"]:
            if versiculo["number"] == verse:
                return versiculo["text"]
        return None
    return None


def build_markdown(version_dirs: list[Path]) -> str:
    lines = [
        "# Comparação de versículos-chave",
        "",
        "> Este arquivo é gerado automaticamente pelo workflow"
        " `.github/workflows/atualizar-comparacao.yml`, que roda"
        " `scripts/gerar_comparacao.py` a cada push na `main` que altere"
        " `versoes/**/json/**` ou `versoes/**/meta.json`. **Não edite este arquivo"
        " manualmente** — para corrigir uma informação, altere o `.json` da versão"
        " correspondente.",
        "",
        "Compara o texto de três versículos amplamente citados entre todas as versões"
        " do repositório, lado a lado.",
        "",
    ]

    for titulo, abbrev, chapter, verse in VERSICULOS_CHAVE:
        lines.append(f"## {titulo}")
        lines.append("")
        lines.append("| Versão | Texto |")
        lines.append("|---|---|")
        for version_dir in version_dirs:
            version = version_dir.name
            nome = load_meta(version_dir).get("name") or version
            texto = find_verse_text(version_dir, version, abbrev, chapter, verse)
            texto_md = texto.replace("|", "\\|") if texto is not None else "*(não disponível nesta versão)*"
            lines.append(f"| {nome} (`{version}`) | {texto_md} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    if not VERSOES_DIR.is_dir():
        print(f"erro: pasta de versoes nao encontrada ({VERSOES_DIR})", file=sys.stderr)
        return 1

    version_dirs = sorted(d for d in VERSOES_DIR.iterdir() if d.is_dir() and (d / "json").is_dir())
    if not version_dirs:
        print("erro: nenhuma versao com pasta json/ encontrada", file=sys.stderr)
        return 1

    OUTPUT_PATH.write_text(build_markdown(version_dirs), encoding="utf-8")
    print(f"{OUTPUT_PATH.relative_to(REPO_ROOT)} gerado ({len(version_dirs)} versao(oes)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
