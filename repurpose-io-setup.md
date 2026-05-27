# Repurpose.io Client Setup Guide

Repurpose.io is the engine for Branches 1 (Video) and 3 (Audio) of the content tree — 22 of the 33 pieces. It handles automated publishing from one source to all destinations: no API calls, no code, pure dashboard config.

**Client cost:** $35/mo Starter (3 accounts/network) or $79/mo Pro (10 accounts/network). Bill the client directly or mark up inside the monthly retainer.

**Supported sources:** YouTube, TikTok, Instagram Reels, Facebook, Podcast RSS, Google Drive (folder watch)
**Supported destinations:** YouTube Shorts, Facebook Page, Facebook Group, Facebook Reels, LinkedIn, Instagram Reels, Instagram Stories, Instagram Feed, Pinterest Idea Pins, Twitter/X, TikTok, Google Drive, Dropbox, Podcast (Spotify/Apple via RSS), Amazon Alexa

---

## Step 1: Create the Client's Repurpose.io Account

1. Go to repurpose.io → Sign up
2. Pick a plan:
   - **Starter ($35/mo)** — 3 accounts per social network. Good for solo creators.
   - **Pro ($79/mo)** — 10 accounts per network. Use when client has multiple brand accounts (e.g., personal IG + business IG, plus alts).
   - **Agency ($179/mo)** — 25 accounts per network. Reserve for genuine multi-client setups managed inside one Repurpose.io login.
3. Set timezone to client's local timezone

