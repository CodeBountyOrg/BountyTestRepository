#!/usr/bin/env python3
"""Validate the deterministic fixture for CodeBounty issue #34.

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
EXPECTED_ISSUE = 34
EXPECTED_AMOUNT = 10
EXPECTED_LINKAGE = "fixes #34"
EXPECTED_COMMENT = (
    "https://github.com/CodeBountyOrg/BountyTestRepository/issues/34"
    "#issuecomment-2723925317"
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
        "test-fixtures/codebounty-issue-34-march14.json"
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
    if issue.get("state_at_snapshot") != "open":
        fail("issue must be open at the captured snapshot")
    if issue.get("locked_at_snapshot") is not False:
        fail("issue must be unlocked at the captured snapshot")
    if issue.get("assignees_at_snapshot") != []:
        fail("issue must be unassigned at the captured snapshot")
    if "💰 Bounty Available" not in issue.get("labels_at_snapshot", []):
        fail("fixture must preserve the public bounty label")
    if "march 14 3am" not in str(issue.get("title", "")).lower():
        fail("fixture title should preserve the March 14 issue identity")

    if bounty.get("amount") != EXPECTED_AMOUNT or bounty.get("currency") != "USD":
        fail(f"expected {EXPECTED_AMOUNT} USD bounty, got {bounty!r}")
    if bounty.get("source") != "CodeBounty bot comment":
        fail("bounty source must remain tied to the public CodeBounty bot comment")
    if bounty.get("announcement_comment_url") != EXPECTED_COMMENT:
        fail("announcement comment URL changed or missing")
    if bounty.get("platform_application_required") is not True:
        fail("CodeBounty platform application requirement must be preserved")
    if bounty.get("verified_payable") is not False:
        fail("verified_payable must stay false until acceptance/payout is verified")

    if collision.get("repo_archived") is not False:
        fail("repo must be non-archived in the collision snapshot")
    if collision.get("same_scope_open_prs") != []:
        fail("fixture requires zero same-scope open PR collisions at snapshot")
    if str(linkage.get("required_phrase", "")).lower() != EXPECTED_LINKAGE:
        fail("PR linkage must include Fixes #34")
    if deliverable.get("type") != "codebounty-platform-flow-fixture":
        fail("deliverable type should identify the CodeBounty platform-flow fixture")

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
