# Feature Landscape

**Domain:** Static blog generator improvements (meta descriptions, RSS, drafts, tags)
**Researched:** 2026-03-29

## Table Stakes

Features users (and search engines / feed readers) expect. Missing = the blog feels incomplete or loses discoverability.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Meta descriptions from content | Every SSG (Hugo, Jekyll, Pelican) auto-generates these. Google uses them for search snippets. Without them, Google fabricates its own (often poorly). The template already has a `{{ description }}` placeholder but blogmaker passes `None` for every post. | Low | Extract first ~155 chars of plain text from post content. Strip markdown/HTML. Already wired in templates. |
| RSS 2.0 feed | RSS is the universal blog subscription mechanism. Readers who subscribe via Feedly, NetNewsWire, Miniflux, etc. cannot follow the blog without it. Every major SSG ships RSS out of the box. | Low-Med | Generate `feed.xml` during build using Python stdlib `xml.etree`. No new dependencies needed. Required fields: channel title/link/description + item title/link/description/pubDate per post. |
| Draft post support | Standard in Hugo (`draft: true`), Jekyll (`published: false`), Pelican (`Status: draft`). Authors need to commit WIP posts without publishing them. Without drafts, the only workflow is a separate git branch per post. | Low | Add `Draft: true` header line. Skip draft posts from index, feed, and output. Convention: drafts are parsed but not rendered or listed. |
| `<link rel="alternate" type="application/rss+xml">` in HTML head | Feed autodiscovery. Without this `<link>` tag in the HTML `<head>`, RSS readers cannot automatically find the feed from the blog URL. | Trivial | Add one line to base.html and index.html templates. Do this alongside RSS feed generation. |

## Differentiators

Features that go beyond baseline. Not expected from a minimal handcrafted blog, but add genuine value.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Tags with tag index pages | Lets readers browse by topic. Useful for a 15+ post blog spanning crypto, AI, philosophy, and athletics. Pelican and Hugo generate per-tag pages automatically. | Medium | Requires: (1) `Tags:` header parsing, (2) tag collection during build, (3) tag index page template, (4) per-tag page generation. The tag page template is new work. |
| Open Graph description meta tag | `og:description` for social sharing previews. Twitter/LinkedIn/Slack use these to render link cards. Currently missing from templates. | Trivial | Piggybacks on meta description work. Add `<meta property="og:description" content="{{ description }}">` to templates. |
| Open Graph image meta tag | `og:image` for social sharing. Posts already extract cover images. Wiring `og:image` into templates means shared links show the cover photo. | Trivial | Add `<meta property="og:image" content="{{ cover_image }}">` to base.html. Data already available. |
| Tag display on post pages | Show tags at the bottom of each post, linking to the tag index page. Helps readers discover related content. | Low | Requires tag index pages to exist first. Simple template addition. |

## Anti-Features

Features to explicitly NOT build. These violate the blog's core philosophy of zero JS, minimal weight, and decade-long durability.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Full-text search | Requires JavaScript (lunr.js, pagefind, etc.). Violates zero-JS constraint. Adds significant page weight. | Tags provide lightweight categorization. Browser Ctrl+F works for single pages. |
| Pagination | 15 posts is not enough to need pagination. The index page is under 10KB. Adding pagination adds complexity for no user benefit at current scale. | Revisit only if post count exceeds 50+. |
| Related posts / "you may also like" | Typically requires JS or complex build-time similarity analysis. Low value for a personal blog. | Tags serve this purpose implicitly. |
| Comments system | Requires external service (Disqus, Utterances, Giscus) or JS. Violates zero-dependency philosophy. | Link to social media or email for discussion. |
| Newsletter / email subscription | Requires external service and tracking. Violates minimalist philosophy. | RSS is the subscription mechanism. |
| Category hierarchy (nested tags) | Over-engineering for 15 posts. Flat tags are sufficient. | Use flat tags. Revisit if tag count exceeds 20+. |
| Scheduled publishing (future dates) | Requires a build trigger mechanism (cron, CI schedule). Adds operational complexity for marginal benefit. | Manually run build when ready to publish. |
| Post excerpts on homepage | User explicitly excluded this from scope in PROJECT.md. | Meta descriptions serve SEO; homepage shows title + date, which is sufficient for a minimalist blog. |

