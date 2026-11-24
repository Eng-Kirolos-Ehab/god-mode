---
name: saudi-news-curator
description: >
  Use this skill whenever the user asks for Saudi Arabian news, trending topics in Saudi Arabia,
  or wants to generate a news article about Saudi business, economy, tourism, tech, sports,
  entertainment, or lifestyle. Triggers on phrases like: "هات تريند السعودية", "اخبار السعودية",
  "Saudi news", "trending in Saudi", "اعمل خبر SEO", "generate saudi news article",
  "اخبار بيزنس السعودية", "سياحة السعودية", "ايه الجديد في السعودية".
  This skill handles the full workflow: live trend discovery → article selection → bilingual
  article generation (Arabic + English) → SEO metadata → social media hashtags.
  Use it even if the user just says "هات اخبار" or "what's trending in KSA".
  NEVER generate political content — business, economy, lifestyle, tourism, tech, sports only.
---

# Saudi Smart News Curator & SEO Optimizer

A full content engine for discovering, writing, and optimizing Saudi news articles — bilingual (Arabic + English), SEO-ready, and humanized.

---

## Workflow Overview

```
Step 1: Discover  → Search live trends (web_search)
Step 2: Present   → Show headline list only (no content yet)
Step 3: Verify    → Multi-source fact check before writing anything
Step 4: Generate  → User picks a headline → Full bilingual article (verified facts only)
Step 5: SEO       → Arabic + English metadata
Step 6: Hashtags  → Ready-to-publish social tags
```

---

## Step 1 — Trend Discovery + Duplicate Check

Use `web_search` with these queries (run 2–3 in parallel):
- `"السعودية" site:argaam.com OR site:zawya.com OR site:aleqt.com` (past 24h)
- `Saudi Arabia business news today`
- `Saudi Arabia tourism tech startups trending`

**If the user publishes a news site, run a duplicate check on it before finalizing headlines (skip this step if they have none):**
Use `web_fetch` on these two URLs to scan recently published articles:
- `<YOUR_SITE_URL>` (Arabic edition; ask the user for it once)
- `<YOUR_SITE_URL>/en` (English edition, if any)

Cross-reference every candidate headline against what's already published on the site.
- If a story is already covered on either version → **skip it entirely**, do not include in the list
- Only include stories that are **not yet published** on the user's site

**Allowed categories only:**
- 🏢 Business / Economy / Finance / Startups / Businessmen
- ✈️ Tourism / Travel & Entertainment
- 💻 Tech / AI / Innovation
- ⚽ Sports
- 🎭 Lifestyle / Events / Conferences
- 👩 Saudi Women achievements

**Hard block — skip any result touching:**
- ❌ Politics, government policy, royal family statements, elections, military, diplomacy

---

## Step 2 — Present Headlines with Date & Category

After searching, extract the **publication date** and **source name** from every search result metadata before building the list. This is mandatory — do not skip.

Present the list formatted **exactly** like this — each piece of info on its own line, with a blank line between items:

```
🔥 تريندات السعودية الآن:

―――――――――――――――――――――
1️⃣
🏷 [الكاتيجوري]
🗓 [التاريخ / منذ كم]
📰 [العنوان العربي]
📰 [English Headline]
―――――――――――――――――――――
2️⃣
🏷 [الكاتيجوري]
🗓 [التاريخ / منذ كم]
📰 [العنوان العربي]
📰 [English Headline]
―――――――――――――――――――――
3️⃣
🏷 [الكاتيجوري]
🗓 [التاريخ / منذ كم]
📰 [العنوان العربي]
📰 [English Headline]
―――――――――――――――――――――

✍️ اختار رقم عشان نعمل المقال الكامل
```

**IMPORTANT — formatting rules:**
- Every field on its own separate line — no combining on one line ever
- Arabic headline and English headline each on their own line, both starting with 📰
- Do NOT write "AR:" or "EN:" labels
- Do NOT use any dash or separator (—, -, –) inside the headlines themselves
- The ――― divider line goes before each item and after the last one

**Date extraction rules — read the search result metadata carefully:**
- Search results include an `age` or publication timestamp — always use it
- نفس اليوم → "اليوم، منذ X ساعات" (e.g. "اليوم، منذ 3 ساعات")
- أمس → "أمس"
- تاريخ محدد → اكتبه كامل (مثال: "28 أبريل 2026")
- مش واضح من المصدر → "تاريخ غير محدد"

**Category extraction rule:** assign from the Category table in Step 5 based on the article topic — always display in Arabic.

**Sorting rule:** sort the list newest → oldest automatically.

Wait for user selection before generating any article content.

---

## Step 3 — Fact Verification (MANDATORY before writing)

This step runs **before** any article is written. Never skip it.

### 3a — Cross-Source Verification
Run **at least 2 additional web searches** specifically about the selected story:
- Search 1: The story's main claim or statistic (e.g. `"123 million tourists Saudi Arabia 2025" source`)
- Search 2: The original source / organization behind the data (e.g. `WTTC Saudi Arabia 2025 report`)

Require **minimum 2 independent sources** that confirm the same facts before using them.

### 3b — Fact Classification
For every data point or claim found, classify it as one of:

| Label | Meaning | Action |
|-------|---------|--------|
| ✅ VERIFIED | Confirmed by 2+ independent sources | Use freely |
| ⚠️ SINGLE SOURCE | Only one source found | Use with attribution only: "وفقاً لـ..." / "According to..." |
| ❌ UNVERIFIED | No reliable source found | DROP — never include |
| 🚫 INFERRED | Logical conclusion not stated in any source | DROP — never include |

