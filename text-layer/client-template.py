"""
Content Repurposing — Branch 2 Text Layer (client template)

Pipeline: YouTube URL -> transcript -> Claude (structured JSON) ->
          OpenAI gpt-image-1 (6 quote graphics) -> approval email ->
          one-click approve -> fan-out post to WordPress + IG + FB +
          LinkedIn + Twitter + Pinterest.

Per-client deploy:
  1.  cp client-template.py client-<name>.py
  2.  Edit the CLIENT CONFIG block below.
  3.  modal secret create content-<name>-secrets --from-dotenv .env
  4.  modal deploy client-<name>.py
  5.  Wire the returned webhook URL to a Google Form or Modal scheduled job.

See text-layer/README.md for the full SOP and .env.example for credentials.
"""

from __future__ import annotations

import base64
import json
import os
import re
import secrets as _stdsecrets
from datetime import datetime, timezone
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import modal

# =============================================================================
# CLIENT CONFIG  --  the only block an operator edits per client
# =============================================================================

CLIENT_NAME = "example-client"           # slugify: lowercase, hyphens, no spaces
BRAND_COLOR = "#0066FF"                  # hex, used in quote-graphic prompts
APPROVAL_EMAIL = "client@example.com"    # where draft approval emails go

# Paste 3 example captions + any brand-voice notes.  This is the system prompt
# that drives every generated piece, so be specific.  Long is fine -- it's
# prompt-cached on every re-run.
BRAND_VOICE = """\
[Paste 3 example captions the client has approved, plus 2-3 sentences on
voice (formal/casual? emojis? signature sign-off?).  Example:

EX 1: "Most coaches think growth = more hours.  Wrong.  Growth = better
systems.  Here are 3 we use weekly..."

EX 2: ...

EX 3: ...

VOICE: Direct, no fluff, 1-2 emojis max per post, always ends with a
question to drive comments.  Never uses corporate-speak.]
"""

# Per-platform hashtag appendix.  Leave empty string to disable.
HASHTAGS: dict[str, str] = {
    "instagram": "",
    "facebook": "",
    "linkedin": "",
    "twitter": "",
    "pinterest": "",
}

# Set of platforms to actually publish to.  Remove a name to disable.
# (You can also leave the platform here and just omit its credentials from
# the Modal Secret; the publish step will skip it gracefully.)
PUBLISH_TARGETS: set[str] = {
    "wordpress",
    "instagram",
    "facebook",
    "linkedin",
    "twitter",
    "pinterest",
}

LLM_MODEL = "claude-sonnet-4-6"

# =============================================================================
# MODAL APP SETUP
# =============================================================================

app = modal.App(f"content-repurposing-{CLIENT_NAME}")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "anthropic>=0.40.0",
        "openai>=1.50.0",
        "yt-dlp>=2024.10.0",
        "requests>=2.32.0",
        "tweepy>=4.14.0",
        "google-api-python-client>=2.120.0",
        "google-auth>=2.30.0",
        "google-auth-oauthlib>=1.2.0",
    )
)

secret = modal.Secret.from_name(f"content-{CLIENT_NAME}-secrets")

# Token store for pending approvals.  Keys auto-deleted on approve.
pending = modal.Dict.from_name("content-pending-approvals", create_if_missing=True)


# =============================================================================
# STAGE 1 -- pull transcript from YouTube
# =============================================================================

@app.function(image=image, secrets=[secret], timeout=600)
def pull_transcript(youtube_url: str) -> dict:
    import yt_dlp

    work_dir = "/tmp/yt"
    os.makedirs(work_dir, exist_ok=True)

    ydl_opts = {
        "writeautomaticsub": True,
        "writesubtitles": True,
        "subtitleslangs": ["en", "en-US", "en-GB"],
        "subtitlesformat": "vtt",
        "skip_download": True,
        "outtmpl": f"{work_dir}/%(id)s.%(ext)s",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)

    video_id = info["id"]
    transcript = ""
    for fname in os.listdir(work_dir):
        if fname.startswith(video_id) and fname.endswith(".vtt"):
            with open(os.path.join(work_dir, fname), encoding="utf-8") as f:
                transcript = _vtt_to_text(f.read())
            break

    if not transcript:
        raise RuntimeError(
            f"No captions found for {youtube_url}. "
            "Video may have captions disabled."
        )

    return {
        "video_id": video_id,
        "title": info.get("title", ""),
        "channel": info.get("uploader", ""),
        "duration": info.get("duration", 0),
        "transcript": transcript,
        "url": youtube_url,
    }


