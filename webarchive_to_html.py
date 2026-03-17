# uv run webarchive_to_html.py "/Users/richardkopcke/Documents/chat_trieste.webarchive" -o "/Users/richardkopcke/Documents/chat_trieste"
# uv run webarchive_to_html.py "/Users/richardkopcke/Documents/gem_trieste.webarchive" -o "/Users/richardkopcke/Documents/gem_trieste"
# see README.md

from __future__ import annotations

import argparse
import hashlib
import mimetypes
import plistlib
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


def slugify_filename(name: str, max_len: int = 120) -> str:
    name = re.sub(r"[^\w.\-]+", "_", name.strip(), flags=re.UNICODE)
    name = re.sub(r"_+", "_", name).strip("._")
    if not name:
        name = "resource"
    return name[:max_len]


def guess_extension(
    mime_type: str | None,
    url: str | None,
    default: str = ".bin",
) -> str:
    if url:
        parsed = urlparse(url)
        suffix = Path(unquote(parsed.path)).suffix
        if suffix and len(suffix) <= 10:
            return suffix.lower()

    if mime_type:
        mime_clean = mime_type.split(";")[0].strip().lower()
        ext = mimetypes.guess_extension(mime_clean)
        if ext:
            if ext == ".jpe":
                return ".jpg"
            return ext.lower()

        mime_map = {
            "text/html": ".html",
            "application/xhtml+xml": ".xhtml",
            "text/css": ".css",
            "application/javascript": ".js",
            "text/javascript": ".js",
            "application/x-javascript": ".js",
            "image/svg+xml": ".svg",
            "application/json": ".json",
            "font/woff": ".woff",
            "font/woff2": ".woff2",
            "application/font-woff": ".woff",
            "application/octet-stream": default,
        }
        return mime_map.get(mime_clean, default)

    return default


def infer_resource_name(
    url: str | None,
    mime_type: str | None,
    data: bytes,
    ordinal: int,
) -> str:
    ext = guess_extension(mime_type, url)

    if url:
        parsed = urlparse(url)
        candidate = Path(unquote(parsed.path)).name
        candidate = slugify_filename(candidate)
        if candidate:
            if Path(candidate).suffix:
                return candidate
            return candidate + ext

    digest = hashlib.sha1(data).hexdigest()[:12]
    return f"resource_{ordinal:04d}_{digest}{ext}"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def read_webarchive(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        obj = plistlib.load(f)

    if not isinstance(obj, dict):
        raise ValueError("Top-level plist object is not a dictionary.")

    if "WebMainResource" not in obj:
        raise ValueError("This file does not appear to be a Safari .webarchive.")

    return obj


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)


def decode_text_bytes(data: bytes, preferred_encoding: str | None = None) -> str:
    candidates: list[str] = []
    if preferred_encoding:
        candidates.append(preferred_encoding)
    candidates.extend(["utf-8", "utf-16", "latin-1", "cp1252"])

    for enc in candidates:
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue

    return data.decode("utf-8", errors="replace")


def extract_main_html(webarchive: dict[str, Any], out_dir: Path) -> tuple[str, str | None]:
    main = webarchive["WebMainResource"]
    if not isinstance(main, dict):
        raise ValueError("WebMainResource is malformed.")

    data = main.get("WebResourceData")
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("Main resource does not contain byte data.")

    mime_type = main.get("WebResourceMIMEType")
    text_encoding = main.get("WebResourceTextEncodingName")
    url = main.get("WebResourceURL")

    html_text = decode_text_bytes(
        bytes(data),
        text_encoding if isinstance(text_encoding, str) else None,
    )

    main_ext = guess_extension(
        mime_type if isinstance(mime_type, str) else None,
        url if isinstance(url, str) else None,
        default=".html",
    )
    if main_ext not in {".html", ".htm", ".xhtml"}:
        main_ext = ".html"

    output_html = out_dir / f"index{main_ext}"
    output_html.write_text(html_text, encoding="utf-8", newline="")

    return html_text, url if isinstance(url, str) else None


def is_css_resource(mime_type: str | None, path: Path) -> bool:
    if mime_type and mime_type.split(";")[0].strip().lower() == "text/css":
        return True
    return path.suffix.lower() == ".css"


