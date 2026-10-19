# Profile header generator

`channel_rack.py` draws `assets/channel-rack.svg`, the FL Studio channel rack at the top of the profile README.
It writes one self-contained SVG: no JavaScript, fonts embedded as base64 subsets, and animation in SMIL and
CSS keyframes, which GitHub still plays inside an `<img>`.

## Regenerate

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/channel_rack.py
```

Then commit `assets/channel-rack.svg`. GitHub's image cache can take a few minutes to show the new version.

## What to edit

All of it is at the top of `channel_rack.py`:

- `channels`: one row per channel as `(name, kind, mixer, content)`.
  - `kind` is `"light"` (sample), `"dark"` (plugin) or `"master"`.
  - `mixer` is the track number shown in the box, or `"---"`.
  - `content` is one of:
    - `("steps", "x...p...")`, a step pattern. `x` is lit, `p` is a quieter (pale) step, `o` is white and `.` is off.
    - `("roll", [(start, length, pitch), ...])`, piano-roll notes in 16th-note steps.
    - `("chords", [(start, length, [pitches]), ...])`, stacked notes.
    - `("pad", pitch)`, one note held for the whole loop.
- `BPM` and `LOOP_STEPS` set the tempo and the pattern length (48 steps is three bars).
- The palette constants hold the theme colors, sampled from the FL Studio pink theme.
- The project name and the "Today" hint text are in the toolbar section.

A channel name should stay under about 74px at 13px PT Sans Narrow, which is roughly 15 characters, to fit the 80px button.

## How it animates

It follows FL Studio's own playback:

- Step rows have no playhead.
- Piano-roll rows show a thin pink line with a soft trail. FL glides it smoothly; here it ticks once per beat (every quarter note) on purpose, for a choppy look.
- Each channel's selector strip fills grey while the channel sounds and fades out about 0.28s after note-off.
- The M:S:CS clock counts up in real time.

## Fonts

All three are SIL Open Font License 1.1. Each license is next to its font in `fonts/`.

- PT Sans Narrow: UI text. FL Studio bundles the same font.
- Roboto Condensed: the clock, tempo and pattern selector, at weight 300.
- Silkscreen: tiny pixel labels. It stands in for FL's proprietary microfont.

The generator subsets each font to the characters in use and renames the subset to its CSS alias, so no Reserved Font Name ships with a modified font.
