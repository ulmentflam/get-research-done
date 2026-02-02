import { describe, test } from 'node:test';
import assert from 'node:assert';
import { existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, '../..');
const commandsDir = join(projectRoot, 'commands/grd');

describe('Renamed Commands Exist', () => {
  test('design-experiment.md exists (was plan-phase)', () => {
    const filePath = join(commandsDir, 'design-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('run-experiment.md exists (was execute-phase)', () => {
    const filePath = join(commandsDir, 'run-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('scope-experiment.md exists (was discuss-phase)', () => {
    const filePath = join(commandsDir, 'scope-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('validate-results.md exists (was verify-work)', () => {
    const filePath = join(commandsDir, 'validate-results.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('literature-review.md exists (was research-phase)', () => {
    const filePath = join(commandsDir, 'literature-review.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('list-experiment-assumptions.md exists (was list-phase-assumptions)', () => {
    const filePath = join(commandsDir, 'list-experiment-assumptions.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('add-experiment.md exists (was add-phase)', () => {
    const filePath = join(commandsDir, 'add-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('insert-experiment.md exists (was insert-phase)', () => {
    const filePath = join(commandsDir, 'insert-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('remove-experiment.md exists (was remove-phase)', () => {
    const filePath = join(commandsDir, 'remove-experiment.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });
});

describe('Old Commands Removed', () => {
  test('plan-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'plan-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('execute-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'execute-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('discuss-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'discuss-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('verify-work.md no longer exists', () => {
    const filePath = join(commandsDir, 'verify-work.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('research-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'research-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('list-phase-assumptions.md no longer exists', () => {
    const filePath = join(commandsDir, 'list-phase-assumptions.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('add-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'add-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('insert-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'insert-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });

  test('remove-phase.md no longer exists', () => {
    const filePath = join(commandsDir, 'remove-phase.md');
    assert.ok(!existsSync(filePath), `Expected ${filePath} to NOT exist (should be renamed)`);
  });
});

describe('Command Chain Endpoints', () => {
  test('new-study.md exists (chain start)', () => {
    const filePath = join(commandsDir, 'new-study.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('complete-study.md exists (chain end)', () => {
    const filePath = join(commandsDir, 'complete-study.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('audit-study.md exists (validation)', () => {
    const filePath = join(commandsDir, 'audit-study.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('evaluate.md exists (evaluation gate)', () => {
    const filePath = join(commandsDir, 'evaluate.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });

  test('graduate.md exists (notebook graduation)', () => {
    const filePath = join(commandsDir, 'graduate.md');
    assert.ok(existsSync(filePath), `Expected ${filePath} to exist`);
  });
});
