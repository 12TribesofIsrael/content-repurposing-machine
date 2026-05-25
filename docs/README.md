# docs/

Setup notes, client-specific configuration, troubleshooting logs, and any reference material that isn't already covered by the root-level guides (`setup-sop.md`, `repurpose-io-setup.md`, `content-tree.md`).

## What lives here

- `repurpose-io-ui-automation.md` — playbook for driving the Repurpose.io dashboard with Playwright (selectors, gotchas, batch-build strategy for remaining workflows)
- Client-specific brand voice / system-prompt overrides for the text layer
- Per-client source-pattern decision (Pattern A or B from `setup-sop.md` Phase 2)
- Platform API gotchas discovered during real setups
- Token rotation logs (Instagram/Facebook expire every 60–90 days; Pinterest every 30)
- Screenshots and walkthroughs that supplement the root SOPs

## What does NOT live here

- The canonical setup SOP — that stays at the root (`setup-sop.md`)
- The text-layer code or its architecture spec — that lives at `text-layer/`
- Anything client-confidential that shouldn't be committed to git
