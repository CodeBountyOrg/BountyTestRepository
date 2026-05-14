#!/usr/bin/env python3
"""Validate the deterministic fixture for CodeBounty issue #10.

This repository is a CodeBounty test surface. The validator is stdlib-only so
maintainers can verify the fixture without platform credentials or dependency
installation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import NoReturn

EXPECTED_REPO = "CodeBountyOrg/BountyTestRepository"
EXPECTED_ISSUE = 10
EXPECTED_AMOUNT = 30
EXPECTED_LINKAGE = "fixes #10"
EXPECTED_COMMENT = (
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/10"
    "#issuecomment-2655476261"
)
EXPECTED_PLATFORM_URL = "https://dev.codebounty.ai/bounty/67ad7b0abf2a3690859c17b4"
EXPECTED_TITLE = "Testing new UI changes"
EXPECTED_BODY = "This is new layout"


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
        "test-fixtures/codebounty-issue-10-ui-layout.json"
    )
    data = load_fixture(fixture_path)

    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    collision = data.get("collision_snapshot") or {}
    linkage = data.get("pr_linkage") or {}
    deliverable = data.get("deliverable") or {}

    if issue.get("repo") != EXPECTED_REPO:
        fail(f"expected repo {EXPECTED_REPO!r}, got {issue.get('repo')!r}")
    if issue.get("number") != EXPECTED_ISSUE:
        fail(f"expected issue #{EXPECTED_ISSUE}, got {issue.get('number')!r}")
    if issue.get("title") != EXPECTED_TITLE:
        fail("fixture title should preserve the issue #10 UI-layout identity")
    if issue.get("body") != EXPECTED_BODY:
        fail("fixture should preserve the issue #10 body snapshot")
    if issue.get("state_at_snapshot") != "open":
        fail("issue must be open at the captured snapshot")
    if issue.get("locked_at_snapshot") is not False:
        fail("issue must be unlocked at the captured snapshot")
    if issue.get("assignees_at_snapshot") != []:
        fail("issue must be unassigned at the captured snapshot")
    labels = issue.get("labels_at_snapshot", [])
    if "💰 Bounty Available" not in labels:
        fail("fixture must preserve the public bounty label")
    if "bug" not in labels:
        fail("fixture must preserve the public bug label")

    if bounty.get("amount") != EXPECTED_AMOUNT or bounty.get("currency") != "USD":
        fail(f"expected {EXPECTED_AMOUNT} USD bounty, got {bounty!r}")
    if bounty.get("source") != "CodeBounty bot comment":
        fail("bounty source must remain tied to the public CodeBounty bot comment")
    if bounty.get("announcement_comment_url") != EXPECTED_COMMENT:
        fail("announcement comment URL changed or missing")
    if bounty.get("platform_bounty_url") != EXPECTED_PLATFORM_URL:
        fail("platform bounty URL changed or missing")
    if bounty.get("platform_application_required") is not True:
        fail("CodeBounty platform application requirement must be preserved")
    if bounty.get("verified_payable") is not False:
        fail("verified_payable must stay false until acceptance/payout is verified")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived in the collision snapshot")
    if collision.get("same_scope_open_prs") != []:
        fail("fixture requires zero same-scope open PR collisions at snapshot")
    if collision.get("raw_open_pr_search_hits", 0) < 0:
        fail("raw open PR search hits must be recorded as a non-negative count")
    terms = collision.get("search_terms", [])
    if "Testing new UI changes" not in terms or "fixes #10" not in terms:
        fail("collision search terms should include the distinctive title and linkage")

    if str(linkage.get("required_phrase", "")).lower() != EXPECTED_LINKAGE:
        fail("PR linkage must include Fixes #10")
    if deliverable.get("type") != "codebounty-ui-layout-fixture":
        fail("deliverable type should identify the CodeBounty UI-layout fixture")

    print(
        json.dumps(
            {
                "ok": True,
                "repo": issue["repo"],
                "issue": issue["number"],
                "visible_amount_usd": bounty["amount"],
                "required_pr_phrase": linkage["required_phrase"],
                "same_scope_open_prs": len(collision["same_scope_open_prs"]),
                "verified_payable": bounty["verified_payable"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
