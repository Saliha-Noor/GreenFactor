CREATE TABLE benchmark_data (id INTEGER PRIMARY KEY, value TEXT, metric REAL);
WITH RECURSIVE cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x<20000)
INSERT INTO benchmark_data (value, metric) SELECT hex(randomblob(16)), random() FROM cnt;
SELECT count(*), avg(metric), sum(metric) FROM benchmark_data WHERE metric > 0.5;
SELECT value FROM benchmark_data ORDER BY metric DESC LIMIT 100;
DROP TABLE benchmark_data;
