# Branch 2 Text Layer

Python + Modal script that generates the 10 text-and-graphic pieces of the content tree (Branch 2 in `../content-tree.md`).

**Status:** Architecture spec only — not yet built. Built per-client because brand-voice prompts, hashtag lists, and posting credentials are client-specific.

## What this layer produces

| Output | Platform | Format |
|--------|----------|--------|
| Blog post (500–800 words) | WordPress | HTML with YouTube embed |
| Summarized text post (~2200 chars) | Instagram Feed | Caption + featured image |
| Summarized text post | Facebook Page | Caption |
| Summarized text post | LinkedIn | Long-form text post |
| Quote graphic + caption | Twitter, FB Page, LinkedIn, IG Feed, IG Reels/Stories, Pinterest | Generated image + short caption |

10 outputs total. See `../content-tree.md` Branch 2 for the full mapping.

## Architecture

```
YouTube URL (manual paste OR scheduled trigger)
        │
        ▼
[1] Pull transcript
    Tool: yt-dlp OR YouTube Data API (captions endpoint)
        │
        ▼
[2] LLM call (Claude or OpenAI)
    System prompt: client brand voice + posting rules per platform
    Outputs (single call, structured JSON):
      - Blog post markdown (500–800 words)
      - 3 summarized captions (IG, FB, LinkedIn)
      - 6 quote-graphic text payloads
        │
        ▼
[3] Render quote graphics
    Tool: Canva API, Bannerbear, or Placid
    Inputs: 6 quote payloads + brand template ID
    Outputs: 6 PNG/JPG image URLs
        │
        ▼
[4] Approval email (optional)
    Drafts → client inbox → reply "approve"
    Skip this step if client wants auto-publish
        │
        ▼
[5] Post to platforms
    - WordPress (XML-RPC or REST API)
    - Direct platform APIs for IG / FB / LinkedIn / Twitter / Pinterest
    - OR queue via Buffer/Metricool API (single integration covers all)
```

## Deployment

```bash
modal deploy text-layer/client-<name>.py
```

Modal returns a webhook URL. Wire it to:
- A Google Form (manual mode — client pastes YouTube URL, form triggers webhook), OR
- A Modal scheduled function (batch mode — runs e.g. Monday 9am, pulls from a content-ideas Google Sheet)

See `../setup-sop.md` Phase 4 for the full deployment SOP.

## Credentials required (per client)

- **Anthropic API key** (Claude) OR **OpenAI API key**
- **WordPress application password** (if blog output enabled)
- **Canva API key** OR **Bannerbear API key** (for quote-graphic rendering)
- **Per-platform posting credentials** — either OAuth tokens or a scheduler API key (Buffer/Metricool covers multiple platforms with one key)

## Why Python + Modal

The dev environment in this repo already has Modal CLI + Anthropic/OpenAI keys configured (see global `CLAUDE.md` and the `youtubeoptermizer/`, `ai-bible-gospels/` Modal deploys). Reusing that stack means:
- No separate workflow-builder dashboard to host or update
- Webhooks are first-class on Modal; scheduled functions are first-class
- Code is source-controllable and reviewable (vs. exported n8n JSON)
- Cheaper at multi-client scale (one Modal account vs. one n8n instance per client)

## Why not n8n / Make.com / Zapier

All three are valid alternatives — pick one if you prefer a visual workflow builder or have non-coding teammates who'll need to edit. Trade-off: each adds another tool to maintain per client. For BMB's stack (Python-fluent dev environment, Modal already deployed for other products), Python wins on simplicity.
