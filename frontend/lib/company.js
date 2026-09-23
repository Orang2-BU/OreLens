/**
 * @template {{id: number}} C
 * @template {{company: number, commodity: number}} E
 * @param {C[]} companies
 * @param {E[]} exposures
 * @param {number} commodityId
 */
export function buildCompanyPeers(companies, exposures, commodityId) {
  const byId = new Map(companies.map((company) => [company.id, company]));
  return exposures
    .filter((exposure) => exposure.commodity === commodityId)
    .flatMap((exposure) => {
      const company = byId.get(exposure.company);
      return company ? [{ company, exposure }] : [];
    });
}

/** @template {{code: string}} C @param {C[]} commodities @param {string} code @returns {C | undefined} */
export function pickCommodity(commodities, code) {
  const normalized = code.toUpperCase();
  return commodities.find((item) => item.code === normalized)
    || commodities.find((item) => item.code === 'COAL')
    || commodities[0];
}
