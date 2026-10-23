-- Run after seed_bench.sql and again after benchmark/indexes.sql.
-- psql -d detai17_db -f benchmark/storage_sizes.sql

WITH relations(relation_name) AS (
    VALUES
        ('comment'::regclass),
        ('comment_path'::regclass),
        ('comment_ns'::regclass),
        ('comment_closure'::regclass),
        ('friendship'::regclass)
)
SELECT relation_name::text AS relation_name,
       pg_relation_size(relation_name) AS table_bytes,
       pg_indexes_size(relation_name) AS index_bytes,
       pg_total_relation_size(relation_name) AS total_bytes,
       pg_size_pretty(pg_relation_size(relation_name)) AS table_size,
       pg_size_pretty(pg_indexes_size(relation_name)) AS index_size,
       pg_size_pretty(pg_total_relation_size(relation_name)) AS total_size
FROM relations
ORDER BY relation_name::text;
