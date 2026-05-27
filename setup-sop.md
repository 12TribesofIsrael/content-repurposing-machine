# Content Repurposing — Client Setup SOP

**Time to complete:** 3–5 hours (Repurpose.io: ~2h, text layer: ~2h for Enterprise clients) | **Difficulty:** Medium

---

## Phase 1: What You Need from the Client

1. **Primary content type** — Long-form YouTube videos? Short Instagram Reels? Both? (determines source pattern in Phase 2)
2. **Platform list** — Which destinations do they want? (use `content-tree.md` to guide)
3. **Logins** — Access to all destination platform accounts (or admin invites)
4. **Brand voice** — 3 examples of captions they like, any hashtags they use regularly
5. **Posting preferences** — Immediate publish or staggered (e.g., delay LinkedIn by 2 hours)?
6. **WordPress / blog URL** — Required if Branch 2 (blog post) is in scope (Enterprise tier)
7. **Anthropic or OpenAI API key** — Required if Branch 2 is in scope
8. **Podcast RSS feed** — Required if Branch 3 (audio) is in scope (Full Stack tier and up). Buzzsprout/Anchor/Captivate are the common hosts.
9. **Approval email** — Where should drafts from the text layer go before publishing? (or set "auto-publish" if client trusts the system)

---

## Phase 2: Choose the Source Pattern

There are two proven patterns. Pick one based on the client's actual content workflow:

### Pattern A: YouTube long-form (the PDF's canonical flow)
- **Source:** Client uploads to YouTube as their first stop
- **How:** Repurpose.io watches the YouTube channel, pulls each new upload, auto-clips into 60s verticals, extracts audio
- **Best for:** Podcasters, course creators, B2B consultants — anyone already publishing long-form video

### Pattern B: Google Drive → Instagram Reels → downstream (two-stage)
- **Stage 1:** Client drops the video file in a Google Drive folder. Repurpose.io watches the folder and auto-publishes to Instagram Reels (and Facebook Reels, TikTok, Twitter)
- **Stage 2:** The newly-posted IG Reel becomes the source for a second batch of workflows that fan it out to YouTube Shorts, Pinterest, LinkedIn, etc.
- **Best for:** Clients who film short-form first (TikTok-natives) and don't have a YouTube long-form habit

Document the choice in `docs/<client-name>.md` so the handoff matches the build.

---

## Phase 3: Repurpose.io Setup (~2 hours)

### 3.1 Account Setup
1. Create account at repurpose.io (or have client create + share login)
2. Pick a plan: **Starter ($35/mo)** for solo clients (3 accounts/network), **Pro ($79/mo)** for clients needing 10+ accounts/network
3. Set timezone to the client's local timezone

### 3.2 Connect Social Profiles (Connections → + Add New Connection)

Work through each platform. Common friction points:
- **Instagram** requires a connected Facebook Business Manager — if the client's IG is personal, convert to a Business account first (free, 5 minutes in the IG app: Settings → Account → Switch to Professional)
- **LinkedIn Company Page** requires the client to add you as a Page admin (or do it together on a call)
- **Pinterest** requires a Business account
- **YouTube** requires connecting via Google account — ensure it's the correct channel

### 3.3 Build the Workflows

For **Pattern A (YouTube source)**, follow `repurpose-io-setup.md` Step 4 to build all 22 workflows (11 video + 11 audio) off the YouTube source.

For **Pattern B (Google Drive → IG Reels)**, build the two-stage flow:
- **Stage 1 (3–4 workflows):** Google Drive Video → Instagram Reels, Facebook Reels, TikTok, Twitter
- **Stage 2 (5+ workflows):** Instagram Reels → YouTube Shorts, Pinterest, LinkedIn, Twitter, etc.

For each workflow:
1. Select source platform
2. Select destination platform
3. Set caption template: `{{original_caption}} [HASHTAGS]`
4. Schedule: Immediate OR delay (set delay in hours)
5. Toggle ON → Save

### 3.4 Test

