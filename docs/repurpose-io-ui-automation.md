# Repurpose.io UI Automation Playbook

How to programmatically drive the Repurpose.io dashboard via Playwright. Captured from the first successful end-to-end build of the "Google Drive Video → Facebook Page (Full)" workflow (ID 805679) on the testing account.

## TL;DR

- The Repurpose.io app is an **Angular 1.x SPA** at `my.repurpose.io` (not `app.repurpose.io`).
- Drive it via the `browser` skill (Playwright) with JSON action arrays.
- Most things click fine with `.click()`. **Menu items inside dropdowns** and **modal Save/Delete buttons** need `dispatchEvent(new MouseEvent('click', ...))` because Repurpose.io uses jQuery-delegated handlers.
- `<select>` value changes need `dispatchEvent('change')` + `dispatchEvent('input')` + `angular.element(el).scope().$apply()` for Angular to register the change.
- Each Python invocation = fresh browser session. State doesn't persist across runs. Drive the **entire wizard in one run**.

---

## URL endpoints

| Path | Purpose |
|------|---------|
| `https://my.repurpose.io/` | Workflows list (home) |
| `https://my.repurpose.io/createWorkflow` | New workflow wizard |
| `https://my.repurpose.io/editWorkflow/<id>` | Edit existing workflow (source/dest only — schedule edited elsewhere) |
| `https://my.repurpose.io/viewEpisodes/<id>` | Workflow's post history |
| `https://my.repurpose.io/connection` | Connections page (one per platform; not "social_profiles") |
| `https://my.repurpose.io/myAccount` | Plan / billing |
| `https://my.repurpose.io/createClips` | Clip generator |
| `https://my.repurpose.io/createBackups` | Backup workflows |
| `https://my.repurpose.io/publish-calendar` | Calendar view |
| `https://my.repurpose.io/custom-templates` | Caption templates |
| `https://my.repurpose.io/login` | Login (Google OAuth, FB, YouTube, Amazon, or email/password) |

**Bad guesses to avoid:** `app.repurpose.io` (doesn't resolve), `/workflows` (404), `/dashboard` (404), `/social_profiles` (404).

---

## Auth & profile

- Playwright uses persistent profile at `~/.meta-playwright-profile/`.
- This profile is **separate from your normal browser** — logging in to Repurpose.io in Chrome/Edge does NOT log in the Playwright profile.
- One-time login required: navigate to `/login`, sign in (Google works); session persists across future runs.
- Norton MITM cert already trusted globally (see `~/.claude/CLAUDE.md` Windows Environment Quirks) — no TLS errors.

---

## The wizard flow (Pattern B — "Repurpose Existing Content")

This is the only proven flow so far. For Pattern A (YouTube long-form auto-trigger), the mode card is different and there's likely no schedule modal.

### Step-by-step

1. **Goto** `/createWorkflow`. Wait 6–7s for Angular to fully render.
2. **Click mode card** "Repurpose Existing Content (On a Schedule)" — default is the *other* mode.
3. **Click source tile** (e.g., Google Drive) in the "Post from" grid.
4. **Account picker modal opens** — click the desired account (e.g., `@Lil Tommy`).
5. **Click destination tile** (e.g., Facebook) in the "Post to" grid.
6. **Account picker modal opens** — click the desired account (e.g., `@Tommy Lee`).
7. **Adjust the destination Type select** if needed. Defaults vary per platform.
8. **Click "Continue"** (pink button at the bottom; activates once both sides are chosen).
9. **Schedule modal opens** ("Choose What to Publish and When"). Click "Enable Automation" to persist + activate, or "Not Right Now" to save as inactive draft.
10. Wizard returns to workflows list. New workflow appears at the top.

### ⚠️ The Continue → draft trap

If you click **Continue** and then **don't click "Enable Automation"** on the schedule modal, Repurpose.io **still persists the workflow** as an inactive draft. Closing the browser or navigating away creates an orphan duplicate. Always either click "Enable Automation" or "Not Right Now" — don't abandon the modal mid-stream.

This trap cost me a duplicate workflow (805678) during the first build. Cleanup required a separate delete pass.

---

## Selectors that worked

### Mode card
```js
const els = Array.from(document.querySelectorAll('div, label, button, a'))
  .filter(el => /Repurpose Existing Content/.test(el.textContent) && /On a Schedule/.test(el.textContent))
  .sort((a, b) => a.textContent.length - b.textContent.length);
els[0].click();  // smallest enclosing match
```

**Gotcha:** sorting by `textContent.length` ASC and taking `[0]` is essential — without it, you'll click the outer `<html>` element (which technically "contains" the text but isn't the card).

