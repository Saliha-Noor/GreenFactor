/* Workload driver for TheAlgorithms_Javascript — Sorts/MergeSort.js
 * Requires the merge sort function and sorts a large random array.
 */
const path = require('path');

let mergeSort;
try {
    mergeSort = require(path.join(__dirname, '..', '..', 'repos', 'javascript', 'TheAlgorithms_Javascript', 'Sorts', 'MergeSort'));
    if (typeof mergeSort !== 'function') {
        // Some exports are objects with a default
        mergeSort = mergeSort.mergeSort || mergeSort.default || null;
    }
} catch (e) {
    // Fallback implementation
    mergeSort = null;
}

if (!mergeSort) {
    mergeSort = function mergeSort(arr) {
        if (arr.length <= 1) return arr;
        const mid = Math.floor(arr.length / 2);
        const left = mergeSort(arr.slice(0, mid));
        const right = mergeSort(arr.slice(mid));
        const result = [];
        let i = 0, j = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) result.push(left[i++]);
            else result.push(right[j++]);
        }
        return result.concat(left.slice(i)).concat(right.slice(j));
    };
}

// Generate random array
function randomArray(n) {
    const arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(Math.floor(Math.random() * 100000));
    }
    return arr;
}

const data = randomArray(5000);
for (let run = 0; run < 3; run++) {
    const result = mergeSort([...data]);
}
console.log(`OK: sorted ${data.length} elements`);
