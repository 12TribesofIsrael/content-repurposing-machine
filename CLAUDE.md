# Content Repurposing Machine — Claude Code Guide

## What This Project Is

A client-delivery system for BMB AI Automations. The product: one video becomes
33 pieces of content distributed automatically across every major platform.

**Two tools power it:**
- **Repurpose.io** — handles video + audio distribution (no code, pure dashboard config)
- **n8n** — handles AI-generated text content (captions, blog posts, LinkedIn articles)

The service is sold in 3 tiers: $500 Starter / $800 Full Stack / $1,500 Enterprise.

## File Map

| File | Purpose |
|------|---------|
| `README.md` | Project overview and pricing |
| `content-tree.md` | The full 33-piece distribution map — what gets posted where |
| `setup-sop.md` | Step-by-step client setup guide (Phases 1–6) |
| `repurpose-io-setup.md` | Repurpose.io-specific setup (platform connections, workflow config) |
| `workflow-social-posting.json` | n8n workflow — import this to set up the text/AI layer |
| `workflow-auto-posting.json` | n8n workflow — auto-posting scheduler |
| `workflow-shorts-clipper.json` | n8n workflow — clips long videos into shorts |
| `.env.example` | All API keys needed — copy to `.env` and fill in |

## What Needs to Be Built

The docs and n8n workflows already exist. The build tasks are:

### 1. n8n Setup (main build task)
- Sign up at app.n8n.io (or self-host)
- Import the three workflow JSON files
- Add credentials for each platform (OpenAI, Gmail, LinkedIn, Facebook, Twitter)
- Customize the system prompt node in `workflow-social-posting.json` with client brand voice
- Set the trigger (manual form or scheduled)
- Test end-to-end: input → AI generates content → approval email → posts live

### 2. Repurpose.io Setup (no-code, dashboard work)
- Follow `repurpose-io-setup.md` step by step
- Connect source platform (TikTok or YouTube)
- Connect all destination platforms
- Build one workflow per destination (10 workflows for the full package)
- Test with a real video post

### 3. Client Intake Form
- Build a simple form (Google Form or Typeform) for clients to submit their content idea
- Connect it to n8n via Google Sheets trigger
- This is how the weekly batch generation gets triggered

### 4. Approval Email Flow
- Configure the n8n email node to send AI-generated drafts to the client's inbox
- Client replies "approve" or requests edits
- Test the full loop

## How to Work in This Repo with Claude Code

Claude Code can help you with all of this. Good prompts to use:

- "Read setup-sop.md and walk me through Phase 3 step by step"
- "I'm setting up the n8n workflow — what credentials do I need and where do I get them?"
- "Help me customize the system prompt in the n8n social posting workflow for [client name]"
- "I need to build the Google Form intake → Google Sheets → n8n trigger connection"
- "Write me a test script that verifies the n8n workflow fires correctly"

## Environment Variables

Copy `.env.example` to `.env` and fill in all values before running anything.
Never commit `.env` to git — it's in `.gitignore`.

## Key Concepts for Troubleshooting

- **n8n credentials** — Each platform needs an OAuth connection in n8n Settings → Credentials. Do this BEFORE activating any workflow.
- **Instagram requires Facebook Business Manager** — Personal IG accounts can't connect. Client must switch to Business/Creator first (free, in IG app).
- **Facebook link reach penalty** — Never put YouTube links in the Facebook post body. Use n8n's "First Comment" approach instead.
- **Token expiry** — Instagram and Facebook tokens expire every 60–90 days. Build a reminder into the monthly maintenance checklist.
- **Repurpose.io watermark removal** — It automatically removes TikTok watermarks when posting to YouTube Shorts. No extra steps needed.
