---
name: deduplicate_sources
track: core
kind: local_formatter
provider: local_python
requires_env: []
inputs: [items]
outputs: [items, input_count, item_count, duplicate_count, duplicates]
side_effect: false
---
# deduplicate_sources

Remove duplicate URLs from an existing source list before formatting a digest.
Use when the user asks to remove duplicate sources or multiple searches return
the same article. Do not use for searching, reading articles, checking truth,
merging similar content on different URLs, or formatting the final digest.
If no source list is available, ask for it rather than inventing items.

Each item must be an object with a nonempty absolute HTTP(S) `url`. Additional
fields (title, summary, source, section, etc.) are preserved. An empty list is
valid. Missing/wrong-type items and malformed URLs return an error dictionary;
no partial result is returned when any item is invalid.

Comparison ignores host/scheme case, default ports, URL fragments, and query
parameters named `utm_*`, `fbclid`, or `gclid` (case-insensitive). Retains path
case, other query parameters and their order, nondefault ports, and scheme.
The first original item wins; its original URL and metadata remain unchanged.
Duplicate records use zero-based indices into the original input list.

No network, files, keys, or publishing. URL normalization is a heuristic:
tracking parameters/fragments can affect content on some sites. Redirects,
syndicated articles, HTTP vs HTTPS, and non-root trailing slashes are not merged.

Example input:
```json
{"items": [{"title": "A", "url": "https://example.com/a"}, {"title": "A again", "url": "https://EXAMPLE.com/a?utm_source=x#top"}]}
```
Returns one retained item, `duplicate_count=1`, and
`duplicates=[{"index": 1, "kept_index": 0}]`.
