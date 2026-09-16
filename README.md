# AI Lead Qualification — n8n

An end-to-end n8n automation that classifies inbound sales leads with an AI model, records the result in Google Sheets, conditionally routes high-priority leads, and creates a Gmail follow-up draft.

## Status

**Core demo workflow: live-verified end to end.**

The successful path was executed in n8n after import and credential reconnection:

`Manual Trigger → Sample Lead → AI Classification → Google Sheets → High-Priority Check → Gmail Draft`

A screenshot from that successful execution is included at `docs/screenshots/live-success.png`.

## What the workflow demonstrates

- n8n workflow orchestration
- structured AI output with a strict JSON schema
- High / Medium / Low lead classification
- data mapping across nodes
- Google Sheets append operations
- conditional routing
- Gmail draft creation
- debugging of imported workflow configuration and expressions

## Workflow

Import:

`workflows/lead-qualification-demo.json`

After import, reconnect:
1. the n8n AI Gateway / OpenAI credential,
2. Google Sheets,
3. Gmail.

Then select:
- Google Sheet document: **n8n Lead Qualification Demo**
- Sheet/tab: **Qualified Leads**

Required sheet columns:

`Name | Email | Company | Budget | Priority | Reason | Recommended Action`

The public workflow intentionally does not contain private credential IDs or the Google Sheet document ID.

## Sample lead

The demo uses:

- John Smith
- john@example.com
- Smith Roofing
- $5,000 budget
- AI sales automation
- Wants to automate lead follow-up and schedule a call this week

## Structured model output

The model is constrained to return:

- `priority`: `High`, `Medium`, or `Low`
- `reason`
- `recommended_action`

Only a `High` priority result follows the Gmail-draft branch.

## Verification

Run:

```bash
python scripts/validate_workflow.py
```

This performs static checks on the public export. Live external execution was separately completed in n8n; see `docs/verification.md`.

## Scope

This repository intentionally focuses on the verified core automation. A Form.io intake path was prototyped separately but is not required for this project's completed core demo.
