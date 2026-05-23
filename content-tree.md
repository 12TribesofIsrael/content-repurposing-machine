# Content Repurposing Tree — Distribution Map

Source: Repurpose.io framework (adapted for BMB client delivery)

One 60-second TikTok (or any short-form video) → 33 pieces of content.

---

## Branch 1: Full Video (handled by Repurpose.io)

| Output | Platform | Tool | Notes |
|--------|----------|------|-------|
| Short video | YouTube Shorts | Repurpose.io | Watermark removed automatically |
| Short video | Facebook Page | Repurpose.io | Original caption + branded hashtags |
| Short video | Facebook Group | Repurpose.io | Community-specific caption |
| Short video | LinkedIn | Repurpose.io | Professional caption layer |
| Short video | Instagram Reels | Repurpose.io | |
| Short video | Instagram Stories | Repurpose.io | Auto-cropped to Stories format |
| Short video | Instagram Feed | Repurpose.io | Square crop |
| Short video | Pinterest Idea Pins | Repurpose.io | |
| Short video | Twitter/X | Repurpose.io | |
| Short video backup | Google Drive / Dropbox | Repurpose.io | Archive copy |

**Total: 10 pieces from full video**

---

## Branch 2: Text (handled by n8n Social Media Posting Machine)

AI extracts transcript from video → generates platform-optimized text content.

| Output | Platform | Tool | Notes |
|--------|----------|------|-------|
| Blog post (500-800 words) | WordPress / Website | n8n + GPT-4o | SEO-optimized, embeds YouTube Short |
| IG Text Post + Graphic | Instagram Feed | n8n + Canva API (optional) | Quote from video as graphic |
| LinkedIn article | LinkedIn | n8n + GPT-4o | Expanded professional version |
| Facebook text post | Facebook Page | n8n + GPT-4o | Conversational version |
| Quote graphic | Facebook Page | n8n + image gen | Key insight pulled from video |
| Quote graphic | LinkedIn | n8n + image gen | Professional framing |
| Quote graphic | Instagram Reels | n8n + image gen | Animated or static |
| Quote graphic | Instagram Stories | n8n + image gen | |
| Quote graphic | Instagram Feed | n8n + image gen | |
| Quote graphic | Pinterest Idea Pins | n8n + image gen | |
| Quote graphic | Twitter/X | n8n + image gen | |

**Total: 11 pieces from text**

---

## Branch 3: Audio (handled by Repurpose.io)

Repurpose.io extracts audio from the video → distributes as podcast-style content.

| Output | Platform | Tool | Notes |
|--------|----------|------|-------|
| Podcast episode | Spotify | Repurpose.io | Requires podcast RSS setup |
| Podcast episode | Apple Podcasts | Repurpose.io | Same RSS feed |
| Alexa Skill audio | Amazon Alexa | Repurpose.io | Flash briefing format |
| Audiogram | YouTube Shorts | Repurpose.io | Audio waveform video |
| Audiogram | Facebook Page | Repurpose.io | |
| Audiogram | Facebook Group | Repurpose.io | |
| Audiogram | LinkedIn | Repurpose.io | |
| Audiogram | Instagram Reels | Repurpose.io | |
| Audiogram | Instagram Stories | Repurpose.io | |
| Audiogram | Instagram Feed | Repurpose.io | |
| Audiogram | Pinterest Idea Pins | Repurpose.io | |
| Audiogram | Twitter/X | Repurpose.io | |

**Total: 12 pieces from audio**

---

## Grand Total: 33 pieces from 1 video

| Branch | Tool | Pieces |
|--------|------|--------|
| Full Video | Repurpose.io | 10 |
| Text | n8n + GPT-4o | 11 |
| Audio | Repurpose.io | 12 |
| **Total** | | **33** |

---

## Starter Package vs. Full Package

Offer clients a tiered setup:

**Starter ($500 setup / $97/mo):**
- Repurpose.io + 5 platforms (TikTok → YouTube Shorts, FB Page, IG Reels, LinkedIn, backup)
- n8n text layer: 1 platform (LinkedIn or Facebook text posts)
- Best for: coaches just getting started with content

**Full Stack ($800 setup / $197/mo):**
- All 10 video destinations
- Full n8n text layer (blog + 4 platforms)
- Monthly content calendar review
- Best for: established creators, consultants with multiple active platforms

**Enterprise ($1,500 setup / $297/mo):**
- All 33 pieces
- Audiograms + podcast distribution
- Weekly review + optimization
- Best for: high-volume content businesses