### Source / destination platform tile
```js
// For source — note the !Post-to exclusion
const sections = Array.from(document.querySelectorAll('div, section, fieldset'))
  .filter(el => {
    const t = el.textContent;
    return /Post from/.test(t) && /Google Drive/.test(t) && !/Post to/.test(t);
  })
  .sort((a, b) => a.textContent.length - b.textContent.length);
const tile = Array.from(sections[0].querySelectorAll('div, button, a'))
  .filter(el => el.textContent.trim() === 'Google Drive')
  .sort((a, b) => a.textContent.length - b.textContent.length)[0];
// Walk up to clickable parent
let target = tile;
while (target.parentElement && target.parentElement.textContent.trim() === target.textContent.trim()) {
  target = target.parentElement;
}
target.click();
```

**Gotcha:** "Facebook" appears in **both** the source AND destination grids — without section-based disambiguation, you'll click the wrong one. Same for Instagram, YouTube, Twitch.

### Account picker modal (after clicking source/destination tile)
```js
const acct = Array.from(document.querySelectorAll('.connect-box'))
  .find(el => /Tommy Lee/.test(el.textContent) && !/Thomas/.test(el.textContent));
acct.click();
```

`.connect-box` is the canonical class for account rows. Note the `&& !/Thomas/` because the account list often has multiple similarly-named entries (`@Tommy Lee` vs `@Thomas Lee`).

### Destination Type select (Reels vs Video vs Stories vs Photos for Facebook)
```js
const selects = document.querySelectorAll('select[name="videoType"]');
for (const s of selects) {
  // Disambiguate: the FB destination select has REELS as an option
  if (Array.from(s.options).some(o => o.value === 'string:REELS')) {
    s.value = 'string:FEED';  // FEED = "Video" (regular video on FB page)
    ['change', 'input'].forEach(e => s.dispatchEvent(new Event(e, {bubbles: true})));
    if (window.angular) {
      try { angular.element(s).scope().$apply(); } catch(e) {}
    }
    break;
  }
}
```

**Gotcha:** there are **two `<select name="videoType">` elements on the page** — same name, same id (`videoType`). Disambiguate by inspecting `.options[]`:
- First select: Media Type (source). Options: `string:0` (Audio), `string:1` (Video), `string:2` (Images).
- Second select: destination format. Options vary per platform (see table below).

### Continue button
```js
const btn = Array.from(document.querySelectorAll('button, a'))
  .filter(b => !b.disabled && b.offsetParent !== null)
  .find(b => /^Continue$/i.test((b.textContent || '').trim()));
btn.click();
```

`offsetParent !== null` filters out hidden buttons (Repurpose.io has many hidden modals in the DOM).

### Enable Automation button (on the schedule modal)
```js
const btn = Array.from(document.querySelectorAll('button'))
  .filter(b => !b.disabled && b.offsetParent !== null)
  .find(b => /Enable Automation/i.test(b.textContent));
btn.click();
```

### 3-dot kebab menu on a workflow card
```js
const editLink = document.querySelector('a[href*="editWorkflow/805679"]');
let card = editLink;
while (card && !card.classList?.contains('view_setting_option_wrapper')) card = card.parentElement;
card.querySelector('a.dropdown-toggle').click();
```

The card-level container has class `view_setting_option_wrapper`. The kebab trigger inside is `a.btn.btn-default.dropdown-toggle`.

### Menu items inside the open kebab dropdown
```js
const a = Array.from(card.querySelectorAll('.dropdown-menu a'))
  .find(el => /^Delete$/i.test((el.textContent || '').trim()));
a.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
```

**Gotcha — critical:** plain `.click()` on `.dropdown-menu a` does NOT fire the action. The Delete anchor has `href="javascript:void(0)"` and the click handler is jQuery-delegated to class `.press_del_btn`. You **must** `dispatchEvent(new MouseEvent('click', ...))` for the delegated handler to run. Same goes for Rename (`.press_rename_btn` or similar) and likely other menu items.

