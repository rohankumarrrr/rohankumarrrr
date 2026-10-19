"""Subset an OFL font to the glyphs a design uses and inline it as a base64 @font-face.

GitHub shows README SVGs through <img>, which can't fetch web fonts but does load data: URIs.
Each subset is renamed to its CSS alias (copyright and licence strings are kept), so no
Reserved Font Name travels with a modified font.
"""
import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent / "fonts"


def face(alias, filename, text, axes=None):
    font = TTFont(FONTS / filename)
    if axes:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, axes)
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = [0, 13, 14]          # copyright + OFL licence text and URL
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(set(text))) + " ")
    sub.subset(font)
    name = font["name"]
    for name_id, value in ((1, alias), (2, "Regular"), (4, alias), (6, alias)):
        name.setName(value, name_id, 3, 1, 0x409)
    font.flavor = "woff"
    buf = io.BytesIO()
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{alias}';src:url(data:font/woff;base64,{b64}) format('woff')}}"
