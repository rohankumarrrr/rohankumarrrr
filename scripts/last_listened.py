"""Write Rohan's latest last.fm track into README.md, between the last-listened markers.

Same source as the Scrobbler widget on rohan-is.me (user.getrecenttracks). Run by
.github/workflows/last-listened.yml; it only rewrites the README when the line changes,
so the workflow only commits when the track (or now-playing state) changes.

Env: LASTFM_API_KEY (required), LASTFM_USER (default imaduck2025).
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- last-listened:start -->", "<!-- last-listened:end -->"


def md_escape(s):
    """Keep track and artist names from being read as markdown."""
    return re.sub(r"([\\`*_{}\[\]<>()#+!|~])", r"\\\1", s)


def latest_track(user, key):
    query = urllib.parse.urlencode({"method": "user.getrecenttracks", "user": user, "api_key": key,
                                    "format": "json", "limit": 1})
    req = urllib.request.Request(f"https://ws.audioscrobbler.com/2.0/?{query}",
                                 headers={"User-Agent": "rohankumarrrr-profile-readme"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    tracks = data["recenttracks"]["track"]
    if isinstance(tracks, dict):  # a single track comes back as an object, not a list
        tracks = [tracks]
    if not tracks:
        return None
    t = tracks[0]
    return {
        "name": t["name"],
        "artist": t["artist"]["#text"],
        "url": t.get("url", ""),
        "now": t.get("@attr", {}).get("nowplaying") == "true",
    }


def render(track):
    # Lowercase like the site. No "x hours ago": it would go stale between runs.
    lead = "currently listening to" if track["now"] else "last listened to"
    name = md_escape(track["name"].lower())
    title = f"[{name}]({track['url']})" if track["url"] else name
    return f"{lead}: {title} by {md_escape(track['artist'].lower())}"


def main():
    key = os.environ.get("LASTFM_API_KEY")
    if not key:  # skip quietly so a missing secret doesn't fail (and email about) every scheduled run
        print("LASTFM_API_KEY is not set, README unchanged")
        return
    user = os.environ.get("LASTFM_USER", "imaduck2025")
    try:
        track = latest_track(user, key)
    except Exception as exc:  # leave the README alone if last.fm is down
        print(f"last.fm request failed, README unchanged: {exc}")
        return
    if not track:
        print("no recent tracks, README unchanged")
        return

    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        sys.exit("last-listened markers not found in README.md")
    # markers on their own lines: a line that starts with an HTML comment would be rendered as raw HTML
    updated = pattern.sub(lambda _: f"{START}\n{render(track)}\n{END}", text, count=1)
    if updated == text:
        print("unchanged")
        return
    README.write_text(updated, encoding="utf-8")
    print(f"updated: {render(track)}")


if __name__ == "__main__":
    main()
