# CodeBounty webhook verification for issue #42

Fixes #42.

This adds a deterministic webhook payload validation fixture for the CodeBounty webhook test issue. The fixture and validator let maintainers confirm that a bounty webhook event carries the fields required to route a bounty notification back to the correct GitHub issue and visible reward.

## Added artifacts

- `test-fixtures/codebounty-webhook-issue-42.json` — sample `bounty.available` payload for `CodeBountyOrg/BountyTestRepository#42` with the $150 visible bounty amount.
- `scripts/validate-codebounty-webhook.mjs` — dependency-free Node.js validator that parses a webhook JSON file/stdin and checks:
  - event name
  - repository full name
  - issue number
  - positive bounty amount
  - bounty status

## Validation commands

```bash
node --check scripts/validate-codebounty-webhook.mjs
node scripts/validate-codebounty-webhook.mjs test-fixtures/codebounty-webhook-issue-42.json
```

Expected normalized output:

```json
{
  "event": "bounty.available",
  "repository": "CodeBountyOrg/BountyTestRepository",
  "issue": "#42",
  "bounty": "$150",
  "status": "available"
}
```
