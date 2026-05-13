# CodeBounty issue #17 receipt

Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/17

Visible bounty: $120 USD through CodeBounty, announced in issue comment https://github.com/CodeBountyOrg/BountyTestRepository/issues/17#issuecomment-2675442925.

## Scope

This repository is a CodeBounty test repository and issue #17 is a minimal test issue whose body/title is `codebountry`. The artifact in this PR preserves a deterministic, machine-readable fixture for that bounty so future validation can verify:

- the issue number and public issue URL;
- the visible bounty amount;
- the required PR syntax: `fixes #17`;
- the platform-application blocker that keeps submitted-visible value separate from verified-payable value.

## Local validation

```bash
python3 -m py_compile scripts/validate-codebounty-issue-17.py
python3 scripts/validate-codebounty-issue-17.py test-fixtures/codebounty-issue-17.json
git diff --check
```

## Payout boundary

This can only be counted as submitted-visible value until CodeBounty application/eligibility and maintainer/platform acceptance are verified. No funds are paid or verified by this PR.
