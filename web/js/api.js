// Busca de dados: tudo via raw.githubusercontent.com, direto do conteudo da
// branch main do repositorio — nenhum dado e duplicado dentro de web/.
// docs/index.json (metadados/links por versao) e cada livro .json sao
// buscados sob demanda; livros ja buscados ficam em cache em memoria pela
// duracao da sessao (evita refetch ao trocar de capitulo).

const REPO = "Projeto-Euaggelion/biblia.publica";
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/main`;

const bookCache = new Map();
let indexPromise = null;

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`falha ao buscar ${url} (HTTP ${response.status})`);
  }
  return response.json();
}

export function fetchIndex() {
  if (!indexPromise) {
    indexPromise = fetchJson(`${RAW_BASE}/docs/index.json`).catch((err) => {
      indexPromise = null;
      throw err;
    });
  }
  return indexPromise;
}

export async function fetchBook(versao, abbrev) {
  const cacheKey = `${versao}/${abbrev}`;
  if (bookCache.has(cacheKey)) {
    return bookCache.get(cacheKey);
  }
  const book = await fetchJson(`${RAW_BASE}/versoes/${versao}/json/${versao}-${abbrev}.json`);
  bookCache.set(cacheKey, book);
  return book;
}