## Feature Dependencies

```
Meta Descriptions -----> OG Description (trivial addition once descriptions exist)
                  \
                   '---> RSS Feed (descriptions used as item <description>)

RSS Feed -----------> Feed autodiscovery link tag (must ship together)

Tags Header Parsing -> Tag display on posts -> Tag index pages
                                            \
                                             '--> Tags excluded from RSS for drafts (if both exist)

Draft Support -------> RSS Feed (drafts must be excluded from feed)
               \
                '----> Index page (drafts must be excluded from index)
```

## MVP Recommendation

**Phase 1 — Ship together (all Low complexity, high impact):**
1. **Meta descriptions** — Extract first ~155 chars of plain text from post content. Already wired in templates (`description` variable exists). Enables OG description for free.
2. **RSS feed** — Generate `feed.xml` with Python stdlib XML. Add autodiscovery `<link>` to templates. Use meta descriptions as item descriptions.
3. **Draft support** — Parse `Draft: true` header. Skip drafts from build output, index, and feed.

**Phase 2 — Tags (Medium complexity, builds on Phase 1):**
4. **Tags** — Parse `Tags:` comma-separated header. Generate per-tag pages. Display tags on posts. Exclude draft post tags from tag pages.

**Rationale for ordering:**
- Meta descriptions are a prerequisite for good RSS item descriptions, so they come first.
- RSS and drafts are independent but drafts affect RSS output, so implementing them together avoids rework.
- Tags are the most complex feature and benefit from the header-parsing patterns established by drafts.

**Defer:** Tag index pages could ship as a separate sub-phase if tags-on-posts alone provides enough value.

## Implementation Notes

### Meta Descriptions
- Strip markdown syntax and HTML tags from first paragraph
- Truncate to 155 characters at word boundary, append ellipsis
- Fallback: site description from CONFIG if post content is too short
- Pass to template as `description` variable (already accepted by templates)

### RSS Feed
- Use RSS 2.0 format (simpler than Atom, widely supported)
- Required channel elements: `<title>`, `<link>`, `<description>`, `<language>`
- Required item elements: `<title>`, `<link>`, `<description>`, `<pubDate>`, `<guid>`
- Use `xml.etree.ElementTree` from stdlib (no new dependencies)
- Output to `docs/feed.xml`
- Include last 20 posts (configurable) sorted by date descending

### Draft Support
- Header format: `Draft: true` (case-insensitive on the value)
- Placed on line 2 (after `Date:` header) or as additional metadata line
- Convention matches existing header pattern (`Date:`, then content)
- Drafts are parsed (for validation) but not rendered, indexed, or included in feed
- Consistent with how org-static-blog and Hugo handle drafts

### Tags
- Header format: `Tags: crypto, ai, philosophy` (comma-separated)
- Normalize: lowercase, strip whitespace
- Generate `/tags.html` index page listing all tags with post counts
- Generate `/tags/{tag}.html` pages listing posts for each tag
- Display tags on post pages as links to tag pages

## Sources

- [RSS 2.0 Specification](https://www.rssboard.org/rss-specification)
- [RSS Feed Best Practices - Kevin Cox](https://kevincox.ca/2022/05/06/rss-feed-best-practices/)
- [Meta Tags That Matter in 2026](https://www.sewwa.com/meta-tags-guide-2026/)
- [Meta Descriptions Best Practices - Analytify](https://analytify.io/how-to-write-meta-descriptions-for-seo-and-ctr/)
- [Jekyll Feed Plugin](https://github.com/jekyll/jekyll-feed)
- [Hugo RSS/Atom Discussion](https://discourse.gohugo.io/t/porting-from-jekyll-and-need-an-atom-feed-and-rss-feed/1512)
- [org-static-blog (draft/tag conventions)](https://github.com/bastibe/org-static-blog)
- [Pelican Documentation](https://docs.getpelican.com/)
