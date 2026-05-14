# Issue #11 validation receipt

- Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/11
- Visible amount/source: $10 USD from CodeBounty bot comment plus `💰 Bounty Available` label
- Announcement comment: https://github.com/CodeBountyOrg/BountyTestRepository/issues/11#issuecomment-2655518687
- Platform bounty URL: https://dev.codebounty.ai/bounty/67ad8292bf2a3690859c18df
- Required linkage: `Fixes #11`
- Local fixture: `test-fixtures/codebounty-issue-11-title-test.json`
- Local validator: `scripts/validate-codebounty-issue-11.py`

## Commands

```bash
python3 -m py_compile scripts/validate-codebounty-issue-11.py
python3 scripts/validate-codebounty-issue-11.py test-fixtures/codebounty-issue-11-title-test.json
git diff --check
```

## Snapshot boundary

Fresh pre-push triage showed issue #11 open, unlocked, unassigned, repo public/not archived, and zero same-scope open PR collisions for `11`, `#11`, `fixes #11`, `issue 11`, `Bounty Launch`, or `Issue title test`.

## Claim boundary

This artifact counts as submitted-visible only after a public PR exists. Verified-payable remains blocked until CodeBounty application eligibility and maintainer/platform acceptance are verified.
