#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const requiredString = (payload, path) => {
  const value = path.split('.').reduce((current, key) => current?.[key], payload);
  if (typeof value !== 'string' || value.trim() === '') {
    throw new Error(`Missing required string: ${path}`);
  }
  return value.trim();
};

const requiredNumber = (payload, path) => {
  const value = path.split('.').reduce((current, key) => current?.[key], payload);
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new Error(`Missing required number: ${path}`);
  }
  return value;
};

const readPayload = () => {
  const inputPath = process.argv[2];
  const raw = inputPath ? readFileSync(inputPath, 'utf8') : readFileSync(0, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Webhook payload is not valid JSON: ${error.message}`);
  }
};

const normalizeWebhookPayload = (payload) => {
  const event = requiredString(payload, 'event');
  const repository = requiredString(payload, 'repository.full_name');
  const issueNumber = requiredNumber(payload, 'issue.number');
  const bountyAmount = requiredNumber(payload, 'bounty.amount_usd');
  const bountyStatus = requiredString(payload, 'bounty.status');

  if (issueNumber <= 0) {
    throw new Error('issue.number must be positive');
  }

  if (bountyAmount <= 0) {
    throw new Error('bounty.amount_usd must be positive');
  }

  return {
    event,
    repository,
    issue: `#${issueNumber}`,
    bounty: `$${bountyAmount}`,
    status: bountyStatus,
  };
};

const main = () => {
  const normalized = normalizeWebhookPayload(readPayload());
  console.log(JSON.stringify(normalized, null, 2));
};

main();
