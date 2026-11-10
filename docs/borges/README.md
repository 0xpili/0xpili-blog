# La Biblioteca Oral de Borges

Static site (plain HTML/CSS/JS). Open `index.html` or serve the folder:

    python3 -m http.server 8000

## Adding texts and audio you hold the rights to

Everything lives in `data/lectures.js`. Each lecture has two empty fields:

- `fullText`: the full text as a string; separate paragraphs with a blank line.
- `audioSrc`: path or URL to an audio file, e.g. `"audio/el-libro.mp3"` (put files in `audio/`).

When `audioSrc` is set, the lecture page shows the built-in player (play/pause,
seek, speed). When `fullText` is set, the text replaces the placeholder.

Borges died in 1986. His lecture texts and recordings are under copyright, so
this site ships only titles, dates, venues, original summaries, one short quote
per lecture and links to public sources.

## Illustrations
Each lecture has an `image` (and `imageAlt`) field in `data/lectures.js` pointing to `img/<id>.jpg`.
All drawings share one hand-drawn ink-on-paper style; the homepage hero (`img/home.jpg`) is a drawing
after a 1969 photograph at Asociación Cultural Rumbo, San Nicolás (Fototeca San Nicolás).
The site uses a single light theme (cream paper, sepia ink, muted gold).

## Links and excerpts (copyright until 2056)
Each lecture has `links` (authorized only: Internet Archive controlled lending,
publisher pages, Harvard's official Woodberry Poetry Room audio, the HUP sample PDF)
and one `excerpt` with a citation. Do not add unauthorized copies.

Every excerpt was checked word for word against a published source:

| Lecture | Verified in |
|---|---|
| El libro | Instituto Cervantes de Nueva York, biblioteca (cites Borges oral, Emecé, p. 165) |
| La inmortalidad | Dergipark academic article on "El inmortal" (cites Borges oral) |
| Emanuel Swedenborg | Editorial Palíndromo blog and a second blog transcription (identical text) |
| El cuento policial | La Nación, "Del clasicismo de Borges a la ficción paranoica de Piglia" |
| El tiempo | Universidad de Concepción thesis (Cisternas Cruz) |
| La Divina Comedia | La Izquierda Diario (Uruguay) and mir.com.uy (identical text) |
| La pesadilla | Escuela de la Orientación Lacaniana, Sección La Plata, blog article |
| Las mil y una noches | Specimen, The Babel Review of Translations |
| El budismo | E. Fishburn, review in Transmodernity (eScholarship, 2020); Buddhistdoor en Español |
| La poesía | Clarín; "Borges interactivo" (Universidad Autónoma de Chiapas), p. 310 |
| La cábala | Iberoamericana Vervuert chapter "«Israel» en la poesía de J. L. Borges"; Radio Sefarad |
| La ceguera | "Borges interactivo" (UNACH), p. 292; La Gacetilla Literaria |
| The Riddle of Poetry | Harvard University Press sample PDF, p. 4 |
| The Metaphor | Ichien et al., CogSci 2024 (cites HUP 2000, p. 41) |
| The Telling of the Tale | Shipwreck Library review of This Craft of Verse |
| Word-Music and Translation | St. Austin Review, "Jorge Luis Borges on Verse Translation" |
| Thought and Poetry | Shipwreck Library review of This Craft of Verse |
| A Poet's Creed | The Guardian (review, 30 May 2013); La Nación "Credo de poeta" (Spanish) |