def save_subresources(
    webarchive: dict[str, Any],
    assets_dir: Path,
) -> tuple[dict[str, str], list[Path]]:
    subresources = webarchive.get("WebSubresources", [])
    if not isinstance(subresources, list):
        return {}, []

    url_to_local: dict[str, str] = {}
    seen_content: dict[str, str] = {}
    css_files: list[Path] = []

    for i, item in enumerate(subresources, start=1):
        if not isinstance(item, dict):
            continue

        data = item.get("WebResourceData")
        if not isinstance(data, (bytes, bytearray)):
            continue

        url = item.get("WebResourceURL")
        mime_type = item.get("WebResourceMIMEType")

        url_str = url if isinstance(url, str) else None
        mime_str = mime_type if isinstance(mime_type, str) else None
        raw = bytes(data)

        digest = hashlib.sha1(raw).hexdigest()
        if digest in seen_content:
            if url_str:
                url_to_local[url_str] = seen_content[digest]
            continue

        filename = infer_resource_name(url_str, mime_str, raw, i)
        out_path = ensure_unique_path(assets_dir / filename)
        write_bytes(out_path, raw)

        relative_path = out_path.relative_to(assets_dir.parent).as_posix()
        seen_content[digest] = relative_path

        if url_str:
            url_to_local[url_str] = relative_path

            parsed = urlparse(url_str)
            path_only = unquote(parsed.path)
            if path_only:
                url_to_local[path_only] = relative_path
                url_to_local[Path(path_only).name] = relative_path

        if is_css_resource(mime_str, out_path):
            css_files.append(out_path)

    return url_to_local, css_files


def build_replacement_candidates(original_url: str) -> list[str]:
    candidates = [original_url, original_url.replace("&", "&amp;")]

    parsed = urlparse(original_url)
    if parsed.scheme and parsed.netloc:
        path_only = unquote(parsed.path)
        if path_only:
            candidates.append(path_only)
            candidates.append(Path(path_only).name)

    seen: set[str] = set()
    ordered: list[str] = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def replace_urls_in_html(html: str, url_map: dict[str, str]) -> str:
    if not url_map:
        return html

    ordered_urls = sorted(url_map.keys(), key=len, reverse=True)
    for original_url in ordered_urls:
        local_url = url_map[original_url]
        for candidate in build_replacement_candidates(original_url):
            html = re.sub(re.escape(candidate), local_url, html)

    return html


def relativize_path(from_file: Path, to_file: Path) -> str:
    return Path(to_file).relative_to(from_file.parent.parent).as_posix() if False else Path(
        re.sub(r"\\", "/", str(Path(to_file).relative_to(from_file.parent)))
    ).as_posix()


def best_relative_reference(from_file: Path, target_rel_from_root: str) -> str:
    root_dir = from_file.parent.parent
    target_abs = root_dir / target_rel_from_root
    return Path(target_abs.relative_to(from_file.parent)).as_posix() if False else (
        Path(
            re.sub(
                r"\\",
                "/",
                str(Path(target_abs).relative_to(from_file.parent))
                if str(target_abs).startswith(str(from_file.parent))
                else str(Path(target_abs)),
            )
        ).as_posix()
    )


def make_relative_url(from_file: Path, root_dir: Path, target_rel_from_root: str) -> str:
    target_abs = root_dir / target_rel_from_root
    rel = Path(
        re.sub(r"\\", "/", str(Path(target_abs).relative_to(from_file.parent)))
    )
    return rel.as_posix()


def safe_relpath(target_abs: Path, from_dir: Path) -> str:
    import os

    return Path(os.path.relpath(target_abs, start=from_dir)).as_posix()


