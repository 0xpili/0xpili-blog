# Domain Pitfalls

**Domain:** Static blog generator feature additions (RSS, meta descriptions, drafts, tags)
**Researched:** 2026-03-29

## Critical Pitfalls

Mistakes that cause broken feeds, SEO damage, or accidental publishing.

### Pitfall 1: RSS Feed XML Encoding Breaks on HTML Content

**What goes wrong:** Blog posts contain HTML (rendered from markdown) with characters like `<`, `>`, `&`, and sometimes emoji or non-ASCII characters. Naive XML generation using Python's `xml.etree.ElementTree` will either double-escape HTML entities (`&lt;` becomes `&amp;lt;`) or produce invalid XML when HTML is dumped raw into elements.

**Why it happens:** `xml.etree.ElementTree` does not support CDATA sections natively. Developers either escape everything (mangling the HTML) or try to inject raw HTML (breaking XML validity).

**Consequences:** Feed readers show garbled content, or reject the feed entirely. The W3C Feed Validator will flag errors. Some readers (Feedly, NetNewsWire) silently drop malformed entries.

**Prevention:** Use one of two approaches:
1. **String templating** (recommended for this project -- no new dependencies): Generate the RSS XML as a string/template, manually wrapping `<description>` content in `<![CDATA[...]]>` sections. This avoids ElementTree's CDATA limitations entirely and keeps the approach consistent with the Jinja2 templating already used in the project.
2. If using `xml.etree`, entity-encode all HTML content rather than trying to use CDATA. But this produces ugly feed source.

**Detection:** Validate the generated feed at https://validator.w3.org/feed/ during development. Add a build test that checks the feed is well-formed XML (`xml.etree.ElementTree.fromstring()`).

**Phase relevance:** RSS feed implementation phase. Write a validation test before writing the generator.

### Pitfall 2: Draft Posts Leak into Production Builds

**What goes wrong:** A post marked as draft appears on the live site because the draft filtering happens in the wrong place (e.g., after the index is built, or only during rendering but not during feed generation or tag page generation).

**Why it happens:** Draft filtering is applied inconsistently -- perhaps posts are filtered from the index template but still generate individual HTML files, or they appear in the RSS feed, or they show up in tag listings. With an incremental build cache, a previously-published post that is later marked as draft may persist as a cached HTML file in `docs/`.

**Consequences:** Unfinished posts visible to readers. Embarrassing partial content indexed by search engines.

**Prevention:** Filter drafts at the earliest possible point: right after `_parse_post()` returns, before any rendering or indexing. Specifically in the current `build()` method, filter immediately after the `for filepath in posts_path.glob("*.md")` loop, before posts are used for anything. Also: when a post becomes a draft, its existing HTML output in `docs/` must be deleted. The incremental build cache must account for this -- a post transitioning to draft status is a cache-invalidating event.

**Detection:** Write a test that creates a draft post, runs a build, and asserts: (1) no HTML file exists for it in `docs/`, (2) it does not appear in `index.html`, (3) it does not appear in the RSS feed.

**Phase relevance:** Draft support phase. This is the single most important test to write.

### Pitfall 3: RSS Feed Missing or Wrong Dates Break Reader Sorting

**What goes wrong:** RSS items lack `<pubDate>` or use incorrect date formats. RSS 2.0 requires RFC 822 dates (e.g., `Thu, 12 Oct 2025 00:00:00 +0000`), not ISO 8601, not the blog's custom `YYYY Mon DD` format.

**Why it happens:** The blog stores dates as `date_obj` (Python `datetime`) but displays them in a custom format. Developers format the date for RSS using the wrong format string, or forget timezone info (RFC 822 requires it).

**Consequences:** Feed readers display wrong dates, sort posts incorrectly, or show all posts as "just now" when they lack parseable dates. Some readers reject items entirely.

**Prevention:** Use `datetime.strftime('%a, %d %b %Y %H:%M:%S +0000')` for RFC 822 format. Since the blog's dates have no time component (only year/month/day), set time to midnight UTC. Store this as a separate `rfc822_date` field in the post dict during parsing.

