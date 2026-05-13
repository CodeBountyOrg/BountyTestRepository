#!/usr/bin/env python3
"""Validate the CodeBounty issue #95 external-sponsor fixture.

The repository is a CodeBounty test surface, so this validator stays stdlib-only
and checks the public GitHub-side bounty metadata without requiring platform
credentials or assuming payout eligibility.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import NoReturn

EXPECTED_REPO = "CodeBountyOrg/BountyTestRepository"
EXPECTED_ISSUE = 95
EXPECTED_AMOUNT_USD = 50
EXPECTED_LINKAGE = "fixes #95"
EXPECTED_ANNOUNCEMENT = (
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/95"
    "#issuecomment-2803965362"
)


def fail(message: str) -> NoReturn:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_fixture(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"fixture not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON fixture: {exc}")


def main(argv: list[str]) -> int:
    fixture_path = Path(argv[1]) if len(argv) > 1 else Path(
        "test-fixtures/codebounty-issue-95-external-sponsor.json"
    )
    data = load_fixture(fixture_path)

    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    submission = data.get("submission") or {}
    collision = data.get("collision_check") or {}

    if issue.get("repo") != EXPECTED_REPO:
        fail(f"expected repo {EXPECTED_REPO!r}, got {issue.get('repo')!r}")
    if issue.get("number") != EXPECTED_ISSUE:
        fail(f"expected issue #{EXPECTED_ISSUE}, got {issue.get('number')!r}")
    if "external sponsor" not in str(issue.get("title", "")).lower():
        fail("fixture title should preserve the external-sponsor signal")
    if issue.get("state") != "open":
        fail("fixture should record the issue as open at validation time")
    if "💰 Bounty Available" not in issue.get("labels", []):
        fail("fixture should preserve the public bounty label")

    if bounty.get("amount_usd") != EXPECTED_AMOUNT_USD:
        fail(f"expected ${EXPECTED_AMOUNT_USD} bounty, got {bounty!r}")
    if bounty.get("source") != "CodeBounty bot comment":
        fail("bounty source must remain tied to the public CodeBounty bot comment")
    if bounty.get("announcement_url") != EXPECTED_ANNOUNCEMENT:
        fail("announcement URL should point at the public CodeBounty bot comment")
    if bounty.get("application_required") is not True:
        fail("CodeBounty platform application requirement must be preserved")
    if bounty.get("verified_payable") is not False:
        fail("verified_payable must stay false until acceptance/payout is verified")
    if str(bounty.get("required_pr_linkage", "")).lower() != EXPECTED_LINKAGE:
        fail("PR linkage must include fixes #95")

    if submission.get("expected_pr_body_token") != "Fixes #95":
        fail("PR body token should be recorded with GitHub-close syntax casing")
    if "does not assert payout eligibility" not in submission.get("claim_boundary", ""):
        fail("claim boundary must prevent overclaiming payout status")

    exact_terms = collision.get("exact_terms_checked") or []
    if {"95", "fixes #95", "issue 95"} - set(exact_terms):
        fail("collision check must record the exact issue search terms")
    if collision.get("exact_open_pr_matches_at_authoring") != 0:
        fail("fixture should only be submitted when exact issue #95 PR matches are zero")

    print(
        json.dumps(
            {
                "ok": True,
                "repo": issue["repo"],
                "issue": issue["number"],
                "visible_amount_usd": bounty["amount_usd"],
                "required_pr_phrase": submission["expected_pr_body_token"],
                "verified_payable": bounty["verified_payable"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
