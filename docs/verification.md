# Verification Record

## Live execution

The core demo path was executed successfully in n8n after the cleaned workflow was imported and the required external credentials were reconnected.

Verified path:

`When clicking Execute workflow → Sample Lead → Message a model1 → Append row in sheet1 → If High Priority → Create a draft1`

Observed in the successful run:
- the manual trigger produced one item;
- the sample lead passed into the model;
- the model node completed successfully;
- Google Sheets appended one item;
- the `High` branch evaluated true;
- Gmail created one draft.

The public repository records the verified execution outcome without publishing account UI or credential-linked screenshots.

## Public-export sanitation

The repository copy removes:
- Google OAuth credential IDs;
- Gmail credential IDs;
- the Google Sheet document ID and URLs;
- webhook IDs;
- n8n instance metadata.

Those values must be reconnected by anyone importing the public workflow.

## Static validation

The included validator checks:
- valid JSON;
- all connection targets exist;
- expressions reference nodes present in the workflow;
- the lead-classification JSON schema exists and requires all three fields;
- the High-priority route reads the structured `priority` field;
- the Sheet mappings include the seven expected columns;
- credential/account identifiers are absent from the public workflow.