**Detection:** Add a test that parses the generated feed XML and validates each `<pubDate>` matches RFC 822 format. Validate with W3C feed validator.

**Phase relevance:** RSS feed implementation phase.

## Moderate Pitfalls

### Pitfall 4: Meta Descriptions Contain Markdown/HTML Artifacts

**What goes wrong:** Auto-generating meta descriptions by slicing the first 160 characters of post content captures markdown syntax (`## `, `**bold**`, `[links](url)`) or rendered HTML tags (`<h2>`, `<strong>`), producing nonsensical meta descriptions.

**Why it happens:** The description is extracted at the wrong stage of the pipeline -- either from raw markdown (before rendering) without stripping syntax, or from rendered HTML (after rendering) without stripping tags.

**Prevention:** Extract from the raw markdown text, then strip markdown syntax before truncating. A simple approach: take the first paragraph after the title heading, strip markdown links (`[text](url)` to `text`), strip bold/italic markers, and truncate to 155 characters with an ellipsis. Do NOT use the HTML-rendered content, as stripping HTML is more error-prone than stripping markdown.

**Detection:** Add a test that creates posts with various markdown features (links, bold, headings, code blocks) in the first paragraph, generates descriptions, and asserts none contain `[`, `]`, `(`, `)`, `#`, `*`, `<`, or `>` characters.

**Phase relevance:** Meta descriptions phase.

### Pitfall 5: Tag Proliferation Creates Thin Content Pages

**What goes wrong:** With no constraints on tag creation, authors create many near-duplicate tags (`ai`, `AI`, `artificial-intelligence`, `machine-learning`) or one-off tags used by a single post. If tag pages are ever generated, each becomes a thin page with one entry.

**Why it happens:** Tags are freeform text with no validation or normalization. No minimum post count is enforced.

**Prevention:** Normalize tags during parsing: lowercase, strip whitespace, convert spaces to hyphens. For this project (15 posts), keep tags simple -- no tag index pages for now, just metadata on posts. If tag pages are added later, only generate pages for tags with 2+ posts. Consider defining a canonical tag list in config rather than purely freeform.

**Detection:** Add a test that warns (not fails) when a tag is used by only one post. Normalize test: `"AI"`, `" ai "`, and `"ai"` should all resolve to the same tag.

**Phase relevance:** Tags implementation phase.

### Pitfall 6: RSS Feed Absolute URL Construction Goes Wrong

**What goes wrong:** RSS `<link>` elements contain relative paths (`/my-post`) instead of absolute URLs (`https://0xpili.xyz/my-post`), or double-slash the site URL (`https://0xpili.xyz//my-post`), or use the wrong domain in development vs production.

**Why it happens:** The blog's `site_url` config value may or may not have a trailing slash. Post slugs may or may not have a leading slash. String concatenation without normalization produces malformed URLs.

**Prevention:** Use a helper function that joins `site_url` and slug cleanly: strip trailing slash from base, ensure no leading slash on slug, join with `/`. Use this consistently for all URL generation (RSS links, canonical URLs, og:url). The current `base.html` template already hardcodes `https://0xpili.xyz/{{ slug }}` which will break if the domain changes -- this is an opportunity to centralize URL construction.

**Detection:** Test that all `<link>` elements in the RSS feed are valid absolute URLs starting with `https://`. Test with both trailing-slash and no-trailing-slash `site_url` configs.

**Phase relevance:** RSS feed implementation phase.

### Pitfall 7: Incremental Build Cache Does Not Account for New Features

**What goes wrong:** After adding meta descriptions, tags, or RSS feed generation, the build cache (SHA256 of file content) still considers a post "unchanged" even though the template now uses new fields. Changing the template does not invalidate the cache, so existing posts are not rebuilt with the new meta description or tag metadata.

**Why it happens:** The current `_needs_rebuild()` only checks the post file's content hash against the cache and whether the output file exists. It does not track template changes or config changes.

**Prevention:** Include template file hashes in the cache check. When any template changes, all posts should rebuild. A simple approach: hash the template files at build start, store in cache, and force full rebuild if templates changed. Alternatively, during development of each new feature, manually clear `.build_cache.json` and document this in the build process.