(Note: the legacy "Marketer $49" plan referenced in older Repurpose.io docs no longer exists. Today's tiers are Starter / Pro / Agency.)

---

## Step 2: Choose the Source Pattern

See `setup-sop.md` Phase 2 for the full Pattern A vs. Pattern B comparison.

- **Pattern A (YouTube long-form):** Client uploads to YouTube; Repurpose.io watches the channel and fans out.
- **Pattern B (Google Drive → IG Reels):** Two-stage flow — Drive folder triggers IG Reel, which then triggers downstream platforms.

The rest of this guide assumes Pattern A. For Pattern B, see the dedicated section near the bottom.

---

## Step 3: Connect the Source Platform

**If source = YouTube (Pattern A):**
1. Dashboard → **Create Workflow**
2. Source: YouTube → Connect Account
3. Select: "New video published" OR "New Short published" as the trigger

**If source = Google Drive (Pattern B Stage 1):**
1. Dashboard → **Create Workflow**
2. Source: Google Drive → Connect Account → pick a watch folder
3. Repurpose.io polls the folder for new video files

**If source = Instagram Reels (Pattern B Stage 2):**
1. Source: Instagram → Connect Account (Business Manager required)
2. Trigger: "New Reel posted"

**If source = Podcast RSS:**
1. Source: Podcast → paste RSS feed URL
2. Repurpose.io reads new episodes automatically

---

## Step 4: Connect Destination Platforms

For each destination, go to **Connections** → **+ Add New Connection**:

**Facebook Page + Group:**
- Connect via Facebook login → select Page
- For Groups: admin must connect the Group separately

**LinkedIn:**
- Connect via LinkedIn OAuth → select Personal Profile or Company Page

**Instagram:**
- Connect via Facebook Business Manager (IG must be a Business account)
- Three separate destinations: Reels, Stories, Feed

**YouTube Shorts:**
- Connect Google account → select YouTube channel

**Pinterest:**
- Connect Pinterest account → select Board for Idea Pins

**Twitter / X:**
- Connect via OAuth

**TikTok:**
- Connect TikTok account via TikTok for Business OAuth

**Google Drive / Dropbox backup:**
- Connect Google account → select destination folder
- Creates automatic backup of every piece of content

---

## Step 5: Build the Workflow Rules

Each workflow = one source → one destination. Build one per destination.

**Recommended workflow set for Pattern A (YouTube source):**

| Workflow Name | Source | Destination | Notes |
|---------------|--------|-------------|-------|
| YouTube → FB Page (Full) | YouTube | Facebook Page | Full video |
| YouTube → FB Group | YouTube | Facebook Group | Full video |
| YouTube → Drive backup | YouTube | Google Drive | Archive folder |
| YouTube → IG Reels | YouTube | Instagram Reels | Auto-clipped 60s |
| YouTube → IG Stories | YouTube | Instagram Stories | Auto-cropped |
| YouTube → IG Feed | YouTube | Instagram Feed | Square crop |
| YouTube → TikTok | YouTube | TikTok | Vertical clip |
| YouTube → Twitter | YouTube | Twitter / X | Vertical clip |
| YouTube → LinkedIn | YouTube | LinkedIn | Add professional caption |
| YouTube → YouTube Shorts | YouTube | YouTube Shorts | Vertical clip |
| YouTube → Pinterest | YouTube | Pinterest Idea Pins | |
| YouTube → Podcast | YouTube | Spotify+Apple (via RSS) | Audio-only |
| YouTube → Alexa | YouTube | Amazon Alexa | Audio clip |
| YouTube → Audiograms (×8) | YouTube | IG/FB/LinkedIn/Twitter/YT/Pinterest | One per destination |

**Workflow settings (each one):**
- **Caption:** Use original (pulls from YouTube title/description) OR set a custom template
- **Custom caption template example:** `{{original_caption}} #[NICHE_HASHTAG] #[BRAND_HASHTAG]`
- **Schedule:** Publish immediately OR delay by X hours (staggers content across the day)
- **Hashtags:** Add 3–5 platform-specific hashtags at workflow level

---

## Step 6: Caption Customization per Platform

Repurpose.io's caption field supports variables:
- `{{original_caption}}` — pulls the original YouTube/IG caption
- `{{title}}` — video title (YouTube)

**Recommended caption templates:**

**Facebook:** `{{original_caption}} 👇 Drop a comment below! #[NICHE] #[BUSINESS]`

**LinkedIn:** `{{original_caption}} [2-sentence professional context about why this matters for their industry]`

**Twitter / X:** Short version of caption (280 char limit) — strip hashtags, add 1–2 relevant ones

**Instagram:** `{{original_caption}} . . . #[HASHTAG_BLOCK_20_30_TAGS]`

---

## Step 7: Test Each Workflow

1. Post a test video on the source platform
2. In Repurpose.io → **Workflows** → verify each workflow shows a "Published Successfully" entry within 5–10 minutes
3. Check each destination platform — confirm the video posted correctly
4. Spot-check captions, hashtags, and format on each platform

---

## Step 8: The Branch 2 Text Layer

Repurpose.io handles Branches 1 (Video) and 3 (Audio) — 22 of the 33 pieces. The remaining 10 pieces (blog post, summarized text posts, quote graphics) require a separate **Python + Modal** layer that:

1. Pulls the transcript from the source video
2. Calls Claude or OpenAI to generate platform-specific text and quote-graphic copy
3. Renders graphics via Canva API or Bannerbear
4. Posts to WordPress / IG / FB / LinkedIn / Twitter / Pinterest via platform APIs (or queues for client approval)

The text layer is built per-client because the brand-voice prompts and credentials are specific. See `text-layer/README.md` for the architecture, and `setup-sop.md` Phase 4 for the deployment SOP.

---

## Pattern B: Two-Stage Workflow Variant

For clients without a YouTube long-form habit, the testing-account approach is a two-stage Google Drive → Instagram Reels → downstream flow.

**Stage 1 — From Google Drive (3–4 workflows):**
- Google Drive Video → Instagram Reels
- Google Drive Video → Facebook Reels
- Google Drive Video → TikTok
- Google Drive Video → Twitter

**Stage 2 — From the Instagram Reel (5+ workflows):**
- Instagram Reels → YouTube Shorts
- Instagram Reels → Pinterest
- Instagram Reels → Twitter
- Instagram Reels → LinkedIn Personal Feed
- Instagram Reels → TikTok

Stage 1 seeds IG; Stage 2 multiplies it across every other platform. Use this when your client's content originates as short-form video files rather than long-form YouTube uploads.
