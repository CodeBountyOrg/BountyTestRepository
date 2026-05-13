# External bounty flow verification for issue #83

Fixes #83.

Issue #83 covers an externally-created bounty where the repository app was not installed at issue creation time. This contribution adds a deterministic fixture and validator for that path so the pending-approval and approved bounty states can be checked without depending on a live CodeBounty environment.

## What is covered

- Repository: `CodeBountyOrg/BountyTestRepository`
- Issue: `#83`
- Source: external sponsor
- No-app-installed path: `installation.app_installed === false`
- Pending state: `pending_maintainer_approval`
- Available state: `available`
- Required PR syntax: `fixes #83`
- Visible bounty amount: `$150 USD`

## Validation commands

```bash
node --check scripts/validate-codebounty-external-bounty.mjs
node scripts/validate-codebounty-external-bounty.mjs test-fixtures/codebounty-external-issue-83.json
python3 - <<'PY'
import json
from pathlib import Path
fixture = json.loads(Path('test-fixtures/codebounty-external-issue-83.json').read_text())
note = Path('bounty-notes/issue-83-external-bounty-flow.md').read_text()
assert fixture['issue']['number'] == 83
assert fixture['installation']['app_installed'] is False
assert fixture['bounty']['amount_usd'] == 150
assert 'fixes #83' in note.lower()
PY
git diff --check
```

## Payout note

The GitHub-visible bounty is treated as submitted-visible only. CodeBounty platform application and maintainer acceptance remain payout blockers until verified.
