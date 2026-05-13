# Functionality smoke fixture for issue #12

Fixes #12.

Issue #12 is a CodeBounty test-functionality issue. This contribution adds a small deterministic fixture plus a dependency-free validator so the issue can be verified locally without relying on a live platform instance.

## Coverage

- Repository: `CodeBountyOrg/BountyTestRepository`
- Issue: `#12`
- Intent: functionality smoke test
- Visible bounty amount: `$100 USD`
- Required PR syntax: `fixes #12`
- Required checks: issue linkage, bounty amount, local validation

## Validation commands

```bash
node --check scripts/validate-codebounty-issue-12-functionality.mjs
node scripts/validate-codebounty-issue-12-functionality.mjs test-fixtures/codebounty-issue-12-functionality.json
python3 - <<'PY'
import json
from pathlib import Path
fixture = json.loads(Path('test-fixtures/codebounty-issue-12-functionality.json').read_text())
note = Path('bounty-notes/issue-12-functionality-smoke.md').read_text()
assert fixture['issue']['number'] == 12
assert fixture['bounty']['amount_usd'] == 100
assert fixture['pr']['required_syntax'] == 'fixes #12'
assert 'fixes #12' in note.lower()
PY
git diff --check
```

## Payout note

This is submitted-visible only until CodeBounty application eligibility and maintainer/platform acceptance are verified.