### 3c — What to Never Include
- ❌ Numbers or percentages not found in a named source
- ❌ Quotes not attributed to a real, named person
- ❌ Future predictions presented as facts ("ستصل إلى..." unless from official forecast)
- ❌ Cause-and-effect relationships not explicitly stated in sources
- ❌ Comparisons or rankings not directly reported
- ❌ Any detail filled in from general knowledge or training data

### 3d — Source Transparency
Keep an internal source log while writing:
```
Fact: [claim]  →  Source: [publication name + URL]  →  Status: ✅/⚠️/❌
```
Only ✅ and ⚠️ facts make it into the article.

---

## Step 4 — Full Article Generation

After user selects a headline and verification is complete, generate both versions:

### Arabic Article Rules
- Tone: صحفي، إنساني، طبيعي — NOT robotic or AI-sounding
- Structure: hook لافت → سياق السوق → تفاصيل (أرقام/تصريحات) → ختام قوي
- Length: 250–400 words
- Style variety: جمل قصيرة + طويلة، تنوع في البداية، تجنب التكرار
- Include: local Saudi context, realistic figures, market references
- Avoid: over-optimization, repetitive phrasing, bullet lists in body

### English Article Rules
- Tone: Journalistic, natural, 100% humanized
- Structure: Strong lede → context → details (stats/quotes) → closing
- Length: 220–380 words
- Style: Varied sentence length, active voice, no AI tells
- Include: Saudi market context, relevant numbers, grounded details

---

## Step 5 — Category Assignment

Auto-assign the best-fit category:

| Arabic | English |
|--------|---------|
| اقتصاد / مال وأعمال / رجال أعمال | Business / Business & Finance / Businessmen |
| سياحة / سياحة وسفر | Tourism / Travel & Tourism |
| مجتمع وأعمال | Startups |
| تقنية / علوم وتكنولوجيا | Tech / Technology / AI Automation |
| الرياضة | Sports |
| المرأة السعودية | Saudi Women |
| فعاليات / مؤتمرات وندوات | Entertainment / Art & Celebrities |
| ترند / لايف ستايل | World (economic/cultural only) |

---

## Step 6 — SEO Output (Yoast-Ready)

Generate for both languages. Each field MUST appear on its own separate line — never combine fields on the same line.

### 🇸🇦 SEO عربي

Focus Keyphrase:
[2–4 كلمات رئيسية]

SEO Title:
[العنوان + الكلمة المفتاحية] — max 60 chars

Slug:
[كلمات-مفصولة-بشرطة]

Meta Description:
[140–160 حرف — hook + keyword + CTA]

---

### 🇬🇧 SEO English

Focus Keyphrase:
[2–4 target keywords]

SEO Title:
[Keyword-rich title] — max 60 chars

Slug:
[short-clean-hyphenated-slug]

Meta Description:
[140–160 chars — hook + keyword + CTR-optimized]

---

**SEO rules:**
- Every field label is on one line, its value is on the next line — never on the same line
- Title: front-load the keyword, max 60 chars
- Slug: 3–5 words, no stopwords, hyphens only
- Meta: keyword in first 20 chars, ends with soft CTA

---

## Step 7 — Hashtags

Add 8–12 hashtags per language after the article:

**Arabic format:**
`#السعودية #ريادة_الأعمال #اقتصاد_السعودية #[topic-specific] ...`

**English format:**
`#SaudiArabia #KSA #Vision2030 #[topic-specific] ...`

Always include: `#السعودية` and `#SaudiArabia` as anchors.

---

## Full Output Template

```
📰 المقال العربي
[Category Tag]
[Title]

[Article body — 250–400 words]

🏷 هاشتاقات:
#السعودية #...

---

🌍 English Article
[Category Tag]
[Title]

[Article body — 220–380 words]

🏷 Hashtags:
#SaudiArabia #...

---

🔍 SEO (عربي)

Focus Keyphrase:
[القيمة]

SEO Title:
[القيمة]

Slug:
[القيمة]

Meta Description:
[القيمة]

---

🔍 SEO (English)

Focus Keyphrase:
[value]

SEO Title:
[value]

Slug:
[value]

Meta Description:
[value]

🖼 Image Keywords
[كلمات بحث مقترحة للصورة — مثلاً: اسم الشركة، اسم الفعالية، اسم الشخصية، أو الموقع الجغرافي]
[Suggested image search keywords — e.g. company name, event name, person name, or location]
```

**Image Keywords rules:**
- لو الخبر عن شركة → اسم الشركة بالعربي والإنجليزي
- لو الخبر عن فعالية أو مؤتمر → اسمه الرسمي
- لو الخبر عن شخصية → اسمها الكامل
- لو الخبر عن مكان أو مشروع → اسمه (مثال: NEOM، AlUla، Red Sea Global)
- لو عام → كلمات وصفية دقيقة (مثال: "Saudi economy growth Riyadh 2026")
- أعطِ 3–5 كلمات أو عبارات بحث كحد أقصى

---

## Hard Rules (Non-Negotiable)

- ❌ Zero political content — any topic touching government, royal family, elections, military = skip
- ❌ No speculative or unverified claims — if you can't source it, cut it
- ❌ No inferred cause-and-effect not stated in sources
- ❌ No numbers, stats, or quotes from training data — live search only
- ❌ No robotic/AI-detectable writing patterns
- ❌ Never include a story already published on the user's site (Arabic or English)
- ✅ Every fact must trace back to a named, verifiable source
- ✅ Single-source facts must be attributed explicitly in the article text
- ✅ Always verify with 2+ searches before writing
- ✅ Always search before writing — no hallucinated news
- ✅ Always fetch the user's site both versions before finalizing headline list
- ✅ Wait for user selection before generating full article
- ✅ When in doubt about a fact → leave it out
