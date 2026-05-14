#!/usr/bin/env python3
"""Validate the CodeBounty issue #82 duplicate-approval fixture.

The fixture records the live GitHub + CodeBounty snapshot used for this PR.
It preserves a specific platform edge case: two pending-approval comments
were followed by two CodeBounty bot announcement comments for the same issue
and $10 amount, with two local bounty IDs. The payout boundary stays explicit:
this remains submitted-visible only until the required CodeBounty application
and maintainer/platform acceptance are verified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_BOUNTY_LINKS = {
    "http://localhost:3000/bounty/67f21306730fd07f850f2d19",
    "http://localhost:3000/bounty/67f21306730fd07f850f2d1d",
}
EXPECTED_PENDING_COMMENTS = {
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2781231507",
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2781231508",
}
EXPECTED_ANNOUNCEMENT_COMMENTS = {
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2808231115",
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/82#issuecomment-2808231684",
}


def fail(message: str) -> None:
    raise SystemExit(f"issue-82 fixture invalid: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-codebounty-issue-82.py <fixture.json>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"missing fixture: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    duplicate = data.get("duplicate_approval_snapshot") or {}
    collision = data.get("collision_snapshot") or {}
    expected_pr = data.get("expected_pr") or {}

    if issue.get("number") != 82:
        fail("issue number must be 82")
    if issue.get("state") != "open":
        fail("issue must be open at snapshot time")
    if issue.get("locked") is not False:
        fail("locked must be false at snapshot time")
    if issue.get("assignees") != []:
        fail("issue must be unassigned at snapshot time")
    labels = set(issue.get("labels", []))
    if "💰 Bounty Available" not in labels:
        fail("bounty-available label missing from live snapshot")
    if "testing" not in issue.get("body", "").lower():
        fail("issue body snapshot should preserve the original testing marker")

    if bounty.get("platform") != "CodeBounty":
        fail("platform must be CodeBounty")
    if bounty.get("visible_amount_usd") != 10:
        fail("visible bounty amount must be $10")
    if bounty.get("visible_amount_source") != "bot_comments":
        fail("visible amount source must stay scoped to bot comments")
    if bounty.get("pending_approval_comment_count") != 2:
        fail("expected two pending-approval comments")
    if bounty.get("announcement_comment_count") != 2:
        fail("expected two CodeBounty bot announcement comments")
    if set(bounty.get("pending_approval_comments", [])) != EXPECTED_PENDING_COMMENTS:
        fail("pending-approval comment URLs must match the live snapshot")
    if set(bounty.get("announcement_comments", [])) != EXPECTED_ANNOUNCEMENT_COMMENTS:
        fail("announcement comment URLs must match the live snapshot")
    if set(bounty.get("bounty_links", [])) != EXPECTED_BOUNTY_LINKS:
        fail("bounty links should match both distinct local bounty IDs")
    if bounty.get("required_pr_linkage", "").lower() != "fixes #82":
        fail("required PR linkage must be `fixes #82`")
    if bounty.get("developer_application_required") is not True:
        fail("developer application requirement must stay explicit")
    if bounty.get("verified_payable_at_snapshot") is not False:
        fail("fixture must not claim verified-payable payout")

    if duplicate.get("duplicate_pending_approval_comments") is not True:
        fail("duplicate pending-approval flag must be true")
    if duplicate.get("duplicate_bot_announcements") is not True:
        fail("duplicate bot-announcement flag must be true")
    if duplicate.get("unique_bounty_link_count") != 2:
        fail("duplicate snapshot must preserve both distinct bounty links")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived at snapshot time")
    if collision.get("repo_visibility") != "PUBLIC":
        fail("repo visibility must be PUBLIC")
    if collision.get("same_scope_open_pr_count") != 0:
        fail("same-scope open PR count must be zero at snapshot time")
    terms = {term.lower() for term in collision.get("open_pr_search_terms", [])}
    if {"82", "#82", "fixes #82", "issue 82"} - terms:
        fail("collision-search terms are incomplete")

    required_body = {item.lower() for item in expected_pr.get("body_must_include", [])}
    for required in {
        "fixes #82",
        "codebounty",
        "$10",
        "developer_application_required",
        "duplicate_pending_approval_comments",
        "verified_payable=false",
    }:
        if required not in required_body:
            fail(f"expected PR body requirement missing: {required}")

    print(
        json.dumps(
            {
                "ok": True,
                "issue": issue["number"],
                "visible_amount_usd": bounty["visible_amount_usd"],
                "visible_amount_source": bounty["visible_amount_source"],
                "required_pr_linkage": bounty["required_pr_linkage"],
                "duplicate_pending_approval_comments": duplicate["duplicate_pending_approval_comments"],
                "duplicate_bot_announcements": duplicate["duplicate_bot_announcements"],
                "verified_payable_at_snapshot": bounty["verified_payable_at_snapshot"],
                "same_scope_open_pr_count": collision["same_scope_open_pr_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
