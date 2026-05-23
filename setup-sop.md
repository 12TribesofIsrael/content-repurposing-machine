# Content Repurposing — Client Setup SOP

**Time to complete:** 2–4 hours | **Difficulty:** Medium (no code, but many platform connections)

---

## Phase 1: What You Need from the Client

1. **Primary content platform** — Where do they post first? (TikTok, Instagram, YouTube)
2. **Platform list** — Which platforms do they want content on? (use content-tree.md to guide)
3. **Logins** — Access to all destination platform accounts (or admin invites you as a manager)
4. **Brand voice** — 3 examples of captions they like, any hashtags they use regularly
5. **Posting preferences** — Immediate publish or staggered (e.g., delay LinkedIn by 2 hours)?
6. **Blog site** — Do they have WordPress? (for blog post output)
7. **OpenAI API key** — For the n8n text generation layer
8. **Email** — Where should approval emails for AI content go before it posts?

---

## Phase 2: Repurpose.io Setup (~1.5 hours)

### 2.1 Account Setup
1. Create account at repurpose.io (or have client create + share login)
2. Upgrade to Marketer plan ($49/mo)
3. Set timezone

### 2.2 Connect All Social Profiles (Settings → Social Profiles)

Work through each platform in order. Common friction points:
- **Instagram** requires a connected Facebook Business Manager — if client's IG is personal, you'll need to convert to Business account first (free, takes 5 minutes in IG app: Settings → Account → Switch to Professional)
- **LinkedIn Company Page** requires the client to add you as a Page admin (or do it together on a call)
- **Pinterest** requires a Business account
- **YouTube** requires connecting via Google account — ensure it's the correct channel

### 2.3 Build All Workflows (Repurpose.io Workflows → + New)

Follow the workflow table in `content-tree.md`. Build one workflow per destination.

For each workflow:
1. Select source platform (e.g., TikTok)
2. Select destination platform
3. Set caption template: `{{original_caption}} [HASHTAGS]`
4. Schedule: Immediate OR delay (set delay in hours)
5. Toggle ON → Save

### 2.4 Test

Post one short test video on the source platform. Wait 10 minutes. Check all destinations in Repurpose.io Activity Log. All should show "Published Successfully."

---

## Phase 3: n8n Social Media Posting Machine Setup (~1 hour)

This layer handles AI-generated text content (blog posts, captions, LinkedIn articles).

### 3.1 Import the Workflow

1. Open n8n (cloud at app.n8n.io or self-hosted)
2. **+ New Workflow** → **Import from File**
3. Upload `workflow-social-posting.json`
4. Workflow name: `[ClientName] — Content Repurposing Text Layer`

### 3.2 Configure Credentials

In n8n → **Credentials** → Add:

| Credential | Where to get it |
|------------|-----------------|
| OpenAI API Key | platform.openai.com → API Keys |
| Gmail OAuth | n8n Google credentials → follow OAuth setup |
| LinkedIn OAuth | n8n LinkedIn credentials → OAuth flow |
| Facebook/Instagram | Facebook Graph API → Meta Developer App |
| Twitter/X OAuth | developer.twitter.com |

### 3.3 Customize the System Prompt Node

Find the node labeled **"Social Media Manager"** or **"Content Generator"** → edit the system prompt:

```
You are a social media content specialist for [CLIENT BUSINESS NAME].

Business type: [TYPE — e.g., "business coach", "credit repair agency"]
Target audience: [AUDIENCE — e.g., "entrepreneurs aged 30-50 who want to scale"]
Brand voice: [VOICE — e.g., "direct, motivational, no fluff, uses real examples"]
Signature phrases or CTAs: [e.g., "DM me 'READY' to get started"]

When generating content:
- Twitter/X: Max 240 chars. Hook first. No hashtags unless they're brand-specific.
- LinkedIn: Professional insight angle. 150-300 words. 3-5 relevant hashtags.
- Instagram: Conversational, emoji-friendly. 100-150 words. 20-30 relevant hashtags.
- Facebook: Conversational, question-based to drive comments. 80-150 words.
- Blog: 500-800 words. SEO-friendly. Include the key message as H2 headers.
```

### 3.4 Configure the Approval Email Node

1. Find the **"Send Approval Email"** node
2. Set recipient: client's email address
3. Set subject: `[Review Needed] New AI Content — {{$now.toFormat('YYYY-MM-DD')}}`
4. The email includes all platform drafts as text — client replies "approve" or requests edits

### 3.5 Set the Trigger

**Option A (manual trigger):** Client pastes their content idea into a Google Form → n8n reads it via Google Sheets trigger → generates content
**Option B (weekly batch):** Set n8n Schedule Trigger → every Monday 9am → pulls from a content ideas list in Google Sheets → generates a week's worth of content

Set up whichever fits the client's workflow. Most clients prefer Option A to start.

### 3.6 Test

1. Add one row to the content ideas Google Sheet (a test topic)
2. Manually trigger the workflow
3. Verify the approval email arrives with content drafts
4. "Approve" it and verify posts go live on connected platforms

---

## Phase 4: Testing Checklist

**Repurpose.io:**
- [ ] Post test video on source → all destination workflows trigger within 15 min
- [ ] Check each platform — video looks correct (no black bars, caption is correct)
- [ ] TikTok watermark removed on YouTube Shorts (Repurpose.io does this automatically)
- [ ] Hashtags appended correctly on each platform

**n8n Text Layer:**
- [ ] Trigger fires correctly (form submit or schedule)
- [ ] AI generates content for all configured platforms
- [ ] Approval email arrives in client's inbox
- [ ] After approval, content posts to platforms
- [ ] Workflow execution log shows no errors

---

## Phase 5: Handoff to Client

**5-minute Loom recording outline:**
1. "Here's your Repurpose.io dashboard — every time you post a TikTok, it goes here automatically"
2. Show Activity Log — "this is how you can see every post that went out"
3. Show the n8n approval email they'll receive — "you'll get this every [frequency], just hit reply to approve"
4. "The only thing you do: keep posting your main content. We handle everything else."

---

## Phase 6: Monthly Maintenance

1. Repurpose.io → Activity Log → check for any "Failed" workflows
2. If any social platform connection expired → re-authenticate (common: every 60-90 days for Instagram/Facebook)
3. n8n → Executions → check for errors
4. Review client's new content and update system prompt if brand voice evolves
5. Check OpenAI usage costs — flag if over $10/mo (usually well under)
6. Ask client: "Any new platforms? Any content types you want to add?"
