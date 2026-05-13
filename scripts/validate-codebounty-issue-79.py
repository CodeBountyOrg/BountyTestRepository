#!/usr/bin/env python3
"""Validate the CodeBounty issue #79 markdown/upload fixture.

The fixture records the live GitHub + CodeBounty snapshot used for this PR.
It keeps the payout boundary explicit: the visible amount comes from bot
announcement comments, not from a verified platform application or payment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_BOUNTY_LINKS = {
    "http://localhost:3000/bounty/67f1cc90f54cb17267113c7e",
    "http://localhost:3000/bounty/67f1ccb1f54cb17267113c83",
}


def fail(message: str) -> None:
    raise SystemExit(f"issue-79 fixture invalid: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-codebounty-issue-79.py <fixture.json>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"missing fixture: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    markdown = data.get("markdown_upload_snapshot") or {}
    collision = data.get("collision_snapshot") or {}
    expected_pr = data.get("expected_pr") or {}

    if issue.get("number") != 79:
        fail("issue number must be 79")
    if issue.get("state") != "open":
        fail("issue must be open at snapshot time")
    if issue.get("locked") is not False:
        fail("locked must be false at snapshot time")
    if issue.get("assignees") != []:
        fail("issue must be unassigned at snapshot time")
    if "enhancement" not in issue.get("labels", []):
        fail("enhancement label missing from live snapshot")
    if "💰 Bounty Available" in issue.get("labels", []):
        fail("snapshot should document that issue #79 does not carry the bounty label")

    body = issue.get("body", "")
    if "**testing markdown**" not in body:
        fail("issue body markdown sample missing")
    if "failed to upload" not in body.lower():
        fail("failed-upload marker missing from issue body")

    if bounty.get("platform") != "CodeBounty":
        fail("platform must be CodeBounty")
    if bounty.get("visible_amount_usd") != 50:
        fail("visible bounty amount must be $50")
    if bounty.get("visible_amount_source") != "bot_comments":
        fail("visible amount source must stay scoped to bot comments")
    if bounty.get("announcement_comment_count") != 2:
        fail("expected two CodeBounty bot announcement comments")
    if bounty.get("required_pr_linkage", "").lower() != "fixes #79":
        fail("required PR linkage must be `fixes #79`")
    if bounty.get("developer_application_required") is not True:
        fail("developer application requirement must stay explicit")
    if bounty.get("verified_payable_at_snapshot") is not False:
        fail("fixture must not claim verified-payable payout")
    if set(bounty.get("bounty_links", [])) != EXPECTED_BOUNTY_LINKS:
        fail("bounty links should match both announcement comment links")

    if markdown.get("bold_markdown_preserved") is not True:
        fail("markdown preservation flag must be true")
    if markdown.get("failed_upload_recorded") is not True:
        fail("failed upload evidence flag must be true")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived at snapshot time")
    if collision.get("repo_visibility") != "PUBLIC":
        fail("repo visibility must be PUBLIC")
    if collision.get("same_scope_open_pr_count") != 0:
        fail("same-scope open PR count must be zero at snapshot time")
    terms = {term.lower() for term in collision.get("open_pr_search_terms", [])}
    if {"79", "fixes #79", "issue 79", "test issue april 3 12pm"} - terms:
        fail("collision-search terms are incomplete")

    required_body = {item.lower() for item in expected_pr.get("body_must_include", [])}
    for required in {"fixes #79", "codebounty", "$50", "developer_application_required", "bounty_label_absent"}:
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
                "verified_payable_at_snapshot": bounty["verified_payable_at_snapshot"],
                "same_scope_open_pr_count": collision["same_scope_open_pr_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
