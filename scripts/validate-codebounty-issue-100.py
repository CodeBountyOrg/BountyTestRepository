#!/usr/bin/env python3
"""Validate the CodeBounty issue #100 duplicate-announcement fixture.

The fixture records the live GitHub + CodeBounty snapshot used for this PR.
It keeps the payout boundary explicit: the visible amount comes from bot
announcement comments and remains submitted-visible only until the required
CodeBounty application and maintainer/platform acceptance are verified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_BOUNTY_LINKS = {
    "http://localhost:3000/bounty/6800af954e2040a18be603c7",
    "http://localhost:3000/bounty/6800af954e2040a18be603cc",
}
EXPECTED_ANNOUNCEMENT_COMMENTS = {
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/100#issuecomment-2812057916",
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/100#issuecomment-2812058021",
}


def fail(message: str) -> None:
    raise SystemExit(f"issue-100 fixture invalid: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-codebounty-issue-100.py <fixture.json>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"missing fixture: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    duplicate = data.get("duplicate_announcement_snapshot") or {}
    collision = data.get("collision_snapshot") or {}
    expected_pr = data.get("expected_pr") or {}

    if issue.get("number") != 100:
        fail("issue number must be 100")
    if issue.get("state") != "open":
        fail("issue must be open at snapshot time")
    if issue.get("locked") is not False:
        fail("locked must be false at snapshot time")
    if issue.get("assignees") != []:
        fail("issue must be unassigned at snapshot time")
    labels = set(issue.get("labels", []))
    if "bug" not in labels:
        fail("bug label missing from live snapshot")
    if "💰 Bounty Available" not in labels:
        fail("bounty-available label missing from live snapshot")
    if "235 am" not in issue.get("body", ""):
        fail("issue body snapshot should preserve the original 235 am marker")

    if bounty.get("platform") != "CodeBounty":
        fail("platform must be CodeBounty")
    if bounty.get("visible_amount_usd") != 50:
        fail("visible bounty amount must be $50")
    if bounty.get("visible_amount_source") != "bot_comments":
        fail("visible amount source must stay scoped to bot comments")
    if bounty.get("announcement_comment_count") != 2:
        fail("expected two CodeBounty bot announcement comments")
    if set(bounty.get("announcement_comments", [])) != EXPECTED_ANNOUNCEMENT_COMMENTS:
        fail("announcement comment URLs must match the live snapshot")
    if set(bounty.get("bounty_links", [])) != EXPECTED_BOUNTY_LINKS:
        fail("bounty links should match both announcement comment links")
    if bounty.get("required_pr_linkage", "").lower() != "fixes #100":
        fail("required PR linkage must be `fixes #100`")
    if bounty.get("developer_application_required") is not True:
        fail("developer application requirement must stay explicit")
    if bounty.get("verified_payable_at_snapshot") is not False:
        fail("fixture must not claim verified-payable payout")

    if duplicate.get("duplicate_bot_announcements") is not True:
        fail("duplicate announcement flag must be true")
    if duplicate.get("unique_bounty_link_count") != 2:
        fail("duplicate snapshot must preserve both distinct bounty links")
    if duplicate.get("human_comment_present") is not True:
        fail("human follow-up comment should be preserved in the snapshot")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived at snapshot time")
    if collision.get("repo_visibility") != "PUBLIC":
        fail("repo visibility must be PUBLIC")
    if collision.get("same_scope_open_pr_count") != 0:
        fail("same-scope open PR count must be zero at snapshot time")
    terms = {term.lower() for term in collision.get("open_pr_search_terms", [])}
    if {"100", "fixes #100", "issue 100", "apr 17 235"} - terms:
        fail("collision-search terms are incomplete")
    for hit in collision.get("false_positive_open_pr_hits", []):
        if "#100" in (hit.get("match_reason", "")):
            fail("false-positive reasons must not claim a same-scope #100 match")

    required_body = {item.lower() for item in expected_pr.get("body_must_include", [])}
    for required in {
        "fixes #100",
        "codebounty",
        "$50",
        "developer_application_required",
        "duplicate_bot_announcements",
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
                "duplicate_bot_announcements": duplicate["duplicate_bot_announcements"],
                "verified_payable_at_snapshot": bounty["verified_payable_at_snapshot"],
                "same_scope_open_pr_count": collision["same_scope_open_pr_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