Post one short test video to the source. Wait 10 minutes. Check all destinations in Repurpose.io's Workflows view. All should show "Published Successfully" with a publish count.

---

## Phase 4: Text Layer Setup (~2 hours, Enterprise tier only)

This phase covers the 10 Branch-2 pieces (blog post + 3 summarized text posts + 6 quote graphics). It's a per-client Python script deployed to Modal. See `text-layer/README.md` for the architecture.

### 4.1 Provision API Credentials

| Credential | Where to get it |
|------------|-----------------|
| Anthropic API key (Claude) | console.anthropic.com → API Keys |
| OR OpenAI API key | platform.openai.com → API Keys |
| WordPress application password | WP-Admin → Users → Application Passwords |
| Canva API key (graphics) | canva.com/developers (or Bannerbear / Placid) |
| Posting credentials | Per-platform — usually the same OAuth tokens used in Repurpose.io, or a scheduler API key (Buffer/Metricool) |

### 4.2 Deploy the Script

1. From `text-layer/`, copy the template to a per-client file: `text-layer/client-<name>.py`
2. Fill in the brand-voice prompt, hashtag list, and target posting platforms
3. Deploy to Modal: `modal deploy text-layer/client-<name>.py`
4. Modal returns a webhook URL — save it for the trigger setup in 4.3

### 4.3 Set the Trigger

- **Option A (manual):** Client pastes the YouTube URL into a Google Form → Form submission calls the Modal webhook → script generates content
- **Option B (scheduled):** A Modal scheduled function runs (e.g., Monday 9am) → pulls from a content-ideas Google Sheet → batch-generates a week's worth

### 4.4 Configure the Approval Email

- Default: drafts emailed to the client before publishing. Client replies "approve" → script publishes.
- Auto-publish: skip the approval step. Faster, but no human review.

### 4.5 Test

1. Manually trigger the script with a real YouTube URL
2. Verify the approval email arrives with all 10 pieces (blog draft + 3 captions + 6 quote-graphic copy)
3. Approve and verify each piece publishes to its target platform
4. Check Modal logs for any errors

---

## Phase 5: Testing Checklist

**Repurpose.io (Branches 1 + 3):**
- [ ] Source upload → all destination workflows trigger within 15 min
- [ ] Each platform — video looks correct (no black bars, caption is correct)
- [ ] Watermarks removed (e.g., TikTok → YouTube Shorts)
- [ ] Hashtags appended correctly per platform
- [ ] Audio extracted + audiograms generated (Full Stack and Enterprise tiers)
- [ ] Podcast episode appears on Spotify/Apple within 24h of RSS publish

**Text Layer (Branch 2, Enterprise tier only):**
- [ ] Modal webhook fires when triggered (Form submit or scheduled)
- [ ] Claude/OpenAI generates content for all configured platforms
- [ ] Quote graphics render correctly (check Canva/Bannerbear outputs)
- [ ] Approval email arrives in client's inbox
- [ ] After approval, content publishes to platforms
- [ ] Modal logs show no errors

---

## Phase 6: Handoff to Client

**5-minute Loom recording outline:**
1. "Here's your Repurpose.io dashboard — every time you upload to [YouTube / Google Drive], the system fans out automatically."
2. Show the Workflows view — "this is how you confirm every post went out."
3. (Enterprise) Show the approval email from the text layer — "you'll get this for every video; reply to approve."
4. "The only thing you do: keep producing your source content. We handle everything else."

---

## Phase 7: Monthly Maintenance

1. Repurpose.io → Workflows → check for any Failed or Inactive workflows
2. Connections page → re-authenticate any expiring connections (Instagram/Facebook tokens expire every 60–90 days; Pinterest every 30)
3. (Enterprise) Modal logs → check for errors in the text layer
4. (Enterprise) Anthropic/OpenAI billing dashboard → flag if usage exceeds budget
5. Review the client's recent posts — flag any caption/hashtag template tweaks or prompt changes
6. Ask client: "Any new platforms? Any content types you want to add?"
