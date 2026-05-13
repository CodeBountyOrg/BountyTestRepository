#!/usr/bin/env python3
"""Validate the CodeBounty issue #37 bounty-linkage fixture.

The fixture is intentionally local and deterministic: it records the live
GitHub/CodeBounty snapshot used for the PR and checks that the public PR can
carry the required `fixes #37` linkage without overstating payout certainty.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"issue-37 fixture invalid: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-codebounty-issue-37.py <fixture.json>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"missing fixture: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    collision = data.get("collision_snapshot") or {}
    expected_pr = data.get("expected_pr") or {}

    if issue.get("number") != 37:
        fail("issue number must be 37")
    if issue.get("state") != "open":
        fail("issue must be open at snapshot time")
    if issue.get("locked") is not False:
        fail("locked must be false at snapshot time")
    if issue.get("assignees") != []:
        fail("issue must be unassigned at snapshot time")
    if "💰 Bounty Available" not in issue.get("labels", []):
        fail("bounty-available label missing")

    if bounty.get("platform") != "CodeBounty":
        fail("platform must be CodeBounty")
    if bounty.get("visible_amount_usd") != 50:
        fail("visible bounty amount must be $50")
    if bounty.get("required_pr_linkage", "").lower() != "fixes #37":
        fail("required PR linkage must be `fixes #37`")
    if bounty.get("developer_application_required") is not True:
        fail("developer application requirement must stay explicit")
    if bounty.get("verified_payable_at_snapshot") is not False:
        fail("fixture must not claim verified-payable payout")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived at snapshot time")
    if collision.get("repo_visibility") != "PUBLIC":
        fail("repo visibility must be PUBLIC")
    if collision.get("same_scope_open_pr_count") != 0:
        fail("same-scope open PR count must be zero at snapshot time")
    terms = {term.lower() for term in collision.get("open_pr_search_terms", [])}
    if {"37", "fixes #37", "issue 37"} - terms:
        fail("collision-search terms are incomplete")

    required_body = {item.lower() for item in expected_pr.get("body_must_include", [])}
    if "fixes #37" not in required_body or "developer_application_required" not in required_body:
        fail("expected PR body requirements must preserve issue linkage and payout blocker")

    print(
        json.dumps(
            {
                "ok": True,
                "issue": issue["number"],
                "visible_amount_usd": bounty["visible_amount_usd"],
                "required_pr_linkage": bounty["required_pr_linkage"],
                "verified_payable_at_snapshot": bounty["verified_payable_at_snapshot"],
                "same_scope_open_pr_count": collision["same_scope_open_pr_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
