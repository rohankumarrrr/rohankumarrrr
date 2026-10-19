# Profile header generator

`channel_rack.py` draws `assets/channel-rack-<hash>.svg`, the FL Studio channel rack at the top of the profile README.
It writes one self-contained SVG: no JavaScript, fonts embedded as base64 subsets, and animation in SMIL and
CSS keyframes, which GitHub still plays inside an `<img>`.

## Regenerate

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/channel_rack.py
```

The script writes `assets/channel-rack-<hash>.svg`, named by a hash of its contents, deletes the previous file, and points `README.md` at the new name. Commit `assets/` and `README.md` together. Each version gets a new URL, so it shows up right away instead of waiting out GitHub's 5-minute image cache.

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

It follows FL Studio's playback, with one deliberate change. Everything runs on a single shared clock, so every moving part changes on the same tick. It's set to 16th notes: 48 ticks per loop, about every 0.107s at 140 BPM. Change `STEPS_PER_TICK` to 2 for 8ths or 4 for quarter notes. FL itself animates smoothly.

- Step rows have no playhead.
- Piano-roll rows show a thin pink line with a soft trail. It jumps one tick at a time.
- Each channel's selector strip fills grey while the channel sounds, then drops off over the next few ticks.
- The M:S:CS clock steps with the clock and restarts with the pattern, as FL does in pattern mode.
- The scope and level meter change frame on each tick. The meter shows how much of the rack is playing.

The clock, scope and meter are drawn as "film strips": one frame per tick, slid up by a shared `.strip` animation with `steps(TICKS)`.

## Fonts

All three are SIL Open Font License 1.1. Each license is next to its font in `fonts/`.

- PT Sans Narrow: UI text. FL Studio bundles the same font.
- Roboto Condensed: the clock, tempo and pattern selector, at weight 300.
- Silkscreen: tiny pixel labels. It stands in for FL's proprietary microfont.

The generator subsets each font to the characters in use and renames the subset to its CSS alias, so no Reserved Font Name ships with a modified font.

## Last listened line

`last_listened.py` writes the latest last.fm track into `README.md`, between the `last-listened` comment markers. It uses the same source as the widget on rohan-is.me (`user.getrecenttracks` for `imaduck2025`). `.github/workflows/last-listened.yml` runs it every 15 minutes and commits only when the line changes. GitHub may start scheduled runs late.

It needs a repository secret named `LASTFM_API_KEY`. Without the secret, runs skip and the line stays as it is:

```sh
gh secret set LASTFM_API_KEY --repo rohankumarrrr/rohankumarrrr
```

To run it by hand: `LASTFM_API_KEY=… python3 scripts/last_listened.py`. Keep the two markers on their own lines. A line that starts with an HTML comment renders as raw HTML, which breaks the track link.
