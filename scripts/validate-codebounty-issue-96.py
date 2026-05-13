#!/usr/bin/env python3
"""Validate the CodeBounty issue #96 external-sponsor fixture.

The fixture is intentionally dependency-free so maintainers can verify the
GitHub-side bounty metadata without installing project tooling.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = {
    "issue_number": 96,
    "amount_usd": 50,
    "required_linkage": "fixes #96",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main(path_arg: str) -> None:
    path = Path(path_arg)
    if not path.is_file():
        fail(f"fixture does not exist: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    submission = data.get("submission") or {}

    if issue.get("number") != EXPECTED["issue_number"]:
        fail(f"issue number must be {EXPECTED['issue_number']}")
    if "CodeBountyOrg/BountyTestRepository/issues/96" not in issue.get("url", ""):
        fail("issue URL must point to CodeBountyOrg/BountyTestRepository#96")
    if issue.get("state") != "open":
        fail("fixture should record the issue as open at validation time")
    if "💰 Bounty Available" not in issue.get("labels", []):
        fail("fixture should preserve the public bounty label")

    if bounty.get("amount_usd") != EXPECTED["amount_usd"]:
        fail(f"bounty amount must be ${EXPECTED['amount_usd']}")
    if not bounty.get("application_required"):
        fail("CodeBounty application requirement must stay explicit")
    if bounty.get("verified_payable") is not False:
        fail("verified_payable must remain false until platform/maintainer acceptance is proven")
    if bounty.get("required_pr_linkage", "").lower() != EXPECTED["required_linkage"]:
        fail("required PR linkage must be fixes #96")

    if submission.get("expected_pr_body_token") != "Fixes #96":
        fail("PR body token should be recorded with GitHub-close syntax casing")
    if "does not assert payout eligibility" not in submission.get("claim_boundary", ""):
        fail("claim boundary must prevent overclaiming payout status")

    print(
        "PASS issue=96 amount_usd=50 linkage='Fixes #96' "
        "verified_payable=false application_required=true"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: validate-codebounty-issue-96.py <fixture.json>")
    main(sys.argv[1])
