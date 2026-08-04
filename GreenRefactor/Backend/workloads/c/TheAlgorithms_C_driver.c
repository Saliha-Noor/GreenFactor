/* Workload driver for TheAlgorithms_C — sorting/merge_sort.c
 * Self-contained: includes a merge_sort implementation and runs it.
 * This gets compiled and run as the workload binary.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1, n2 = r - m;
    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));
    memcpy(L, arr + l, n1 * sizeof(int));
    memcpy(R, arr + m + 1, n2 * sizeof(int));
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
    free(L); free(R);
}

void merge_sort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        merge_sort(arr, l, m);
        merge_sort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int main(void) {
    const int N = 10000;
    int *data = malloc(N * sizeof(int));
    srand(42);
    for (int run = 0; run < 3; run++) {
        for (int i = 0; i < N; i++) data[i] = rand() % 100000;
        merge_sort(data, 0, N - 1);
    }
    /* Quick verify */
    int sorted = 1;
    for (int i = 1; i < N; i++) {
        if (data[i] < data[i-1]) { sorted = 0; break; }
    }
    printf("OK: sorted %d elements, verified=%d\n", N, sorted);
    free(data);
    return 0;
}
