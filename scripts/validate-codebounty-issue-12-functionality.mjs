#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const fail = (message) => {
  throw new Error(message);
};

const payloadPath = process.argv[2] ?? 'test-fixtures/codebounty-issue-12-functionality.json';
const payload = JSON.parse(readFileSync(payloadPath, 'utf8'));

if (payload.repository?.full_name !== 'CodeBountyOrg/BountyTestRepository') {
  fail('repository.full_name mismatch');
}
if (payload.issue?.number !== 12) {
  fail('issue.number must be 12');
}
if (payload.issue?.intent !== 'functionality_smoke_test') {
  fail('issue intent must be functionality_smoke_test');
}
if (payload.bounty?.amount_usd !== 100) {
  fail('bounty amount must match the announced $100');
}
if (!Array.isArray(payload.checks) || payload.checks.length < 3) {
  fail('fixture must define at least three functionality checks');
}

const requiredChecks = new Set(['issue_linkage', 'bounty_amount', 'local_validation']);
for (const check of payload.checks) {
  if (check.required === true) {
    requiredChecks.delete(check.id);
  }
}
if (requiredChecks.size > 0) {
  fail(`missing required checks: ${[...requiredChecks].join(', ')}`);
}

const normalized = {
  issue: payload.issue.number,
  amount_usd: payload.bounty.amount_usd,
  required_checks: payload.checks.filter((check) => check.required).map((check) => check.id),
  pr_syntax: payload.pr.required_syntax,
};

if (normalized.pr_syntax !== 'fixes #12') {
  fail('PR syntax must be fixes #12');
}

console.log(JSON.stringify(normalized, null, 2));
