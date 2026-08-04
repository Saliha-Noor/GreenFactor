// Workload driver for TheAlgorithms_Go — sort/mergesort.go
// Self-contained merge sort workload.
// Build: go build -o algo_go_driver workloads/go/TheAlgorithms_Go_driver.go
package main

import (
	"fmt"
	"math/rand"
	"sort"
)

func mergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}
	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])
	return merge(left, right)
}

func merge(left, right []int) []int {
	result := make([]int, 0, len(left)+len(right))
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
	result = append(result, left[i:]...)
	result = append(result, right[j:]...)
	return result
}

func main() {
	const N = 10000
	data := make([]int, N)
	rng := rand.New(rand.NewSource(42))
	var result []int
	for run := 0; run < 3; run++ {
		for i := range data {
			data[i] = rng.Intn(100000)
		}
		result = mergeSort(data)
	}
	sorted := sort.IntsAreSorted(result)
	fmt.Printf("OK: sorted %d elements, verified=%v\n", N, sorted)
}
