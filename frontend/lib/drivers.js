/**
 * @template T
 * @param {Array<T & {metric: string}>} drivers
 * @param {Array<{name: string, impact_direction: string, description: string}>} persisted
 * @returns {Array<T & {metric: string, direction: string | undefined, description: string | undefined}>}
 */
export function enrichDrivers(drivers, persisted) {
  const byName = new Map(persisted.map((item) => [item.name, item]));
  return drivers.map((driver) => {
    const detail = byName.get(driver.metric);
    return { ...driver, direction: detail?.impact_direction, description: detail?.description };
  });
}
