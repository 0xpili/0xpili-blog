/*
 * La Biblioteca Oral de Borges — data file
 * ------------------------------------------------------------------
 * Every lecture is one object in LECTURES. To add material you hold the
 * rights to, fill these two fields and reload the page:
 *
 *   fullText : the full text as a string. Separate paragraphs with a
 *              blank line ("\n\n"). Leave "" to show the placeholder.
 *   audioSrc : path or URL to an audio file, e.g. "audio/el-libro.mp3".
 *              When set, the built-in player appears on the lecture page.
 *
 *   links    : authorized places to read or listen (lending, publisher,
 *              official audio). Never add unauthorized copies.
 *   excerpt  : one short quotation with its citation, checked word for
 *              word against a published source.
 *
 * Nothing else needs to change. Dates use ISO format (YYYY-MM-DD) when the
 * exact day is documented; otherwise "date" is "" and "dateLabel" is shown.
 */
window.COLLECTIONS = [
  {
    id: "borges-oral",
    code: "BO",
    title: "Borges oral",
    year: "1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    lang: "es",
    blurb: {
      es: "Cinco clases dictadas en la Universidad de Belgrano entre mayo y junio de 1978. Las transcribió Martín Müller y se publicaron en 1979 (Emecé / Editorial de Belgrano).",
      en: "Five talks given at the Universidad de Belgrano in May–June 1978. Transcribed by Martín Müller and published in 1979 (Emecé / Editorial de Belgrano)."
    },
    sources: [
      { label: "Internet Archive — Borges, oral (Emecé, 1979), préstamo digital / digital lending", url: "https://archive.org/details/borgesoral0000borg", kind: "texto" },
      { label: "Wikipedia — Borges oral", url: "https://es.wikipedia.org/wiki/Borges_oral", kind: "referencia" },
      { label: "Borges Center (Univ. of Pittsburgh) — Bibliografía 1979", url: "https://www.borges.pitt.edu/bibliography/1979-1", kind: "referencia" }
    ]
  },
  {
    id: "siete-noches",
    code: "SN",
    title: "Siete noches",
    year: "1977",
    venue: "Teatro Coliseo, Buenos Aires",
    lang: "es",
    blurb: {
      es: "Siete conferencias en el Teatro Coliseo, entre el 1 de junio y el 3 de agosto de 1977. Revisadas con Roy Bartholomew, se publicaron en 1980 (Fondo de Cultura Económica).",
      en: "Seven lectures at the Teatro Coliseo, 1 June – 3 August 1977. Revised with Roy Bartholomew and published in 1980 (Fondo de Cultura Económica)."
    },
    sources: [
      { label: "Internet Archive — Siete noches (FCE, 1980), préstamo digital / digital lending", url: "https://archive.org/details/sietenoches0000borg", kind: "texto" },
      { label: "Fondo de Cultura Económica — Siete noches (editorial / publisher)", url: "https://www.fcede.es/site/es/libros/detalles.aspx?id_libro=1143", kind: "editorial" },
      { label: "Borges Center (Univ. of Pittsburgh) — Bibliografía 1977", url: "https://www.borges.pitt.edu/bibliography/1977-1", kind: "referencia" }
    ]
  },
  {
    id: "craft-of-verse",
    code: "CV",
    title: "This Craft of Verse",
    year: "1967–1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    lang: "en",
    blurb: {
      es: "Las Charles Eliot Norton Lectures, seis conferencias en inglés dictadas en Harvard en 1967–1968. Las cintas reaparecieron décadas después y Harvard University Press publicó la transcripción en 2000, editada por Călin-Andrei Mihăilescu.",
      en: "The Charles Eliot Norton Lectures: six talks given in English at Harvard in 1967–68. The tapes resurfaced decades later; Harvard University Press published the transcript in 2000, edited by Călin-Andrei Mihăilescu."
    },
    sources: [
      { label: "Harvard — Woodberry Poetry Room, Listening Booth (audio oficial / official audio)", url: "https://library.harvard.edu/sites/default/files/static/poetry/listeningbooth/poets/borges.html", kind: "audio" },
      { label: "Harvard University Press — This Craft of Verse (ed. 2025)", url: "https://www.hup.harvard.edu/books/9780674302457", kind: "editorial" },
      { label: "Harvard University Press — muestra PDF / sample PDF", url: "https://www.hup.harvard.edu/file/feeds/PDF/9780674302457_sample.pdf", kind: "texto" },
      { label: "Open Culture — sobre las grabaciones / on the recordings", url: "https://www.openculture.com/2012/05/jorge_luis_borges_1967-8_norton_lectures_on_poetry_and_everything_else_literary.html", kind: "referencia" }
    ]
  }
];

