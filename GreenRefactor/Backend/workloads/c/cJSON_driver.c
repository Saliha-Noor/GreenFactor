/* Workload driver for cJSON — cJSON.c
 * Creates, traverses, and frees a large JSON tree using cJSON's API.
 * Compile: gcc -O2 workloads/c/cJSON_driver.c repos/c/cJSON/cJSON.c -I repos/c/cJSON -o cjson_driver -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Try to include cJSON from the repo */
#include "cJSON.h"

int main(void) {
    const int N = 1000;
    
    for (int run = 0; run < 3; run++) {
        cJSON *root = cJSON_CreateArray();
        for (int i = 0; i < N; i++) {
            cJSON *item = cJSON_CreateObject();
            cJSON_AddNumberToObject(item, "id", i);
            cJSON_AddStringToObject(item, "name", "benchmark_item");
            cJSON_AddNumberToObject(item, "value", i * 3.14);
            cJSON_AddItemToArray(root, item);
        }
        
        /* Serialize to string */
        char *json_str = cJSON_PrintUnformatted(root);
        
        /* Parse it back */
        cJSON *parsed = cJSON_Parse(json_str);
        int count = cJSON_GetArraySize(parsed);
        
        free(json_str);
        cJSON_Delete(parsed);
        cJSON_Delete(root);
    }
    
    printf("OK: created/serialized/parsed %d JSON objects\n", N);
    return 0;
}
