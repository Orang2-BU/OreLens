const entityTypes = new Set(['Commodity', 'Company', 'Macro']);
const confidenceLevels = new Set(['High', 'Medium', 'Low']);

/** @param {{entityType?: string, confidence?: string, search?: string, page?: string}} [filters] */
export function buildEvidenceQuery({ entityType, confidence, search, page } = {}) {
  const query = new URLSearchParams();
  if (entityType && entityTypes.has(entityType)) query.set('entity_type', entityType);
  if (confidence && confidenceLevels.has(confidence)) query.set('confidence', confidence);
  if (search?.trim()) query.set('search', search.trim());
  if (page && /^[1-9]\d*$/.test(page) && page !== '1') query.set('page', page);
  return query.toString();
}
