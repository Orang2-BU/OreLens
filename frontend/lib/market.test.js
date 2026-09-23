import assert from 'node:assert/strict';
import test from 'node:test';
import { buildSparkline } from './market.js';

test('buildSparkline handles empty, flat, and rising price series', () => {
  assert.equal(buildSparkline([]), '');
  assert.equal(buildSparkline([5, 5], 100, 40), '0.0,20.0 100.0,20.0');
  assert.equal(buildSparkline([10, 20, 30], 100, 40), '0.0,40.0 50.0,20.0 100.0,0.0');
});
