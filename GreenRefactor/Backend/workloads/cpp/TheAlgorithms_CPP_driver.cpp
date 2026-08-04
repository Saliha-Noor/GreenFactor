/* Workload driver for TheAlgorithms_CPP — sorting/merge_sort.cpp
 * Self-contained merge sort workload.
 * Compile: g++ -O2 -std=c++17 workloads/cpp/TheAlgorithms_CPP_driver.cpp -o algo_cpp_driver
 */
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>

void merge_sort(std::vector<int>& arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    merge_sort(arr, l, m);
    merge_sort(arr, m + 1, r);
    std::vector<int> tmp(r - l + 1);
    int i = l, j = m + 1, k = 0;
    while (i <= m && j <= r) {
        if (arr[i] <= arr[j]) tmp[k++] = arr[i++];
        else tmp[k++] = arr[j++];
    }
    while (i <= m) tmp[k++] = arr[i++];
    while (j <= r) tmp[k++] = arr[j++];
    for (int x = 0; x < k; x++) arr[l + x] = tmp[x];
}

int main() {
    const int N = 10000;
    std::vector<int> data(N);
    srand(42);
    for (int run = 0; run < 3; run++) {
        for (int i = 0; i < N; i++) data[i] = rand() % 100000;
        merge_sort(data, 0, N - 1);
    }
    bool sorted = std::is_sorted(data.begin(), data.end());
    printf("OK: sorted %d elements, verified=%d\n", N, sorted ? 1 : 0);
    return 0;
}