def rewrite_css_text(css_text: str, css_file: Path, root_dir: Path, url_map: dict[str, str]) -> tuple[str, int]:
    replacements = 0

    def resolve_reference(raw_ref: str) -> str | None:
        ref = raw_ref.strip().strip('"').strip("'")
        if not ref or ref.startswith("data:"):
            return None

        for key, rel_target in url_map.items():
            if ref == key:
                return safe_relpath(root_dir / rel_target, css_file.parent)

        parsed = urlparse(ref)
        path_only = unquote(parsed.path) if parsed.path else ""
        basename = Path(path_only).name if path_only else Path(ref).name

        if path_only and path_only in url_map:
            return safe_relpath(root_dir / url_map[path_only], css_file.parent)
        if basename and basename in url_map:
            return safe_relpath(root_dir / url_map[basename], css_file.parent)

        return None

    def replace_url_func(match: re.Match[str]) -> str:
        nonlocal replacements
        original = match.group(0)
        inner = match.group(1)

        new_ref = resolve_reference(inner)
        if new_ref is None:
            return original

        replacements += 1
        return f'url("{new_ref}")'

    def replace_import_func(match: re.Match[str]) -> str:
        nonlocal replacements
        prefix = match.group(1)
        quoted_ref = match.group(2)
        suffix = match.group(3) or ""

        new_ref = resolve_reference(quoted_ref)
        if new_ref is None:
            return match.group(0)

        replacements += 1
        return f'{prefix}"{new_ref}"{suffix}'

    url_pattern = re.compile(
        r"""url\(\s*([^)]+?)\s*\)""",
        flags=re.IGNORECASE,
    )

    import_pattern = re.compile(
        r"""(@import\s+)(?:"([^"]+)"|'([^']+)')(\s*[^;]*;)""",
        flags=re.IGNORECASE,
    )

    css_text = url_pattern.sub(replace_url_func, css_text)

    def import_wrapper(match: re.Match[str]) -> str:
        quoted = match.group(2) if match.group(2) is not None else match.group(3)
        rebuilt = replace_import_func(
            re.match(
                r"(?s)(@import\s+)(.*?)(\s*[^;]*;)",
                f'{match.group(1)}"{quoted}"{match.group(4)}',
            )
        )
        return rebuilt

    css_text = import_pattern.sub(import_wrapper, css_text)
    return css_text, replacements


def rewrite_css_files(css_files: list[Path], root_dir: Path, url_map: dict[str, str]) -> dict[str, int]:
    stats: dict[str, int] = {}

    for css_file in css_files:
        raw = css_file.read_bytes()
        css_text = decode_text_bytes(raw)
        new_text, count = rewrite_css_text(css_text, css_file, root_dir, url_map)

        if count > 0:
            css_file.write_text(new_text, encoding="utf-8", newline="")
        stats[str(css_file)] = count

    return stats


def write_report(
    out_dir: Path,
    source_file: Path,
    main_url: str | None,
    resource_count: int,
    html_rewrite_hits: int,
    css_stats: dict[str, int],
) -> None:
    css_total = sum(css_stats.values())
    css_lines = "\n".join(
        f"  {Path(path).name}: {count} replacements"
        for path, count in sorted(css_stats.items())
    ) or "  none"

    report = f"""Source file: {source_file}
Main URL: {main_url or "unknown"}
Resources extracted: {resource_count}
HTML replacements: {html_rewrite_hits}
CSS replacements: {css_total}

CSS file details:
{css_lines}

Open:
  {out_dir / "index.html"}

Notes:
- Some pages still will not render perfectly if the archive omitted external resources.
- JavaScript-heavy pages may rely on browser state that is not reproducible offline.
- Inline scripts can contain URLs that are difficult to rewrite safely with regex alone.
"""
    (out_dir / "README.txt").write_text(report, encoding="utf-8")


def convert_webarchive(input_file: Path, output_dir: Path) -> None:
    webarchive = read_webarchive(input_file)

    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    html_text, main_url = extract_main_html(webarchive, output_dir)
    url_map, css_files = save_subresources(webarchive, assets_dir)

    rewritten_html = replace_urls_in_html(html_text, url_map)
    index_html = output_dir / "index.html"
    index_html.write_text(rewritten_html, encoding="utf-8", newline="")

    html_rewrite_hits = sum(1 for key in url_map if key in html_text)
    css_stats = rewrite_css_files(css_files, output_dir, url_map)

    write_report(
        out_dir=output_dir,
        source_file=input_file,
        main_url=main_url,
        resource_count=len(url_map),
        html_rewrite_hits=html_rewrite_hits,
        css_stats=css_stats,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a Safari .webarchive into a browsable local folder."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the .webarchive file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Default: sibling folder named after the input file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_file: Path = args.input_file
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if args.output_dir is None:
        output_dir = input_file.parent / f"{input_file.stem}_extracted"
    else:
        output_dir = args.output_dir

    convert_webarchive(input_file=input_file, output_dir=output_dir)
    print(f"Done. Open: {output_dir / 'index.html'}")


if __name__ == "__main__":
    main()