# Repurpose.io Client Setup Guide

Repurpose.io is the engine for the video/audio distribution tree. It handles the automated publishing from one source to all platforms — no API calls, no code. Pure drag-and-drop.

**Client cost:** ~$49/mo (Marketer plan). Either bill client directly or mark up in monthly retainer.
**Supported sources:** TikTok, Instagram Reels, YouTube Shorts, Facebook, Podcast RSS
**Supported destinations:** YouTube Shorts, Facebook Page, Facebook Group, LinkedIn, Instagram Reels, Instagram Stories, Instagram Feed, Pinterest Idea Pins, Twitter/X, Google Drive, Dropbox

---

## Step 1: Create the Client's Repurpose.io Account

1. Go to repurpose.io → Start Free Trial (or client creates account)
2. Upgrade to **Marketer plan** ($49/mo) — supports 5 social profiles
3. Set timezone to client's local timezone

---

## Step 2: Connect the Source Platform

This is where the client's original content lives.

**If source = TikTok:**
1. Dashboard → **Workflows** → **+ New Workflow**
2. Source: TikTok → Connect Account → log into client's TikTok
3. Select: "New video posted" as the trigger

**If source = Instagram Reels:**
1. Source: Instagram → Connect Account (requires Facebook Business Manager)
2. Select: "New Reel posted"

**If source = YouTube:**
1. Source: YouTube → Connect Account
2. Select: "New video published" OR "New Short published"

**If source = Podcast (audio-only):**
1. Source: Podcast → paste RSS feed URL
2. Repurpose.io reads new episodes automatically

---

## Step 3: Connect Destination Platforms

For each destination, go to Settings → Social Profiles → Connect:

**Facebook Page + Group:**
- Connect via Facebook login → select Page
- For Groups: admin must connect the Group separately

**LinkedIn:**
- Connect via LinkedIn OAuth → select Personal Profile or Company Page

**Instagram:**
- Connect via Facebook Business Manager (Instagram must be a Business account)
- Three separate destinations: Reels, Stories, Feed

**YouTube Shorts:**
- Connect Google account → select YouTube channel

**Pinterest:**
- Connect Pinterest account → select Board for Idea Pins

**Twitter/X:**
- Connect Twitter account via OAuth

**Google Drive backup:**
- Connect Google account → select destination folder
- Creates automatic backup of every piece of content

---

## Step 4: Build the Workflow Rules

Each workflow = one source → one destination (you need multiple workflows for multiple destinations).

**Recommended workflow set for a TikTok creator:**

| Workflow Name | Source | Destination | Notes |
|---------------|--------|-------------|-------|
| TikTok → YouTube Shorts | TikTok | YouTube Shorts | Remove TikTok watermark (Repurpose.io does this automatically) |
| TikTok → FB Page | TikTok | Facebook Page | Add custom caption template |
| TikTok → FB Group | TikTok | Facebook Group | Same video, different audience |
| TikTok → LinkedIn | TikTok | LinkedIn | Add professional context caption |
| TikTok → IG Reels | TikTok | Instagram Reels | May need aspect ratio crop |
| TikTok → IG Stories | TikTok | Instagram Stories | Auto-crops to Story format |
| TikTok → IG Feed | TikTok | Instagram Feed | Square crop for feed |
| TikTok → Pinterest | TikTok | Pinterest Idea Pins | |
| TikTok → Twitter/X | TikTok | Twitter/X | |
| TikTok → Drive | TikTok | Google Drive | Backup folder |

**Workflow settings (each one):**
- **Caption:** Use original caption (pulls from TikTok) OR set custom template
- **Custom caption template example:** `{{original_caption}} #[NICHE_HASHTAG] #[BRAND_HASHTAG]`
- **Schedule:** Publish immediately OR delay by X hours (staggers content across the day)
- **Hashtags:** Add 3-5 platform-specific hashtags at workflow level

---

## Step 5: Caption Customization per Platform

Repurpose.io's caption field supports variables:
- `{{original_caption}}` — pulls the original TikTok/IG caption
- `{{title}}` — video title (YouTube)

**Recommended caption templates:**

**Facebook:** `{{original_caption}} 👇 Drop a comment below! #[NICHE] #[BUSINESS]`

**LinkedIn:** `{{original_caption}} [2-sentence professional context about why this matters for their industry]`

**Twitter/X:** Short version of caption (280 char limit) — remove hashtags, add 1-2 relevant ones

---

## Step 6: Test Each Workflow

1. Post a test video on the source platform (TikTok, etc.)
2. In Repurpose.io → **Activity Log** — verify each workflow triggers within 5–10 minutes
3. Check each destination platform — confirm the video posted correctly
4. Spot-check captions, hashtags, and format on each platform

---

## Step 7: The n8n Layer (AI Text Content)

Repurpose.io handles video distribution. For AI-generated text content (captions, blog posts, LinkedIn articles from the video), we layer in the n8n **Social Media Posting Machine**:

1. Import `workflow-social-posting.json` into n8n
2. Configure the OpenAI node with client's API key
3. Set trigger: manual (client pastes in content idea) or scheduled (weekly batch)
4. Workflow outputs: platform-specific caption drafts → email for approval → posts to connected accounts
5. This covers: Blog post from video transcript, LinkedIn article, email newsletter excerpt

See `setup-sop.md` for the full n8n setup steps.
