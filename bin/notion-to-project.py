#!/usr/bin/env python3
# slug = 페이지 영문 이름 (소문자-하이픈): bin/notion-to-project.py export.zip my-project  =>  _projects/my-project.md, /projects/my-project/
"""Notion HTML export (.zip, .html or folder) -> _projects/<slug>.md draft + images.

Unrecognised blocks are left as `<!-- notion: ... -->` comments.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
NOTION_BODY_PX = 708  # Notion's default page width; image widths are px against it
FULL_WIDTH_SLACK = 0.9

VOID = {"img", "br", "hr", "input", "meta", "link", "col", "source", "wbr"}


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []

    @property
    def classes(self):
        return self.attrs.get("class", "").split()

    def has(self, cls):
        return cls in self.classes

    def elements(self):
        return [c for c in self.children if isinstance(c, Node)]

    def find(self, tag=None, cls=None):
        for c in self.elements():
            if (tag is None or c.tag == tag) and (cls is None or c.has(cls)):
                return c
            hit = c.find(tag, cls)
            if hit:
                return hit
        return None

    def find_all(self, tag=None, cls=None):
        out = []
        for c in self.elements():
            if (tag is None or c.tag == tag) and (cls is None or c.has(cls)):
                out.append(c)
            out.extend(c.find_all(tag, cls))
        return out

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("#root")

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(path):
    b = TreeBuilder()
    b.feed(Path(path).read_text(encoding="utf-8"))
    return b.root


def style_px(node, prop="width"):
    m = re.search(prop + r"\s*:\s*([\d.]+)px", node.attrs.get("style", ""))
    return float(m.group(1)) if m else None



def inline_md(node):
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(escape_text(c))
            continue
        inner = inline_md(c)
        t = c.tag
        if c.has("notion-text-equation-token"):
            tex = c.find("annotation")
            out.append(f"$${tex.text().strip()}$$" if tex else inner)
        elif t in ("strong", "b"):
            out.append(wrap(inner, "**"))
        elif t in ("em", "i"):
            out.append(wrap(inner, "*"))
        elif t in ("s", "del"):
            out.append(wrap(inner, "~~"))
        elif t == "code":
            out.append(f"`{escape_liquid(c.text())}`")
        elif t == "a":
            out.append(f"[{inner}]({c.attrs.get('href', '')})")
        elif t == "br":
            out.append("<br>")
        else:
            out.append(inner)
    return "".join(out)


def inline_html(node):
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(escape_text(html.escape(c, quote=False)))
            continue
        inner = inline_html(c)
        t = c.tag
        if c.has("notion-text-equation-token"):
            tex = c.find("annotation")
            out.append(f"$${html.escape(tex.text().strip(), quote=False)}$$" if tex else inner)
        elif t in ("strong", "b", "em", "i", "s", "del", "code"):
            t = {"b": "strong", "i": "em"}.get(t, t)
            out.append(f"<{t}>{inner}</{t}>")
        elif t == "a":
            out.append(f'<a href="{html.escape(c.attrs.get("href", ""))}">{inner}</a>')
        elif t == "br":
            out.append("<br>")
        else:
            out.append(inner)
    return "".join(out)


def wrap(s, mark):
    core = s.strip()
    if not core:
        return s
    lead = s[: len(s) - len(s.lstrip())]
    trail = s[len(s.rstrip()) :]
    return f"{lead}{mark}{core}{mark}{trail}"


def clean(s):
    s = re.sub(r"[ \t]+\n", "\n", s).strip()
    return re.sub(r"(<br>\s*)+$", "", s).strip()


def escape_text(s):
    return escape_liquid(re.sub(r"<(?=[A-Za-z/!])", "&lt;", s))


def escape_liquid(s):
    return s.replace("{{", "{{ '{{' }}").replace("{%", "{{ '{%' }}")


def escape_block_start(s):
    s = re.sub(r"^([*+-]|#+)(?=\s)", r"\\\1", s)
    return re.sub(r"^(\d+)\.(?=\s)", r"\1\\.", s)



class Converter:
    def __init__(self, html_path, slug):
        self.base = Path(html_path).parent
        self.slug = slug
        self.images = []  # (source Path, published name)
        self.missing_alt = []
        self.unhandled = []
        self.heading_shift = 0

    def register_image(self, fig):
        img = fig.find("img")
        src = img.attrs.get("src", "") if img else ""
        if src.startswith(("http://", "https://")):
            return src, None, img
        path = self.base / unquote(src)
        name = f"{len(self.images) + 1:02d}{path.suffix.lower() or '.png'}"
        self.images.append((path, name))
        return f"assets/img/projects/{self.slug}/{name}", name, img

    def figure(self, fig, container_px):
        path, _, img = self.register_image(fig)
        cap = fig.find("figcaption")
        caption = clean(inline_md(cap)) if cap else ""
        alt = clean(cap.text()) if cap else ""
        if not alt:
            self.missing_alt.append(path)
        attrs = [f'path="{path}"'] if not path.startswith("http") else [f'url="{path}"', 'path=""']
        cls = "img-fluid"
        width = style_px(img) if img else None
        if width and width < container_px * FULL_WIDTH_SLACK:
            align = "left" if "text-align:left" in fig.attrs.get("style", "").replace(" ", "") else "center"
            if align == "center":
                cls += " d-block mx-auto"
            attrs.append(f'class="{cls}"')
            attrs.append(f'max-width="{round(100 * width / container_px)}%"')
        else:
            attrs.append(f'class="{cls}"')
        attrs += ["zoomable=true", f'alt="{alt.replace(chr(34), chr(39))}"']
        return "{% include figure.liquid " + " ".join(attrs) + " %}", caption

    def blocks(self, node, container_px=NOTION_BODY_PX):
        out = []
        for c in node.elements():
            md = self.block(c, container_px)
            if md is not None and md.strip():
                out.append(md.rstrip())
        return out

    def block(self, n, container_px):
        t, cls = n.tag, n.classes
        if n.has("column-list"):
            return self.columns(n)
        if t == "figure" and n.has("image"):
            fig, cap = self.figure(n, container_px)
            return fig + (f'\n\n<p class="caption">{cap}</p>' if cap else "")
        if t in ("h1", "h2", "h3", "h4"):
            level = min(6, int(t[1]) + self.heading_shift)
            return "#" * level + " " + clean(inline_md(n))
        if t == "p":
            return escape_block_start(clean(inline_md(n)))
        if t in ("ul", "ol"):
            return self.list_block(n)
        if t == "pre":
            code = n.find("code")
            lang = next((c[len("language-") :] for c in (code.classes if code else []) if c.startswith("language-")), "")
            lang = "" if lang.lower() == "plain" else lang.lower()
            return f"```{lang}\n{escape_liquid((code or n).text().rstrip())}\n```"
        if t == "blockquote":
            return quote(clean(inline_md(n)))
        if t == "figure" and n.has("callout"):
            body = [b for b in self.blocks(n.elements()[-1], container_px)] if n.elements() else []
            return quote("\n\n".join(body) or clean(inline_md(n)))
        if t == "figure" and n.has("equation"):
            tex = n.find("annotation")
            return f"$$\n{tex.text().strip()}\n$$" if tex else None
        if t == "table":
            return self.table(n)
        if t == "hr":
            return "***"
        if t == "div" and (n.has("indented") or not cls):
            return "\n\n".join(self.blocks(n, container_px))
        if t == "details":
            return self.toggle(n)
        if t == "figure" and n.find("div", "source") and not n.find("a", "bookmark"):
            return embed(n)
        if t == "figure" and (n.has("link-to-page") or n.find("a", "bookmark")):
            a = n.find("a")
            return f"[{clean(a.text())}]({a.attrs.get('href', '')})" if a else None
        if t in ("script", "style", "link"):
            return None
        label = f"{t}.{'.'.join(cls)}" if cls else t
        self.unhandled.append(label)
        text = clean(n.text())
        return f"<!-- notion: unhandled {label} -->" + (f"\n\n{text}" if text else "")

    def list_block(self, n, pad=""):
        lines = []
        start = int(n.attrs.get("start", "1") or 1)
        for i, li in enumerate(li for li in n.elements() if li.tag == "li"):
            if n.has("toggle"):
                return self.toggle(li)
            head = Node("li")
            head.children = [c for c in li.children if not (isinstance(c, Node) and c.tag in ("ul", "ol"))]
            text = clean(inline_md(head))
            if n.has("to-do-list"):
                bullet = "- [x]" if li.find(cls="checkbox-on") else "- [ ]"
            elif n.tag == "ol":
                bullet = f"{start + i}."
            else:
                bullet = "-"
            lines.append(f"{pad}{bullet} {text}")
            # kramdown nests a sub-list only at the parent's text column
            sub_pad = pad + " " * (len(bullet if n.tag == "ol" else "-") + 1)
            for sub in li.elements():
                if sub.tag in ("ul", "ol"):
                    lines.append(self.list_block(sub, sub_pad))
        return "\n".join(lines)

    def toggle(self, li):
        det = li.find("details") or li
        summ = det.find("summary")
        body = Node("div")
        body.children = [c for c in det.children if c is not summ]
        inner = "\n\n".join(self.blocks(body))
        return f'<details markdown="1">\n<summary>{inline_html(summ) if summ else ""}</summary>\n\n{inner}\n\n</details>'

    def table(self, n):
        rows = []
        for tr in n.find_all("tr"):
            rows.append([clean(inline_md(c)).replace("|", "\\|").replace("\n", " ") for c in tr.elements() if c.tag in ("td", "th")])
        if not rows:
            return None
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(lines)

    def columns(self, n):
        cols = [c for c in n.elements() if c.has("column")]
        ratios = [float(c.attrs.get("data-notion-column-ratio") or 1 / len(cols)) for c in cols]
        grows = [round(r * 16) or 1 for r in ratios]
        g = gcd_all(grows)
        grows = [x // g for x in grows]
        equal = len(set(grows)) == 1
        out = ['<div class="row mt-3">']
        for col, ratio, grow in zip(cols, ratios, grows):
            style = "" if equal else f' style="flex-grow: {grow}"'
            out.append(f'  <div class="col-sm mt-3 mt-md-0"{style}>')
            for item in self.column_items(col, NOTION_BODY_PX * ratio):
                out.extend("    " + line if line else "" for line in item.split("\n"))
            out.append("  </div>")
        out.append("</div>")
        return "\n".join(out)

    def column_items(self, col, col_px):
        # kramdown does not parse Markdown inside an HTML block
        items = []
        for c in col.elements():
            if c.tag == "figure" and c.has("image"):
                fig, cap = self.figure(c, col_px)
                items.append(fig + (f'\n<p class="caption">{html_from_md_caption(c)}</p>' if cap else ""))
            elif c.tag in ("p", "h1", "h2", "h3", "h4"):
                text = clean(inline_html(c))
                if text:
                    items.append(f"<p>{text}</p>" if c.tag == "p" else f"<p><strong>{text}</strong></p>")
            elif c.tag in ("ul", "ol"):
                items.append(self.list_html(c))
            elif c.has("column-list"):
                items.append(self.columns(c))
            elif c.tag == "figure" and c.find("div", "source"):
                items.append(embed(c))
            elif c.tag == "pre":
                code = c.find("code") or c
                items.append(f"<pre><code>{escape_liquid(html.escape(code.text().rstrip(), quote=False))}</code></pre>")
            else:
                label = f"{c.tag}.{'.'.join(c.classes)}"
                self.unhandled.append(label + " (in column)")
                items.append(f"<!-- notion: unhandled {label} in column -->")
        return items

    def list_html(self, n):
        tag = "ol" if n.tag == "ol" else "ul"
        lis = []
        for li in n.find_all("li"):
            if li.parent is not n:
                continue
            head = Node("li")
            head.children = [c for c in li.children if not (isinstance(c, Node) and c.tag in ("ul", "ol"))]
            subs = "".join(self.list_html(s) for s in li.elements() if s.tag in ("ul", "ol"))
            lis.append(f"<li>{inline_html(head).strip()}{subs}</li>")
        return f"<{tag}>{''.join(lis)}</{tag}>"

    def convert(self, root):
        body = root.find("div", "page-body")
        if body is None:
            sys.exit("no <div class=\"page-body\"> found: is this a Notion HTML export?")
        body = merge_lists(body)
        levels = [int(h.tag[1]) for h in body.find_all() if h.tag in ("h1", "h2", "h3")]
        self.heading_shift = 3 - min(levels) if levels else 0
        return "\n\n".join(self.blocks(body))


def html_from_md_caption(fig):
    cap = fig.find("figcaption")
    return inline_html(cap).strip() if cap else ""


def embed_url(url):
    m = re.match(r"https://docs\.google\.com/(presentation|document|spreadsheets)/d/([\w-]+)", url)
    if m:
        kind, doc_id = m.groups()
        if kind == "presentation":
            return f"https://docs.google.com/presentation/d/{doc_id}/embed?start=false&loop=false"
        return f"https://docs.google.com/{kind}/d/{doc_id}/preview"
    m = re.match(r"https://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    return None


def embed(fig):
    # Notion embed block. Viewers need access to the source (e.g. Google sharing settings).
    a = fig.find("a")
    url = html.unescape(a.attrs.get("href", "")) if a else ""
    src = embed_url(url)
    if not src:
        return f"[{url}]({url})"
    return (
        f'<iframe src="{html.escape(src)}" loading="lazy" allowfullscreen '
        'style="width: 100%; aspect-ratio: 16 / 9; border: 0"></iframe>'
    )


def quote(s):
    return "\n".join("> " + line if line else ">" for line in s.split("\n"))


def gcd_all(xs):
    from math import gcd

    g = 0
    for x in xs:
        g = gcd(g, x)
    return g or 1


def merge_lists(node):
    # Notion writes every list item as its own <ul>/<ol>
    merged = []
    for c in node.children:
        if isinstance(c, Node):
            merge_lists(c)
        if isinstance(c, str) and not c.strip():
            merged.append(c)
            continue
        prev = next((m for m in reversed(merged) if not (isinstance(m, str) and not m.strip())), None)
        if (
            isinstance(c, Node)
            and isinstance(prev, Node)
            and c.tag in ("ul", "ol")
            and prev.tag == c.tag
            and prev.classes == c.classes
            and not c.has("toggle")
        ):
            for li in c.elements():
                li.parent = prev
                prev.children.append(li)
            continue
        merged.append(c)
    node.children = merged
    return node



def front_matter(root, conv):
    title = clean(root.find("h1", "page-title").text()) if root.find("h1", "page-title") else conv.slug
    desc_node = root.find("p", "page-description")
    desc = clean(desc_node.text()) if desc_node else ""
    props = {}
    table = root.find("table", "properties")
    if table:
        for tr in table.find_all("tr"):
            th, td = tr.find("th"), tr.find("td")
            if th and td:
                vals = [clean(s.text()) for s in td.find_all("span") if s.has("selected-value")]
                props[clean(th.text())] = ", ".join(vals) if vals else clean(td.text())
    year = next((v for k, v in props.items() if k.lower() in ("year", "date") and re.match(r"\d{4}", v)), "")
    first_img = f"assets/img/projects/{conv.slug}/{conv.images[0][1]}" if conv.images else ""

    def q(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' if s else ""

    lines = [
        "---",
        "layout: page",
        f"title: {q(title)}",
        "subtitle:",
        f"description: {q(desc)}".rstrip(),
        f"img: {first_img}",
        "category:",
        # an empty `date:` fails the whole build
        f"date: {year[:4]}-01-01" if year else "# date: YYYY-MM-DD (no Year property in Notion)",
        "period:",
        "role:",
        "status: completed",
        "tech_stack: []",
        "github:",
        "demo:",
        "has_detail: true",
    ]
    if props:
        lines.append("# Notion properties (reference only, not read by the site):")
        lines += [f"#   {k}: {v}" for k, v in props.items()]
    lines.append("---")
    return "\n".join(lines)



def locate_html(src, tmp):
    src = Path(src)
    if src.is_file() and src.suffix == ".html":
        return src
    if src.is_file() and src.suffix == ".zip":
        root = Path(tmp) / "export"
        with zipfile.ZipFile(src) as z:
            z.extractall(root)
        for inner in list(root.rglob("*.zip")):
            with zipfile.ZipFile(inner) as z:
                z.extractall(inner.parent)
        src = root
    if src.is_dir():
        pages = sorted(src.rglob("*.html"), key=lambda p: (len(p.parts), p.name))
        if not pages:
            sys.exit(f"no .html in {src}")
        if len(pages) > 1:
            print(f"note: {len(pages)} pages in export, converting the top-level one: {pages[0].name}", file=sys.stderr)
        return pages[0]
    sys.exit(f"not a .zip, .html or directory: {src}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", help="Notion HTML export: .zip, .html, or unzipped directory")
    ap.add_argument("slug", help="output name: _projects/<slug>.md, assets/img/projects/<slug>/")
    ap.add_argument("--out", help="write the Markdown here instead of _projects/<slug>.md")
    ap.add_argument("--force", action="store_true", help="re-run over an existing page: keeps its front matter, replaces body and images")
    ap.add_argument("--dry-run", action="store_true", help="print the Markdown, copy nothing")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit("slug must be lowercase kebab-case, e.g. oxford-iiit-segmentation")

    md_path = Path(args.out) if args.out else REPO / "_projects" / f"{args.slug}.md"
    img_dir = REPO / "assets" / "img" / "projects" / args.slug

    rerun = md_path.exists() and args.force
    with tempfile.TemporaryDirectory() as tmp:
        page = locate_html(args.source, tmp)
        root = parse(page)
        conv = Converter(page, args.slug)
        body = conv.convert(root)
        fm = front_matter(root, conv)
        if rerun:
            # Re-running after a Notion edit: keep the hand-filled front matter, replace the body.
            m = re.match(r"---\n.*?\n---\n", md_path.read_text(encoding="utf-8"), re.S)
            fm = m.group(0).rstrip("\n") if m else fm
        doc = fm + "\n\n" + body + "\n"

        missing = [str(p) for p, _ in conv.images if not p.is_file()]
        if missing:
            sys.exit("images referenced but not in export:\n  " + "\n  ".join(missing))

        if args.dry_run:
            sys.stdout.write(doc)
        else:
            if not args.force:
                if md_path.exists():
                    sys.exit(f"{md_path} exists (use --force, or --out somewhere else)")
                if img_dir.exists() and any(img_dir.iterdir()):
                    sys.exit(f"{img_dir} is not empty (use --force)")
            img_dir.mkdir(parents=True, exist_ok=True)
            for old in img_dir.iterdir():
                if re.fullmatch(r"\d{2}\.\w+", old.name):
                    old.unlink()
            for src, name in conv.images:
                shutil.copyfile(src, img_dir / name)
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(doc, encoding="utf-8")
            subprocess.run(["npx", "--no-install", "prettier", "--write", str(md_path)], cwd=REPO, capture_output=True)
            print(f"wrote {os.path.relpath(md_path, Path.cwd())} and {len(conv.images)} images to {os.path.relpath(img_dir, Path.cwd())}/")

    report = []
    if conv.missing_alt:
        report.append(f"{len(conv.missing_alt)} images have no alt text (Notion caption was empty)")
    if conv.unhandled:
        report.append("unhandled Notion blocks, left as <!-- notion: ... --> comments: " + ", ".join(sorted(set(conv.unhandled))))
    if not rerun:
        report.append("fill in front matter by hand: subtitle, description, category, period, role, tech_stack")
    for line in report:
        print("note: " + line, file=sys.stderr)


if __name__ == "__main__":
    main()
