# CodeBounty issue #82 duplicate-approval fixture

Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/82

## Snapshot

- State: open
- Locked: false
- Assignees: none
- Labels: `💰 Bounty Available`
- Visible CodeBounty amount: `$10 USD`
- Amount source: CodeBounty bot comments
- Required PR syntax from bot announcement: `fixes #82`
- Duplicate approval evidence: two pending-approval comments were posted before two later CodeBounty bot announcements:
  - Pending approval: https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2781231507
  - Pending approval: https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2781231508
  - Bounty announcement: https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2808231115
  - Bounty announcement: https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2808231684
- Distinct local bounty IDs preserved:
  - `http://localhost:3000/bounty/67f21306730fd07f850f2d19`
  - `http://localhost:3000/bounty/67f21306730fd07f850f2d1d`
- Collision searches run immediately before this branch: `82`, `#82`, `fixes #82`, `issue 82`, `test new issue apr 6 1235am`, and `test issue 1235am`.
- Exact same-scope open PR count: `0`.

## Payout boundary

This is a submitted-visible CodeBounty action only. The bot announcement says a developer must submit an application through CodeBounty to be eligible, so this PR must not be treated as verified-payable or paid until platform/maintainer acceptance is confirmed.

## Local validation

```bash
python3 -m py_compile scripts/validate-codebounty-issue-82.py
python3 scripts/validate-codebounty-issue-82.py test-fixtures/codebounty-issue-82-duplicate-approval.json
git diff --check
```

The PR body should include `fixes #82` to satisfy the CodeBounty linkage rule.
