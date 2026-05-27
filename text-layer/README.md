# Branch 2 Text Layer

Python + Modal script that generates the 10 text-and-graphic pieces of the content tree (Branch 2 in `../content-tree.md`).

**Status:** Template ready — see [`client-template.py`](client-template.py). Per-client deploy: copy → fill the CLIENT CONFIG block at the top → wire credentials into a Modal Secret → `modal deploy`. The script itself is generic; only the brand-voice prompt, hashtags, approval email, and credentials change per client.

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

## Quick start (per new Enterprise client)

```bash
cd content-repurposing-machine/text-layer

# 1. Copy the template
cp client-template.py client-<name>.py

# 2. Edit the CLIENT CONFIG block at the top of client-<name>.py:
#    - CLIENT_NAME, BRAND_COLOR, APPROVAL_EMAIL
#    - BRAND_VOICE (paste 3 example captions + voice notes)
#    - HASHTAGS per platform
#    - PUBLISH_TARGETS set (remove any platforms you don't want)

# 3. Fill in .env from .env.example, then load into a Modal Secret
cp .env.example .env
# ...edit .env...
modal secret create content-<name>-secrets --from-dotenv .env
rm .env  # don't leave credentials on disk

# 4. Deploy
modal deploy client-<name>.py

# 5. Copy the printed webhook URL into MODAL_PUBLIC_URL in the Secret,
#    then redeploy once so the approval-email link points at it.

# 6. Wire the webhook into a Google Form (manual) or scheduled function (batch).
```

Manual smoke test before handing off:

```bash
modal run client-<name>.py --youtube-url=https://youtu.be/<short test video>
```

Watch Modal logs — you should see all 5 stages fire and an approval email
land at APPROVAL_EMAIL with 6 inline quote graphics. Click the link → check
the deployed platforms for the posts.

## Triggers

The webhook accepts `POST {"youtube_url": "..."}` and returns
`{"status": "drafts emailed", "token": "..."}`. Wire it to:
- A Google Form (manual mode — client pastes YouTube URL, form triggers webhook), OR
- The included `weekly_batch` scheduled function (cron `0 9 * * 1` — fill in
  `_read_pending_urls()` to pull from your source: Google Sheet, Notion DB, Airtable).

See `../setup-sop.md` Phase 4 for the full deployment SOP.

## Credentials

Full list with format and provenance in [`.env.example`](.env.example).
Loaded into a Modal Secret named `content-<client-name>-secrets`.
Anything you omit → that platform is skipped at publish time (logged, not
fatal), so day-one deploys can hit just one or two platforms and add the
rest over time.

## Why Python + Modal

The dev environment in this repo already has Modal CLI + Anthropic/OpenAI keys configured (see global `CLAUDE.md` and the `youtubeoptermizer/`, `ai-bible-gospels/` Modal deploys). Reusing that stack means:
- No separate workflow-builder dashboard to host or update
- Webhooks are first-class on Modal; scheduled functions are first-class
- Code is source-controllable and reviewable (vs. exported n8n JSON)
- Cheaper at multi-client scale (one Modal account vs. one n8n instance per client)

## Why not n8n / Make.com / Zapier

All three are valid alternatives — pick one if you prefer a visual workflow builder or have non-coding teammates who'll need to edit. Trade-off: each adds another tool to maintain per client. For BMB's stack (Python-fluent dev environment, Modal already deployed for other products), Python wins on simplicity.
