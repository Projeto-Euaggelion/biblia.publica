// Tabela canonica dos 66 livros do canon protestante, na ordem tradicional,
// com o numero de capitulos de cada um. Mesma fonte de
// docs/estrutura-arquivos/estrutura-xml.md#tabela-de-livros; usada apenas
// para montar a navegacao (lista/ordem/contagem) sem precisar buscar todos
// os livros de uma versao so pra listar — o texto em si sempre vem do
// .json real da versao (ver js/api.js).
export const BOOKS = [
  { abbrev: "gn", name: "Gênesis", testament: "AT", chapters: 50 },
  { abbrev: "ex", name: "Êxodo", testament: "AT", chapters: 40 },
  { abbrev: "lv", name: "Levítico", testament: "AT", chapters: 27 },
  { abbrev: "nm", name: "Números", testament: "AT", chapters: 36 },
  { abbrev: "dt", name: "Deuteronômio", testament: "AT", chapters: 34 },
  { abbrev: "js", name: "Josué", testament: "AT", chapters: 24 },
  { abbrev: "jz", name: "Juízes", testament: "AT", chapters: 21 },
  { abbrev: "rt", name: "Rute", testament: "AT", chapters: 4 },
  { abbrev: "1sm", name: "1 Samuel", testament: "AT", chapters: 31 },
  { abbrev: "2sm", name: "2 Samuel", testament: "AT", chapters: 24 },
  { abbrev: "1rs", name: "1 Reis", testament: "AT", chapters: 22 },
  { abbrev: "2rs", name: "2 Reis", testament: "AT", chapters: 25 },
  { abbrev: "1cr", name: "1 Crônicas", testament: "AT", chapters: 29 },
  { abbrev: "2cr", name: "2 Crônicas", testament: "AT", chapters: 36 },
  { abbrev: "ed", name: "Esdras", testament: "AT", chapters: 10 },
  { abbrev: "ne", name: "Neemias", testament: "AT", chapters: 13 },
  { abbrev: "et", name: "Ester", testament: "AT", chapters: 10 },
  { abbrev: "job", name: "Jó", testament: "AT", chapters: 42 },
  { abbrev: "sl", name: "Salmos", testament: "AT", chapters: 150 },
  { abbrev: "pv", name: "Provérbios", testament: "AT", chapters: 31 },
  { abbrev: "ec", name: "Eclesiastes", testament: "AT", chapters: 12 },
  { abbrev: "ct", name: "Cânticos", testament: "AT", chapters: 8 },
  { abbrev: "is", name: "Isaías", testament: "AT", chapters: 66 },
  { abbrev: "jr", name: "Jeremias", testament: "AT", chapters: 52 },
  { abbrev: "lm", name: "Lamentações de Jeremias", testament: "AT", chapters: 5 },
  { abbrev: "ez", name: "Ezequiel", testament: "AT", chapters: 48 },
  { abbrev: "dn", name: "Daniel", testament: "AT", chapters: 12 },
  { abbrev: "os", name: "Oséias", testament: "AT", chapters: 14 },
  { abbrev: "jl", name: "Joel", testament: "AT", chapters: 3 },
  { abbrev: "am", name: "Amós", testament: "AT", chapters: 9 },
  { abbrev: "ob", name: "Obadias", testament: "AT", chapters: 1 },
  { abbrev: "jn", name: "Jonas", testament: "AT", chapters: 4 },
  { abbrev: "mq", name: "Miquéias", testament: "AT", chapters: 7 },
  { abbrev: "na", name: "Naum", testament: "AT", chapters: 3 },
  { abbrev: "hc", name: "Habacuque", testament: "AT", chapters: 3 },
  { abbrev: "sf", name: "Sofonias", testament: "AT", chapters: 3 },
  { abbrev: "ag", name: "Ageu", testament: "AT", chapters: 2 },
  { abbrev: "zc", name: "Zacarias", testament: "AT", chapters: 14 },
  { abbrev: "ml", name: "Malaquias", testament: "AT", chapters: 4 },
  { abbrev: "mt", name: "Mateus", testament: "NT", chapters: 28 },
  { abbrev: "mc", name: "Marcos", testament: "NT", chapters: 16 },
  { abbrev: "lc", name: "Lucas", testament: "NT", chapters: 24 },
  { abbrev: "jo", name: "João", testament: "NT", chapters: 21 },
  { abbrev: "at", name: "Atos", testament: "NT", chapters: 28 },
  { abbrev: "rm", name: "Romanos", testament: "NT", chapters: 16 },
  { abbrev: "1co", name: "1 Coríntios", testament: "NT", chapters: 16 },
  { abbrev: "2co", name: "2 Coríntios", testament: "NT", chapters: 13 },
  { abbrev: "gl", name: "Gálatas", testament: "NT", chapters: 6 },
  { abbrev: "ef", name: "Efésios", testament: "NT", chapters: 6 },
  { abbrev: "fp", name: "Filipenses", testament: "NT", chapters: 4 },
  { abbrev: "cl", name: "Colossenses", testament: "NT", chapters: 4 },
  { abbrev: "1ts", name: "1 Tessalonicenses", testament: "NT", chapters: 5 },
  { abbrev: "2ts", name: "2 Tessalonicenses", testament: "NT", chapters: 3 },
  { abbrev: "1tm", name: "1 Timóteo", testament: "NT", chapters: 6 },
  { abbrev: "2tm", name: "2 Timóteo", testament: "NT", chapters: 4 },
  { abbrev: "tt", name: "Tito", testament: "NT", chapters: 3 },
  { abbrev: "fm", name: "Filemom", testament: "NT", chapters: 1 },
  { abbrev: "hb", name: "Hebreus", testament: "NT", chapters: 13 },
  { abbrev: "tg", name: "Tiago", testament: "NT", chapters: 5 },
  { abbrev: "1pe", name: "1 Pedro", testament: "NT", chapters: 5 },
  { abbrev: "2pe", name: "2 Pedro", testament: "NT", chapters: 3 },
  { abbrev: "1jo", name: "1 João", testament: "NT", chapters: 5 },
  { abbrev: "2jo", name: "2 João", testament: "NT", chapters: 1 },
  { abbrev: "3jo", name: "3 João", testament: "NT", chapters: 1 },
  { abbrev: "jd", name: "Judas", testament: "NT", chapters: 1 },
  { abbrev: "ap", name: "Apocalipse", testament: "NT", chapters: 22 },
];

export function booksForVersion(versionEntry) {
  const missing = new Set(versionEntry?.completeness?.missingBooks ?? []);
  return BOOKS.filter((book) => !missing.has(book.abbrev));
}

export function bookByAbbrev(abbrev) {
  return BOOKS.find((book) => book.abbrev === abbrev);
}

// Posicao do livro no canon completo (Gênesis = 1 ... Apocalipse = 66),
// independente de quais livros a versao atual possui.
export function bookPosition(abbrev) {
  return BOOKS.findIndex((book) => book.abbrev === abbrev) + 1;
}
