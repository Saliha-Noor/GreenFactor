/**
 * Workload driver for TheAlgorithms_CSharp — MergeSorter.cs
 * Self-contained merge sort workload.
 * Run: dotnet run (after creating a minimal .csproj)
 */
using System;

class TheAlgorithms_CSharp_Driver
{
    static void Merge(int[] arr, int l, int m, int r)
    {
        int n1 = m - l + 1, n2 = r - m;
        int[] L = new int[n1], R = new int[n2];
        Array.Copy(arr, l, L, 0, n1);
        Array.Copy(arr, m + 1, R, 0, n2);
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2)
        {
            if (L[i] <= R[j]) arr[k++] = L[i++];
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    static void MergeSort(int[] arr, int l, int r)
    {
        if (l < r)
        {
            int m = l + (r - l) / 2;
            MergeSort(arr, l, m);
            MergeSort(arr, m + 1, r);
            Merge(arr, l, m, r);
        }
    }

    static void Main(string[] args)
    {
        const int N = 10000;
        int[] data = new int[N];
        var rng = new Random(42);
        for (int run = 0; run < 3; run++)
        {
            for (int i = 0; i < N; i++) data[i] = rng.Next(100000);
            MergeSort(data, 0, N - 1);
        }
        bool sorted = true;
        for (int i = 1; i < N; i++)
        {
            if (data[i] < data[i - 1]) { sorted = false; break; }
        }
        Console.WriteLine($"OK: sorted {N} elements, verified={sorted}");
    }
}
