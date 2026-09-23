/**
 * Convert a price series into SVG polyline points.
 * @param {number[]} values
 * @param {number} [width]
 * @param {number} [height]
 * @returns {string}
 */
export function buildSparkline(values, width = 320, height = 80) {
  const clean = values.filter(Number.isFinite);
  if (!clean.length) return '';

  const min = Math.min(...clean);
  const max = Math.max(...clean);
  const range = max - min;
  const step = clean.length === 1 ? 0 : width / (clean.length - 1);

  return clean.map((value, index) => {
    const x = clean.length === 1 ? width / 2 : index * step;
    const y = range === 0 ? height / 2 : height - ((value - min) / range) * height;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
}
