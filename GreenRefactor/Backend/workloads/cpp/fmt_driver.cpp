/* Workload driver for fmt — src/format.cc
 * Exercises fmt's string formatting with many iterations.
 * Compile: g++ -O2 -std=c++17 -I repos/cpp/fmt/include workloads/cpp/fmt_driver.cpp repos/cpp/fmt/src/format.cc -o fmt_driver
 */
#include <cstdio>
#include <string>

/* Try to include fmt from the repo */
#ifdef __has_include
#if __has_include("fmt/format.h")
#include "fmt/format.h"
#define HAS_FMT 1
#endif
#endif

#ifndef HAS_FMT
#define HAS_FMT 0
#endif

int main() {
    const int N = 50000;
    
#if HAS_FMT
    std::string result;
    for (int i = 0; i < N; i++) {
        result = fmt::format("item_{}: value={:.4f}, hex={:#x}", i, i * 3.14159, i);
    }
    printf("OK: formatted %d strings with fmt, last=%s\n", N, result.c_str());
#else
    /* Fallback: use snprintf */
    char buf[256];
    for (int i = 0; i < N; i++) {
        snprintf(buf, sizeof(buf), "item_%d: value=%.4f, hex=0x%x", i, i * 3.14159, i);
    }
    printf("OK: formatted %d strings (fmt not available, used snprintf)\n", N);
#endif
    return 0;
}
