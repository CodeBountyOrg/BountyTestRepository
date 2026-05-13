# CodeBounty issue #37 linkage note

Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/37

## Snapshot

- State: open
- Locked: false
- Assignees: none
- Label: `💰 Bounty Available`
- Visible CodeBounty amount: `$50 USD`
- Required PR syntax from bot announcement: `fixes #37`
- Collision searches run immediately before this branch: `37`, `fixes #37`, `issue 37`, and `issue march 14 315pm`; exact same-scope open PR count was `0`.

## Payout boundary

This is a submitted-visible CodeBounty action only. The bot announcement says a developer must submit an application through CodeBounty to be eligible, so this PR must not be treated as verified-payable or paid until platform/maintainer acceptance is confirmed.

## Local validation

```bash
python3 -m py_compile scripts/validate-codebounty-issue-37.py
python3 scripts/validate-codebounty-issue-37.py test-fixtures/codebounty-issue-37-bounty-linkage.json
git diff --check
```

The PR body should include `fixes #37` to satisfy the CodeBounty linkage rule.
