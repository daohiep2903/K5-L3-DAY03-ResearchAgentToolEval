from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tools._shared import err


def _source_key(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError("Each item needs an absolute HTTP(S) URL")
    if parts.username is not None or parts.password is not None:
        raise ValueError("URLs containing credentials are not supported")
    host = parts.hostname.lower()
    if any(char.isspace() for char in host):
        raise ValueError("URL hostname must not contain whitespace")
    if ":" in host:
        host = f"[{host}]"
    port = parts.port  # Also validates malformed or out-of-range ports.
    scheme = parts.scheme.lower()
    if port is not None and (scheme, port) not in {("http", 80), ("https", 443)}:
        host += f":{port}"
    query = [
        (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}
    ]
    return urlunsplit((scheme, host, parts.path or "/", urlencode(query), ""))


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Remove URL duplicates without fetching sources or changing retained items."""
    try:
        if not isinstance(items, list):
            raise ValueError("items must be an array of source objects")
        unique: list[dict[str, Any]] = []
        seen: dict[str, int] = {}
        duplicates: list[dict[str, int]] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"items[{index}] must be an object")
            url = item.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"items[{index}].url must be a nonempty string")
            key = _source_key(url)
            if key in seen:
                duplicates.append({"index": index, "kept_index": seen[key]})
            else:
                seen[key] = index
                unique.append(dict(item))
        return {
            "tool": "deduplicate_sources",
            "items": unique,
            "input_count": len(items),
            "item_count": len(unique),
            "duplicate_count": len(duplicates),
            "duplicates": duplicates,
        }
    except Exception as exc:
        return err("deduplicate_sources", exc)