### Confirm modal buttons (Delete, Save in Rename modal, etc.)
```js
const modal = Array.from(document.querySelectorAll('.modal-dialog'))
  .filter(m => m.offsetParent !== null)
  .find(m => /Delete Workflow/.test(m.textContent));
const btn = Array.from(modal.querySelectorAll('button, a'))
  .filter(el => el.offsetParent !== null)
  .find(el => /^Delete$/i.test((el.textContent || '').trim()));
btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
```

Always **scope the search to the visible modal first** to avoid matching the menu's "Delete" item that's still in DOM.

### Rename modal text input
```js
const modal = Array.from(document.querySelectorAll('.modal-dialog'))
  .filter(m => m.offsetParent !== null)
  .find(m => /Rename|Name this Workflow/i.test(m.textContent));
const input = modal.querySelector('input[type="text"]');
input.focus();
input.value = 'Google Drive Video to Facebook Page (Full)';
['input', 'change', 'keyup'].forEach(e => input.dispatchEvent(new Event(e, {bubbles: true})));
if (window.angular) {
  try { angular.element(input).scope().$apply(); } catch(e) {}
}
// Then click Save in the same modal
```

---

## Reference data captured from the testing account

### Connections present (12 total, all green)

| Platform | Handle | Token expires |
|----------|--------|---------------|
| Facebook | @Thomas Lee | 88d |
| Facebook2 | @Tommy Lee | 88d |
| Google Drive | @Lil Tommy | — |
| Instagram | @bmbaiautomations | 60d |
| Instagram2 | @aibiblegospels | 58d |
| LinkedIn | @Tommy Lee | 58d |
| Pinterest | @bmbaiautomation | 28d |
| TikTok | @bmbaiautomations | — |
| TikTok2 | @aibiblegospels_ | — |
| Twitter | @tommy_lee5422 | — |
| Twitter2 | @aibiblegospels | — |
| YouTube | @tommylee-z3j | — |

### Destination Type select values (per platform)

| Platform | Type options |
|----------|--------------|
| Facebook | `string:REELS` (Reels), `string:FEED` (Video), `string:STORIES` (Stories), `string:IMAGE` (Photos/carousels) |
| Instagram | (Likely similar — REELS / FEED / STORIES / IMAGE — confirm before use) |
| Others | TBD — inspect via `document.querySelectorAll('select[name="videoType"]')` after picking the destination |

### Facebook Page IDs (the `playlistItem` select for FB destination)

| Page name | playlistItem value |
|-----------|---------------------|
| AI Bible Gospels | `string:601690023018873` |
| Robert Brown Elliott Associations | `string:109349685302451` |
| Born Made Bosses Solutions LLC | `string:1273418259441218` |
| 21 Day Challenge | `string:104703478451566` |
| For Our Culture | `string:102685945410122` |
| Robert Brown Elliott Gun Club | `string:771619716276007` |
| Weareisrael | `string:103012108141653` |
| BCD & Born Made Bosses | `string:1941176385959767` |

### Plan tiers (as of 2026-05-25)

| Plan | Price | Accounts per network | Use case |
|------|-------|----------------------|----------|
| Starter | $35/mo | 3 | Solo client |
| Pro | $79/mo | 10 | Client w/ multiple brand accounts |
| Agency | $179/mo | 25 | Multi-client agency mode |

Older docs mention "Marketer $49" — that plan no longer exists. Don't quote it to clients.

---

## Schedule modal defaults (Pattern B "Existing Content" mode)

When the schedule modal opens after Continue:

- "Which posts to include": `All posts` (default)
- "Publishing order": `Newest first` (default)
- "Posts per day": `5` (default)
- Time slots: 9am, 11am, 1pm, 3pm, 5pm (every 2 hours)
- Days enabled: Monday + Tuesday by default
- Time slot selects are native `<select>` with values like `"09:00"`, `"11:00"`, etc.

If you accept defaults and click **Enable Automation**, Repurpose.io will scan the source folder, queue all matching files, and start publishing 5/day on Mon/Tue. The first time I enabled this for the FB Page workflow, it queued **25 existing files** from the watched GDrive folder.

---

## Batch-building the remaining workflows

These are the missing workflows from `../content-tree.md` for the Pattern B 2-stage flow on the testing account. The first one (`Google Drive → FB Page Full`) is built and named "Google Drive Video to Facebook Page (Full)" — workflow 805679.

### Branch 1 (Video) — 4 more to build

