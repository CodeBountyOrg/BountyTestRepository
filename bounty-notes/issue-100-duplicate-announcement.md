# CodeBounty issue #100 duplicate-announcement fixture

Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/100

## Snapshot

- State: open
- Locked: false
- Assignees: none
- Labels: `bug`, `💰 Bounty Available`
- Visible CodeBounty amount: `$50 USD`
- Amount source: two CodeBounty bot announcement comments
- Required PR syntax from bot announcement: `fixes #100`
- Duplicate announcement evidence: two distinct local bounty links were posted for the same issue:
  - `http://localhost:3000/bounty/6800af954e2040a18be603c7`
  - `http://localhost:3000/bounty/6800af954e2040a18be603cc`
- Collision searches run immediately before this branch: `100`, `fixes #100`, `issue 100`, and `apr 17 235`.
- Exact same-scope open PR count: `0`. Three GitHub search hits were false positives from `$100` / issue `#103` contexts, not issue #100 linkage.

## Payout boundary

This is a submitted-visible CodeBounty action only. The bot announcement says a developer must submit an application through CodeBounty to be eligible, so this PR must not be treated as verified-payable or paid until platform/maintainer acceptance is confirmed.

## Local validation

```bash
python3 -m py_compile scripts/validate-codebounty-issue-100.py
python3 scripts/validate-codebounty-issue-100.py test-fixtures/codebounty-issue-100-duplicate-announcement.json
git diff --check
```

The PR body should include `fixes #100` to satisfy the CodeBounty linkage rule.
