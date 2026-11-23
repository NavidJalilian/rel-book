"""Builds index.html (the library home) from the chapter files. Usage: python3 -I tools/build_index.py"""
import re, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS = [
 ('finkel', 'ازدواج همه یا هیچ', 'الی جی. فینکل', 'The All-or-Nothing Marriage', 'Eli J. Finkel · 2017', 'var(--e1)',
  'چرا ازدواج امروز هم سخت‌تر شده و هم ارزشمندتر، و چه می‌توان کرد.',
  ['Preface: Panic in Evanston','Temperamental but Thrilling','The Pragmatic Marriage','From Pragmatism to Love','From Love to Self-Expression','Personal Fulfillment and Marital Commitment: The Détente','Marriage at the Summit','For Richer or Poorer','For Better or Worse','Lovehacking','Going All In','Recalibrating','The Marital Buffet'], 0),
 ('gottman', 'هفت اصل برای موفقیت ازدواج', 'جان گاتمن و نان سیلور', 'The Seven Principles for Making Marriage Work', 'John Gottman & Nan Silver · 2015', 'var(--e2)',
  'یافته‌های آزمایشگاه عشق: چه چیزی طلاق را پیش‌بینی می‌کند و هفت اصلِ ازدواج پایدار.',
  ['Introduction','Inside the Seattle Love Lab: The Truth About Happy Marriages','What Does Make Marriage Work?','How I Predict Divorce','Principle 1: Enhance Your Love Maps','Principle 2: Nurture Your Fondness and Admiration','Principle 3: Turn Toward Each Other Instead of Away','Principle 4: Let Your Partner Influence You','The Two Kinds of Marital Conflict','Principle 5: Solve Your Solvable Problems','Coping with Typical Solvable Problems','Principle 6: Overcome Gridlock','Principle 7: Create Shared Meaning','Afterword: What Now?'], 0),
 ('johnson', 'محکم بغلم کن', 'سو جانسون', 'Hold Me Tight', 'Dr. Sue Johnson · 2008', 'var(--e3)',
  'عشق به‌عنوان پیوند دلبستگی، و هفت گفتگو برای ساختن پیوندی امن.',
  ['Introduction','Love — A Revolutionary New View','Where Did Our Love Go? Losing Connection','Emotional Responsiveness — The Key to a Lifetime of Love','Conversation 1: Recognizing the Demon Dialogues','Conversation 2: Finding the Raw Spots','Conversation 3: Revisiting a Rocky Moment','Conversation 4: Hold Me Tight — Engaging and Connecting','Conversation 5: Forgiving Injuries','Conversation 6: Bonding Through Sex and Touch','Conversation 7: Keeping Your Love Alive','Healing Traumatic Wounds — The Power of Love','Ultimate Connection — Love as the Final Frontier'], 0),
 ('attached', 'دلبسته', 'امیر لوین و ریچل هلر', 'Attached', 'Amir Levine & Rachel Heller · 2010', 'var(--good)',
  'سه سبک دلبستگی (ایمن، اضطرابی، اجتنابی) و اینکه در رابطه چه می‌کنند.',
  ['Decoding Relationship Behavior','Dependency Is Not a Bad Word','Step One: What Is My Attachment Style?','Step Two: Cracking the Code — What Is My Partner’s Style?','Living with a Sixth Sense for Danger: The Anxious Attachment Style','Keeping Love at Arm’s Length: The Avoidant Attachment Style','Getting Comfortably Close: The Secure Attachment Style','The Anxious-Avoidant Trap','Escaping the Anxious-Avoidant Trap','When Abnormal Becomes the Norm: An Attachment Guide to Breaking Up','Effective Communication: Getting the Message Across','Working Things Out: Five Secure Principles for Dealing with Conflict','Epilogue'], 1),
 ('markman', 'جنگیدن برای ازدواج', 'مارکمن، استنلی و بلومبرگ', 'Fighting for Your Marriage', 'Markman, Stanley & Blumberg · 2010', '#b98fd0',
  'برنامه‌ی PREP: الگوهای مخرب، گفتگوی امن، حل مسئله، دوستی، بخشش و تعهد.',
  ['Introduction','Five Keys for a Great Relationship: PREP in a Nutshell','Destructive Patterns: Signs of Danger Ahead','Changing Roles, Changing Rules: Men and Women in Conflict','When What You Heard Isn’t What I Said: Understanding Filters in Communication','Talking Safely Without Fighting: The Speaker Listener Technique','Controlling the Home Fires: Handling Issues and Events Well','New Perspectives on Problems and Problem Solving','Keeping Conflict Under Control: Ground Rules for a Great Relationship','Safe Harbor: Preserving and Protecting Friendship','Being There: Supporting One Another in Life','Playing Together: How to Succeed in Fun Without Really Trying','Sense and Sensuality: Enhancing and Protecting Your Sex Life','Sacred Places: Core Beliefs and Spiritual Intimacy','Why You Can’t Always Get What You Want: Unraveling the Mysteries of Expectations','Forgiveness: Restoring Hope','Sticking, Stuck, or Stopped: On the Path to Commitment','Moving Forward'], 0),
]
fa = lambda s: re.sub(r'\d', lambda m: '۰۱۲۳۴۵۶۷۸۹'[int(m.group())], str(s))
esc = html.escape
def chapter_info(p):
    s = p.read_text(encoding='utf-8')
    meta = json.loads(re.search(r'<script type="application/json" id="meta">(.*?)</script>', s, re.S).group(1))
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else meta['chapter']
    secs = sum(float(x) for x in re.findall(r'<section class="scene[^"]*"[^>]*data-t="([\d.]+)"', s))
    n = len(re.findall(r'<section class="scene', s))
    return meta['chapter'], title, n, secs

