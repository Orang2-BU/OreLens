import assert from 'node:assert/strict';
import test from 'node:test';
import { buildEvidenceQuery } from './evidence.js';

test('buildEvidenceQuery validates filters and encodes search values', () => {
  assert.equal(buildEvidenceQuery({ entityType: 'Company', confidence: 'Low', search: ' Revenue Growth ', page: '2' }), 'entity_type=Company&confidence=Low&search=Revenue+Growth&page=2');
  assert.equal(buildEvidenceQuery({ entityType: 'Unknown', confidence: 'Certain', page: '-1' }), '');
});
