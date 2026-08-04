/**
 * Workload driver for TheAlgorithms_Java — MergeSort.java
 * Self-contained merge sort workload.
 * Compile: javac workloads/java/TheAlgorithms_Java_Driver.java
 * Run: java -cp workloads/java TheAlgorithms_Java_Driver
 */
import java.util.Random;

public class TheAlgorithms_Java_Driver {
    
    static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1, n2 = r - m;
        int[] L = new int[n1], R = new int[n2];
        System.arraycopy(arr, l, L, 0, n1);
        System.arraycopy(arr, m + 1, R, 0, n2);
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) arr[k++] = L[i++];
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }
    
    static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }
    
    public static void main(String[] args) {
        final int N = 10000;
        int[] data = new int[N];
        Random rng = new Random(42);
        for (int run = 0; run < 3; run++) {
            for (int i = 0; i < N; i++) data[i] = rng.nextInt(100000);
            mergeSort(data, 0, N - 1);
        }
        boolean sorted = true;
        for (int i = 1; i < N; i++) {
            if (data[i] < data[i-1]) { sorted = false; break; }
        }
        System.out.printf("OK: sorted %d elements, verified=%b%n", N, sorted);
    }
}
