#!/usr/bin/env python3
"""Validate the deterministic fixture for CodeBounty issue #97.

This repo is a CodeBounty test fixture surface. The validator is intentionally
stdlib-only so maintainers can run it without installing project dependencies.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import NoReturn

EXPECTED_REPO = "CodeBountyOrg/BountyTestRepository"
EXPECTED_ISSUE = 97
EXPECTED_AMOUNT = 50
EXPECTED_LINKAGE = "fixes #97"


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
        "test-fixtures/codebounty-issue-97-external.json"
    )
    data = load_fixture(fixture_path)

    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    linkage = data.get("pr_linkage") or {}
    deliverable = data.get("deliverable") or {}

    if issue.get("repo") != EXPECTED_REPO:
        fail(f"expected repo {EXPECTED_REPO!r}, got {issue.get('repo')!r}")
    if issue.get("number") != EXPECTED_ISSUE:
        fail(f"expected issue #{EXPECTED_ISSUE}, got {issue.get('number')!r}")
    if "external" not in str(issue.get("title", "")).lower():
        fail("fixture title should preserve the external-issue signal")
    if bounty.get("amount") != EXPECTED_AMOUNT or bounty.get("currency") != "USD":
        fail(f"expected {EXPECTED_AMOUNT} USD bounty, got {bounty!r}")
    if bounty.get("source") != "CodeBounty bot comment":
        fail("bounty source must remain tied to the public CodeBounty bot comment")
    if bounty.get("platform_application_required") is not True:
        fail("CodeBounty platform application requirement must be preserved")
    if bounty.get("verified_payable") is not False:
        fail("verified_payable must stay false until acceptance/payout is verified")
    if str(linkage.get("required_phrase", "")).lower() != EXPECTED_LINKAGE:
        fail("PR linkage must include fixes #97")
    if deliverable.get("type") != "external-issue-fixture":
        fail("deliverable type should identify the issue #97 external fixture")

    print(
        json.dumps(
            {
                "ok": True,
                "repo": issue["repo"],
                "issue": issue["number"],
                "visible_amount_usd": bounty["amount"],
                "required_pr_phrase": linkage["required_phrase"],
                "verified_payable": bounty["verified_payable"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
