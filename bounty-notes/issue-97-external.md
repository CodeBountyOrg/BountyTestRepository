# CodeBounty issue #97 external issue fixture

Fixes #97.

## Scope

Issue #97 is a CodeBounty test-repo issue titled `external issue` with a public CodeBounty bot bounty announcement for **$50 USD**. The public bot instructions require PR descriptions to include `fixes #97` and state that CodeBounty platform application/eligibility is still required.

This patch adds a deterministic fixture and dependency-free validator that preserve the public bounty facts without requiring live CodeBounty credentials.

## Added artifacts

- `test-fixtures/codebounty-issue-97-external.json` captures the issue URL, amount, required linkage, and payout-boundary state.
- `scripts/validate-codebounty-issue-97.py` validates the fixture with Python stdlib only.

## Validation

Run from the repository root:

```bash
python3 -m py_compile scripts/validate-codebounty-issue-97.py
python3 scripts/validate-codebounty-issue-97.py test-fixtures/codebounty-issue-97-external.json
git diff --check
```

Expected validator summary includes:

```json
{"issue": 97, "ok": true, "required_pr_phrase": "fixes #97", "repo": "CodeBountyOrg/BountyTestRepository", "verified_payable": false, "visible_amount_usd": 50}
```

## Payout boundary

This is submitted-visible only. It is not verified-payable until the CodeBounty application requirement and maintainer/platform acceptance are confirmed.
