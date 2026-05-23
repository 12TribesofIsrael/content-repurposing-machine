# Content Repurposing Service

**Stack:** Repurpose.io + n8n (Social Media Posting Machine + Auto Posting)
**Build time per client:** 2–4 hours
**Setup fee:** $500–$800 | **Monthly retainer:** $97–$197/mo (plus Repurpose.io $49/mo, billed to client)

## What the Client Gets

One piece of content automatically becomes 10–33 pieces distributed across every platform — without touching a single app manually.

**The Content Tree (from 1 short-form video):**
- Full video → YouTube Shorts, FB Page, FB Group, LinkedIn, IG Reels, IG Stories, IG Feed, Pinterest Idea Pins, Twitter/X, Google Drive backup
- Text (AI-extracted transcript) → Blog post, IG Text Graphic, LinkedIn article, Facebook post
- Quote Graphics (AI-pulled key moments) → FB, LinkedIn, IG Reels/Stories/Feed, Pinterest, Twitter
- Audio → Podcast episode (Spotify/Apple), Audiograms → all video platforms

**Tool split:**
- **Repurpose.io** handles the video/audio distribution tree (automatic, no-code)
- **n8n Social Media Posting Machine** handles AI-generated text content (captions, blog, email, LinkedIn articles)

## Proven ROI (use in sales conversations)

- Average creator saves 4–8 hours/week on manual repurposing
- Repurpose.io competitor charges $49–$299/mo — client pays less getting a custom build
- Coaches who post consistently report 2–5x follower growth vs. sporadic posting
- Time savings at $50/hr equivalent = $200–$400/week returned to the client

## What You Need from the Client

- [ ] Their main content source: TikTok? YouTube? Instagram? (determines Repurpose.io source)
- [ ] All destination platform logins (or platform admin access to connect)
- [ ] OpenAI API key (for AI caption + content generation nodes in n8n)
- [ ] Brand voice doc or 3 example posts they like
- [ ] Posting schedule preference (post immediately vs. queue for specific times)
- [ ] Email for content approval workflow (optional — can auto-post or require approval)
- [ ] WordPress/blog URL (if blog post output is wanted)

## Files in This Directory

- `setup-sop.md` — full build walkthrough
- `repurpose-io-setup.md` — Repurpose.io account setup + platform connections
- `content-tree.md` — the full 33-piece distribution map with platform specs
- `workflow-social-posting.json` — n8n Social Media Posting Machine (import to n8n)
- `workflow-auto-posting.json` — n8n Auto Posting scheduler (import to n8n)
- `workflow-shorts-clipper.json` — n8n Shorts Clipper for video-to-clips (import to n8n)