def _vtt_to_text(vtt: str) -> str:
    lines: list[str] = []
    for raw in vtt.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or "-->" in line:
            continue
        if re.match(r"^\d+$", line) or line.startswith(("NOTE", "STYLE", "Kind:", "Language:")):
            continue
        clean = re.sub(r"<[^>]+>", "", line)
        if clean and (not lines or lines[-1] != clean):
            lines.append(clean)
    return " ".join(lines)


# =============================================================================
# STAGE 2 -- single Claude call returns structured JSON for all 10 pieces
# =============================================================================

SYSTEM_PROMPT_TEMPLATE = """\
You are a content repurposing assistant for {client_name}.

BRAND VOICE (match this for every output):
{brand_voice}

TASK: Take a YouTube video transcript and produce 10 content pieces in one
strict-JSON response:
  - 1 blog post (500-800 words, HTML, embeds the source YouTube video)
  - 3 summarized captions tailored to Instagram / Facebook / LinkedIn
  - 6 quote-graphic payloads (one per platform), each = a pull-quote that
    will be rendered as a static image, plus a short caption to post under it

Per-platform rules:
  - instagram caption (~2200 chars max): conversational, line breaks for
    readability, emojis allowed, ends with a CTA or question
  - facebook caption: question-led to drive comments, no external links in
    body (post link in first comment instead)
  - linkedin caption: professional insight angle, 1-2 paragraph hook,
    plain text, no hashtag spam
  - quote_graphics quotes: 8-15 words, must stand alone (no "as I said
    earlier..."), punchy, the kind of line that survives without context
  - quote_graphics captions: 1-2 sentences below the image post, same voice

OUTPUT FORMAT (return ONLY this JSON, no prose, no code fences):
{{
  "blog_post": {{
    "title": "...",
    "html": "<p>Intro paragraph...</p><p>...</p><h2>Section</h2>..."
  }},
  "captions": {{
    "instagram": "...",
    "facebook": "...",
    "linkedin": "..."
  }},
  "quote_graphics": [
    {{"platform": "twitter",         "quote": "...", "caption": "..."}},
    {{"platform": "facebook",        "quote": "...", "caption": "..."}},
    {{"platform": "linkedin",        "quote": "...", "caption": "..."}},
    {{"platform": "instagram_feed",  "quote": "...", "caption": "..."}},
    {{"platform": "instagram_reels", "quote": "...", "caption": "..."}},
    {{"platform": "pinterest",       "quote": "...", "caption": "..."}}
  ]
}}

The blog_post.html MUST include a YouTube embed iframe near the top.  Use:
<iframe width="560" height="315" src="https://www.youtube.com/embed/{{VIDEO_ID}}"
title="YouTube video player" frameborder="0" allowfullscreen></iframe>

Do not add commentary.  Do not wrap in ```json.  Return raw JSON only.
"""


