# Content Repurposing Machine — Claude Code Guide

## What This Project Is

A client-delivery system for BMB AI Automations. The product: one video becomes
up to 22 pieces of content distributed automatically across every major platform.

**One tool powers it:**
- **Repurpose.io** — handles all video and audio distribution (no code, pure dashboard config)

The service is sold in 3 tiers: $500 Starter / $800 Full Stack / $1,500 Enterprise.

## File Map

| File | Purpose |
|------|---------|
| `README.md` | Project overview and pricing |
| `content-tree.md` | The full distribution map — what gets posted where |
| `setup-sop.md` | Step-by-step client setup guide (Phases 1–5) |
| `repurpose-io-setup.md` | Repurpose.io-specific setup (platform connections, workflow config) |

## What Needs to Be Built

The docs are reference material. Per-client work is all dashboard configuration:

### 1. Repurpose.io Setup (the entire build)
- Follow `repurpose-io-setup.md` step by step
- Create or take over the client's Repurpose.io account (Marketer plan, $49/mo)
- Connect source platform (TikTok, YouTube, IG Reels, or Podcast RSS)
- Connect all destination platforms
- Build one workflow per destination (up to 10 video, plus podcast/audiogram workflows for the audio branch)
- Test with a real video post

### 2. Caption Templates per Platform
- Build platform-specific caption templates using Repurpose.io's `{{original_caption}}` and `{{title}}` variables
- See `repurpose-io-setup.md` Step 5 for recommended templates
- Tune to brand voice using the examples the client provides

### 3. Handoff
- Record a 5-minute Loom walking the client through the Repurpose.io Activity Log
- Set expectation: their only job is to keep posting on the source platform

## How to Work in This Repo with Claude Code

Good prompts to use:

- "Read setup-sop.md and walk me through Phase 2 step by step"
- "What does Instagram need in Repurpose.io and how do I connect it?"
- "Help me write a Facebook caption template for [client name] using Repurpose.io variables"
- "Draft the Loom handoff outline for [client name]"

## Key Concepts for Troubleshooting

- **Instagram requires Facebook Business Manager** — Personal IG accounts can't connect. Client must switch to Business/Creator first (free, in IG app).
- **Facebook link reach penalty** — Never put YouTube links in the Facebook post body. Either drop them in the first comment manually, or add them as a separate line at the bottom of the caption template.
- **Token expiry** — Instagram and Facebook tokens expire every 60–90 days. Build a re-auth reminder into the monthly maintenance checklist.
- **Repurpose.io watermark removal** — Automatically removes TikTok watermarks when posting to YouTube Shorts. No extra steps needed.
- **LinkedIn Company Page** — Client must add you as a Page admin before Repurpose.io can post to it.
