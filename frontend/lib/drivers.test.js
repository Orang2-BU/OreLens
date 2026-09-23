import assert from 'node:assert/strict';
import test from 'node:test';
import { enrichDrivers } from './drivers.js';

test('enrichDrivers maps persisted direction without dropping unavailable hypotheses', () => {
  const result = enrichDrivers(
    [{ metric: 'China GDP Growth', status: 'observed_context' }, { metric: 'Coal Imports', status: 'unavailable' }],
    [{ name: 'China GDP Growth', impact_direction: 'POSITIVE', description: 'Macro context' }],
  );
  assert.deepEqual(result[0], { metric: 'China GDP Growth', status: 'observed_context', direction: 'POSITIVE', description: 'Macro context' });
  assert.deepEqual(result[1], { metric: 'Coal Imports', status: 'unavailable', direction: undefined, description: undefined });
});