books_html, total_ch, total_min, done_ch = [], 0, 0, 0
for bid, fa_t, fa_a, en_t, en_a, col, blurb, chapters, first in BOOKS:
    rows = []
    bmin = 0; bdone = 0
    for i, en in enumerate(chapters):
        num = i + first
        f = ROOT / 'books' / bid / f'ch{num:02d}.html'
        total_ch += 1
        if f.exists():
            label, title, n, secs = chapter_info(f)
            bmin += secs / 60; bdone += 1
            rows.append(f'<li><a href="books/{bid}/ch{num:02d}.html"><span class="no">{esc(label)}</span><span class="t"><b>{esc(title)}</b><span class="en">{esc(en)}</span></span><span class="m">{fa(round(secs/60))} دقیقه</span></a></li>')
        else:
            rows.append(f'<li class="todo"><span class="no">فصل {fa(num)}</span><span class="t"><b>در حال ساخت</b><span class="en">{esc(en)}</span></span><span class="m"></span></li>')
    total_min += bmin; done_ch += bdone
    books_html.append(f'''<section class="book" id="{bid}" style="--c:{col}">
  <header><div class="spine"></div><div><h2>{esc(fa_t)}</h2><p class="by">{esc(fa_a)} · <span class="en">{esc(en_t)} — {esc(en_a)}</span></p><p class="blurb">{esc(blurb)}</p>
  <p class="stat">{fa(bdone)} از {fa(len(chapters))} بخش · حدود {fa(round(bmin))} دقیقه</p></div></header>
  <ol class="chs">{''.join(rows)}</ol>
</section>''')

page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>کتابخانه‌ی ویدئویی روان‌شناسی رابطه</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lalezar&family=Vazirmatn:wght@400;500;700;800&display=swap">
<style>
/* Layout: one column of books, each a coloured spine + chapter list; same palette as the player */
:root{{--ground:#16121c;--ground2:#1f1827;--panel:#2a2133;--line:#3e334a;--ink:#f3ece4;--muted:#a99db2;--e1:#dba65e;--e2:#e3688c;--e3:#6fc0d6;--good:#86d3a0;
--display:"Lalezar","Vazirmatn",Tahoma,sans-serif;--body:"Vazirmatn",Tahoma,system-ui,sans-serif;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font:400 16px/1.7 var(--body)}}
.wrap{{max-width:980px;margin:0 auto;padding-block:48px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:40px}}
.hero h1{{font:400 clamp(38px,7vw,64px)/1.15 var(--display);margin:0;text-wrap:balance}}
.hero p{{margin:8px 0 0;color:var(--muted);max-width:40em}}
.hero .tot{{color:var(--ink);font-weight:700}}
.en{{direction:ltr;unicode-bidi:isolate}}
.book{{display:flex;flex-direction:column;gap:14px}}
.book header{{display:flex;gap:18px;align-items:stretch}}
.spine{{width:10px;border-radius:6px;background:var(--c);flex:none}}
.book h2{{font:400 34px/1.25 var(--display);margin:0;color:var(--c)}}
.by{{margin:2px 0;color:var(--muted);font-size:15px}}
.blurb{{margin:2px 0}}
.stat{{margin:2px 0;font-size:14px;color:var(--muted)}}
.chs{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}}
.chs a,.chs .todo{{display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:14px;align-items:center;padding:10px 14px;border-radius:12px;background:var(--ground2);color:inherit;text-decoration:none;border:1px solid transparent}}
.chs a:hover,.chs a:focus-visible{{border-color:var(--c);outline:none;background:var(--panel)}}
.chs .todo{{opacity:.5}}
.no{{font-size:14px;color:var(--c);font-weight:700}}
.t{{display:flex;flex-direction:column;min-width:0}}
.t b{{font-weight:700;font-size:17px;line-height:1.5}}
.t .en{{font-size:12.5px;color:var(--muted);text-align:right;overflow-wrap:anywhere}}
.m{{font-size:13px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}}
@media (max-width:560px){{.chs a,.chs .todo{{grid-template-columns:minmax(0,1fr) auto}}.no{{grid-column:1/-1}}}}
.foot{{color:var(--muted);font-size:13px}}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>کتابخانه‌ی ویدئویی روان‌شناسی رابطه</h1>
    <p>خلاصه‌ی متحرک و فارسیِ پنج کتاب درسی، فصل به فصل و بخش به بخش. هر فصل خودش پخش می‌شود؛ با فاصله مکث کنید و با فلش‌ها جلو و عقب بروید.</p>
    <p class="tot">{fa(done_ch)} از {fa(total_ch)} فصل آماده · حدود {fa(int(total_min//60))} ساعت و {fa(round(total_min%60))} دقیقه ویدئو</p>
  </header>
  {''.join(books_html)}
  <p class="foot">این خلاصه‌ها برگردان و برداشتِ آزاد برای مطالعه‌اند و جای خودِ کتاب‌ها را نمی‌گیرند.</p>
</div>
</body>
</html>
'''
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print(f'index.html: {done_ch}/{total_ch} chapters, {total_min/60:.1f} h')