**Detection:** Test: modify a template, run build, verify posts are rebuilt. Currently this test would fail -- the cache does not track templates.

**Phase relevance:** Relevant to ALL phases. Should be addressed first or flagged as a known limitation during each feature phase.

## Minor Pitfalls

### Pitfall 8: Meta Description Length Edge Cases

**What goes wrong:** Posts with very short content (under 160 chars), or posts that start with an image/code block instead of text, produce empty or unhelpful meta descriptions.

**Prevention:** Fall back to the site-wide description (already in CONFIG: "Thoughtful writings on technology, privacy...") when the auto-generated description is too short (under 50 chars) or empty. Skip non-text content (images, code blocks, headings) when scanning for description text.

**Phase relevance:** Meta descriptions phase.

### Pitfall 9: RSS Feed Size Grows Unbounded

**What goes wrong:** Including full HTML content for every post in the feed makes it grow linearly with post count. At 15 posts this is fine, but at 100+ posts with images, the feed becomes multiple MB.

**Prevention:** Limit the feed to the most recent 20 posts. Use truncated descriptions (first 500 chars of text content) rather than full HTML in `<description>`. Optionally offer full content in `<content:encoded>` for feed readers that support it.

**Phase relevance:** RSS feed implementation phase. Not urgent at 15 posts, but design for it now.

### Pitfall 10: Tag Header Format Conflicts with Existing Post Parsing

**What goes wrong:** Adding a `Tags:` header line to posts could interfere with the existing parser, which expects line 1 to be `Date:` and line 2 to optionally be `# Title`. A `Tags:` line inserted between them, or after the title, shifts line indices and breaks content extraction.

**Prevention:** Parse ALL header fields (Date, Tags, Draft) as a block at the top of the file before processing content. Use a loop that consumes header lines until it hits a non-header line (doesn't match `Key: Value` pattern or is a markdown heading). This replaces the current fragile index-based parsing (`lines[0]`, `lines[1]`).

**Detection:** Test with posts that have: (1) only Date header, (2) Date + Tags, (3) Date + Tags + Draft, (4) Date + Title + Tags. All should parse correctly with no content loss.

**Phase relevance:** Tags and drafts phases. Consider refactoring the header parser before adding any new header fields.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Meta descriptions | HTML/markdown artifacts in description text | Strip markdown before truncating, test with various content types |
| RSS feed | XML encoding of HTML content, wrong date format, malformed URLs | Use Jinja2 template for feed XML, validate with W3C validator, test RFC 822 dates |
| Draft support | Drafts leaking into index, feed, or tag listings; cached HTML persisting | Filter at parse time, delete stale output files, test all output surfaces |
| Tags | Inconsistent normalization, thin content if tag pages added | Normalize to lowercase-hyphenated, no tag pages initially, warn on single-use tags |
| All phases | Build cache not invalidated by template changes | Clear cache during development, consider adding template hashing to cache |
| Header parsing | New headers break index-based line parsing | Refactor to loop-based header parser before adding Tags/Draft headers |

## Sources

- [RSS Feed Errors: Common Problems & How to Fix Them](https://rssvalidator.app/rss-feed-errors)
- [WordPress Trac: CDATA in RSS feed titles/descriptions](https://core.trac.wordpress.org/ticket/59082)
- [Python issue 36874: ElementTree CDATA support](https://bugs.python.org/issue36874)
- [10 Mistakes to Avoid When Writing Meta Descriptions](https://www.searchenginejournal.com/meta-description-mistakes/250897/)
- [SEO and meta descriptions: Everything you need to know in 2025](https://searchengineland.com/seo-meta-descriptions-everything-to-know-447910)
- [Categories and Tags on Your Blog: How to Use Them the Right Way](https://delante.co/categories-and-tags-on-the-blog/)
- [Static site generators are great, but have limitations](https://www.garybell.co.uk/the-down-side-of-static-site-generators/)
- [W3C Feed Validator: Encoding Mismatch Warning](https://validator.w3.org/feed/docs/warning/EncodingMismatch.html)
- [W3C Wiki: RSS Content](https://www.w3.org/wiki/RssContent)
