# How to write a chapter explainer

Each chapter of each book becomes one self-playing, Persian (RTL) motion-graphics page: `books/<book>/chNN.html`.
The reference chapter is **`books/finkel/ch01.html`**. Read it fully before writing anything; copy its structure, scene types and tone.
The shared engine is `assets/player.css` + `assets/player.js` — **never edit them**. Put chapter-specific CSS/keyframes in a `<style>` inside the chapter file.

Audience: Iranian university students studying these books as course material. They need to understand every section and remember the key terms for exams.

## 1. File skeleton

```html
<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{Persian book title}، فصل {N in Persian digits}</title>       <!-- intro: «…، مقدمه» -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lalezar&family=Vazirmatn:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="../../assets/player.css">
</head>
<body>
<script type="application/json" id="meta">
{"book":"…","author":"…","chapter":"فصل ۲","home":"../../index.html#<book>","prev":"ch01.html","next":"ch03.html",
 "sections":[["فارسی","Original English heading"], …, ["جمع‌بندی","Recap"]]}
</script>
<div class="stage" id="stage">
  <section class="scene s-title" data-t="9" data-sec="0" data-title="عنوان فصل"> … </section>
  …
</div>
<script src="../../assets/player.js"></script>
</body>
</html>
```

- `prev`/`next`: neighbouring files of the same book (`null` at the ends). The chapter list per book is in section 7.
- `chapter`: «فصل ۲», or «مقدمه» / «پیش‌گفتار» / «پس‌گفتار» / «سخن پایانی» for front/back matter.
- `sections`: one entry per heading of the chapter **in book order**, plus a first «آغاز فصل / Chapter opening» entry when the chapter opens with text before its first heading, and a last «جمع‌بندی / Recap». Keep the original English heading exactly as printed (it lets students match the book).
- The player builds the top bar, menu, timeline, controls and the end-of-chapter buttons. Don't add any of that.

## 2. Coverage

