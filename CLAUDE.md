# Content Repurposing Machine — Claude Code Guide

## What This Project Is

A client-delivery system for BMB AI Automations. The product: one YouTube long-form video becomes up to 33 pieces of content distributed automatically across every major platform.

**Two tools power it:**
- **Repurpose.io** (Starter $35/mo or Pro $79/mo, billed to client) — handles 22 pieces (Branches 1 + 3, video + audio)
- **Python + Modal text layer** — handles the remaining 10 pieces (Branch 2: blog post, summarized captions, quote graphics) via Claude or OpenAI

The service is sold in 3 tiers: $500 Starter / $800 Full Stack / $1,500 Enterprise.

## File Map

| File | Purpose |
|------|---------|
| `README.md` | Project overview and pricing |
| `content-tree.md` | Full 33-piece distribution map across the three branches |
| `setup-sop.md` | Step-by-step client setup guide (Phases 1–7) |
| `repurpose-io-setup.md` | Repurpose.io-specific setup — account, plans, connections, both source patterns |
| `text-layer/README.md` | Architecture spec for the Branch 2 Python + Modal text-generation script (build per client) |
| `Turn-1-YouTube-Video-into-33-Pieces-of-Content (1).pdf` | Repurpose.io's official tree diagram (source of truth for `content-tree.md`) |

## What Needs to Be Built Per Client

### 1. Repurpose.io setup (~2 hours)
- Follow `repurpose-io-setup.md`
- Create or take over the client's Repurpose.io account (Starter $35 or Pro $79)
- Pick the source pattern (Pattern A: YouTube long-form, OR Pattern B: Google Drive → IG Reels → downstream)
- Connect destination platforms
- Build workflows for Branches 1 (Video, 11 destinations) and 3 (Audio, 11 destinations)
- Test with a real video post

### 2. Python + Modal text layer (~2 hours per client)
- The text layer is built per-client because brand-voice prompts and platform credentials are client-specific
- Pulls transcript from the source video (yt-dlp or YouTube Data API)
- Calls Claude/OpenAI to generate: blog post, 3 summarized captions, 6 quote-graphic text payloads
- Renders quote graphics via Canva API or Bannerbear
- Posts to WordPress / IG / FB / LinkedIn / Twitter / Pinterest via platform APIs (or queues for approval)
- Deployed to Modal as a webhook-triggered function
- See `text-layer/README.md` for full architecture

### 3. Handoff (~30 min)
- 5-minute Loom walking the client through Repurpose.io + the text-layer approval email
- Set expectation: their job is to keep producing the source video; the system handles the rest

## How to Work in This Repo with Claude Code

Good prompts:

- "Read setup-sop.md and walk me through Phase 3 step by step"
- "Help me draft the Claude system prompt for the blog-post generator for [client name]"
- "What credentials do I need for the IG posting step of the text layer?"
- "Compare Pattern A vs. Pattern B for a client whose main content is TikTok-style shorts"
- "Draft the Loom handoff outline for [client name]"

## Key Concepts for Troubleshooting

- **Plan naming changed** — Repurpose.io retired the "Marketer $49" plan. Current tiers: Starter $35 / Pro $79 / Agency $179. Default to Starter for solo clients, Pro when they need 10+ accounts per network.
- **Instagram requires Facebook Business Manager** — Personal IG accounts can't connect. Client must switch to Business/Creator first (free, in IG app).
- **Facebook link reach penalty** — Never put YouTube links in the Facebook post body. Drop them in the first comment (manually or via the text layer's posting step).
- **Token expiry** — Instagram/Facebook tokens expire every 60–90 days; Pinterest every 30. Build a re-auth reminder into the monthly maintenance checklist.
- **Repurpose.io watermark removal** — Automatically removes TikTok watermarks when posting to YouTube Shorts. No extra steps needed.
- **Two source patterns** — Pattern A (YouTube long-form, per the PDF) vs. Pattern B (Google Drive → IG Reels → downstream, the proven two-stage flow). See `setup-sop.md` Phase 2 to pick.
- **Branch 2 alternatives to Python+Modal** — n8n, Make.com, Zapier all work; Python+Modal is chosen because the dev environment already has Modal CLI + Anthropic/OpenAI auth configured.
