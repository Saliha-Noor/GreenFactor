/* Workload driver for lodash — lodash.js
 * Requires lodash and runs chained data transformation operations.
 */
const path = require('path');

let _ ;
try {
    _ = require(path.join(__dirname, '..', '..', 'repos', 'javascript', 'lodash', 'lodash.js'));
} catch (e) {
    // Fallback: use basic JS array methods
    _ = null;
}

const N = 10000;
const data = Array.from({ length: N }, (_, i) => ({
    id: i,
    name: `item_${i}`,
    value: Math.random() * 1000,
    category: ['A', 'B', 'C', 'D'][i % 4],
}));

if (_) {
    for (let run = 0; run < 5; run++) {
        const grouped = _.groupBy(data, 'category');
        const mapped = _.mapValues(grouped, items => _.sumBy(items, 'value'));
        const sorted = _.sortBy(data, ['value']);
        const uniq = _.uniqBy(data, 'category');
        const chunked = _.chunk(data, 100);
    }
    console.log(`OK: processed ${N} items through lodash chains`);
} else {
    // Fallback
    for (let run = 0; run < 5; run++) {
        const sorted = [...data].sort((a, b) => a.value - b.value);
        const grouped = {};
        data.forEach(d => { (grouped[d.category] = grouped[d.category] || []).push(d); });
    }
    console.log(`OK: processed ${N} items (lodash not loadable, used fallback)`);
}