@app.function(image=image, secrets=[secret], timeout=600)
def generate_content(transcript_data: dict) -> dict:
    from anthropic import Anthropic

    client = Anthropic()

    system_text = SYSTEM_PROMPT_TEMPLATE.format(
        client_name=CLIENT_NAME,
        brand_voice=BRAND_VOICE,
    )

    # Cap transcript to ~50k chars to stay well within context.
    transcript = transcript_data["transcript"][:50_000]
    user_msg = (
        f"VIDEO_ID: {transcript_data['video_id']}\n"
        f"TITLE: {transcript_data['title']}\n"
        f"CHANNEL: {transcript_data['channel']}\n\n"
        f"TRANSCRIPT:\n{transcript}"
    )

    def _call(reinforce: bool = False) -> str:
        messages = [{"role": "user", "content": user_msg}]
        if reinforce:
            messages.append({
                "role": "assistant",
                "content": "I will return only raw JSON, no code fences, no prose.",
            })
        resp = client.messages.create(
            model=LLM_MODEL,
            max_tokens=16_000,
            system=[{
                "type": "text",
                "text": system_text,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=messages,
        )
        return resp.content[0].text

    raw = _call()
    try:
        return json.loads(_strip_fences(raw))
    except json.JSONDecodeError:
        raw = _call(reinforce=True)
        return json.loads(_strip_fences(raw))


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()


# =============================================================================
# STAGE 3 -- render 6 quote graphics via OpenAI gpt-image-1
# =============================================================================

# Platforms whose feed favors a 9:16 portrait crop.
_PORTRAIT_PLATFORMS = {"instagram_reels", "pinterest"}


@app.function(image=image, secrets=[secret], timeout=900)
def render_quote_graphics(payloads: list[dict]) -> list[dict]:
    from openai import OpenAI

    client = OpenAI()
    results: list[dict] = []

    for payload in payloads:
        quote = payload["quote"]
        platform = payload["platform"]
        size = "1024x1536" if platform in _PORTRAIT_PLATFORMS else "1024x1024"

        prompt = (
            f"Design a clean, modern quote graphic for {platform.replace('_', ' ')}.\n"
            f"Quote text (render exactly as written, no paraphrasing, "
            f"no added quotation marks): {quote!r}\n"
            f"Style: minimalist, generous whitespace, white background, "
            f"bold sans-serif typography centered, single accent line in "
            f"brand color {BRAND_COLOR}.  No decorative shapes, no people, "
            f"no logos.  Typography must be sharp and accurately spelled."
        )

        resp = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality="high",
            n=1,
        )
        image_b64 = resp.data[0].b64_json

        results.append({
            **payload,
            "image_b64": image_b64,
            "size": size,
        })

    return results


# =============================================================================
# STAGE 4 -- approval email
# =============================================================================

@app.function(image=image, secrets=[secret], timeout=300)
def send_approval_email(content_pkg: dict, video_url: str) -> str:
    """Send the approval email via Gmail API (OAuth token, auto-refreshing).

    Reuses the same Gmail OAuth pattern as the rest of the repo ecosystem --
    see ecosystem/gmail/send_punchlist.py and skills/personalized-ads/scripts/
    send_delivery_email.py.  Token comes from the Modal Secret as
    GMAIL_TOKEN_JSON (the full token.json contents as a single env string)."""
    token = _stdsecrets.token_urlsafe(16)

    pending[token] = {
        "content": content_pkg,
        "video_url": video_url,
        "ts": datetime.now(timezone.utc).isoformat(),
    }

    public_url = os.environ.get("MODAL_PUBLIC_URL", "")
    approve_link = (
        f"{public_url}/approve?token={token}"
        if public_url
        else f"(set MODAL_PUBLIC_URL; token={token})"
    )

    html_body = _build_approval_html(content_pkg, approve_link, video_url)
    sender = os.environ.get("GMAIL_SENDER", "me")

    msg = MIMEMultipart("related")
    msg["Subject"] = f"[Approve] Content for: {content_pkg['blog_post']['title']}"
    msg["From"] = sender
    msg["To"] = APPROVAL_EMAIL

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)

    for i, graphic in enumerate(content_pkg["quote_graphics"]):
        img = MIMEImage(base64.b64decode(graphic["image_b64"]))
        img.add_header("Content-ID", f"<graphic{i}>")
        img.add_header("Content-Disposition", "inline", filename=f"graphic{i}.png")
        msg.attach(img)

    service = _gmail_service()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

    print(f"[approval] sent to {APPROVAL_EMAIL} token={token}")
    return token


