"""Small helpers for writing README SVGs."""
from html import escape as _esc
from pathlib import Path


def esc(s):
    return _esc(str(s), quote=True)


def svg(w, h, body, title, family, style=""):
    st = f"<style>{style}</style>" if style else ""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{esc(family)}"><title>{esc(title)}</title>{st}{body}</svg>\n'
    )


def write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path} ({len(content.encode()) / 1024:.1f} KB)")
