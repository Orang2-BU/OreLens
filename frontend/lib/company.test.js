import assert from 'node:assert/strict';
import test from 'node:test';
import { buildCompanyPeers, pickCommodity } from './company.js';

test('buildCompanyPeers keeps only companies exposed to the selected commodity', () => {
  const companies = [{ id: 1, ticker: 'COAL' }, { id: 2, ticker: 'GOLD' }];
  const exposures = [{ company: 1, commodity: 10 }, { company: 2, commodity: 20 }, { company: 99, commodity: 10 }];
  assert.deepEqual(buildCompanyPeers(companies, exposures, 10), [{ company: companies[0], exposure: exposures[0] }]);
});

test('pickCommodity uses Coal as the stable fallback', () => {
  const commodities = [{ code: 'NICKEL' }, { code: 'COAL' }];
  assert.equal(pickCommodity(commodities, 'invalid'), commodities[1]);
});