window.THEMES = {
  libro:      { es: "El libro",        en: "Books" },
  tiempo:     { es: "El tiempo",       en: "Time" },
  muerte:     { es: "Muerte e inmortalidad", en: "Death & immortality" },
  mistica:    { es: "Mística",         en: "Mysticism" },
  suenos:     { es: "Sueños",          en: "Dreams" },
  oriente:    { es: "Oriente",         en: "The East" },
  poesia:     { es: "Poesía",          en: "Poetry" },
  lenguaje:   { es: "Lenguaje y traducción", en: "Language & translation" },
  narrar:     { es: "El arte de narrar", en: "Storytelling" },
  ceguera:    { es: "Ceguera",         en: "Blindness" },
  dante:      { es: "Dante",           en: "Dante" }
};

const IA_BO = "https://archive.org/details/borgesoral0000borg";
const IA_SN = "https://archive.org/details/sietenoches0000borg";
const FCE_SN = "https://www.fcede.es/site/es/libros/detalles.aspx?id_libro=1143";
const HARVARD_LB = "https://library.harvard.edu/sites/default/files/static/poetry/listeningbooth/poets/borges.html";
const HARVARD_MP3 = "https://library.harvard.edu/sites/default/files/static/poetry/audio/listeningbooth/borges/";
const HUP_CV = "https://www.hup.harvard.edu/books/9780674302457";
const HUP_SAMPLE = "https://www.hup.harvard.edu/file/feeds/PDF/9780674302457_sample.pdf";

/* "links": authorized places to read or listen. Only official, publisher or
   controlled-lending sources. Never add unauthorized copies. */
const LINKS_BO = [
  { kind: "prestamo", label: "Leer — Internet Archive, préstamo digital", en: "Read — borrow from Internet Archive", url: IA_BO }
];
const LINKS_SN = [
  { kind: "prestamo", label: "Leer — Internet Archive, préstamo digital", en: "Read — borrow from Internet Archive", url: IA_SN },
  { kind: "comprar", label: "Comprar — Fondo de Cultura Económica", en: "Buy — publisher page", url: FCE_SN }
];
const linksCV = mp3 => [
  { kind: "audio", label: "Escuchar — audio oficial de Harvard (Woodberry Poetry Room)", en: "Listen — official Harvard recording", url: HARVARD_MP3 + mp3 },
  { kind: "audio", label: "Escuchar — las seis conferencias en la página de Harvard", en: "Listen — all six on Harvard's Listening Booth", url: HARVARD_LB },
  { kind: "muestra", label: "Leer una muestra — PDF de Harvard University Press", en: "Read a sample — HUP PDF", url: HUP_SAMPLE },
  { kind: "comprar", label: "Comprar — Harvard University Press", en: "Buy — publisher page", url: HUP_CV }
];

/* "excerpt": one short quotation per lecture (citation right). Every text was
   checked word for word against a published source; see README.md. */

