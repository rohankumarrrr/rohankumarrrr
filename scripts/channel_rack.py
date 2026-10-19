"""Option: rohan-is.me as an FL Studio channel rack, in Rohan's own theme (light UI, hot-pink accents).

Colours are sampled from Rohan's screenshots; geometry is the 2x capture at half size (native 1x).
Animation follows a screen recording of FL playing:
  - step rows have no playhead;
  - piano-roll rows show a thin pink line with a soft pink trail on its left (here it ticks once per beat,
    a deliberately choppy look; FL itself glides smoothly);
  - each channel's selector strip fills grey while the channel sounds and fades out after note-off.
Fonts: PT Sans Narrow (UI text) and Roboto Condensed Light (clock, tempo, pattern), both bundled with FL
and OFL-licensed; Silkscreen stands in for FL's proprietary pixel microfont.
"""
import random
from pathlib import Path

from fontkit import face
from svgkit import esc, svg, write

OUT = Path(__file__).resolve().parent.parent / "assets" / "channel-rack.svg"

W, H = 860, 444
BPM = 140
STEP = 60 / BPM / 4            # one 16th note, seconds
LOOP_STEPS = 48                # three bars, longer than the 41 visible steps, like a real pattern
LOOP = STEP * LOOP_STEPS
REL = 2.6                      # selector release, in steps (~0.28 s, as in the recording)

# ── palette (sampled) ──
WHITE, PANEL_BAR, BAR_LINE = "#ffffff", "#e9e9e9", "#cfcfcf"
LIT_T, LIT_M, LIT_B, LIT_EDGE = "#fd5ba6", "#f04996", "#da2b7d", "#c4488a"
OFF_T, OFF_M, OFF_B, OFF_EDGE = "#f9f9f9", "#dfe1e3", "#bdbfc1", "#b4b6b8"
PALE_T, PALE_B = "#ffd3ec", "#ffaedb"
ROLL_A, ROLL_B, NOTE = "#d9d9d9", "#e3e3e3", "#fb0092"
DARK_T, DARK_B = "#383838", "#2a2a2a"
LBTN_T, LBTN_B, BTN_EDGE = "#f8f8f8", "#dcdcdc", "#a9abad"
LED_ON, LED_RING = "#fe54bd", "#bf0e6e"
PINK, PINK_D = "#ff1f8f", "#d0007e"
PH_LINE, PH_TRAIL = "#fe5aa6", "#ffb8e6"
TEXT, TEXT_SOFT, ICON = "#2f2f33", "#8b8d92", "#3d2f37"
SEL_ON = "#9a9a9a"

# ── layout (1x) ──
ROW0, PITCH_Y = 112, 30
SX0, SPITCH, SW, SH = 209, 15.85, 11.5, 17
N_VIS = 41

channels = [
    # name, kind, mixer, content
    ("rohan...Master", "master", "---", ("steps", "....xxxx....xxxx")),
    ("building vinskal", "dark", "---", ("roll", [(0, 3, 6), (4, 2, 8), (8, 3, 5), (12, 2, 9), (16, 3, 6), (20, 2, 8), (24, 4, 3),
                                                   (29, 2, 9), (32, 3, 6), (36, 2, 10), (40, 4, 7), (45, 2, 5)])),
    ("cs+stats@uiuc", "light", "1", ("steps", "x...x...x...x..x")),
    ("pinterest", "dark", "3", ("chords", [(0, 12, [2, 4, 6, 8]), (16, 12, [1, 3, 5, 9]), (32, 14, [2, 5, 7, 9])])),
    ("prev@amazon", "light", "9", ("steps", "xpxpxpxpxpxpxpxp")),
    ("uiuc hci", "light", "---", ("steps", "....x..p....x..p")),
    ("prev@relativity", "dark", "6", ("pad", 5)),
    ("chicago", "light", "---", ("steps", "..x...x...x...xo")),
    ("nyc", "dark", "2", ("roll", [(0, 2, 2), (3, 1, 3), (6, 2, 2), (10, 2, 5), (14, 1, 4), (16, 2, 2), (19, 1, 3), (22, 2, 2),
                                   (26, 2, 6), (30, 1, 4), (32, 2, 2), (35, 1, 3), (38, 3, 1), (42, 2, 5), (46, 1, 4)])),
    ("rohan-is.me", "light", "7", ("chords", [(s, 2, [2, 4, 6]) for s in (3, 6, 11, 14, 19, 22, 27, 30, 35, 38, 43, 46)])),
]