- **Every heading (section and sub-section) of the chapter gets at least one scene.** Long or dense sections get 2–3 scenes. Typical chapter: 15–26 scenes, 7–11 minutes.
- Scene 1 is the title card (`s-title`, copy ch01's: chapter pill, big title, one-line question, English title line; a background SVG motif drawn with the engine).
- Last scene is the recap: `.grid` of 6–8 `.term` cards (term + one-line definition) and an `.endbar` holding only `<span class="note">منبع: Author, <span class="en">Book Title</span>، فصل N. خلاصه و برگردانِ آزاد برای مطالعه.</span>`. The player appends replay/next buttons.
- Teach the **ideas**: models, lists, steps, research findings with their numbers, examples/case couples, exercises (summarise what the exercise asks the reader to do), and the author's argument. A student who watches only this should be able to answer exam questions on the chapter.
- When the book gives a numbered list (e.g. "four horsemen", "five keys", "seven conversations"), show **all** items.
- Long quizzes/questionnaires in the book: summarise their purpose and scoring idea plus 2–3 sample items; don't reproduce them whole.

## 3. Writing (Persian)

- Clear, natural academic Persian; short sentences; explain like a good teaching assistant. No machine-translation calques.
- Use ZWNJ (U+200C, «‌») correctly: می‌شود، نمی‌خواهد، ازدواج‌ها، سخت‌تر، بزرگ‌ترین، خانه‌ی، رابطه‌ای، شده‌اند.
- Persian letters ی and ک (never Arabic ي ك). Persian digits everywhere in Persian text (۱۹۶۵، ۳٫۵، ٪۴۰، ۱٬۲۳۱). Latin text and digits only inside `<span class="en">`.
- First time a key term appears in a chapter, give the English original: `اثر میکل‌آنژ <span class="en">(Michelangelo effect)</span>`. Keep terms consistent with the glossary in section 6.
- People's names in Persian transliteration (جان گاتمن، سو جانسون). Case-study couples keep their names transliterated.
- **Copyright**: summarise and explain in your own words. Never reproduce passages. At most 2 short quotes per chapter, each under 15 words, in «» with attribution.
- **Honesty**: numbers must come from the chapter text. If you draw a chart whose exact values the text doesn't give, label it `نمودار مفهومی است، نه داده‌ی واقعی` (or «شکل کلی روند»). Never invent statistics, studies or quotes.

## 4. Scene layouts (all from ch01)

Stage is a fixed 1280×720 canvas (landscape) or 720×1280 (portrait, phones); the same markup must work in both. Font sizes are in stage pixels.

| Layout | Markup | Use for |
|---|---|---|
| Text + visual | `<header>` (eyebrow + h2) then `.cols` > `.txt` (2–3 `<p>`) + `.vis` (an SVG or HTML diagram) | most scenes |
| Era/stage cards | `.eras` with `.era` cards and `.tr` arrows, then `.cap` | 3–4 stages or types side by side |
| Chain / timeline | `.chain` of `.node` (+ final `.node.res`) inside `.vis` | causes → effect, dated events |
| Numbered steps | `.steps` of `.step` (`<b>` + `<small>`) inside `.vis` | a real procedure or ordered list |
| Two cards | `.duo` of `article.card` (`.tag`, `h3`, small SVG, `<p>`) | contrasts: good vs bad, two types |
| Dialogue | `.talk` of `.say.r` / `.say.l` (add `.bad` or `.ok`), `<b>` = speaker | example conversations (paraphrased) |
| Equation | `.eq` of `.chip` + `.op` + `.result` | "A + B = C" syntheses |
| Quote | `.quote` with `<small>` attribution | one short key quote |
| Recap | `.grid` of `.term` + `.endbar` | last scene |

Eyebrow: `<div class="eyebrow a">{Persian section name} <span class="en">{English heading}</span></div>`.
Key sentence: `<p class="key a" style="--d:…"><mark>…</mark></p>` (gets an animated highlighter). One per scene at most.

**Text budget per scene (hard limits so nothing overflows):**
- `.cols` scenes: h2 ≤ 7 words; `.txt` ≤ 3 paragraphs and ≤ ~60 words total.
- Full-width layouts (`.eras`, `.duo`, `.grid`): each card ≤ ~35 words; `.cap` ≤ 40 words.
- `.chain`/`.steps`: ≤ 5 items, title ≤ 6 words, `<small>` ≤ 12 words.
- `.talk`: ≤ 5 bubbles, each ≤ 18 words.
More content → split into more scenes.

## 5. Motion engine

- Any element with class `a` animates in when its scene starts, after `--d` seconds: `style="--d:2.4"`. Default animation is `up`. Pick another with `--k`: `fade`, `pop`, `draw`, `growY`, `growX`, `pulse`, `twinkle`, `bubble`, `tap`, `shiftL`, `train`. Duration `--du:1.4s`; repeat `--it:infinite` (only for small ambient things like `pulse`).
- Exit/dim: add class `x` with `--x` (seconds) and `--xk` (`dim` → 20% opacity, `gone` → 0, `fly` with `--tx --ty --r`).
- Line drawing: `<path class="a dr" style="--k:draw;--du:1.6s;--d:1" pathLength="1" …>` (`pathLength="1"` is required). Bars growing up: class `a gy` + `--k:growY`. Bars growing from the right: `a gxr` + `--k:growX`.
- **Never put `a`/`x` on an SVG element that has a `transform` attribute** (CSS animation overrides it). Wrap: `<g class="a" style="--k:pop"><g transform="translate(100 90)">…</g></g>`.
- Movement along a route: define keyframes in the chapter `<style>` (like ch01's `climb0`) and use `class="a climb" style="--k:myClimb;--du:6s"`; `climb` uses view-box coordinates.
- Stagger reveals to follow the narration: text paragraph, then the part of the visual it describes, then the next paragraph. Every scene should *move*: draw lines, grow bars, pop icons, highlight.
- Scene length `data-t` (seconds): last `--d` + reading time of what remains. Roughly 1 s per 2.5 Persian words of text on the scene + 4 s. Typically 16–28 s. The validator fails a scene whose last element enters less than 4 s before its end.

### SVG rules
- Typical viewBox `0 0 560 440` (or `0 0 560 400`), `aria-hidden="true"`. Colours only via tokens: `var(--ink)`, `var(--muted)`, `var(--panel)`, `var(--line)`, `var(--e1)` gold, `var(--e2)` rose, `var(--e3)` teal, `var(--good)` green, `var(--stone)`; semi-transparent fills as `rgba(...)` of those hues.
- Text: `text-anchor="middle"` almost always; font-size ≥ 14; leave ≥ 8px between labels; keep every label inside the viewBox (the checker catches overlap and spill).
- Draw meaningful diagrams of the idea (cycles, scales, ladders, maps, networks, bridges, thermometers, Venn diagrams, flows), not decoration. Simple flat geometry; no clip-art, no emoji.
- Data charts: to scale, axis labels in Persian, units stated, source numbers from the text only.

## 6. Glossary (keep these renderings)

**Gottman, Seven Principles** — Love Lab: آزمایشگاه عشق · four horsemen: چهار سوارکار (آخرالزمان) · criticism: انتقاد · contempt: تحقیر · defensiveness: حالت تدافعی · stonewalling: دیوار سکوت · harsh startup: شروع تند · flooding: غرقگیِ هیجانی · repair attempts: تلاش‌های ترمیمی · love maps: نقشه‌های عشق · fondness and admiration: علاقه و تحسین · turn toward / away / against: روی‌آوردن / روی‌گرداندن / روی‌برگرداندن علیه · bids: درخواست‌های ارتباطی · emotional bank account: حساب بانکیِ عاطفی · positive sentiment override: غلبه‌ی احساس مثبت · accept influence: پذیرش نفوذ · solvable / perpetual problems: مسائل حل‌شدنی / دائمی · gridlock: بن‌بست · dreams within conflict: رؤیاهای پنهان در تعارض · softened startup: شروع نرم · compromise: مصالحه · shared meaning: معنای مشترک · rituals of connection: آیین‌های پیوند · emotional intelligence: هوش هیجانی.

**Johnson, Hold Me Tight** — EFT: درمان متمرکز بر هیجان (EFT) · attachment: دلبستگی · A.R.E. (Accessible, Responsive, Engaged): در دسترس بودن، پاسخ‌گویی، درگیری عاطفی · Demon Dialogues: گفتگوهای اهریمنی · Find the Bad Guy: پیدا کردن مقصر · Protest Polka: رقص اعتراض · Freeze and Flee: یخ‌زدن و گریختن · raw spots: نقاط زخمی · rocky moment: لحظه‌ی سنگلاخی · Hold Me Tight conversation: گفتگوی «محکم بغلم کن» · attachment injury: زخم دلبستگی · primal panic: هراس بنیادین · bonding: پیوند · emotional responsiveness: پاسخ‌گوییِ هیجانی · safe haven / secure base: پناهگاه امن / پایگاه امن.

**Levine & Heller, Attached** — attachment style: سبک دلبستگی · secure / anxious / avoidant: ایمن / اضطرابی / اجتنابی · anxious-avoidant trap: تله‌ی اضطرابی–اجتنابی · activating / deactivating strategies: راهبردهای فعال‌ساز / غیرفعال‌ساز · protest behavior: رفتار اعتراضی · dependency paradox: پارادوکس وابستگی · effective communication: ارتباط مؤثر · phantom ex: معشوقِ سابقِ خیالی · attachment system: سیستم دلبستگی · the abundance philosophy: نگرش فراوانی.

**Markman, Stanley & Blumberg, Fighting for Your Marriage** — PREP: برنامه‌ی PREP · escalation: تشدید · invalidation: بی‌اعتبارسازی · negative interpretations: تفسیرهای منفی · withdrawal and avoidance: کناره‌گیری و اجتناب · filters: فیلترها · Speaker Listener Technique: تکنیک گوینده–شنونده · the floor: «نوبت صحبت» (کارتِ زمین) · issues vs events: موضوع‌ها در برابر رویدادها · hidden issues: موضوع‌های پنهان · problem discussion / problem solution: گفتگو درباره‌ی مسئله / حل مسئله · ground rules: قوانین پایه · Time Out / Stop Action: توقف · XYZ statement: جمله‌ی XYZ · friendship, fun, sensuality: دوستی، تفریح، حسّانیت · expectations: انتظارات · forgiveness: بخشش · commitment: تعهد · dedication: تعهدِ شخصی (فداکاری) · constraint: قیدها (تعهدِ اجباری).

**Finkel, The All-or-Nothing Marriage** — see ch01: pragmatic / love-based / self-expressive: عمل‌گرا / عشق‌محور / خودابرازگر · Mount Maslow: کوه مازلو · suffocation: خفگی · Michelangelo effect: اثر میکل‌آنژ · authentic self: خودِ اصیل · lovehacking: عشق‌هک · going all in: همه‌چیز را گذاشتن · recalibrating: تنظیم دوباره · the marital buffet: بوفه‌ی ازدواج.

Add other terms as you need them; stay consistent within a book.

## 7. Books, ids and Persian titles

| id | Persian title | Author (Persian) | Files |
|---|---|---|---|
| finkel | ازدواج همه یا هیچ | الی جی. فینکل | ch00 (پیش‌گفتار), ch01–ch12 |
| gottman | هفت اصل برای موفقیت ازدواج | جان گاتمن و نان سیلور | ch00 (مقدمه), ch01–ch12, ch13 (پس‌گفتار) |
| johnson | محکم بغلم کن | سو جانسون | ch00 (مقدمه), ch01–ch12 |
| attached | دلبسته | امیر لوین و ریچل هلر | ch01–ch12, ch13 (سخن پایانی) |
| markman | جنگیدن برای ازدواج | هاوارد مارکمن، اسکات استنلی و سوزان بلومبرگ | ch00 (مقدمه), ch01–ch17 |

Source text for every chapter: `_source/<book>/chNN.txt` (same numbering). Read the whole chapter before writing; headings are often marked with `#` or appear as short standalone lines. Book-level part titles (e.g. "Part Two: Seven Transforming Conversations") can go on the title card as a small line.

## 8. Before you finish a chapter

Run both and fix everything they report (warnings too, unless clearly a false positive):

```
python3 -I tools/validate.py books/<book>/chNN.html
python3 -I tools/check.py books/<book>/chNN.html
```

`check.py` opens the page in headless Chrome in both orientations with every scene frozen at its end state and reports anything outside the stage, overflowing boxes and overlapping SVG labels.