window.LECTURES = [
  /* ---------------- Borges oral (1978) ---------------- */
  {
    id: "el-libro", collection: "borges-oral", number: 1,
    title: "El libro", titleEn: "The Book",
    date: "1978-05-24", dateLabel: "24 de mayo de 1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    themes: ["libro", "tiempo"],
    summary: {
      es: "Borges hace del libro el más íntimo de los inventos humanos: no una herramienta del cuerpo, sino una prolongación de la memoria y la imaginación. Recorre la desconfianza de los antiguos hacia la escritura, el culto del libro sagrado y la idea de que releer vale más que leer.",
      en: "Borges presents the book as the most intimate human invention: not a tool of the body but an extension of memory and imagination. He moves from the ancients' distrust of writing to the cult of the sacred book and the idea that rereading matters more than reading."
    },
    excerpt: { text: "De los diversos instrumentos del hombre, el más asombroso es, sin duda, el libro. Los demás son extensiones de su cuerpo. El microscopio, el telescopio, son extensiones de su vista; el teléfono es extensión de la voz…", lang: "es", cite: "Borges oral (Emecé / Editorial de Belgrano, 1979)" },
    links: LINKS_BO,
    sources: [],
    image: "img/el-libro.jpg", imageAlt: "Un libro abierto cuyas páginas se vuelven pájaros · An open book whose pages turn into birds",
    fullText: "", audioSrc: ""
  },
  {
    id: "la-inmortalidad", collection: "borges-oral", number: 2,
    title: "La inmortalidad", titleEn: "Immortality",
    date: "1978-06-05", dateLabel: "5 de junio de 1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    themes: ["muerte", "mistica"],
    summary: {
      es: "A partir de William James, Platón y Schopenhauer, Borges examina la vieja esperanza (o amenaza) de seguir existiendo después de la muerte. Rechaza la inmortalidad personal y propone otra, más humilde: la que sobrevive en la memoria y en los actos de los demás.",
      en: "Drawing on William James, Plato and Schopenhauer, Borges weighs the old hope (or threat) of living on after death. He rejects personal immortality and proposes a humbler kind: the one that survives in other people's memory and deeds."
    },
    excerpt: { text: "…creo en la inmortalidad: no en la inmortalidad personal, pero sí en la cósmica. Seguiremos siendo inmortales; más allá de nuestra muerte corporal queda nuestra memoria, y más allá de nuestra memoria quedan nuestros actos…", lang: "es", cite: "Borges oral (Emecé / Editorial de Belgrano, 1979)" },
    links: LINKS_BO,
    sources: [],
    image: "img/la-inmortalidad.jpg", imageAlt: "Un reloj de arena con la arena suspendida · An hourglass with the sand suspended",
    fullText: "", audioSrc: ""
  },
  {
    id: "emanuel-swedenborg", collection: "borges-oral", number: 3,
    title: "Emanuel Swedenborg", titleEn: "Emanuel Swedenborg",
    date: "1978-06-09", dateLabel: "9 de junio de 1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    themes: ["mistica", "muerte"],
    summary: {
      es: "Un retrato del sabio sueco, hombre de ciencia antes que visionario, que dijo haber recorrido el cielo y el infierno. Borges se detiene en su idea más singular: nadie es condenado por un tribunal, cada muerto elige libremente el lugar que le corresponde.",
      en: "A portrait of the Swedish scholar, a man of science before he was a visionary, who claimed to have walked through heaven and hell. Borges dwells on his most striking idea: no tribunal condemns anyone; each of the dead freely chooses where they belong."
    },
    excerpt: { text: "Nos dice que cuando un hombre muere no se da cuenta de que ha muerto, ya que todo lo que lo rodea es igual. Se encuentra en su casa, lo visitan sus amigos, recorre las calles de su ciudad, no piensa que ha muerto…", lang: "es", cite: "Borges oral (Emecé / Editorial de Belgrano, 1979)" },
    links: LINKS_BO,
    sources: [],
    image: "img/emanuel-swedenborg.jpg", imageAlt: "Un hombre en una escalera entre dos mundos, con ángeles · A man on a stair between two worlds, with angels",
    fullText: "", audioSrc: ""
  },
  {
    id: "el-cuento-policial", collection: "borges-oral", number: 4,
    title: "El cuento policial", titleEn: "The Detective Story",
    date: "1978-06-16", dateLabel: "16 de junio de 1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    themes: ["narrar", "libro"],
    summary: {
      es: "Borges cuenta cómo Edgar Allan Poe inventó el género policial y, con él, un nuevo tipo de lector, desconfiado y atento. Defiende el policial como una de las pocas formas que conservan el orden clásico de principio, medio y fin.",
      en: "Borges tells how Edgar Allan Poe invented the detective story and, with it, a new kind of reader, suspicious and alert. He defends the genre as one of the few forms that still keeps the classical order of beginning, middle and end."
    },
    excerpt: { text: "En esta época nuestra, tan caótica, hay algo que, humildemente, ha mantenido las virtudes clásicas: el cuento policial. Ya que no se entiende un cuento policial sin principio, sin medio y sin fin.", lang: "es", cite: "Borges oral (Emecé / Editorial de Belgrano, 1979)" },
    links: LINKS_BO,
    sources: [],
    image: "img/el-cuento-policial.jpg", imageAlt: "Una lupa sobre un laberinto · A magnifying glass over a labyrinth",
    fullText: "", audioSrc: ""
  },
  {
    id: "el-tiempo", collection: "borges-oral", number: 5,
    title: "El tiempo", titleEn: "Time",
    date: "1978-06-23", dateLabel: "23 de junio de 1978",
    venue: "Universidad de Belgrano, Buenos Aires",
    themes: ["tiempo", "mistica"],
    summary: {
      es: "Para Borges, el tiempo sigue siendo el problema esencial de la metafísica. Pasa del río de Heráclito a Platón y San Agustín, y se pregunta qué queda de nosotros si somos a la vez lo que cambia y lo que permanece.",
      en: "For Borges, time remains the essential problem of metaphysics. He moves from Heraclitus' river to Plato and Saint Augustine, and asks what is left of us if we are both what changes and what endures."
    },
    excerpt: { text: "Es decir, somos algo cambiante y algo permanente. Somos algo, esencialmente misterioso.", lang: "es", cite: "Borges oral (Emecé / Editorial de Belgrano, 1979)" },
    links: LINKS_BO,
    sources: [],
    image: "img/el-tiempo.jpg", imageAlt: "Un uróboros que encierra un río y un reloj de arena · An ouroboros around a river and an hourglass",
    fullText: "", audioSrc: ""
  },

  /* ---------------- Siete noches (1977) ---------------- */
  {
    id: "la-divina-comedia", collection: "siete-noches", number: 1,
    title: "La Divina Comedia", titleEn: "The Divine Comedy",
    date: "1977-06-01", dateLabel: "1 de junio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["dante", "poesia", "libro"],
    summary: {
      es: "Borges invita a leer a Dante sin miedo a los comentarios, como quien entra en un relato. Se detiene en la intensidad de sus personajes, en Francesca, Ulises y Ugolino, y en la precisión de cada imagen.",
      en: "Borges invites us to read Dante without fear of the commentaries, as one enters a story. He lingers on the intensity of its characters, Francesca, Ulysses and Ugolino, and on the precision of every image."
    },
    excerpt: { text: "Al principio debemos leer el libro con fe de niño, abandonarnos a él; después nos acompañará hasta el fin. A mí me ha acompañado durante tantos años, y sé que apenas lo abra mañana encontraré cosas que no he encontrado hasta ahora.", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/la-divina-comedia.jpg", imageAlt: "Los círculos del infierno vistos desde arriba · The circles of hell seen from above",
    fullText: "", audioSrc: ""
  },
  {
    id: "la-pesadilla", collection: "siete-noches", number: 2,
    title: "La pesadilla", titleEn: "Nightmares",
    date: "1977-06-15", dateLabel: "15 de junio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["suenos", "mistica", "lenguaje"],
    summary: {
      es: "Borges recorre los sueños de la literatura y la historia, y relata algunas de sus propias pesadillas: laberintos, espejos, máscaras. A través de las palabras incubus, nightmare y Alp, sospecha que la pesadilla tiene algo de sobrenatural.",
      en: "Borges surveys dreams in literature and history and recounts some of his own nightmares: labyrinths, mirrors, masks. Through the words incubus, nightmare and Alp, he suspects that the nightmare has something supernatural about it."
    },
    excerpt: { text: "¿Y si las pesadillas fueran estrictamente sobrenaturales? ¿Si las pesadillas fueran grietas del infierno? ¿Si en las pesadillas estuviéramos literalmente en el infierno?", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/la-pesadilla.jpg", imageAlt: "Una cabeza dormida de la que surge un caballo oscuro · A sleeping head with a dark horse emerging",
    fullText: "", audioSrc: ""
  },
  {
    id: "las-mil-y-una-noches", collection: "siete-noches", number: 3,
    title: "Las mil y una noches", titleEn: "The Thousand and One Nights",
    date: "1977-06-22", dateLabel: "22 de junio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["oriente", "narrar", "libro"],
    summary: {
      es: "Una meditación sobre cómo Occidente descubrió el Oriente y sobre el libro que lo volvió imaginable. Borges compara las traducciones de Galland, Lane y Burton y celebra un libro tan vasto que parece infinito.",
      en: "A meditation on how the West discovered the East, and on the book that made it imaginable. Borges compares the translations of Galland, Lane and Burton and celebrates a book so vast it seems infinite."
    },
    excerpt: { text: "Un acontecimiento capital de la historia de las naciones occidentales es el descubrimiento del Oriente. Sería más exacto hablar de una conciencia del Oriente, continua, comparable a la presencia de Persia en la historia griega.", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/las-mil-y-una-noches.jpg", imageAlt: "Una lámpara cuyo humo dibuja un palacio · A lamp whose smoke draws a palace",
    fullText: "", audioSrc: ""
  },
  {
    id: "el-budismo", collection: "siete-noches", number: 4,
    title: "El budismo", titleEn: "Buddhism",
    date: "1977-07-06", dateLabel: "6 de julio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["oriente", "mistica", "tiempo"],
    summary: {
      es: "Borges narra la leyenda del Buda y explica la doctrina de la transmigración, el karma y el nirvana. Termina en el zen, donde descubre una idea que lo fascina: que el yo es una ilusión.",
      en: "Borges retells the legend of the Buddha and explains transmigration, karma and nirvana. He ends with Zen, where he finds an idea that fascinates him: that the self is an illusion."
    },
    excerpt: { text: "Para mí, el budismo no es una pieza de museo: es un camino de salvación. No para mí, pero para millones de hombres.", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/el-budismo.jpg", imageAlt: "Un tigre sereno bajo una higuera · A calm tiger under a fig tree",
    fullText: "", audioSrc: ""
  },
  {
    id: "la-poesia", collection: "siete-noches", number: 5,
    title: "La poesía", titleEn: "Poetry",
    date: "1977-07-13", dateLabel: "13 de julio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["poesia", "lenguaje"],
    summary: {
      es: "Borges sostiene que la poesía no se define: se siente, como tantas cosas que conocemos íntimamente sin poder definirlas. Recorre versos de varias lenguas y propone que la belleza es una experiencia física que nos espera en cualquier página.",
      en: "Borges argues that poetry cannot be defined, only felt, like so many things we know intimately but cannot define. He moves through verses in several languages and proposes that beauty is a physical experience waiting for us on any page."
    },
    excerpt: { text: "Hay personas que sienten escasamente la poesía; generalmente se dedican a enseñarla. Yo creo sentir la poesía y creo no haberla enseñado…", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/la-poesia.jpg", imageAlt: "Una rosa dibujada con una sola línea · A rose drawn with one line",
    fullText: "", audioSrc: ""
  },
  {
    id: "la-cabala", collection: "siete-noches", number: 6,
    title: "La cábala", titleEn: "The Kabbalah",
    date: "1977-07-26", dateLabel: "26 de julio de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["mistica", "lenguaje", "libro"],
    summary: {
      es: "Borges eligió este tema la víspera, en lugar de los gnósticos anunciados. Explica la idea cabalística de un texto sagrado donde nada es casual, ni una letra, y la leyenda del Golem, para cerrar con la esperanza de que en cada uno haya una partícula de divinidad.",
      en: "Borges chose this subject the day before, instead of the announced talk on the Gnostics. He explains the Kabbalistic idea of a sacred text where nothing, not even a letter, is accidental, and the legend of the Golem, ending with the hope that each of us holds a particle of the divine."
    },
    excerpt: { text: "En cada uno de nosotros hay una partícula de divinidad. Este mundo, evidentemente, no puede ser la obra de un Dios todopoderoso y justo, pero depende de nosotros.", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/la-cabala.jpg", imageAlt: "Un gólem de barro rodeado de signos · A clay golem surrounded by signs",
    fullText: "", audioSrc: ""
  },
  {
    id: "la-ceguera", collection: "siete-noches", number: 7,
    title: "La ceguera", titleEn: "Blindness",
    date: "1977-08-03", dateLabel: "3 de agosto de 1977",
    venue: "Teatro Coliseo, Buenos Aires",
    themes: ["ceguera", "poesia", "tiempo"],
    summary: {
      es: "Borges habla de su propia ceguera, lenta y sin dramatismo, y de los colores que todavía ve. Evoca a Homero, Milton y Groussac, y convierte la pérdida en un modo de vida y en material para el arte.",
      en: "Borges speaks of his own blindness, slow and undramatic, and of the colours he can still see. He invokes Homer, Milton and Groussac and turns loss into a way of life and raw material for art."
    },
    excerpt: { text: "Un escritor, o todo hombre, debe pensar que cuanto le ocurre es un instrumento; todas las cosas le han sido dadas para un fin y esto tiene que ser más fuerte en el caso de un artista.", lang: "es", cite: "Siete noches (Fondo de Cultura Económica, 1980)" },
    links: LINKS_SN,
    sources: [],
    image: "img/la-ceguera.jpg", imageAlt: "Borges de perfil, con los ojos cerrados, sobre un halo amarillo · Borges in profile, eyes closed, in a yellow glow",
    fullText: "", audioSrc: ""
  },

  /* ---------------- This Craft of Verse (1967–68) ---------------- */
  {
    id: "the-riddle-of-poetry", collection: "craft-of-verse", number: 1,
    title: "The Riddle of Poetry", titleEn: "El enigma de la poesía",
    date: "1967-10-24", dateLabel: "24 de octubre de 1967",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["poesia", "libro"],
    summary: {
      es: "Borges abre el ciclo confesando que no tiene revelaciones que ofrecer, solo perplejidades. Recuerda a su padre leyéndole a Keats y sostiene que la poesía se vive antes de entenderse, como una pasión y una alegría.",
      en: "Borges opens the series admitting he has no revelations to offer, only perplexities. He recalls his father reading Keats to him and argues that poetry is lived before it is understood, as a passion and a joy."
    },
    excerpt: { text: "I do not think I understood the words, but I felt that something was happening to me. It was happening not to my mere intelligence but to my whole being, to my flesh and blood.", lang: "en", cite: "This Craft of Verse (Harvard University Press, ed. 2025), p. 4" },
    links: linksCV("borges_Norton_riddle1/Lecture1_RiddlePoetry.mp3"),
    sources: [],
    image: "img/the-riddle-of-poetry.jpg", imageAlt: "Una esfinge con un libro abierto · A sphinx with an open book",
    fullText: "", audioSrc: ""
  },
  {
    id: "the-metaphor", collection: "craft-of-verse", number: 2,
    title: "The Metaphor", titleEn: "La metáfora",
    date: "", dateLabel: "1967–1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["poesia", "lenguaje"],
    summary: {
      es: "Borges sugiere que las grandes metáforas son pocas y vuelven siempre: el tiempo como río, la vida como sueño, la muerte como sueño. Las compara con las kenningar nórdicas, metáforas fijas que muestran tanto el ingenio como sus límites.",
      en: "Borges suggests that the great metaphors are few and keep returning: time as a river, life as a dream, death as sleep. He sets them beside the Norse kenningar, fixed figures that show both the wit and the limits of the form."
    },
    excerpt: { text: "The metaphors will strike the imagination. But it may also be given to us—and why not hope for this as well?—it may also be given to us to invent metaphors that do not belong, or that do not yet belong, to accepted patterns.", lang: "en", cite: "This Craft of Verse (Harvard University Press, 2000, p. 41)" },
    links: linksCV("borges_Norton_metaphor2/Lecture2_Metaphor.mp3"),
    sources: [],
    image: "img/the-metaphor.jpg", imageAlt: "La luna reflejada en un espejo de mano · The moon reflected in a hand mirror",
    fullText: "", audioSrc: ""
  },
  {
    id: "the-telling-of-the-tale", collection: "craft-of-verse", number: 3,
    title: "The Telling of the Tale", titleEn: "El arte de contar",
    date: "", dateLabel: "1967–1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["narrar", "poesia"],
    summary: {
      es: "Borges recuerda que el poeta fue alguna vez un narrador y que la épica unía canto y relato. Lamenta que la novela los haya separado y se pregunta si la épica volverá a nacer.",
      en: "Borges recalls that the poet was once a storyteller and that the epic joined song and tale. He regrets that the novel split them apart and wonders whether the epic will be born again."
    },
    excerpt: { text: "…we cannot really believe in happiness and success. And this may be one of the poverties of our time.", lang: "en", cite: "This Craft of Verse (Harvard University Press, 2000)" },
    links: linksCV("borges_Norton_telling3/Lecture_TellingTale.mp3"),
    sources: [],
    image: "img/the-telling-of-the-tale.jpg", imageAlt: "Un velero sobre un mar de líneas · A sailing ship on a sea of lines",
    fullText: "", audioSrc: ""
  },
  {
    id: "word-music-and-translation", collection: "craft-of-verse", number: 4,
    title: "Word-Music and Translation", titleEn: "Música verbal y traducción",
    date: "", dateLabel: "1967–1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["lenguaje", "poesia"],
    summary: {
      es: "Contra la idea de que la poesía es intraducible, Borges defiende las traducciones que se convierten en obras propias. Habla de las versiones de Homero, de la Biblia inglesa y del Rubáiyát de FitzGerald, y de la música de las palabras que sobrevive al cambio de lengua.",
      en: "Against the idea that poetry is untranslatable, Borges defends translations that become works in their own right. He discusses versions of Homer, the English Bible and FitzGerald's Rubáiyát, and the word-music that survives a change of language."
    },
    excerpt: { text: "…men will care for beauty, not for the circumstances of beauty. Then we will have translations not only as good (we have them already) but as famous as Chapman’s Homer, as Urquhart’s Rabelais, as Pope’s Odyssey.", lang: "en", cite: "This Craft of Verse (Harvard University Press, 2000)" },
    links: linksCV("borges_Norton_music4/Lecture4_WordMusic.mp3"),
    sources: [],
    image: "img/word-music-and-translation.jpg", imageAlt: "Una lira cuyas cuerdas se vuelven líneas · A lyre whose strings become lines",
    fullText: "", audioSrc: ""
  },
  {
    id: "thought-and-poetry", collection: "craft-of-verse", number: 5,
    title: "Thought and Poetry", titleEn: "Pensamiento y poesía",
    date: "", dateLabel: "1967–1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["poesia", "lenguaje"],
    summary: {
      es: "Borges se pregunta si el sentido de un poema importa tanto como su sonido. Con ejemplos de muchas lenguas, sugiere que en un verso la emoción llega antes que el significado.",
      en: "Borges asks whether a poem's meaning matters as much as its sound. With examples from many languages, he suggests that in verse emotion arrives before meaning."
    },
    excerpt: { text: "I have suspected many a time that meaning is really something added to verse. I know for a fact that we feel the beauty of a poem before we even begin to think of a meaning.", lang: "en", cite: "This Craft of Verse (Harvard University Press, 2000)" },
    links: linksCV("borges_Norton_thought5/Lecture5_ThoughtPoetry.mp3"),
    sources: [],
    image: "img/thought-and-poetry.jpg", imageAlt: "Piezas de ajedrez que se disuelven en tinta · Chess pieces dissolving into ink",
    fullText: "", audioSrc: ""
  },
  {
    id: "a-poets-creed", collection: "craft-of-verse", number: 6,
    title: "A Poet's Creed", titleEn: "Credo de poeta",
    date: "", dateLabel: "1968",
    venue: "Harvard University, Cambridge (Massachusetts)",
    themes: ["poesia", "libro", "ceguera"],
    summary: {
      es: "En la última conferencia, Borges habla de sí mismo: de la biblioteca de su padre, de sus primeros libros y de lo que aprendió escribiendo. Confiesa que se considera ante todo un lector.",
      en: "In the final lecture Borges speaks about himself: his father's library, his first books and what writing taught him. He admits he thinks of himself above all as a reader."
    },
    excerpt: { text: "I think of myself as being essentially a reader. As you are aware, I have ventured into writing; but I think that what I have read is far more important than what I have written.", lang: "en", cite: "This Craft of Verse (Harvard University Press, 2000)" },
    links: linksCV("borges_Norton_creed6/Lecture6_poetCreed.mp3"),
    sources: [],
    image: "img/a-poets-creed.jpg", imageAlt: "Un anciano con bastón camina por un largo camino · An old man with a cane walks a long road",
    fullText: "", audioSrc: ""
  }
];

window.EPIGRAPHS = [
  { text: "Yo, que me figuraba el Paraíso / bajo la especie de una biblioteca.", src: "«Poema de los dones», 1960" },
  { text: "Los espejos y la cópula son abominables, porque multiplican el número de los hombres.", src: "«Tlön, Uqbar, Orbis Tertius», 1940" },
  { text: "El tiempo es la substancia de que estoy hecho.", src: "«Nueva refutación del tiempo», 1947" },
  { text: "De los diversos instrumentos del hombre, el más asombroso es, sin duda, el libro.", src: "«El libro», Borges oral, 1978" },
  { text: "Somos algo cambiante y algo permanente. Somos algo, esencialmente misterioso.", src: "«El tiempo», Borges oral, 1978" },
  { text: "En cada uno de nosotros hay una partícula de divinidad.", src: "«La cábala», Siete noches, 1977" }
];