def _gmail_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token_json = os.environ.get("GMAIL_TOKEN_JSON")
    if not token_json:
        raise _MissingCreds(
            "GMAIL_TOKEN_JSON not set -- paste contents of token.json "
            "(scopes: gmail.send or gmail.modify) into the Modal Secret"
        )
    info = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(info, info.get("scopes") or [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.modify",
    ])
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _build_approval_html(content_pkg: dict, approve_link: str, video_url: str) -> str:
    blog = content_pkg["blog_post"]
    captions = content_pkg["captions"]
    graphics = content_pkg["quote_graphics"]

    card = (
        "background:#fff;border:1px solid #e2e2e2;border-radius:8px;"
        "padding:16px;margin:12px 0;font-family:system-ui,sans-serif;"
    )
    btn = (
        f"display:inline-block;padding:14px 28px;background:{BRAND_COLOR};"
        "color:#fff;text-decoration:none;border-radius:6px;font-weight:600;"
    )

    caption_cards = "".join(
        f'<div style="{card}"><h3 style="margin-top:0;text-transform:capitalize">'
        f'{platform}</h3><pre style="white-space:pre-wrap;font-family:inherit;'
        f'margin:0">{_escape(text)}</pre></div>'
        for platform, text in captions.items()
    )

    graphic_cards = "".join(
        f'<div style="{card}"><h3 style="margin-top:0;text-transform:capitalize">'
        f'{g["platform"].replace("_", " ")}</h3>'
        f'<img src="cid:graphic{i}" style="max-width:100%;border-radius:4px"/>'
        f'<p style="margin:8px 0 0"><em>Caption:</em> {_escape(g["caption"])}</p></div>'
        for i, g in enumerate(graphics)
    )

    return f"""\
<html><body style="background:#f4f4f4;padding:24px;font-family:system-ui,sans-serif;color:#222">
<div style="max-width:720px;margin:0 auto">
  <h1 style="margin-top:0">Drafts ready for: {_escape(blog['title'])}</h1>
  <p>Source: <a href="{_escape(video_url)}">{_escape(video_url)}</a></p>
  <p><a href="{_escape(approve_link)}" style="{btn}">Approve &amp; publish all</a></p>

  <h2>Blog post draft</h2>
  <div style="{card}">
    <h3 style="margin-top:0">{_escape(blog['title'])}</h3>
    {blog['html']}
  </div>

  <h2>Captions</h2>
  {caption_cards}

  <h2>Quote graphics (6)</h2>
  {graphic_cards}

  <p style="color:#666;font-size:13px;margin-top:32px">
    Don't approve? Just ignore this email -- the token expires when unused.
  </p>
</div>
</body></html>
"""


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# =============================================================================
# STAGE 5 -- publish to platforms (fan-out)
# =============================================================================

@app.function(image=image, secrets=[secret], timeout=1200)
def publish_all(content_pkg: dict, video_url: str) -> dict:
    results: dict[str, str] = {}

    if "wordpress" in PUBLISH_TARGETS:
        results["wordpress"] = _safe_post(
            "wordpress", post_wordpress, content_pkg["blog_post"], video_url
        )

    caption_map = {
        "instagram": "instagram",
        "facebook": "facebook",
        "linkedin": "linkedin",
    }
    for plat_key, plat_label in caption_map.items():
        if plat_key not in PUBLISH_TARGETS:
            continue
        caption = content_pkg["captions"][plat_label]
        suffix = HASHTAGS.get(plat_key, "")
        text = f"{caption}\n\n{suffix}".strip()
        fn = {
            "instagram": post_instagram_text,
            "facebook": post_facebook_text,
            "linkedin": post_linkedin_text,
        }[plat_key]
        results[f"{plat_key}_caption"] = _safe_post(plat_key, fn, text, video_url)

    for graphic in content_pkg["quote_graphics"]:
        plat = graphic["platform"]
        plat_key = plat.split("_")[0]
        if plat_key not in PUBLISH_TARGETS:
            continue
        suffix = HASHTAGS.get(plat_key, "")
        caption = f"{graphic['caption']}\n\n{suffix}".strip()
        fn = _GRAPHIC_POSTERS.get(plat)
        if not fn:
            results[f"{plat}_graphic"] = f"skip: no poster for {plat}"
            continue
        results[f"{plat}_graphic"] = _safe_post(
            plat, fn, graphic["image_b64"], caption
        )

    print(f"[publish_all] results: {results}")
    return results


def _safe_post(label: str, fn, *args) -> str:
    try:
        return fn(*args) or "ok"
    except _MissingCreds as e:
        print(f"[publish_all] skipping {label}: {e}")
        return f"skip: {e}"
    except Exception as e:  # noqa: BLE001
        print(f"[publish_all] error posting {label}: {e}")
        return f"error: {e}"


class _MissingCreds(Exception):
    pass


def _need(*names: str) -> tuple[str, ...]:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        raise _MissingCreds(f"missing env: {', '.join(missing)}")
    return tuple(os.environ[n] for n in names)


# --- WordPress ----------------------------------------------------------------

