# کتابخانه‌ی ویدئویی روان‌شناسی رابطه

Persian motion-graphics explainers for five relationship books, one self-playing page per chapter.

## Open it

Double-click `index.html` (works offline; fonts load from Google Fonts when online, otherwise the system font is used).

## Layout

- `index.html` — library home (generated)
- `books/<book>/chNN.html` — one chapter per file
- `assets/player.css`, `assets/player.js` — shared player (timeline, menu, controls, layout self-check)
- `AUTHORING.md` — rules for writing a chapter
- `tools/validate.py` — static checks · `tools/check.py` — layout check in headless Chrome · `tools/build_index.py` — rebuilds `index.html`
- `_source/` — extracted book text (not for sharing; ignored by git)

## Player keys

Space = pause/play · ← next scene · → previous scene · click the picture to pause · `#s5` at the end of a chapter URL opens scene 5.
