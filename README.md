# Content Repurposing Service

**Stack:** Repurpose.io + a Python/Modal text layer (built per client)
**Build time per client:** 3–5 hours (Repurpose.io setup + text layer deploy)
**Setup fee:** $500–$1,500 | **Monthly retainer:** $97–$297/mo (plus Repurpose.io $35/mo Starter, billed to client)

## What the Client Gets

One YouTube long-form video automatically becomes up to **33 pieces of content** across every major platform — across three branches.

**Branch 1 — Video (11 pieces, Repurpose.io)**
Full video → FB Page, FB Group, Google Drive/Dropbox.
Vertical clips (60s, auto-clipped) → IG Reels/Stories, IG Feed, TikTok, Twitter, LinkedIn, YouTube Shorts, Pinterest Idea Pins, FB Page.

**Branch 2 — Text (10 pieces, Python + Modal + Claude/OpenAI)**
Blog post w/ YouTube embed (1); summarized text posts for IG/FB/LinkedIn (3); 6 quote graphics across Twitter/FB/LinkedIn/IG Feed/IG Reels/Pinterest.

**Branch 3 — Audio (11 pieces, Repurpose.io)**
Full audio → Podcast (Spotify+Apple), Drive backup.
Audio clips → Alexa skills, 8 vertical audiograms across IG Reels/IG Feed/TikTok/LinkedIn/Twitter/FB Page/YouTube Shorts/Pinterest.

See `content-tree.md` for the full mapping. See `text-layer/README.md` for the Branch 2 architecture.

## Proven ROI (use in sales conversations)

- Average creator saves 6–10 hours/week on manual repurposing
- Repurpose.io alone is $35/mo — client pays you for the custom build + the text layer + ongoing oversight
- Coaches who post consistently report 2–5x follower growth vs. sporadic posting
- Time savings at $50/hr equivalent = $300–$500/week returned to the client

## What You Need from the Client

- [ ] **Primary source pattern** — YouTube long-form (Pattern A, per the PDF) OR Google Drive → IG Reels (Pattern B, proven two-stage flow). See `setup-sop.md` Phase 2.
- [ ] All destination platform logins (or admin access)
- [ ] Brand voice doc or 3 example posts they like (powers the Branch 2 prompts)
- [ ] **Anthropic or OpenAI API key** — only if Branch 2 is in scope
- [ ] WordPress / blog URL — only if Branch 2 blog-post output is wanted
- [ ] Podcast RSS feed — only if Branch 3 is in scope
- [ ] Email for content-approval workflow (optional — auto-post or require approval)

## Files in This Directory

- `setup-sop.md` — full build walkthrough (Phases 1–7)
- `repurpose-io-setup.md` — Repurpose.io account setup + platform connections (both source patterns)
- `content-tree.md` — the full 33-piece distribution map
- `text-layer/README.md` — Python + Modal text-generation architecture for Branch 2
- `docs/` — client-specific notes and per-build configuration
- `Turn-1-YouTube-Video-into-33-Pieces-of-Content (1).pdf` — Repurpose.io's official tree diagram (source for `content-tree.md`)
