#!/usr/bin/env python3
"""Validate the CodeBounty issue #17 fixture.

This repository is a CodeBounty test surface, so the useful artifact is a
small deterministic receipt that preserves the bounty metadata and PR linkage
requirements without depending on external services.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = {
    "issue_number": 17,
    "issue_key": "codebountry",
    "amount_usd": 120,
    "required_pr_phrase": "fixes #17",
}


def fail(message: str) -> None:
    raise SystemExit(f"fixture validation failed: {message}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        fail("usage: validate-codebounty-issue-17.py <fixture.json>")

    fixture_path = Path(argv[1])
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    issue = data.get("issue") or {}
    bounty = data.get("bounty") or {}
    validation = data.get("validation") or {}

    if issue.get("number") != EXPECTED["issue_number"]:
        fail(f"expected issue #{EXPECTED['issue_number']}, got {issue.get('number')!r}")

    normalized = " ".join(str(issue.get("body") or issue.get("title") or "").lower().split())
    if EXPECTED["issue_key"] not in normalized:
        fail(f"expected issue key {EXPECTED['issue_key']!r} in title/body")

    if bounty.get("amount_usd") != EXPECTED["amount_usd"]:
        fail(f"expected ${EXPECTED['amount_usd']} amount, got {bounty.get('amount_usd')!r}")

    if bounty.get("required_pr_phrase", "").strip().lower() != EXPECTED["required_pr_phrase"]:
        fail("required PR phrase must be 'fixes #17'")

    if validation.get("expected_amount_usd") != EXPECTED["amount_usd"]:
        fail("validation expected_amount_usd drifted from bounty amount")

    if "verified-payable" not in bounty.get("eligibility_blocker", ""):
        fail("eligibility blocker must preserve submitted-visible vs verified-payable boundary")

    print(
        "ok: issue #{number} {key} fixture records ${amount} CodeBounty metadata and PR phrase {phrase!r}".format(
            number=issue["number"],
            key=EXPECTED["issue_key"],
            amount=bounty["amount_usd"],
            phrase=bounty["required_pr_phrase"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