def post_wordpress(blog_post: dict, video_url: str) -> str:
    import requests

    base_url, user, app_pw = _need("WORDPRESS_URL", "WORDPRESS_USER", "WORDPRESS_APP_PASSWORD")
    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts"
    r = requests.post(
        endpoint,
        auth=(user, app_pw),
        json={
            "title": blog_post["title"],
            "content": blog_post["html"],
            "status": "publish",
        },
        timeout=60,
    )
    r.raise_for_status()
    return f"ok: {r.json().get('link', '')}"


# --- Twitter / X --------------------------------------------------------------

def post_twitter(text: str) -> str:
    import tweepy

    ck, cs, at, ats = _need(
        "TWITTER_API_KEY", "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
    )
    client = tweepy.Client(
        consumer_key=ck, consumer_secret=cs,
        access_token=at, access_token_secret=ats,
    )
    resp = client.create_tweet(text=text[:280])
    return f"ok: id={resp.data['id']}"


def post_twitter_image(image_b64: str, caption: str) -> str:
    import tempfile
    import tweepy

    ck, cs, at, ats = _need(
        "TWITTER_API_KEY", "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
    )
    auth = tweepy.OAuth1UserHandler(ck, cs, at, ats)
    api = tweepy.API(auth)
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs,
                           access_token=at, access_token_secret=ats)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(base64.b64decode(image_b64))
        path = tmp.name
    media = api.media_upload(path)
    resp = client.create_tweet(text=caption[:280], media_ids=[media.media_id])
    return f"ok: id={resp.data['id']}"


# --- LinkedIn -----------------------------------------------------------------

def post_linkedin_text(text: str, video_url: str = "") -> str:
    import requests

    token, urn = _need("LINKEDIN_ACCESS_TOKEN", "LINKEDIN_ACTOR_URN")
    body = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=60,
    )
    r.raise_for_status()
    return f"ok: id={r.headers.get('x-restli-id', '?')}"


def post_linkedin_image(image_b64: str, caption: str) -> str:
    # LinkedIn image post requires a 3-step register/upload/publish dance.
    # For MVP we post as text-only with a note; wire the full flow if the
    # client lives on LinkedIn.  See:
    # https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/images-api
    return post_linkedin_text(caption)


# --- Facebook Page ------------------------------------------------------------

def post_facebook_text(text: str, video_url: str = "") -> str:
    import requests

    token, page_id = _need("FB_PAGE_ACCESS_TOKEN", "FB_PAGE_ID")
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/feed",
        data={"message": text, "access_token": token},
        timeout=60,
    )
    r.raise_for_status()
    return f"ok: id={r.json().get('id')}"


def post_facebook_image(image_b64: str, caption: str) -> str:
    import requests

    token, page_id = _need("FB_PAGE_ACCESS_TOKEN", "FB_PAGE_ID")
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/photos",
        data={"caption": caption, "access_token": token},
        files={"source": ("graphic.png", base64.b64decode(image_b64), "image/png")},
        timeout=120,
    )
    r.raise_for_status()
    return f"ok: id={r.json().get('id')}"


# --- Instagram (Graph API, requires linked FB Business) -----------------------

def post_instagram_text(text: str, video_url: str = "") -> str:
    # IG Graph API only supports image/video posts -- no text-only feed posts.
    # For an MVP, the summarized text caption rides along with the IG quote
    # graphic.  This helper is a no-op stub so publish_all stays uniform.
    print("[instagram] caption-only post skipped (IG requires media)")
    return "skip: IG requires media (caption used in quote-graphic post)"


def post_instagram_image(image_b64: str, caption: str) -> str:
    import tempfile
    import requests

    token, ig_id = _need("IG_ACCESS_TOKEN", "IG_BUSINESS_ACCOUNT_ID")

    # IG Graph API requires a publicly fetchable image URL.  Easiest:
    # upload to imgbb / Cloudinary / Modal-served endpoint.  For the
    # template, we use imgbb (free tier, 32MB cap) if IMGBB_API_KEY is set;
    # otherwise we surface a clear error.
    imgbb_key = os.environ.get("IMGBB_API_KEY")
    if not imgbb_key:
        raise _MissingCreds(
            "IMGBB_API_KEY (or wire your own public-URL host)"
        )

    upload = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": imgbb_key, "image": image_b64},
        timeout=60,
    )
    upload.raise_for_status()
    image_url = upload.json()["data"]["url"]

    container = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        data={"image_url": image_url, "caption": caption, "access_token": token},
        timeout=60,
    )
    container.raise_for_status()
    creation_id = container.json()["id"]

    publish = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        data={"creation_id": creation_id, "access_token": token},
        timeout=60,
    )
    publish.raise_for_status()
    return f"ok: id={publish.json().get('id')}"


