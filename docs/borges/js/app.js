(() => {
  "use strict";
  const L = window.LECTURES || [], C = window.COLLECTIONS || [], T = window.THEMES || {}, E = window.EPIGRAPHS || [];
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const roman = n => ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][n] || n;
  const coll = id => C.find(c => c.id === id) || {};
  const callNo = l => `${coll(l.collection).code} · ${roman(l.number)}`;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const norm = s => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  /* ---------- rotating epigraph ---------- */
  const epi = $(".epigraph");
  let ei = Math.floor(Math.random() * E.length);
  function showEpi() {
    if (!E.length) return;
    const e = E[ei % E.length];
    $("#epi-text").textContent = e.text;
    $("#epi-src").textContent = "— Borges, " + e.src;
  }
  showEpi();
  if (!reduce) setInterval(() => {
    if (document.hidden || $("#view-home").hidden) return;
    epi.classList.add("out");
    setTimeout(() => { ei++; showEpi(); epi.classList.remove("out"); }, 1200);
  }, 9000);

  /* ---------- catalog ---------- */
  const state = { q: "", coll: "all", theme: "all" };
  const chips = $("#chips");
  const chipDefs = [{ id: "all", es: "Todas", en: "All" }, ...C.map(c => ({ id: c.id, es: c.title, en: c.year }))];
  chips.innerHTML = chipDefs.map(c => `<button type="button" class="chip" data-c="${c.id}" aria-pressed="${c.id === "all"}">${esc(c.es)}<span class="en">${esc(c.en)}</span></button>`).join("");
  chips.addEventListener("click", e => {
    const b = e.target.closest(".chip"); if (!b) return;
    state.coll = b.dataset.c;
    chips.querySelectorAll(".chip").forEach(x => x.setAttribute("aria-pressed", x === b));
    renderCards();
  });
  const sel = $("#theme");
  sel.innerHTML = `<option value="all">Todos los temas · All themes</option>` +
    Object.entries(T).map(([k, v]) => `<option value="${k}">${esc(v.es)} · ${esc(v.en)}</option>`).join("");
  sel.addEventListener("change", () => { state.theme = sel.value; renderCards(); });
  $("#q").addEventListener("input", e => { state.q = norm(e.target.value.trim()); renderCards(); });

  const haystack = l => norm([l.title, l.titleEn, l.dateLabel, l.venue, coll(l.collection).title, l.summary?.es, l.summary?.en, l.quote?.text,
    ...(l.themes || []).flatMap(t => [T[t]?.es, T[t]?.en])].join(" "));

  function renderCards() {
    const list = L.filter(l =>
      (state.coll === "all" || l.collection === state.coll) &&
      (state.theme === "all" || (l.themes || []).includes(state.theme)) &&
      (!state.q || haystack(l).includes(state.q)));
    $("#cards").innerHTML = list.map(l => {
      const c = coll(l.collection);
      const extras = [l.audioSrc ? "♪ audio" : "", l.fullText ? "texto" : ""].filter(Boolean).join(" · ");
      return `<li class="card"><a href="#/conferencia/${l.id}">
        ${l.image ? `<div class="card-art"><img class="illus" src="${esc(l.image)}" alt="" loading="lazy" decoding="async" width="900" height="675"></div>` : ""}
        <div class="callno"><span>${esc(callNo(l))}</span><span>${esc(c.title)}</span></div>
        <h3>${esc(l.title)}</h3>
        <div class="alt">${esc(l.titleEn)}</div>
        <p class="meta"><span>${esc(l.dateLabel)}</span><span class="venue">${esc(l.venue)}</span></p>
        <div class="tags">${(l.themes || []).map(t => `<span class="tag">${esc(T[t]?.es || t)}</span>`).join("")}</div>
        ${extras ? `<span class="badge">${extras}</span>` : ""}
      </a></li>`;
    }).join("");
    $("#empty").hidden = list.length > 0;
    $("#count").textContent = `${list.length} de ${L.length} conferencias · ${list.length} of ${L.length} lectures`;
  }
  renderCards();

  /* ---------- collections ---------- */
  $("#collections").innerHTML = C.map(c => {
    const ls = L.filter(l => l.collection === c.id).sort((a, b) => a.number - b.number);
    return `<section class="coll" aria-labelledby="c-${c.id}">
      <div class="code" aria-hidden="true">${esc(c.code)}</div>
      <div>
        <h2 id="c-${c.id}">${esc(c.title)}</h2>
        <p class="where">${esc(c.venue)} · ${esc(c.year)}</p>
        <p>${esc(c.blurb.es)}</p><p class="en-p">${esc(c.blurb.en)}</p>
        <ol>${ls.map(l => `<li><a href="#/conferencia/${l.id}">${esc(l.title)}</a></li>`).join("")}</ol>
        <div class="section-label">Fuentes <span class="en">Sources</span></div>
        ${sourcesList(c.sources)}
      </div></section>`;
  }).join("");

  function sourcesList(src) {
    return `<ul class="sources">${(src || []).map(s =>
      `<li><span class="kind ${esc(s.kind)}">${esc(s.kind)}</span><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.label)}</a></li>`).join("")}</ul>`;
  }

  /* ---------- lecture view ---------- */
  const fmt = s => { if (!isFinite(s)) return "--:--"; s = Math.floor(s); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = String(s % 60).padStart(2, "0"); return h ? `${h}:${String(m).padStart(2, "0")}:${x}` : `${m}:${x}`; };
  const ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z"/></svg>';
  const ICON_PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';

  function renderLecture(id) {
    const l = L.find(x => x.id === id);
    const v = $("#view-lecture");
    if (!l) { v.innerHTML = `<p class="placeholder">Ese volumen no está en este hexágono. <a href="#/">Volver al catálogo</a></p>`; return; }
    const c = coll(l.collection);
    const sibs = L.filter(x => x.collection === l.collection).sort((a, b) => a.number - b.number);
    const i = sibs.indexOf(l), prev = sibs[i - 1], next = sibs[i + 1];
    const paras = String(l.fullText || "").split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
    v.innerHTML = `
      <a class="back" href="#/">← Catálogo · Catalog</a>
      <header>
        <div class="callno"><span>${esc(callNo(l))}</span><span>${esc(c.title)}</span></div>
        <h1 id="lec-title">${esc(l.title)}<span class="en">${esc(l.titleEn)}</span></h1>
        <dl class="facts">
          <div><dt>Fecha <span class="en">Date</span></dt><dd>${esc(l.dateLabel)}</dd></div>
          <div><dt>Lugar <span class="en">Venue</span></dt><dd>${esc(l.venue)}</dd></div>
          <div><dt>Colección <span class="en">Collection</span></dt><dd>${esc(c.title)} (${roman(l.number)})</dd></div>
        </dl>
        ${l.image ? `<figure class="lecture-art"><img class="illus" src="${esc(l.image)}" alt="${esc(l.imageAlt || "Ilustración a tinta · Ink illustration")}" width="900" height="675"></figure>` : ""}
      </header>
      ${l.quote ? `<figure class="pull"><blockquote lang="${esc(l.quote.lang)}">${esc(l.quote.text)}</blockquote><figcaption>Borges, «${esc(l.title)}»</figcaption></figure>` : ""}
      <div class="section-label">Resumen <span class="en">Summary</span></div>
      <div class="summary"><p>${esc(l.summary.es)}</p><p class="en-p" lang="en">${esc(l.summary.en)}</p></div>
      <div class="section-label">Escuchar <span class="en">Listen</span></div>
      ${l.audioSrc ? playerHTML(l) : `<p class="placeholder">Audio no alojado aquí. Puede escucharse en las fuentes de abajo, o agregarse en <code>audioSrc</code>.<span class="en">Audio is not hosted here. Listen via the sources below, or add a file in <code>audioSrc</code>.</span></p>`}
      <div class="section-label">Texto <span class="en">Text</span></div>
      ${paras.length ? `<div class="fulltext">${paras.map(p => `<p>${esc(p)}</p>`).join("")}</div>`
        : `<p class="placeholder">El texto completo está protegido por derechos de autor. Puede leerse en la edición citada en las fuentes; si tenés los derechos, agregalo en <code>fullText</code>.<span class="en">The full text is under copyright. Read it in the edition listed below; if you hold the rights, add it in <code>fullText</code>.</span></p>`}
      <div class="section-label">Fuentes <span class="en">Sources</span></div>
      ${sourcesList([...(l.sources || []), ...(c.sources || []).filter(s => !(l.sources || []).some(x => x.url === s.url))])}
      <nav class="pager" aria-label="Conferencias vecinas · Adjacent lectures">
        ${prev ? `<a class="prev" href="#/conferencia/${prev.id}"><small>← Anterior · Previous</small>${esc(prev.title)}</a>` : ""}
        ${next ? `<a class="next" href="#/conferencia/${next.id}"><small>Siguiente · Next →</small>${esc(next.title)}</a>` : ""}
      </nav>`;
    if (l.audioSrc) wirePlayer(v);
  }

  function playerHTML(l) {
    return `<div class="player" role="group" aria-label="Reproductor · Audio player">
      <audio preload="metadata" src="${esc(l.audioSrc)}"></audio>
      <button class="play" type="button" aria-label="Reproducir · Play">${ICON_PLAY}</button>
      <div class="track"><span class="ttl">${esc(l.title)}</span>
        <input class="seek" type="range" min="0" max="1000" value="0" step="1" aria-label="Posición · Position"></div>
      <div class="time"><span class="cur">0:00</span> / <span class="dur">--:--</span><button class="rate" type="button" aria-label="Velocidad · Speed">1×</button></div>
    </div>`;
  }
  function wirePlayer(root) {
    const a = $("audio", root), btn = $(".play", root), seek = $(".seek", root), cur = $(".cur", root), dur = $(".dur", root), rate = $(".rate", root);
    const rates = [1, 1.25, 1.5, 0.75]; let ri = 0, dragging = false;
    btn.onclick = () => a.paused ? a.play() : a.pause();
    a.onplay = () => { btn.innerHTML = ICON_PAUSE; btn.setAttribute("aria-label", "Pausa · Pause"); };
    a.onpause = () => { btn.innerHTML = ICON_PLAY; btn.setAttribute("aria-label", "Reproducir · Play"); };
    a.onloadedmetadata = () => dur.textContent = fmt(a.duration);
    a.ontimeupdate = () => { cur.textContent = fmt(a.currentTime); if (!dragging && a.duration) seek.value = a.currentTime / a.duration * 1000; };
    a.onerror = () => { dur.textContent = "error"; };
    seek.oninput = () => { dragging = true; if (a.duration) cur.textContent = fmt(seek.value / 1000 * a.duration); };
    seek.onchange = () => { if (a.duration) a.currentTime = seek.value / 1000 * a.duration; dragging = false; };
    rate.onclick = () => { ri = (ri + 1) % rates.length; a.playbackRate = rates[ri]; rate.textContent = rates[ri] + "×"; };
  }

  /* ---------- router ---------- */
  const views = { home: $("#view-home"), collections: $("#view-collections"), about: $("#view-about"), lecture: $("#view-lecture") };
  function route() {
    document.querySelectorAll("audio").forEach(a => a.pause());
    const h = location.hash.replace(/^#\/?/, "");
    let key = "home";
    if (h.startsWith("conferencia/")) { key = "lecture"; renderLecture(decodeURIComponent(h.split("/")[1])); }
    else if (h === "colecciones") key = "collections";
    else if (h === "acerca") key = "about";
    Object.entries(views).forEach(([k, el]) => el.hidden = k !== key);
    document.querySelectorAll(".site-header nav a").forEach(a => {
      const m = (a.getAttribute("href") === "#/" && key === "home") || a.getAttribute("href") === "#/" + h;
      m ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current");
    });
    const l = key === "lecture" && L.find(x => x.id === h.split("/")[1]);
    document.title = (l ? l.title + " — " : "") + "La Biblioteca Oral de Borges";
    if (key !== "home" || h) { scrollTo(0, 0); $("#main").focus({ preventScroll: true }); }
  }
  addEventListener("hashchange", route); route();
})();
