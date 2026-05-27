# Content Repurposing Tree — Distribution Map

Source: official Repurpose.io infographic — `Turn-1-YouTube-Video-into-33-Pieces-of-Content (1).pdf`.

One YouTube long-form video → up to **33 pieces of content** across three branches.

---

## Branch 1: Video (11 pieces) — Repurpose.io

| Output | Source clip | Platform | Tool | Notes |
|--------|-------------|----------|------|-------|
| Full video | Full | Facebook Page | Repurpose.io | |
| Full video | Full | Facebook Group | Repurpose.io | |
| Full video backup | Full | Google Drive / Dropbox | Repurpose.io | Archive copy |
| Vertical clip | 60s | Instagram Reels / Stories | Repurpose.io | Auto-clipped via Repurpose.io's clip feature |
| Vertical clip | 60s | Instagram Feed | Repurpose.io | Square crop |
| Vertical clip | 60s | TikTok | Repurpose.io | |
| Vertical clip | 60s | Twitter / X | Repurpose.io | |
| Vertical clip | 60s | LinkedIn | Repurpose.io | Professional caption layer |
| Vertical clip | 60s | YouTube Shorts | Repurpose.io | Watermark removed automatically |
| Vertical clip | 60s | Pinterest Idea Pin | Repurpose.io | |
| Vertical clip | 60s | Facebook Page | Repurpose.io | Short-form version on the page |

**Total: 11 pieces**

---

## Branch 2: Text (10 pieces) — Python + Modal + Claude/OpenAI

A per-client Python script (deployed to Modal) pulls the video transcript, calls an LLM, and either posts directly or queues for client approval. See `text-layer/README.md` for the architecture.

| Output | Platform | Tool | Notes |
|--------|----------|------|-------|
| Blog post (500–800 words) with YouTube embed | WordPress / Website | Python + Claude/OpenAI | SEO-optimized, embeds the source YouTube video |
| Summarized text post (~2200 chars) | Instagram Feed | Python + Claude/OpenAI | Conversational, emoji-friendly, plus featured image |
| Summarized text post | Facebook Page | Python + Claude/OpenAI | Question-based to drive comments |
| Summarized text post | LinkedIn | Python + Claude/OpenAI | Professional insight angle |
| Quote graphic | Twitter / X | Python + Claude/OpenAI + Canva/Bannerbear | Key insight pulled from video |
| Quote graphic | Facebook Page | Python + Claude/OpenAI + Canva/Bannerbear | |
| Quote graphic | LinkedIn | Python + Claude/OpenAI + Canva/Bannerbear | Professional framing |
| Quote graphic | Instagram Feed | Python + Claude/OpenAI + Canva/Bannerbear | |
| Quote graphic | Instagram Reels / Stories | Python + Claude/OpenAI + Canva/Bannerbear | Static or animated |
| Quote graphic | Pinterest Idea Pin | Python + Claude/OpenAI + Canva/Bannerbear | |

**Total: 10 pieces**

---

## Branch 3: Audio (11 pieces) — Repurpose.io

Repurpose.io extracts audio natively from the source video.

| Output | Source | Platform | Tool | Notes |
|--------|--------|----------|------|-------|
| Podcast episode | Full audio | Spotify + Apple Podcasts | Repurpose.io | Single RSS feed serves both (Buzzsprout, Anchor, Captivate as host) |
| Audio backup | Full audio | Google Drive / Dropbox | Repurpose.io | Archive copy |
| Alexa Skill audio | 60s clip | Amazon Alexa | Repurpose.io | Flash briefing format |
| Vertical audiogram | 60s clip | Instagram Reels / Stories | Repurpose.io | Waveform-on-image video |
| Vertical audiogram | 60s clip | Instagram Feed | Repurpose.io | |
| Vertical audiogram | 60s clip | TikTok | Repurpose.io | |
| Vertical audiogram | 60s clip | LinkedIn | Repurpose.io | |
| Vertical audiogram | 60s clip | Twitter / X | Repurpose.io | |
| Vertical audiogram | 60s clip | Facebook Page | Repurpose.io | |
| Vertical audiogram | 60s clip | YouTube Shorts | Repurpose.io | |
| Vertical audiogram | 60s clip | Pinterest Idea Pin | Repurpose.io | |

**Total: 11 pieces**

---

## Grand Total

| Branch | Tool | Pieces |
|--------|------|--------|
| 1. Video | Repurpose.io | 11 |
| 2. Text | Python + Modal + Claude/OpenAI | 10 |
| 3. Audio | Repurpose.io | 11 |
| **Total** | | **32** |

Repurpose.io's marketing rounds to "33" — the count varies depending on whether bundled destinations (Spotify+Apple, IG Reels+Stories, Drive+Dropbox) are counted as one or two. The tree above honors the PDF's official grouping.

> **Note on Instagram Feed:** the PDF lists "IG Feed" as a separate destination on both Branch 1 and Branch 3. In practice, Repurpose.io does not support a distinct "Feed video" workflow target for Instagram — Reels appear in the Feed automatically. The IG Feed rows in the tables above describe coverage *via* IG Reels rather than a second workflow you'd build. See `docs/repurpose-io-ui-automation.md` for the technical detail.

---

## Starter Package vs. Full Package

Offer clients a tiered setup:

**Starter ($500 setup / $97/mo):**
- Repurpose.io + Branch 1 only — 5–11 video destinations of the client's choosing
- Best for: coaches just getting started with content

**Full Stack ($800 setup / $197/mo):**
- Repurpose.io + Branches 1 and 3 — all 22 video + audio pieces
- Podcast RSS setup, audiograms across every platform
- Monthly content calendar review
- Best for: established creators, consultants, B2B with podcast appetite

**Enterprise ($1,500 setup / $297/mo):**
- All 33 pieces — adds the Python + Modal text layer (Branch 2)
- Custom Claude/OpenAI prompt tuned to client's brand voice
- Quote-graphic template designed in Canva (or Bannerbear), then rendered programmatically
- Weekly review + prompt optimization
- Best for: high-volume content businesses, agencies, B2B coaches who need blog SEO