NARROW, LIGHT, MICRO = "ptn", "rcl", "mic"
ui_text = ("".join(c[0] for c in channels) + "0123456789-.:+ All Channel rack Line Today rohan kumar is building "
           "vinskal.com [rohankumar] rohan-is.me ?")
fonts = (face(NARROW, "PT_Sans-Narrow-Web-Regular.ttf", ui_text)
         + face(LIGHT, "RobotoCondensed[wght].ttf", "0123456789:. Pattern", axes={"wght": 300})
         + face(MICRO, "Silkscreen-Regular.ttf", "PAT SONG M:S:CS MB 0123456789"))


def t(x, y, s, size, fill=TEXT, anchor="start", fam=NARROW, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}" font-family="{fam}"{a}{extra}>{esc(s)}</text>'


css, out = [], []
out.append(
    "<defs>"
    f'<linearGradient id="lit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LIT_T}"/><stop offset="0.5" stop-color="{LIT_M}"/><stop offset="1" stop-color="{LIT_B}"/></linearGradient>'
    f'<linearGradient id="off" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OFF_T}"/><stop offset="0.55" stop-color="{OFF_M}"/><stop offset="1" stop-color="{OFF_B}"/></linearGradient>'
    f'<linearGradient id="pale" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PALE_T}"/><stop offset="1" stop-color="{PALE_B}"/></linearGradient>'
    '<linearGradient id="white" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eeeeee"/></linearGradient>'
    f'<linearGradient id="lbtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LBTN_T}"/><stop offset="1" stop-color="{LBTN_B}"/></linearGradient>'
    f'<linearGradient id="dbtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DARK_T}"/><stop offset="1" stop-color="{DARK_B}"/></linearGradient>'
    '<linearGradient id="mbtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#626a71"/><stop offset="1" stop-color="#575f65"/></linearGradient>'
    '<linearGradient id="tool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ececec"/></linearGradient>'
    f'<linearGradient id="pinkbtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3d9f"/><stop offset="1" stop-color="{PINK_D}"/></linearGradient>'
    f'<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PH_TRAIL}" stop-opacity="0"/><stop offset="1" stop-color="{PH_TRAIL}" stop-opacity="0.95"/></linearGradient>'
    '<radialGradient id="knob" cx="0.45" cy="0.35" r="0.7"><stop offset="0" stop-color="#ffffff"/><stop offset="0.7" stop-color="#ececec"/><stop offset="1" stop-color="#cfcfcf"/></radialGradient>'
    f'<radialGradient id="led" cx="0.45" cy="0.4" r="0.6"><stop offset="0" stop-color="#ff8fd4"/><stop offset="0.6" stop-color="{LED_ON}"/><stop offset="1" stop-color="{LED_RING}"/></radialGradient>'
    "</defs>"
)
out.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{WHITE}" stroke="#c9cbcf"/>')


