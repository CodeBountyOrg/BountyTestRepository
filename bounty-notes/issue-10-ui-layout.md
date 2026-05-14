# CodeBounty issue #10 — UI-layout fixture note

This note captures the public CodeBounty evidence for issue #10 so the test repository has a small, deterministic artifact tied to the UI-layout bounty flow.

## Public evidence

- GitHub issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/10
- Title: `Testing new UI changes`
- Body snapshot: `This is new layout`
- Public labels: `bug`, `💰 Bounty Available`
- Announcement: https://github.com/CodeBountyOrg/BountyTestRepository/issues/10#issuecomment-2655476261
- Visible amount: `$30 USD`
- Bot-linked bounty URL: `https://dev.codebounty.ai/bounty/67ad7b0abf2a3690859c17b4`
- Non-claim discussion at snapshot: one commenter expressed interest in testing the design, but the fresh open-PR collision search found no exact same-scope PR for issue #10.

## Public-action gate

The pre-push snapshot found the issue open, unlocked, unassigned, and free of exact same-scope open PR collisions. The required PR body linkage is `Fixes #10`.

## Validation

```bash
python3 -m py_compile scripts/validate-codebounty-issue-10.py
python3 scripts/validate-codebounty-issue-10.py test-fixtures/codebounty-issue-10-ui-layout.json
git diff --check
```

## Payout boundary

This is submitted-visible only after the PR is public. It is not verified-payable until CodeBounty platform application eligibility plus maintainer/platform acceptance are verified. No paid funds are assumed from this fixture.
