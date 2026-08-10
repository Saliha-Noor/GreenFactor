// Automatically generated from Backend/config/repos.yaml (120 repositories)
export const realBenchmarkRepos = [
  {
    "name": "TheAlgorithms_Python",
    "language": "python",
    "entrypoint": "sorts/merge_sort.py",
    "url": "https://github.com/TheAlgorithms/Python",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "requests",
    "language": "python",
    "entrypoint": "src/requests/adapters.py",
    "url": "https://github.com/psf/requests",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "flask",
    "language": "python",
    "entrypoint": "src/flask/app.py",
    "url": "https://github.com/pallets/flask",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "click",
    "language": "python",
    "entrypoint": "src/click/core.py",
    "url": "https://github.com/pallets/click",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "rich",
    "language": "python",
    "entrypoint": "rich/console.py",
    "url": "https://github.com/Textualize/rich",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "httpx",
    "language": "python",
    "entrypoint": "httpx/_client.py",
    "url": "https://github.com/encode/httpx",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "faker",
    "language": "python",
    "entrypoint": "faker/proxy.py",
    "url": "https://github.com/joke2k/faker",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "gunicorn",
    "language": "python",
    "entrypoint": "gunicorn/workers/base.py",
    "url": "https://github.com/benoitc/gunicorn",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "typer",
    "language": "python",
    "entrypoint": "typer/main.py",
    "url": "https://github.com/tiangolo/typer",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "pydantic",
    "language": "python",
    "entrypoint": "pydantic/main.py",
    "url": "https://github.com/pydantic/pydantic",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "tqdm",
    "language": "python",
    "entrypoint": "tqdm/std.py",
    "url": "https://github.com/tqdm/tqdm",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "black",
    "language": "python",
    "entrypoint": "src/black/__init__.py",
    "url": "https://github.com/psf/black",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "sqlalchemy",
    "language": "python",
    "entrypoint": "lib/sqlalchemy/engine/base.py",
    "url": "https://github.com/sqlalchemy/sqlalchemy",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "scrapy",
    "language": "python",
    "entrypoint": "scrapy/core/engine.py",
    "url": "https://github.com/scrapy/scrapy",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Inherently network-bound and non-deterministic.",
    "patterns_checked": 0
  },
  {
    "name": "tornado",
    "language": "python",
    "entrypoint": "tornado/ioloop.py",
    "url": "https://github.com/tornadoweb/tornado",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "TheAlgorithms_Javascript",
    "language": "javascript",
    "entrypoint": "Sorts/MergeSort.js",
    "url": "https://github.com/TheAlgorithms/Javascript",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "lodash",
    "language": "javascript",
    "entrypoint": "lodash.js",
    "url": "https://github.com/lodash/lodash",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "axios",
    "language": "javascript",
    "entrypoint": "lib/axios.js",
    "url": "https://github.com/axios/axios",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "express",
    "language": "javascript",
    "entrypoint": "lib/router/index.js",
    "url": "https://github.com/expressjs/express",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "chart_js",
    "language": "javascript",
    "entrypoint": "src/core/core.controller.js",
    "url": "https://github.com/chartjs/Chart.js",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings.",
    "patterns_checked": 0
  },
  {
    "name": "moment",
    "language": "javascript",
    "entrypoint": "src/moment.js",
    "url": "https://github.com/moment/moment",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "socket_io",
    "language": "javascript",
    "entrypoint": "lib/index.js",
    "url": "https://github.com/socketio/socket.io",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "d3",
    "language": "javascript",
    "entrypoint": "src/index.js",
    "url": "https://github.com/d3/d3",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings.",
    "patterns_checked": 0
  },
  {
    "name": "webpack",
    "language": "javascript",
    "entrypoint": "lib/Compiler.js",
    "url": "https://github.com/webpack/webpack",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a target project to compile; highly variable based on target source.",
    "patterns_checked": 0
  },
  {
    "name": "eslint",
    "language": "javascript",
    "entrypoint": "lib/linter/linter.js",
    "url": "https://github.com/eslint/eslint",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool; benchmarking linting performance varies wildly based on the target source code.",
    "patterns_checked": 0
  },
  {
    "name": "commander",
    "language": "javascript",
    "entrypoint": "lib/commander.js",
    "url": "https://github.com/tj/commander.js",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "jquery",
    "language": "javascript",
    "entrypoint": "src/jquery.js",
    "url": "https://github.com/jquery/jquery",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings.",
    "patterns_checked": 0
  },
  {
    "name": "vue",
    "language": "javascript",
    "entrypoint": "src/core/index.js",
    "url": "https://github.com/vuejs/vue",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings.",
    "patterns_checked": 0
  },
  {
    "name": "koa",
    "language": "javascript",
    "entrypoint": "lib/application.js",
    "url": "https://github.com/koajs/koa",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "react",
    "language": "javascript",
    "entrypoint": "packages/react/src/React.js",
    "url": "https://github.com/facebook/react",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings.",
    "patterns_checked": 0
  },
  {
    "name": "TheAlgorithms_Java",
    "language": "java",
    "entrypoint": "src/main/java/com/thealgorithms/sorts/MergeSort.java",
    "url": "https://github.com/TheAlgorithms/Java",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "guava",
    "language": "java",
    "entrypoint": "guava/src/com/google/common/collect/ImmutableList.java",
    "url": "https://github.com/google/guava",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "commons_lang",
    "language": "java",
    "entrypoint": "src/main/java/org/apache/commons/lang3/StringUtils.java",
    "url": "https://github.com/apache/commons-lang",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "jsoup",
    "language": "java",
    "entrypoint": "src/main/java/org/jsoup/parser/HtmlTreeBuilder.java",
    "url": "https://github.com/jhy/jsoup",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "junit4",
    "language": "java",
    "entrypoint": "src/main/java/org/junit/runners/BlockJUnit4ClassRunner.java",
    "url": "https://github.com/junit-team/junit4",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (test framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "java_design_patterns",
    "language": "java",
    "entrypoint": "singleton/src/main/java/com/iluwatar/singleton/App.java",
    "url": "https://github.com/iluwatar/java-design-patterns",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Repo is a design-pattern showcase (Singleton example); no natural sustained workload exists, and looping the trivial call artificially would measure loop/JIT overhead rather than genuine program behavior.",
    "patterns_checked": 0
  },
  {
    "name": "rxjava",
    "language": "java",
    "entrypoint": "src/main/java/io/reactivex/rxjava3/core/Observable.java",
    "url": "https://github.com/ReactiveX/RxJava",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "gson",
    "language": "java",
    "entrypoint": "gson/src/main/java/com/google/gson/Gson.java",
    "url": "https://github.com/google/gson",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "commons_io",
    "language": "java",
    "entrypoint": "src/main/java/org/apache/commons/io/FileUtils.java",
    "url": "https://github.com/apache/commons-io",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "commons_collections",
    "language": "java",
    "entrypoint": "src/main/java/org/apache/commons/collections4/CollectionUtils.java",
    "url": "https://github.com/apache/commons-collections",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "okhttp",
    "language": "java",
    "entrypoint": "okhttp/src/main/kotlin/okhttp3/OkHttpClient.kt",
    "url": "https://github.com/square/okhttp",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "retrofit",
    "language": "java",
    "entrypoint": "retrofit/src/main/java/retrofit2/Retrofit.java",
    "url": "https://github.com/square/retrofit",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "commons_csv",
    "language": "java",
    "entrypoint": "src/main/java/org/apache/commons/csv/CSVParser.java",
    "url": "https://github.com/apache/commons-csv",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "jackson_databind",
    "language": "java",
    "entrypoint": "src/main/java/com/fasterxml/jackson/databind/ObjectMapper.java",
    "url": "https://github.com/FasterXML/jackson-databind",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "vertx",
    "language": "java",
    "entrypoint": "vertx-core/src/main/java/io/vertx/core/impl/VertxImpl.java",
    "url": "https://github.com/eclipse-vertx/vert.x",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "TheAlgorithms_C",
    "language": "c",
    "entrypoint": "sorting/merge_sort.c",
    "url": "https://github.com/TheAlgorithms/C",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "stb",
    "language": "c",
    "entrypoint": "stb_image.h",
    "url": "https://github.com/nothings/stb",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "cJSON",
    "language": "c",
    "entrypoint": "cJSON.c",
    "url": "https://github.com/DaveGamble/cJSON",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "lz4",
    "language": "c",
    "entrypoint": "lib/lz4.c",
    "url": "https://github.com/lz4/lz4",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "zlib",
    "language": "c",
    "entrypoint": "deflate.c",
    "url": "https://github.com/madler/zlib",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "mongoose",
    "language": "c",
    "entrypoint": "mongoose.c",
    "url": "https://github.com/cesanta/mongoose",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "sqlite",
    "language": "c",
    "entrypoint": "workloads/c/sqlite_cli.c",
    "url": "https://github.com/sqlite/sqlite",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "No isolatable refactor target without a custom multi-file build pipeline; would require Makefile/CMake integration out of scope for this project.",
    "patterns_checked": 0
  },
  {
    "name": "redis",
    "language": "c",
    "entrypoint": "src/server.c",
    "url": "https://github.com/redis/redis",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "No isolatable refactor target without a custom multi-file build pipeline; would require Makefile/CMake integration out of scope for this project.",
    "patterns_checked": 0
  },
  {
    "name": "jq",
    "language": "c",
    "entrypoint": "src/execute.c",
    "url": "https://github.com/jqlang/jq",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "No isolatable refactor target without a custom multi-file build pipeline; would require Makefile/CMake integration out of scope for this project.",
    "patterns_checked": 0
  },
  {
    "name": "tiny_aes",
    "language": "c",
    "entrypoint": "aes.c",
    "url": "https://github.com/kokke/tiny-AES-c",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "zstd",
    "language": "c",
    "entrypoint": "lib/compress/zstd_compress.c",
    "url": "https://github.com/facebook/zstd",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "curl",
    "language": "c",
    "entrypoint": "lib/transfer.c",
    "url": "https://github.com/curl/curl",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "No isolatable refactor target without a custom multi-file build pipeline; would require Makefile/CMake integration out of scope for this project.",
    "patterns_checked": 0
  },
  {
    "name": "libuv",
    "language": "c",
    "entrypoint": "src/unix/core.c",
    "url": "https://github.com/libuv/libuv",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "uthash",
    "language": "c",
    "entrypoint": "src/uthash.h",
    "url": "https://github.com/troydhanson/uthash",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "lua",
    "language": "c",
    "entrypoint": "lvm.c",
    "url": "https://github.com/lua/lua",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "TheAlgorithms_CPP",
    "language": "cpp",
    "entrypoint": "sorting/merge_sort.cpp",
    "url": "https://github.com/TheAlgorithms/C-Plus-Plus",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "nlohmann_json",
    "language": "cpp",
    "entrypoint": "single_include/nlohmann/json.hpp",
    "url": "https://github.com/nlohmann/json",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "simdjson",
    "language": "cpp",
    "entrypoint": "src/simdjson.cpp",
    "url": "https://github.com/simdjson/simdjson",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "fmt",
    "language": "cpp",
    "entrypoint": "src/format.cc",
    "url": "https://github.com/fmtlib/fmt",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "catch2",
    "language": "cpp",
    "entrypoint": "src/catch2/catch_session.cpp",
    "url": "https://github.com/catchorg/Catch2",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (test framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "spdlog",
    "language": "cpp",
    "entrypoint": "src/spdlog.cpp",
    "url": "https://github.com/gabime/spdlog",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "abseil_cpp",
    "language": "cpp",
    "entrypoint": "absl/strings/str_cat.cc",
    "url": "https://github.com/abseil/abseil-cpp",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "leveldb",
    "language": "cpp",
    "entrypoint": "db/db_impl.cc",
    "url": "https://github.com/google/leveldb",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "fifo_map",
    "language": "cpp",
    "entrypoint": "src/fifo_map.hpp",
    "url": "https://github.com/nlohmann/fifo_map",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "rapidjson",
    "language": "cpp",
    "entrypoint": "include/rapidjson/document.h",
    "url": "https://github.com/Tencent/rapidjson",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "googletest",
    "language": "cpp",
    "entrypoint": "googletest/src/gtest.cc",
    "url": "https://github.com/google/googletest",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (test framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "cli11",
    "language": "cpp",
    "entrypoint": "include/CLI/App.hpp",
    "url": "https://github.com/CLIUtils/CLI11",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "entt",
    "language": "cpp",
    "entrypoint": "src/entt/entity/registry.hpp",
    "url": "https://github.com/skypjack/entt",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "taskflow",
    "language": "cpp",
    "entrypoint": "taskflow/core/executor.hpp",
    "url": "https://github.com/taskflow/taskflow",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "ncnn",
    "language": "cpp",
    "entrypoint": "src/net.cpp",
    "url": "https://github.com/Tencent/ncnn",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "TheAlgorithms_Go",
    "language": "go",
    "entrypoint": "sort/mergesort.go",
    "url": "https://github.com/TheAlgorithms/Go",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "gin",
    "language": "go",
    "entrypoint": "gin.go",
    "url": "https://github.com/gin-gonic/gin",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "gorilla_mux",
    "language": "go",
    "entrypoint": "mux.go",
    "url": "https://github.com/gorilla/mux",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "cobra",
    "language": "go",
    "entrypoint": "command.go",
    "url": "https://github.com/spf13/cobra",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "viper",
    "language": "go",
    "entrypoint": "viper.go",
    "url": "https://github.com/spf13/viper",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "logrus",
    "language": "go",
    "entrypoint": "logrus.go",
    "url": "https://github.com/sirupsen/logrus",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "fiber",
    "language": "go",
    "entrypoint": "app.go",
    "url": "https://github.com/gofiber/fiber",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "fasthttp",
    "language": "go",
    "entrypoint": "server.go",
    "url": "https://github.com/valyala/fasthttp",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "urfave_cli",
    "language": "go",
    "entrypoint": "app.go",
    "url": "https://github.com/urfave/cli",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "go_redis",
    "language": "go",
    "entrypoint": "redis.go",
    "url": "https://github.com/go-redis/redis",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "badger",
    "language": "go",
    "entrypoint": "db.go",
    "url": "https://github.com/dgraph-io/badger",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "zap",
    "language": "go",
    "entrypoint": "logger.go",
    "url": "https://github.com/uber-go/zap",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "echo",
    "language": "go",
    "entrypoint": "echo.go",
    "url": "https://github.com/labstack/echo",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "bbolt",
    "language": "go",
    "entrypoint": "db.go",
    "url": "https://github.com/etcd-io/bbolt",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "prometheus",
    "language": "go",
    "entrypoint": "cmd/prometheus/main.go",
    "url": "https://github.com/prometheus/prometheus",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "TheAlgorithms_Rust",
    "language": "rust",
    "entrypoint": "src/sorting/merge_sort.rs",
    "url": "https://github.com/TheAlgorithms/Rust",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "ripgrep",
    "language": "rust",
    "entrypoint": "crates/core/main.rs",
    "url": "https://github.com/BurntSushi/ripgrep",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "serde",
    "language": "rust",
    "entrypoint": "serde/src/lib.rs",
    "url": "https://github.com/serde-rs/serde",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "tokio",
    "language": "rust",
    "entrypoint": "tokio/src/runtime/runtime.rs",
    "url": "https://github.com/tokio-rs/tokio",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "mdbook",
    "language": "rust",
    "entrypoint": "src/main.rs",
    "url": "https://github.com/rust-lang/mdBook",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "clap",
    "language": "rust",
    "entrypoint": "clap_builder/src/builder/command.rs",
    "url": "https://github.com/clap-rs/clap",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "rayon",
    "language": "rust",
    "entrypoint": "rayon-core/src/lib.rs",
    "url": "https://github.com/rayon-rs/rayon",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "hyper",
    "language": "rust",
    "entrypoint": "src/client/conn/http1.rs",
    "url": "https://github.com/hyperium/hyper",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "actix_web",
    "language": "rust",
    "entrypoint": "actix-web/src/app.rs",
    "url": "https://github.com/actix/actix-web",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "bat",
    "language": "rust",
    "entrypoint": "src/main.rs",
    "url": "https://github.com/sharkdp/bat",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "fd",
    "language": "rust",
    "entrypoint": "src/main.rs",
    "url": "https://github.com/sharkdp/fd",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "starship",
    "language": "rust",
    "entrypoint": "src/main.rs",
    "url": "https://github.com/starship/starship",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "rustlings",
    "language": "rust",
    "entrypoint": "src/main.rs",
    "url": "https://github.com/rust-lang/rustlings",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "alacritty",
    "language": "rust",
    "entrypoint": "alacritty/src/main.rs",
    "url": "https://github.com/alacritty/alacritty",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "tikv",
    "language": "rust",
    "entrypoint": "src/server/server.rs",
    "url": "https://github.com/tikv/tikv",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available.",
    "patterns_checked": 0
  },
  {
    "name": "TheAlgorithms_CSharp",
    "language": "csharp",
    "entrypoint": "Algorithms/Sorters/Comparison/MergeSorter.cs",
    "url": "https://github.com/TheAlgorithms/C-Sharp",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "automapper",
    "language": "csharp",
    "entrypoint": "src/AutoMapper/Mapper.cs",
    "url": "https://github.com/AutoMapper/AutoMapper",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "newtonsoft_json",
    "language": "csharp",
    "entrypoint": "Src/Newtonsoft.Json/JsonConvert.cs",
    "url": "https://github.com/JamesNK/Newtonsoft.Json",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "serilog",
    "language": "csharp",
    "entrypoint": "src/Serilog/Core/Logger.cs",
    "url": "https://github.com/serilog/serilog",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "restsharp",
    "language": "csharp",
    "entrypoint": "src/RestSharp/RestClient.cs",
    "url": "https://github.com/restsharp/RestSharp",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "moq",
    "language": "csharp",
    "entrypoint": "src/Moq/Mock.cs",
    "url": "https://github.com/moq/moq",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (mocking framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "fluentvalidation",
    "language": "csharp",
    "entrypoint": "src/FluentValidation/AbstractValidator.cs",
    "url": "https://github.com/FluentValidation/FluentValidation",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (validation framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "nlog",
    "language": "csharp",
    "entrypoint": "src/NLog/Logger.cs",
    "url": "https://github.com/NLog/NLog",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "xunit",
    "language": "csharp",
    "entrypoint": "src/xunit.v3.core/Framework/TheoryDiscoverer.cs",
    "url": "https://github.com/xunit/xunit",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Meta-tool (test framework); requires a target project to exercise meaningfully.",
    "patterns_checked": 0
  },
  {
    "name": "polly",
    "language": "csharp",
    "entrypoint": "src/Polly.Core/ResiliencePipeline.cs",
    "url": "https://github.com/App-vNext/Polly",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "humanizer",
    "language": "csharp",
    "entrypoint": "src/Humanizer/StringHumanizeExtensions.cs",
    "url": "https://github.com/Humanizr/Humanizer",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "masstransit",
    "language": "csharp",
    "entrypoint": "src/MassTransit/MassTransit/Bus.cs",
    "url": "https://github.com/MassTransit/MassTransit",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Distributed messaging framework requiring live brokers.",
    "patterns_checked": 0
  },
  {
    "name": "stateless",
    "language": "csharp",
    "entrypoint": "src/Stateless/StateMachine.cs",
    "url": "https://github.com/dotnet-state-machine/stateless",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  },
  {
    "name": "akka_net",
    "language": "csharp",
    "entrypoint": "src/core/Akka/Actor/ActorBase.cs",
    "url": "https://github.com/akkadotnet/akka.net",
    "status": "Excluded",
    "excluded": true,
    "exclusion_reason": "Distributed messaging framework requiring live brokers.",
    "patterns_checked": 0
  },
  {
    "name": "reactiveui",
    "language": "csharp",
    "entrypoint": "src/ReactiveUI/ReactiveObject.cs",
    "url": "https://github.com/reactiveui/ReactiveUI",
    "status": "Configured & Ingested",
    "excluded": false,
    "exclusion_reason": null,
    "patterns_checked": 8
  }
];
