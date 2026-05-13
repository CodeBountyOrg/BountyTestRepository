#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const loadPayload = (path) => {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (error) {
    throw new Error(`Unable to read external bounty fixture at ${path}: ${error.message}`);
  }
};

const payloadPath = process.argv[2] ?? 'test-fixtures/codebounty-external-issue-83.json';
const payload = loadPayload(payloadPath);

assert(payload.repository?.full_name === 'CodeBountyOrg/BountyTestRepository', 'repository.full_name must match the target repository');
assert(payload.issue?.number === 83, 'issue.number must be 83');
assert(payload.issue?.source === 'external_sponsor', 'issue.source must identify an external sponsor');
assert(payload.installation?.app_installed === false, 'fixture must cover the no-app-installed path');
assert(payload.bounty?.amount_usd === 150, 'bounty.amount_usd must stay at the announced $150');
assert(payload.bounty?.currency === 'USD', 'bounty currency must be USD');
assert(Array.isArray(payload.timeline) && payload.timeline.length >= 2, 'timeline must include pending and available states');

const states = payload.timeline.map((event) => event.status);
assert(states[0] === 'pending_maintainer_approval', 'first timeline state must be pending maintainer approval');
assert(states.includes('available'), 'timeline must include the available state after approval');

const pending = payload.timeline.find((event) => event.status === 'pending_maintainer_approval');
const available = payload.timeline.find((event) => event.status === 'available');
assert(pending?.requires_maintainer_action === true, 'pending state must require maintainer action');
assert(available?.requires_maintainer_action === false, 'available state must no longer require maintainer action');
assert(available?.required_pr_syntax === 'fixes #83', 'available state must preserve required PR syntax');

const normalized = {
  issue: payload.issue.number,
  amount_usd: payload.bounty.amount_usd,
  external_sponsor: payload.issue.source === 'external_sponsor',
  no_app_installed_path: payload.installation.app_installed === false,
  final_status: available.status,
  required_pr_syntax: available.required_pr_syntax,
};

console.log(JSON.stringify(normalized, null, 2));
