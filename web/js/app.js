import { fetchIndex, fetchBook } from "./api.js";
import { booksForVersion, bookByAbbrev, bookPosition } from "./books.js";

const appEl = document.getElementById("app");
const breadcrumbEl = document.getElementById("breadcrumb");

function clear(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

// Pequeno helper de construcao de DOM — nao e um framework, so evita
// repetir document.createElement/appendChild em cada render*().
function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value == null) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else node.setAttribute(key, value);
  }
  for (const child of Array.isArray(children) ? children : [children]) {
    if (child == null) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

function setBreadcrumb(items) {
  clear(breadcrumbEl);
  if (items.length === 0) return;
  const ol = el("ol");
  items.forEach((item, i) => {
    const isLast = i === items.length - 1;
    const li = el(
      "li",
      isLast ? { "aria-current": "page" } : {},
      isLast ? item.label : el("a", { href: item.href, text: item.label })
    );
    ol.appendChild(li);
  });
  breadcrumbEl.appendChild(ol);
}

function showLoading(message) {
  clear(appEl);
  appEl.appendChild(el("p", { class: "status", text: message || "Carregando…" }));
}

function showError(message) {
  clear(appEl);
  appEl.appendChild(el("p", { class: "status error", text: message }));
}

// ---------- componentes reutilizaveis ----------

function statBlock(value, label) {
  return el("div", { class: "stat" }, [
    el("span", { class: "stat__value", text: String(value) }),
    el("span", { class: "stat__label", text: label }),
  ]);
}

function versionCard(version) {
  const bookCount = version.counts?.books ?? "?";
  const status = version.completeness?.status === "complete" ? "Completa" : "Incompleta";
  const bits = [version.abbrev];
  if (version.year) bits.push(String(version.year));
  bits.push(`${bookCount} livros`, status);
  return el("a", { class: "version-card", href: `#/${version.abbrev}` }, [
    el("span", { class: "version-card__abbrev", text: version.abbrev }),
    el("span", { class: "version-card__name", text: version.name || version.abbrev }),
    el("span", { class: "version-card__meta", text: bits.join(" · ") }),
  ]);
}

function otherVersionsLine(versions, currentAbbrev) {
  const others = versions.filter((v) => v.abbrev !== currentAbbrev);
  if (others.length === 0) return [];
  const nodes = ["Para outras traduções, "];
  others.forEach((v, i) => {
    nodes.push(el("a", { href: `#/${v.abbrev}`, text: v.abbrev }));
    if (i < others.length - 2) nodes.push(", ");
    else if (i === others.length - 2) nodes.push(" ou ");
  });
  nodes.push(".");
  return nodes;
}

function bookRow(book, versao) {
  return el("li", { class: "book-row" }, [
    el("span", { class: "book-row__num", text: String(bookPosition(book.abbrev)) }),
    el("a", { class: "book-row__name", href: `#/${versao}/${book.abbrev}`, text: book.name }),
    el("span", { class: "book-row__chapters", text: `${book.chapters} cap.` }),
  ]);
}

function bookColumns(versionEntry, versao) {
  const books = booksForVersion(versionEntry);
  const wrap = el("div", { class: "book-columns" });
  for (const testament of ["AT", "NT"]) {
    const list = books.filter((b) => b.testament === testament);
    if (list.length === 0) continue;
    wrap.appendChild(
      el("div", { class: "book-column" }, [
        el("h3", {}, [
          testament === "AT" ? "Antigo Testamento" : "Novo Testamento",
          el("span", { class: "count", text: `${list.length} livros` }),
        ]),
        el(
          "ul",
          { class: "book-list" },
          list.map((b) => bookRow(b, versao))
        ),
      ])
    );
  }
  return wrap;
}

// Monta o href de uma pill de versao, tentando preservar o livro/capitulo
// atual — só cai pra raiz da versao se o livro nao existir naquela versao.
function versionSwitchHref(target, currentVersao, abbrev, capitulo) {
  if (!abbrev) return `#/${target.abbrev}`;
  const missing = new Set(target.completeness?.missingBooks ?? []);
  if (missing.has(abbrev)) return `#/${target.abbrev}`;
  return capitulo ? `#/${target.abbrev}/${abbrev}/${capitulo}` : `#/${target.abbrev}/${abbrev}`;
}

function versionPills(versions, currentVersao, abbrev, capitulo) {
  return el(
    "nav",
    { class: "version-pills", "aria-label": "Trocar de tradução" },
    versions.map((v) =>
      el("a", {
        class: "pill" + (v.abbrev === currentVersao ? " is-active" : ""),
        href: versionSwitchHref(v, currentVersao, abbrev, capitulo),
        text: v.abbrev,
      })
    )
  );
}

function versionMetaLine(version) {
  const bits = [];
  if (version.year) bits.push(String(version.year));
  if (version.language) bits.push(version.language);
  bits.push(version.completeness?.status === "complete" ? "Cânon completo" : "Incompleta");
  if (version.textualBasis) bits.push(version.textualBasis);
  return bits.join(" · ");
}

function chapterNav(data, versao, abbrev, capituloNum, withBackLink) {
  const idx = data.chapters.findIndex((c) => c.number === capituloNum);
  const prev = data.chapters[idx - 1];
  const next = data.chapters[idx + 1];
  const nav = el("div", { class: "chapter-nav" });
  if (prev) nav.appendChild(el("a", { href: `#/${versao}/${abbrev}/${prev.number}`, text: "‹ Anterior" }));
  if (withBackLink) {
    nav.appendChild(
      el("a", { class: "back", href: `#/${versao}/${abbrev}`, text: `Todos os capítulos de ${data.name}` })
    );
  }
  if (next) nav.appendChild(el("a", { class: "next", href: `#/${versao}/${abbrev}/${next.number}`, text: "Próximo ›" }));
  return nav;
}

// ---------- paginas ----------

async function renderHome() {
  document.title = "biblia.publica";
  setBreadcrumb([]);
  showLoading("Carregando versões…");

  let index;
  try {
    index = await fetchIndex();
  } catch (err) {
    showError(`Não foi possível carregar a lista de versões (${err.message}).`);
    return;
  }

  clear(appEl);

  const reference = index.versions.find((v) => v.completeness?.status === "complete") || index.versions[0];
  const totalBooks = reference?.counts?.books ?? "—";
  const totalChapters = reference?.counts?.chapters ?? "—";
  const totalVersions = index.versions.length;

  appEl.appendChild(
    el("section", { class: "hero" }, [
      el("span", { class: "hero__letter", "aria-hidden": "true", text: "B" }),
      el("p", { class: "eyebrow", text: "Texto bíblico · código aberto" }),
      el("h1", { class: "hero__title" }, ["A ", el("em", { text: "Bíblia" }), ` completa, em ${totalVersions} traduções.`]),
      el("p", {
        class: "hero__lead",
        text: `${totalBooks} livros, ${totalChapters} capítulos, publicados em domínio público e Creative Commons — leia direto no navegador, sem clonar nada.`,
      }),
      el("div", { class: "stats" }, [
        statBlock(totalBooks, "livros"),
        statBlock(totalChapters, "capítulos"),
        statBlock(totalVersions, "traduções"),
      ]),
    ])
  );

  appEl.appendChild(
    el("section", { class: "section" }, [
      el("div", { class: "section__header" }, [
        el("p", { class: "eyebrow", text: "Escolha sua tradução" }),
        el("h2", { class: "section__title" }, ["Várias ", el("em", { text: "traduções" }), ", uma mesma palavra."]),
      ]),
      el(
        "div",
        { class: "version-grid" },
        index.versions.map((v) => versionCard(v))
      ),
    ])
  );

  if (reference) {
    const altSection = el("section", { class: "section section--alt" });
    altSection.appendChild(
      el("div", { class: "section__inner" }, [
        el("div", { class: "section__header" }, [
          el("p", { class: "eyebrow", text: `${reference.name || reference.abbrev} · padrão` }),
          el("h2", { class: "section__title", text: `Os ${totalBooks} livros da Bíblia` }),
          el("p", { class: "section__subtitle" }, otherVersionsLine(index.versions, reference.abbrev)),
        ]),
        bookColumns(reference, reference.abbrev),
      ])
    );
    appEl.appendChild(altSection);
  }
}

async function renderVersionPage(versao) {
  showLoading("Carregando versão…");

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

  document.title = `${version.name || versao} — biblia.publica`;
  setBreadcrumb([{ label: "Versões", href: "#/" }, { label: version.name || versao }]);

  clear(appEl);
  appEl.appendChild(
    el("section", { class: "book-hero" }, [
      el("p", { class: "eyebrow", text: `Tradução · ${version.abbrev}` }),
      el("h1", { class: "book-hero__title", text: version.name || version.abbrev }),
      el("p", { class: "book-hero__meta", text: versionMetaLine(version) }),
      versionPills(index.versions, versao),
    ])
  );

  appEl.appendChild(el("section", { class: "section" }, [bookColumns(version, version.abbrev)]));
}

async function renderBookPage(versao, abbrev) {
  showLoading("Carregando capítulos…");

  let index, data;
  try {
    [index, data] = await Promise.all([fetchIndex(), fetchBook(versao, abbrev)]);
  } catch (err) {
    showError(`Não foi possível carregar este livro (${err.message}).`);
    return;
  }

  const version = index.versions.find((v) => v.abbrev === versao);
  const staticBook = bookByAbbrev(abbrev);
  const testamentLabel = staticBook?.testament === "NT" ? "Novo Testamento" : "Antigo Testamento";
  const position = bookPosition(abbrev);

  document.title = `${data.name} — biblia.publica`;
  setBreadcrumb([
    { label: "Versões", href: "#/" },
    { label: version?.name || versao, href: `#/${versao}` },
    { label: data.name },
  ]);

  clear(appEl);
  appEl.appendChild(
    el("section", { class: "book-hero" }, [
      el("p", { class: "eyebrow", text: `${testamentLabel} · Livro ${position}` }),
      el("h1", { class: "book-hero__title", text: data.name }),
      el("p", {
        class: "book-hero__meta",
        text: `${data.chapters.length} capítulos · Tradução ${version?.name || versao}`,
      }),
      versionPills(index.versions, versao, abbrev),
    ])
  );

  const grid = el(
    "div",
    { class: "chapter-grid" },
    data.chapters.map((chapter) =>
      el("a", { class: "chapter-card", href: `#/${versao}/${abbrev}/${chapter.number}` }, [
        el("span", { class: "chapter-card__num", text: String(chapter.number) }),
        el("span", { class: "chapter-card__verses", text: `${chapter.verses.length} v.` }),
      ])
    )
  );
  appEl.appendChild(el("section", { class: "section" }, [el("h2", { text: "Capítulos" }), grid]));
}

async function renderChapterPage(versao, abbrev, capituloNum) {
  showLoading("Carregando capítulo…");

  let index, data;
  try {
    [index, data] = await Promise.all([fetchIndex(), fetchBook(versao, abbrev)]);
  } catch (err) {
    showError(`Não foi possível carregar este livro (${err.message}).`);
    return;
  }

  const chapter = data.chapters.find((c) => c.number === capituloNum);
  if (!chapter) {
    showError(`Capítulo ${capituloNum} não encontrado em ${data.name}.`);
    return;
  }

  const version = index.versions.find((v) => v.abbrev === versao);
  const staticBook = bookByAbbrev(abbrev);
  const testamentLabel = staticBook?.testament === "NT" ? "Novo Testamento" : "Antigo Testamento";

  document.title = `${data.name} ${capituloNum} — biblia.publica`;
  setBreadcrumb([
    { label: "Versões", href: "#/" },
    { label: version?.name || versao, href: `#/${versao}` },
    { label: data.name, href: `#/${versao}/${abbrev}` },
    { label: String(capituloNum) },
  ]);

  clear(appEl);
  appEl.appendChild(
    el("section", { class: "chapter-hero" }, [
      el("p", { class: "eyebrow", text: `${testamentLabel} · ${version?.name || versao}` }),
      el("p", { class: "chapter-hero__book", text: data.name }),
      el("h1", { class: "chapter-hero__num", text: String(capituloNum) }),
      el("p", { class: "chapter-hero__count", text: `${chapter.verses.length} versículos` }),
      versionPills(index.versions, versao, abbrev, capituloNum),
    ])
  );

  appEl.appendChild(chapterNav(data, versao, abbrev, capituloNum, false));

  appEl.appendChild(
    el(
      "ol",
      { class: "verse-list" },
      chapter.verses.map((verse) =>
        el("li", {}, [el("sup", { class: "verse-num", text: String(verse.number) }), verse.text])
      )
    )
  );

  appEl.appendChild(chapterNav(data, versao, abbrev, capituloNum, true));
}

// ---------- roteamento ----------

function parseHash() {
  const raw = window.location.hash.replace(/^#\/?/, "");
  return raw.split("/").filter(Boolean).map(decodeURIComponent);
}

function route() {
  const [versao, abbrev, capitulo] = parseHash();

  if (!versao) {
    renderHome();
  } else if (!abbrev) {
    renderVersionPage(versao);
  } else if (!capitulo) {
    renderBookPage(versao, abbrev);
  } else {
    const capituloNum = Number.parseInt(capitulo, 10);
    if (Number.isNaN(capituloNum)) {
      showError(`Capítulo inválido: '${capitulo}'.`);
      return;
    }
    renderChapterPage(versao, abbrev, capituloNum);
  }
}

window.addEventListener("hashchange", route);
route();
