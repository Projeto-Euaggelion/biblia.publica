import { fetchIndex, fetchBook } from "./api.js";
import { booksForVersion, bookByAbbrev } from "./books.js";

const appEl = document.getElementById("app");
const breadcrumbEl = document.getElementById("breadcrumb");

function clear(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

function setBreadcrumb(items) {
  clear(breadcrumbEl);
  const ol = document.createElement("ol");
  items.forEach((item, i) => {
    const li = document.createElement("li");
    if (item.href && i < items.length - 1) {
      const a = document.createElement("a");
      a.href = item.href;
      a.textContent = item.label;
      li.appendChild(a);
    } else {
      li.textContent = item.label;
      li.setAttribute("aria-current", "page");
    }
    ol.appendChild(li);
  });
  breadcrumbEl.appendChild(ol);
}

function showLoading(message) {
  clear(appEl);
  const p = document.createElement("p");
  p.className = "status";
  p.textContent = message || "Carregando…";
  appEl.appendChild(p);
}

function showError(message) {
  clear(appEl);
  const p = document.createElement("p");
  p.className = "status error";
  p.textContent = message;
  appEl.appendChild(p);
}

async function renderHome() {
  document.title = "biblia.publica";
  setBreadcrumb([{ label: "Versões" }]);
  showLoading("Carregando versões…");

  let index;
  try {
    index = await fetchIndex();
  } catch (err) {
    showError(`Não foi possível carregar a lista de versões (${err.message}).`);
    return;
  }

  clear(appEl);
  const ul = document.createElement("ul");
  ul.className = "version-list";
  for (const version of index.versions) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = `#/${version.abbrev}`;
    a.className = "version-link";

    const name = document.createElement("span");
    name.className = "version-name";
    name.textContent = version.name || version.abbrev;
    a.appendChild(name);

    const meta = document.createElement("span");
    meta.className = "version-meta";
    const bookCount = version.counts?.books ?? "?";
    const status = version.completeness?.status === "complete" ? "completa" : "incompleta";
    meta.textContent = `${version.abbrev} · ${bookCount} livros · ${status}`;
    a.appendChild(meta);

    li.appendChild(a);
    ul.appendChild(li);
  }
  appEl.appendChild(ul);
}

async function renderBookList(versao) {
  document.title = `${versao} — biblia.publica`;
  showLoading("Carregando livros…");

  let index;
  try {
    index = await fetchIndex();
  } catch (err) {
    showError(`Não foi possível carregar a lista de versões (${err.message}).`);
    return;
  }

  const version = index.versions.find((v) => v.abbrev === versao);
  if (!version) {
    showError(`Versão '${versao}' não encontrada.`);
    return;
  }

  setBreadcrumb([
    { label: "Versões", href: "#/" },
    { label: version.name || version.abbrev },
  ]);

  clear(appEl);
  const books = booksForVersion(version);

  for (const testament of ["AT", "NT"]) {
    const testBooks = books.filter((b) => b.testament === testament);
    if (testBooks.length === 0) continue;

    const h2 = document.createElement("h2");
    h2.textContent = testament === "AT" ? "Antigo Testamento" : "Novo Testamento";
    appEl.appendChild(h2);

    const ul = document.createElement("ul");
    ul.className = "book-list";
    for (const book of testBooks) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `#/${versao}/${book.abbrev}`;
      a.textContent = book.name;
      li.appendChild(a);
      ul.appendChild(li);
    }
    appEl.appendChild(ul);
  }
}

async function renderChapterList(versao, abbrev) {
  const staticBook = bookByAbbrev(abbrev);
  document.title = `${staticBook ? staticBook.name : abbrev} — biblia.publica`;
  showLoading("Carregando capítulos…");

  let data;
  try {
    data = await fetchBook(versao, abbrev);
  } catch (err) {
    showError(`Não foi possível carregar este livro (${err.message}).`);
    return;
  }

  setBreadcrumb([
    { label: "Versões", href: "#/" },
    { label: versao, href: `#/${versao}` },
    { label: data.name },
  ]);

  clear(appEl);
  const ul = document.createElement("ul");
  ul.className = "chapter-list";
  for (const chapter of data.chapters) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = `#/${versao}/${abbrev}/${chapter.number}`;
    a.textContent = String(chapter.number);
    li.appendChild(a);
    ul.appendChild(li);
  }
  appEl.appendChild(ul);
}

function buildChapterNav(data, versao, abbrev, capituloNum) {
  const nav = document.createElement("div");
  nav.className = "chapter-nav";
  const idx = data.chapters.findIndex((c) => c.number === capituloNum);
  const prev = data.chapters[idx - 1];
  const next = data.chapters[idx + 1];

  if (prev) {
    const a = document.createElement("a");
    a.href = `#/${versao}/${abbrev}/${prev.number}`;
    a.textContent = "‹ Capítulo anterior";
    nav.appendChild(a);
  } else {
    nav.appendChild(document.createElement("span"));
  }

  if (next) {
    const a = document.createElement("a");
    a.href = `#/${versao}/${abbrev}/${next.number}`;
    a.textContent = "Próximo capítulo ›";
    a.className = "next";
    nav.appendChild(a);
  }

  return nav;
}

async function renderChapter(versao, abbrev, capituloNum) {
  const staticBook = bookByAbbrev(abbrev);
  document.title = `${staticBook ? staticBook.name : abbrev} ${capituloNum} — biblia.publica`;
  showLoading("Carregando capítulo…");

  let data;
  try {
    data = await fetchBook(versao, abbrev);
  } catch (err) {
    showError(`Não foi possível carregar este livro (${err.message}).`);
    return;
  }

  const chapter = data.chapters.find((c) => c.number === capituloNum);
  if (!chapter) {
    showError(`Capítulo ${capituloNum} não encontrado em ${data.name}.`);
    return;
  }

  setBreadcrumb([
    { label: "Versões", href: "#/" },
    { label: versao, href: `#/${versao}` },
    { label: data.name, href: `#/${versao}/${abbrev}` },
    { label: String(capituloNum) },
  ]);

  clear(appEl);
  appEl.appendChild(buildChapterNav(data, versao, abbrev, capituloNum));

  const h2 = document.createElement("h2");
  h2.textContent = `${data.name} ${capituloNum}`;
  appEl.appendChild(h2);

  const ol = document.createElement("ol");
  ol.className = "verse-list";
  for (const verse of chapter.verses) {
    const li = document.createElement("li");
    li.value = verse.number;
    li.textContent = verse.text;
    ol.appendChild(li);
  }
  appEl.appendChild(ol);

  appEl.appendChild(buildChapterNav(data, versao, abbrev, capituloNum));
}

function parseHash() {
  const raw = window.location.hash.replace(/^#\/?/, "");
  return raw.split("/").filter(Boolean).map(decodeURIComponent);
}

function route() {
  const [versao, abbrev, capitulo] = parseHash();

  if (!versao) {
    renderHome();
  } else if (!abbrev) {
    renderBookList(versao);
  } else if (!capitulo) {
    renderChapterList(versao, abbrev);
  } else {
    const capituloNum = Number.parseInt(capitulo, 10);
    if (Number.isNaN(capituloNum)) {
      showError(`Capítulo inválido: '${capitulo}'.`);
      return;
    }
    renderChapter(versao, abbrev, capituloNum);
  }
}

window.addEventListener("hashchange", route);
route();
