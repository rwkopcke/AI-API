# uv run md_to_html.py 

from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

import environ as env

DEFAULT_CSS = """
:root {
 color-scheme: light dark;
}

html {
 box-sizing: border-box;
}

*, *:before, *:after {
 box-sizing: inherit;
}

body {
 margin: 0;
 padding: 0;
 font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
 line-height: 1.6;
 background: Canvas;
 color: CanvasText;
}

.container {
 max-width: 900px;
 margin: 0 auto;
 padding: 2rem 1.25rem 4rem;
}

article {
 font-size: 1rem;
}

h1, h2, h3, h4, h5, h6 {
 line-height: 1.25;
 margin-top: 2rem;
 margin-bottom: 0.75rem;
}

h1 {
 font-size: 2rem;
 border-bottom: 1px solid #8884;
 padding-bottom: 0.3rem;
}

h2 {
 font-size: 1.5rem;
 border-bottom: 1px solid #8883;
 padding-bottom: 0.2rem;
}

p, ul, ol, table, blockquote, pre {
 margin-top: 0;
 margin-bottom: 1rem;
}

ul, ol {
 padding-left: 1.5rem;
}

li > ul, li > ol {
 margin-top: 0.4rem;
 margin-bottom: 0.4rem;
}

code, pre, kbd, samp {
 font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

code {
 background: rgba(127, 127, 127, 0.12);
 padding: 0.15em 0.35em;
 border-radius: 6px;
}

pre {
 background: rgba(127, 127, 127, 0.12);
 padding: 1rem;
 border-radius: 10px;
 overflow-x: auto;
}

pre code {
 background: none;
 padding: 0;
 border-radius: 0;
}

blockquote {
 margin-left: 0;
 padding: 0.1rem 1rem;
 border-left: 4px solid #8886;
 color: color-mix(in srgb, CanvasText 85%, Canvas 15%);
}

table {
 border-collapse: collapse;
 width: 100%;
}

th, td {
 border: 1px solid #8884;
 padding: 0.5rem 0.75rem;
 text-align: left;
 vertical-align: top;
}

th {
 background: rgba(127, 127, 127, 0.08);
}

img {
 max-width: 100%;
 height: auto;
}

a {
 text-decoration-thickness: 1px;
 text-underline-offset: 2px;
}

hr {
 border: 0;
 border-top: 1px solid #8884;
 margin: 2rem 0;
}

.toc {
 margin: 0 0 2rem 0;
 padding: 1rem 1.25rem;
 border: 1px solid #8884;
 border-radius: 10px;
 background: rgba(127, 127, 127, 0.06);
}

.toc h2 {
 margin-top: 0;
 border-bottom: none;
 padding-bottom: 0;
 font-size: 1.1rem;
}

.toc ul {
 margin-bottom: 0;
}

.header-anchor {
 text-decoration: none;
 opacity: 0.35;
 margin-left: 0.35rem;
}

.header-anchor:hover {
 opacity: 1;
}

@media (max-width: 640px) {
 .container {
   padding: 1rem 0.9rem 3rem;
 }

 article {
   font-size: 0.98rem;
 }
}
"""


def slugify(text: str) -> str:
 import re
 text = text.strip().lower()
 text = re.sub(r"[^\w\s-]", "", text)
 text = re.sub(r"[\s_-]+", "-", text)
 text = re.sub(r"^-+|-+$", "", text)
 return text or "section"


def extract_headings(md_text: str) -> list[tuple[int, str, str]]:
 headings = []
 used = {}

 for line in md_text.splitlines():
   if not line.startswith("#"):
     continue

   level = len(line) - len(line.lstrip("#"))
   if not (1 <= level <= 6):
     continue

   text = line[level:].strip()
   if not text:
     continue

   base = slugify(text)
   count = used.get(base, 0)
   used[base] = count + 1
   slug = base if count == 0 else f"{base}-{count}"
   headings.append((level, text, slug))

 return headings


def build_toc(headings: list[tuple[int, str, str]]) -> str:
 if not headings:
   return ""

 html = ['<nav class="toc">', "<h2>Contents</h2>"]
 current_level = 0

 for level, text, slug in headings:
   while current_level < level:
     html.append("<ul>")
     current_level += 1
   while current_level > level:
     html.append("</ul>")
     current_level -= 1
   html.append(f'<li><a href="#{slug}">{text}</a></li>')

 while current_level > 0:
   html.append("</ul>")
   current_level -= 1

 html.append("</nav>")
 return "\n".join(html)


def make_markdown_parser() -> MarkdownIt:
 return (
   MarkdownIt("gfm-like", {"html": True, "linkify": True, "typographer": True})
   .use(anchors_plugin, permalink=True, permalinkSymbol="#", slug_func=slugify)
   .use(attrs_plugin)
   .use(tasklists_plugin)
 )


def markdown_to_html_document(
 md_text: str,
 title: str = "Document",
 include_toc: bool = True,
 css: str = DEFAULT_CSS,
) -> str:
 headings = extract_headings(md_text)
 toc_html = build_toc(headings) if include_toc else ""

 md = make_markdown_parser()
 body_html = md.render(md_text)

 return f"""<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="utf-8">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <title>{title}</title>
 <style>
{css}
 </style>
</head>
<body>
 <div class="container">
   {toc_html}
   <article>
{body_html}
   </article>
 </div>
</body>
</html>
"""


def convert_markdown_file(
 input_path: str | Path,
 output_path: str | Path | None = None,
 include_toc: bool = True,
) -> Path:
 input_path = Path(input_path)
 if output_path is None:
   output_path = input_path.with_suffix(".html")
 else:
   output_path = Path(output_path)

 md_text = input_path.read_text(encoding="utf-8")
 title = input_path.stem.replace("_", " ").replace("-", " ").title()

 html = markdown_to_html_document(
   md_text=md_text,
   title=title,
   include_toc=include_toc,
 )

 output_path.write_text(html, encoding="utf-8")
 return output_path


if __name__ == "__main__":
 print("\nInput markdown file should be in dir 'output_files/trieste'")
 input_ = input("Enter name of markdown source file:\n")
 in_file = env.TRIESTE_OUTPUT_FLDR / input_
 p = Path(input_)
 output = p.with_suffix(".html").name
 out_file = env.TRIESTE_OUTPUT_FLDR / output
 out = convert_markdown_file(input_path= in_file, 
                             output_path= out_file)
 print(f"Wrote {out}")