# Issue #97 validation receipt

- Issue: https://github.com/CodeBountyOrg/BountyTestRepository/issues/97
- Visible amount/source: $50 USD from CodeBounty bot comment
- Required linkage: `fixes #97`
- Local fixture: `test-fixtures/codebounty-issue-97-external.json`
- Local validator: `scripts/validate-codebounty-issue-97.py`

## Commands

```bash
python3 -m py_compile scripts/validate-codebounty-issue-97.py
python3 scripts/validate-codebounty-issue-97.py test-fixtures/codebounty-issue-97-external.json
git diff --check
```

## Claim boundary

Counts as submitted-visible only after a public PR/comment exists. Verified-payable remains blocked until CodeBounty application eligibility and maintainer/platform acceptance are verified.