# --- Pinterest ----------------------------------------------------------------

def post_pinterest_image(image_b64: str, caption: str) -> str:
    import requests

    token, board_id = _need("PINTEREST_ACCESS_TOKEN", "PINTEREST_BOARD_ID")
    r = requests.post(
        "https://api.pinterest.com/v5/pins",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "board_id": board_id,
            "description": caption,
            "media_source": {
                "source_type": "image_base64",
                "content_type": "image/png",
                "data": image_b64,
            },
        },
        timeout=120,
    )
    r.raise_for_status()
    return f"ok: id={r.json().get('id')}"


_GRAPHIC_POSTERS = {
    "twitter": post_twitter_image,
    "facebook": post_facebook_image,
    "linkedin": post_linkedin_image,
    "instagram_feed": post_instagram_image,
    "instagram_reels": post_instagram_image,
    "pinterest": post_pinterest_image,
}


# =============================================================================
# ENTRY POINTS
# =============================================================================

@app.function(image=image, secrets=[secret], timeout=1800)
@modal.fastapi_endpoint(method="POST")
def webhook(payload: dict):
    youtube_url = payload.get("youtube_url")
    if not youtube_url:
        return {"error": "missing youtube_url in payload"}

    transcript = pull_transcript.remote(youtube_url)
    content = generate_content.remote(transcript)
    content["quote_graphics"] = render_quote_graphics.remote(content["quote_graphics"])
    token = send_approval_email.remote(content, youtube_url)
    return {"status": "drafts emailed", "token": token}


@app.function(image=image, secrets=[secret])
@modal.fastapi_endpoint(method="GET")
def approve(token: str = ""):
    if not token or token not in pending:
        return _html_response("Invalid or expired token.", status=404)
    pkg = pending[token]
    publish_all.spawn(pkg["content"], pkg["video_url"])
    del pending[token]
    return _html_response("Approved -- publishing now. Check Modal logs in ~2 min.")


def _html_response(body: str, status: int = 200):
    from fastapi.responses import HTMLResponse
    return HTMLResponse(
        content=f"<html><body style='font-family:system-ui;padding:48px'>"
                f"<h2>{body}</h2></body></html>",
        status_code=status,
    )


@app.function(image=image, secrets=[secret], schedule=modal.Cron("0 9 * * 1"))
def weekly_batch():
    """Optional batch entry: read queued YouTube URLs from a source and
    process each.  Wire the source per client (Google Sheet, Notion DB,
    Airtable).  Left as a stub because the source schema is client-specific."""
    urls = _read_pending_urls()
    print(f"[weekly_batch] dispatching {len(urls)} url(s)")
    for url in urls:
        webhook.spawn({"youtube_url": url})


def _read_pending_urls() -> list[str]:
    # TODO per client: implement against the client's content-ideas source.
    # Common options:
    #   - Google Sheet: gspread + service-account JSON in the Modal Secret
    #   - Notion DB:    notion-client + integration token
    #   - Airtable:     pyairtable + API key
    # Return a list of YouTube URLs to process this week.
    return []


# =============================================================================
# LOCAL DEV ENTRY (modal run client-template.py)
# =============================================================================

@app.local_entrypoint()
def main(youtube_url: str = ""):
    """Smoke test: modal run client-template.py --youtube-url=<url>"""
    if not youtube_url:
        print("usage: modal run client-template.py --youtube-url=<url>")
        return
    transcript = pull_transcript.remote(youtube_url)
    print(f"[local] transcript: {len(transcript['transcript'])} chars")
    content = generate_content.remote(transcript)
    print(f"[local] generated: {list(content.keys())}")
    content["quote_graphics"] = render_quote_graphics.remote(content["quote_graphics"])
    print(f"[local] rendered {len(content['quote_graphics'])} graphics")
    token = send_approval_email.remote(content, youtube_url)
    print(f"[local] approval email sent, token={token}")