def tool(x, y, w=24, h=24, pink=False, inner=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3.5" fill="url(#{"pinkbtn" if pink else "tool"})" stroke="{PINK_D if pink else BTN_EDGE}"/>'
            f'<g transform="translate({x + w / 2} {y + h / 2})">{inner}</g>')


# ── toolbar row 1 ──
out.append(f'<path d="M1 10a9 9 0 0 1 9 -9H{W - 10}a9 9 0 0 1 9 9V36H1z" fill="#fbfcff"/>')
for k, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    out.append(f'<circle cx="{14 + k * 17}" cy="18" r="5.6" fill="{c}" stroke="#00000022"/>')
out.append(f'<rect x="66" y="5" width="34" height="26" rx="6" fill="#e2e4e5" stroke="{BTN_EDGE}"/>'
           f'<path d="M66 18H100V25a6 6 0 0 1 -6 6H72a6 6 0 0 1 -6 -6z" fill="{PINK}"/>'
           + t(83, 15, "PAT", 6, "#9a9ca0", "middle", MICRO) + t(83, 27.5, "SONG", 6, "#ffffff", "middle", MICRO))
out.append(f'<rect x="106" y="5" width="56" height="26" rx="13" fill="url(#tool)" stroke="{BTN_EDGE}"/><line x1="134" y1="7" x2="134" y2="29" stroke="#d6d6d6"/>'
           f'<path d="M116 12l10 6-10 6z" fill="{ICON}"/><rect x="143" y="13" width="10" height="10" fill="{ICON}"/>')
out.append(f'<circle cx="179" cy="18" r="12" fill="url(#tool)" stroke="{BTN_EDGE}"/><circle cx="179" cy="18" r="6" fill="#ededed" stroke="#c7c7c7"/>')
out.append(f'<rect x="196" y="6" width="62" height="24" rx="4" fill="#ffffff" stroke="{BTN_EDGE}"/>'
           + t(232, 25, "140", 19, ICON, "end", LIGHT) + t(232.5, 25, ".000", 10.5, ICON, fam=LIGHT)
           + '<path d="M253 14l-2 -3-2 3M253 22l-2 3-2 -3" fill="none" stroke="#b0b0b0"/>')
out.append(tool(266, 6, inner='<path d="M-6 6L0 -7L6 6Z M0 3L5 -5" fill="none" stroke="#3d3d3d" stroke-width="1.6" stroke-linejoin="round"/>'))
out.append(tool(294, 6, pink=True, inner=t(0, 4.5, "3.2", 12, "#5a0030", "middle", extra=' font-style="italic"')))
out.append(tool(322, 6, pink=True, inner='<path d="M-7 -5h14v10h-14z M-3 -5v6 M1 -5v6 M5 -2h4M7 -4v4" fill="none" stroke="#5a0030" stroke-width="1.6"/>'))
# song position, M:S:CS, really counting
out.append(f'<rect x="354" y="4" width="102" height="28" rx="3" fill="#ffffff" stroke="{BTN_EDGE}"/>' + t(451, 11, "M:S:CS", 4.5, "#5a4652", "end", MICRO))
TY = 28
xs = {"m": 366, "c1": 375, "s1": 384, "s2": 397, "c2": 407, "cs1": 418, "cs2": 429}
for key, ch in (("m", "0"), ("c1", ":"), ("c2", ":")):
    out.append(t(xs[key], TY, ch, 26, ICON, "middle", LIGHT))
out.append('<clipPath id="tclip"><rect x="377" y="7" width="72" height="24"/></clipPath>')
for key, n, dur, size in (("s1", 6, 60, 26), ("s2", 10, 10, 26), ("cs1", 10, 1, 18), ("cs2", 10, 0.1, 18)):
    strip = "".join(t(xs[key], TY + i * 30, str(i), size, ICON, "middle", LIGHT) for i in range(n))
    vals = ";".join(f"0 {-i * 30}" for i in range(n))
    out.append(f'<g clip-path="url(#tclip)"><g>{strip}<animateTransform attributeName="transform" type="translate" values="{vals}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></g></g>')
# scope
out.append(f'<rect x="462" y="4" width="112" height="28" rx="3" fill="#ffffff" stroke="{BTN_EDGE}"/>')
def scope(seed):
    r = random.Random(seed)
    return "M" + "L".join(f"{478 + i * 3.2:.1f} {18 + r.uniform(-1, 1) * r.choice((0.5, 1.5, 4)):.1f}" for i in range(29))
sc = [scope(s) for s in range(5)] + [scope(0)]
out.append(f'<rect x="466" y="8" width="7" height="20" fill="#f0f0f0"/><rect x="466" y="14" width="7" height="14" fill="#5b4a52"><animate attributeName="y" values="14;20;11;17;14" dur="{LOOP / 3:.3f}s" repeatCount="indefinite"/><animate attributeName="height" values="14;8;17;11;14" dur="{LOOP / 3:.3f}s" repeatCount="indefinite"/></rect>')
out.append(f'<path d="{sc[0]}" fill="none" stroke="#8d8f94" stroke-width="1"><animate attributeName="d" values="{";".join(sc)}" dur="{LOOP:.3f}s" repeatCount="indefinite"/></path>')
# cpu / memory
out.append(f'<rect x="580" y="4" width="124" height="28" rx="3" fill="#ffffff" stroke="{BTN_EDGE}"/>'
           f'<rect x="584" y="8" width="9" height="9" fill="#5b4a52"/>' + t(650, 15.5, "19", 6, ICON, "end", MICRO)
           + f'<rect x="654" y="8" width="7" height="9" fill="#5b4a52"/>' + t(700, 15.5, "2993 MB", 6, ICON, "end", MICRO)
           + t(690, 28.5, "0", 6, ICON, "end", MICRO) + '<path d="M584 28h16l3 -3 4 2 5 -1h70" fill="none" stroke="#8d8f94"/>')
icons = ['<circle r="6" fill="none" stroke="#3d3d3d" stroke-width="1.8"/><path d="M-2 -8l3 2-3 2" fill="none" stroke="#3d3d3d" stroke-width="1.8"/>',
         '<path d="M-5 -6l10 12M5 -6l-10 12" stroke="#3d3d3d" stroke-width="1.8"/><circle cx="-4" cy="6" r="2" fill="none" stroke="#3d3d3d"/><circle cx="4" cy="6" r="2" fill="none" stroke="#3d3d3d"/>',
         '<rect x="-3" y="-7" width="6" height="10" rx="3" fill="#3d3d3d"/><path d="M-5 0a5 5 0 0 0 10 0M0 5v3" fill="none" stroke="#3d3d3d" stroke-width="1.5"/>',
         t(0, 5, "?", 15, "#3d3d3d", "middle", extra=' font-weight="700"'),
         '<path d="M-6 -6h10l2 2v10h-12z" fill="#3d3d3d"/><rect x="-3" y="-6" width="6" height="4" fill="#fff"/>']
for k, ic in enumerate(icons):
    out.append(tool(712 + k * 28, 6, inner=ic))

# ── toolbar row 2 ──
out.append(f'<line x1="1" y1="36.5" x2="{W - 1}" y2="36.5" stroke="#e1e3e6"/>')
out.append(f'<rect x="8" y="40" width="210" height="24" rx="2" fill="{PANEL_BAR}" stroke="#d2d2d2"/>' + t(14, 56, "[rohankumar] rohan-is.me", 11, TEXT_SOFT))
out.append(tool(226, 40, pink=True, inner='<rect x="-7" y="-5" width="14" height="10" fill="none" stroke="#5a0030" stroke-width="1.6"/><path d="M-7 0h14M-3 -5v10M2 -5v10" stroke="#5a0030" stroke-width="1.2"/>'))
out.append(tool(254, 40, inner='<path d="M-6 0h10M1 -4l4 4-4 4" fill="none" stroke="#3d3d3d" stroke-width="2"/>'))
out.append(tool(282, 40, inner='<path d="M-1 5V-6l6 3" fill="none" stroke="#3d3d3d" stroke-width="1.8"/><circle cx="-3.5" cy="5" r="2.5" fill="#3d3d3d"/>'))
out.append(tool(310, 40, pink=True, inner='<path d="M-6 3l4 -4M-2 6l8 -8M2 -6l4 4" fill="none" stroke="#5a0030" stroke-width="1.8" stroke-linecap="round"/>'))
out.append(f'<rect x="342" y="42" width="58" height="20" rx="2" fill="#e8e8e8" stroke="#d0d0d0"/>' + t(348, 56, "Line", 11, TEXT) + '<path d="M392 49l3 3-3 3" fill="none" stroke="#777"/>')
out.append(f'<rect x="408" y="42" width="16" height="20" rx="2" fill="#ffffff" stroke="{BTN_EDGE}"/><path d="M414 48l4 4-4 4" fill="none" stroke="#555"/>'
           f'<rect x="426" y="42" width="96" height="20" rx="2" fill="#ffffff" stroke="{BTN_EDGE}"/>' + t(508, 58, "Pattern 1", 15, TEXT, "end", LIGHT)
           + f'<rect x="524" y="42" width="16" height="20" rx="2" fill="#ffffff" stroke="{BTN_EDGE}"/>' + t(532, 57, "+", 13, TEXT, "middle"))
glyphs = ['<rect x="-6" y="-5" width="12" height="10" fill="none" stroke="#3d3d3d" stroke-width="1.4"/><path d="M-6 -1h12" stroke="#3d3d3d"/><rect x="-4" y="1" width="5" height="2" fill="#ff1f8f"/>',
          '<path d="M-6 -5v10M-2 -5v10M2 -1v6M6 -3v8" stroke="#3d3d3d" stroke-width="2"/>',
          '<rect x="-6" y="-6" width="12" height="4" fill="none" stroke="#3d3d3d"/><rect x="-6" y="-1" width="12" height="4" fill="none" stroke="#3d3d3d"/><rect x="-6" y="4" width="12" height="3" fill="none" stroke="#3d3d3d"/>',
          '<path d="M-4 -6v12M0 -6v12M4 -6v12" stroke="#3d3d3d" stroke-width="1.4"/><rect x="-6" y="-2" width="4" height="3" fill="#3d3d3d"/><rect x="2" y="1" width="4" height="3" fill="#3d3d3d"/>',
          '<path d="M-5 -6h7l3 3v9h-10z" fill="#3d3d3d"/>']
for k, g in enumerate(glyphs):
    out.append(tool(548 + k * 28, 40, inner=g))
out.append(f'<rect x="690" y="39" width="162" height="27" rx="2" fill="#fffffc" stroke="#d6d6d6"/>'
           + t(696, 51, "Today", 10, "#9b9da2") + t(722, 51, "rohan kumar is", 10.5, TEXT)
           + t(696, 62.5, "building vinskal.com", 10.5, TEXT))

# ── channel rack window ──
RY = 72
out.append(f'<rect x="1" y="{RY}" width="{W - 2}" height="28" fill="{PANEL_BAR}"/><line x1="1" y1="{RY + 28.5}" x2="{W - 1}" y2="{RY + 28.5}" stroke="{BAR_LINE}"/>')
out.append(f'<path d="M9 {RY + 9}l6 5-6 5z" fill="#555"/><path d="M33 {RY + 17}a5 5 0 1 0 -2 -6M29 {RY + 7}l2 4 4 -2" fill="none" stroke="#555" stroke-width="1.6"/>')
out.append(f'<rect x="103" y="{RY + 4}" width="80" height="20" rx="2" fill="url(#lbtn)" stroke="#8f9194"/>' + t(108, RY + 18.5, "All", 12, TEXT)
           + f'<path d="M176 {RY + 11}l3 3-3 3" fill="none" stroke="#777"/>')
out.append(f'<path d="M198 {RY + 6}v16" stroke="#c4c4c4" stroke-dasharray="1 2"/>')
out.append(f'<path d="M213 {RY + 11}h3l4 -4v14l-4 -4h-3z" fill="none" stroke="#444" stroke-width="1.4"/><path d="M223 {RY + 10}l4 4-4 4" fill="#444"/>'
           + t(232, RY + 19.5, "Channel rack", 14, "#3b3b3e"))

out.append(f'<clipPath id="grid"><rect x="{SX0 - 4}" y="{ROW0 - 4}" width="{W - SX0 + 2}" height="{len(channels) * PITCH_Y + 4}"/></clipPath>')


def keycap_def(kind):
    fill = {"x": "url(#lit)", "p": "url(#pale)", "o": "url(#white)", ".": "url(#off)"}[kind]
    edge = {"x": LIT_EDGE, "p": "#f08cc0", "o": "#c9c9c9", ".": OFF_EDGE}[kind]
    slot = {"x": "#7d0b44", "p": "#e05a9c", "o": "#9a9a9a", ".": "#7f8285"}[kind]
    kid = {"x": "kx", "p": "kp", "o": "ko", ".": "kd"}[kind]
    return (f'<g id="{kid}"><rect x="0" y="0" width="{SW}" height="{SH}" rx="2.6" fill="{fill}" stroke="{edge}" stroke-width="0.8"/>'
            f'<rect x="3" y="3.2" width="{SW - 6}" height="1.6" rx="0.8" fill="{slot}" opacity="0.75"/>'
            f'<rect x="1.2" y="0.9" width="{SW - 2.4}" height="1.4" rx="0.7" fill="#fff" opacity="{0.55 if kind != "x" else 0.35}"/></g>')


out.append("<defs>" + "".join(keycap_def(k) for k in "xpo.") + "</defs>")
keycap = lambda x, y, kind: f'<use href="#{ {"x": "kx", "p": "kp", "o": "ko", ".": "kd"}[kind] }" x="{x:.1f}" y="{y}"/>'


def envelope(notes):
    """Selector fill over one loop: on at note start, held while the note sounds, linear release after."""
    def v(tt):
        best = 0.0
        for s, ln, pk in notes:
            for shift in (0, -LOOP_STEPS):      # tails from the previous loop
                s2, e2 = s + shift, s + ln + shift
                if s2 <= tt < e2:
                    best = max(best, pk)
                elif e2 <= tt < e2 + REL:
                    best = max(best, pk * (1 - (tt - e2) / REL))
        return best
    res = 8
    pts = [(i / res, v(i / res)) for i in range(LOOP_STEPS * res + 1)]
    keep = [pts[0]]
    for a, b in zip(pts[1:-1], pts[2:]):
        p = keep[-1]
        # drop a point that lies on the line between its neighbours
        if abs((a[1] - p[1]) * (b[0] - p[0]) - (b[1] - p[1]) * (a[0] - p[0])) > 1e-4:
            keep.append(a)
    keep.append(pts[-1])
    return keep


grid, roll_rows = [], []
for r, (name, kind, mixer, content) in enumerate(channels):
    y = ROW0 + r * PITCH_Y
    cy = y + 12
    out.append(f'<circle cx="14" cy="{cy}" r="5.2" fill="url(#led)" stroke="#9e9e9e" stroke-width="0.8"/>')
    for kx, ang in ((31, 0), (48, [95, 140, 120, 60, 130, 100, 110, 90, 105, 125][r])):
        out.append(f'<g transform="translate({kx} {cy})"><circle r="7.4" fill="url(#knob)" stroke="#b9b9b9" stroke-width="0.8"/>'
                   f'<line x1="0" y1="0" x2="0" y2="-6.2" stroke="#3b3b3b" stroke-width="1.5" stroke-linecap="round" transform="rotate({ang})"/></g>')
    out.append(f'<rect x="62" y="{y + 1}" width="32" height="22" rx="3" fill="#ffffff" stroke="#b7b9bb"/>'
               + t(86, y + 17.5, mixer, 14 if mixer != "---" else 11, "#4a4c50", "end")
               + f'<path d="M89 {y + 7}l2 -2 2 2M89 {y + 17}l2 2 2 -2" fill="none" stroke="#c9c9c9" stroke-width="0.8"/>')
    fill = {"light": "url(#lbtn)", "dark": "url(#dbtn)", "master": "url(#mbtn)"}[kind]
    out.append(f'<rect x="104" y="{y}" width="80" height="24" rx="2.5" fill="{fill}" stroke="{BTN_EDGE if kind == "light" else "#1a1a1a"}"/>'
               + t(144, y + 16.8, name, 13, "#222225" if kind == "light" else "#f0f0f0", "middle"))
    # selector strip: pink outline on the selected channel, grey fill while the channel sounds
    out.append(f'<rect x="193" y="{y + 1.5}" width="6" height="21" rx="2" fill="#f7f7f7" stroke="{PINK if r == 0 else "#d4d4d4"}" stroke-width="{1.6 if r == 0 else 0.8}"/>')
    out.append(f'<rect class="act{r}" x="194" y="{y + 2.5}" width="4" height="19" rx="1.5" fill="{SEL_ON}"/>')

    ctype, notes = content[0], []
    if ctype == "steps":
        pat = content[1]
        for i in range(N_VIS):
            grid.append(keycap(SX0 + i * SPITCH, y + 3, pat[i % len(pat)]))
        for i in range(LOOP_STEPS):
            ch = pat[i % len(pat)]
            if ch in "xp":
                notes.append((i, 1, 1.0 if ch == "x" else 0.55))
    else:
        roll_rows.append(y)
        for b in range(0, N_VIS, 16):
            grid.append(f'<rect x="{SX0 + b * SPITCH - 2:.1f}" y="{y}" width="{16 * SPITCH:.1f}" height="{PITCH_Y - 2}" fill="{ROLL_A if (b // 16) % 2 == 0 else ROLL_B}"/>')
        ny = lambda p: y + PITCH_Y - 5 - p * 2.1
        bar = lambda s, ln, p, th=2.6: f'<rect x="{SX0 + s * SPITCH - 2:.1f}" y="{ny(p):.1f}" width="{ln * SPITCH - 2:.1f}" height="{th}" fill="{NOTE}"/>'
        if ctype == "roll":
            for s, ln, p in content[1]:
                grid.append(bar(s, ln, p))
                notes.append((s, ln, 1.0))
        elif ctype == "chords":
            for s, ln, ps in content[1]:
                grid.extend(bar(s, ln, p) for p in ps)
                notes.append((s, ln, 1.0))
        elif ctype == "pad":
            grid.append(f'<rect x="{SX0 - 2}" y="{ny(content[1]):.1f}" width="{W - SX0}" height="4" fill="{NOTE}"/>')
            notes.append((0, LOOP_STEPS, 1.0))
    env = envelope(notes)
    frames = " ".join(f"{tt / LOOP_STEPS * 100:.3f}% {{ opacity: {vv:.2f} }}" for tt, vv in env)
    css.append(f"@keyframes act{r} {{ {frames} }} .act{r} {{ animation: act{r} {LOOP:.4f}s linear infinite }}")

out.append(f'<g clip-path="url(#grid)">{"".join(grid)}</g>')

# playhead: piano-roll rows only, a thin line with a pink trail behind it, ticking once per beat (every 4 steps)
out.append('<clipPath id="rolls">' + "".join(f'<rect x="{SX0 - 2}" y="{y}" width="{W - SX0}" height="{PITCH_Y - 2}"/>' for y in roll_rows) + "</clipPath>")
out.append(f'<g clip-path="url(#rolls)"><g class="ph"><rect x="{SX0 - 2 - 18}" y="{ROW0}" width="18" height="{len(channels) * PITCH_Y}" fill="url(#trail)"/>'
           f'<rect x="{SX0 - 2}" y="{ROW0}" width="1.3" height="{len(channels) * PITCH_Y}" fill="{PH_LINE}"/></g></g>')
css.append(f"@keyframes ph {{ from {{ transform: translate(0px, 0px) }} to {{ transform: translate({LOOP_STEPS * SPITCH:.2f}px, 0px) }} }}"
           f" .ph {{ animation: ph {LOOP:.4f}s steps({LOOP_STEPS // 4}) infinite }}")

# add-channel button + scrollbar, as in the real rack
by = ROW0 + len(channels) * PITCH_Y + 6
out.append(t(W / 2 - 40, by + 12, "+", 17, "#555", "middle", extra=' font-weight="700"'))
out.append(f'<rect x="{SX0}" y="{H - 10}" width="{W - SX0 - 10}" height="5" rx="2.5" fill="#e6e6e6"/><rect x="{SX0}" y="{H - 10}" width="300" height="5" rx="2.5" fill="#cfcfcf"/>')

write(OUT, svg(W, H, "".join(out),
      "FL Studio channel rack, [rohankumar] rohan-is.me at 140 BPM. Channels: rohan...Master, building vinskal, cs+stats@uiuc, pinterest, prev@amazon, uiuc hci, prev@relativity, chicago, nyc, rohan-is.me.",
      family=NARROW, style=fonts + " " + " ".join(css)))
