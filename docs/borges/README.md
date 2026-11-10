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