| # | Source | Destination | Destination Type select value | Notes |
|---|--------|-------------|-------------------------------|-------|
| 2 | Google Drive | Facebook Group | (TBD — confirm select options) | Different from FB Page; needs FB Group connection (admin) |
| 3 | Google Drive | Instagram Stories | `string:STORIES` (likely) | Instagram destination |
| 4 | Google Drive | Instagram Feed | `string:FEED` (likely) | Instagram destination |
| 5 | Google Drive | Google Drive backup | n/a | "Drive → Drive" workflow; different output folder |

### Branch 3 (Audio) — 11 to build

For the audio branch, the source media type needs to be set to **audio** (`string:0`) in the first videoType select. Then each workflow targets a different destination:

| # | Output | Destination | Notes |
|---|--------|-------------|-------|
| 1 | Podcast episode | Spotify+Apple (via RSS) | Requires podcast RSS host (Buzzsprout/Anchor/Captivate) — external setup |
| 2 | Audio backup | Google Drive (different folder) | |
| 3 | Alexa flash briefing | Amazon Alexa | Requires Amazon Developer connection |
| 4–11 | Vertical audiograms | IG Reels/Stories, IG Feed, TikTok, LinkedIn, Twitter, FB Page, YouTube Shorts, Pinterest | 8 audiogram workflows |

### Suggested batch script approach

Parameterize the wizard JSON with placeholders:

```python
WORKFLOW_SPECS = [
    {"source": "Google Drive", "source_acct": "Lil Tommy", "dest": "Facebook", "dest_acct": "Tommy Lee", "type_value": "string:FEED", "name": "Google Drive Video to Facebook Page (Full)"},
    {"source": "Google Drive", "source_acct": "Lil Tommy", "dest": "Facebook", "dest_acct": "Tommy Lee", "type_value": "<FB Group value>", "name": "Google Drive Video to Facebook Group"},
    {"source": "Google Drive", "source_acct": "Lil Tommy", "dest": "Instagram", "dest_acct": "<acct>", "type_value": "string:STORIES", "name": "Google Drive Video to Instagram Stories"},
    # ...
]
```

Then loop: render `build-workflow.json` for each spec, run pilot, screenshot, verify. The wizard takes ~80s per workflow end-to-end. 15 workflows = ~20 minutes.

**Before batching:** prove ONE more workflow with a DIFFERENT destination (e.g., FB Group or IG Stories) to validate the script generalizes beyond the FB Page case. The Instagram-side dropdown options may differ from Facebook's.

---

## Pitfalls log

Things that went wrong on the way to 805679 — keep handy for the next build:

1. **`app.repurpose.io` doesn't exist.** It's `my.repurpose.io`.
2. **First "click mode card" attempt hit `<html>`.** Selector matched outermost text-containing element. Fix: sort by textContent.length ASC, take `[0]`.
3. **Source/destination platform names overlap.** "Facebook" exists in both grids — use section-based exclusion (`!Post-to` in the source section selector).
4. **`@Lil Tommy` clicked the modal-body.** First attempt walked up the parent chain too aggressively. Fix: target `.connect-box` class directly, no parent walking.
5. **`<select>` value changes didn't update the UI** until `dispatchEvent('change')` + `dispatchEvent('input')` + `angular.element(s).scope().$apply()` were all called.
6. **`.click()` on Delete menu item did nothing.** jQuery-delegated handlers don't fire on programmatic `.click()`. Fix: `dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))`.
7. **Continue without Enable Automation creates a draft duplicate.** Don't abandon the schedule modal mid-flow.
8. **Workflow names auto-suffix "(existing)" in Pattern B mode.** Rename to remove the suffix if the doc spec is the target name.
9. **Each Python run = fresh browser.** Wizard state isn't preserved. Drive the full wizard in one JSON action array.
10. **Take screenshots between every key transition.** When something fails silently, the screenshot tells you what state you're actually in.
11. **The dashboard pops announcement modals periodically.** Dismiss with `.close` button find, or just navigate past — the modals don't block the URL navigation.
12. **For destructive operations (Delete) — always do a separate diagnostic run first** to inspect the confirm modal's exact button text and structure. The labels look obvious but real DOM may not match expectations.

---

## See also

- `../repurpose-io-setup.md` — the human-facing client setup guide
- `../setup-sop.md` Phase 2 — choice of Pattern A vs Pattern B
- `../content-tree.md` — the 33-piece target distribution
- `~/.claude/skills/browser/` — the Playwright pilot script and JSON action reference
