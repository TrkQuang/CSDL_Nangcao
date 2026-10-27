# QUY TRINH THIET KE VAT LY VA BENCHMARK

## Completed Task 5 run

Verified run: `results/runs/20261027T115624004654Z/` on PostgreSQL 16.15.
360 measurements cover 3 sizes, 4 models, 2 index modes, 3 workloads and 5 repeats.

- Report: `../report/task5_benchmark_results.md`.
- Experiment log: `../docs/experiment_log/task5_completed.md`.
- Slide content: `../slides/task5_benchmark.md`.
- Results: `results/benchmark_results.csv`, `results/benchmark_summary.md`, `results/charts/`.
- Corpus verification: `results/generated_data_manifest.json`.

### Safe full reproduction on Windows

```powershell
python -m pip install -r benchmark/requirements.txt
python benchmark/scripts/run_complete.py --postgres-bin "C:/Program Files/PostgreSQL/16/bin"
python benchmark/scripts/gen_tree_data.py --sizes 1000 10000 100000
python benchmark/scripts/gen_graph_data.py --all
python benchmark/scripts/verify_generated_data.py
python benchmark/scripts/verify_tree_shapes.py
```

The runner creates a fresh private SCRAM-protected cluster on a free loopback
port. No existing PostgreSQL password is needed. Existing databases are not
modified. The cluster stops and is removed after the run. Python must have
`psycopg2-binary` and `matplotlib`; the PostgreSQL bin directory must contain
`initdb`, `pg_ctl` and `psql`. Run from the repository root.

When the runner prints a completed run path, publish it:

```powershell
python benchmark/scripts/publish_results.py --run-dir benchmark/results/runs/20261027T115624004654Z
```

Replace the example run path with the new run path. Publication preserves old
CSV measurements in `results/archive/` before updating the central results.
The publication step generates Vietnamese report, slide content and log.

### Additional tree shapes and FD regression checks

`verify_tree_shapes.py` generates random trees at 1k/10k/100k nodes and a
1k-node chain, cross-checks all four CSV representations, and regenerates each
dataset to verify byte-for-byte reproducibility. Seed defaults to 42.
Results: `results/tree_shapes_manifest.json`. These are corpus checks, not
additional timing results; the published benchmark still uses the ternary tree.
Chain generation is capped at 1k nodes because closure storage is quadratic.

```powershell
python benchmark/scripts/gen_tree_data.py --shape random --sizes 1000 10000 100000
python benchmark/scripts/gen_tree_data.py --shape chain --sizes 1000
```

The isolated full runner also executes `validate_fd.py` on the small seed.
Temporary unconstrained copies deliberately contain conflicting dependent
attributes, including NULL/non-NULL parent IDs. Every malformed case must raise
an exception; rollback restores the valid data. Assertions cover the complete
rows for f1-f5 and BR2/BR6/BR9. Passing finite data checks supports, but does not
prove, the business dependencies defined by Task 1.

### Measurement semantics

`has_index=false` retains PK/UNIQUE constraint indexes; it does not mean zero
indexes. The runner removes all unconstrained secondary indexes from the five
benchmark relations, then adds `indexes.sql` in the indexed phase. All index
changes are rolled back before closing the connection. Use a dedicated database
to avoid blocking other users while measuring.

Read and storage measurements happen before write workloads. INSERT adds a leaf
under node 2; UPDATE moves leaf N under node 2. These operations update the base
comment row plus the selected model's metadata. Savepoints roll writes back;
sequence gaps, WAL and physical dead tuples are possible. Results are warm-cache
execution times, not COMMIT latency or whole-subtree update throughput.
Raw JSON plans and storage/index snapshots are retained in each run's artifacts.

`database/seed_bench.sql` truncates existing application data. Do not run it on a
database containing data you need to retain; use the isolated full runner instead.

## Muc tieu

Do hieu nang Q2 (lay toan bo hau due) tren 4 mo hinh cay voi cung du lieu va cung node goc:

- Adjacency List: `comment`.
- Path Enumeration: `comment_path` (`ltree`).
- Nested Set: `comment_ns`.
- Closure Table: `comment_closure`.

Moi phep do chay mot lan warm-up, sau do lap 5 lan. Script luu tung lan chay, trung vi nam trong cot `notes`.

## Ke hoach chi muc

| Mo hinh | Chi muc | Truy van muc tieu |
| --- | --- | --- |
| Adjacency List | B-tree `(post_id, parent_id)` | Tim con truc tiep trong CTE de quy |
| Path Enumeration | GiST `(path)`, B-tree `(post_id)` | `path <@ root.path` |
| Nested Set | B-tree `(post_id, lft, rgt)` | `lft BETWEEN root.lft AND root.rgt` |
| Closure Table | B-tree `(ancestor, depth, descendant)`, `(descendant, ancestor)` | Lay hau due va to tien |
| Friendship | B-tree `(user_b, user_a)` | Duyet `friend_edge` hai chieu |

File `benchmark/indexes.sql` tao toan bo chi muc. Runner tu dong drop/tao cac chi muc nay khi dung `--mode both`.

## Chuan bi

```powershell
pip install -r benchmark/requirements.txt
psql -d social_learning -f database/schema.sql
psql -d social_learning -v bench_size=1000 -f database/seed_bench.sql
```

Lap lai lenh seed voi `bench_size=10000` va `bench_size=100000`. Seed tao cay tam phan co do sau xap xi 7, 9, 11; dong bo du lieu sang ca 4 mo hinh.

## Chay benchmark

Dat chuoi ket noi PostgreSQL vao `DATABASE_URL`, hoac truyen `--dsn`.

```powershell
$env:DATABASE_URL = 'postgresql://postgres:password@localhost:5432/social_learning'
python benchmark/scripts/run_benchmark.py --dataset-size 1000 --repeats 5 --mode both
```

Chay cho 3 quy mo:

```powershell
python benchmark/scripts/run_benchmark.py --dataset-size 1000 --repeats 5 --mode both
python benchmark/scripts/run_benchmark.py --dataset-size 10000 --repeats 5 --mode both
python benchmark/scripts/run_benchmark.py --dataset-size 100000 --repeats 5 --mode both
```

Ket qua them vao `benchmark/results/benchmark_results.csv`. Cac chi so:

- `execution_time_ms`, `planning_time_ms`.
- `shared_hit_blocks`, `shared_read_blocks`.
- `plan_node_type` tu plan goc.
- `has_index=false/true` de so sanh truoc va sau indexing.

Khong dien so lieu mau vao CSV. Chi ghi so do tu lan chay that va chep ma thi nghiem vao `docs/experiment_log/`.

## Ve bieu do tu so do that

Sau khi CSV co ket qua Q2, tao PNG cho bao cao va slide:

```powershell
python benchmark/scripts/plot_results.py
```

Script tao `benchmark/results/charts/q2_subtree_1000.png`, `q2_subtree_10000.png`
va `q2_subtree_100000.png` neu CSV co du lieu tuong ung. Script dung trung vi
cua cac lan lap, khong tu dien gia tri mau khi CSV rong.

## Tong hop bao cao va dung luong

```powershell
psql -d social_learning -f benchmark/storage_sizes.sql
python benchmark/scripts/summarize_results.py
```

`storage_sizes.sql` tra ve dung luong bang/index de ghi vao nhat ky. Script
summary tao `benchmark/results/benchmark_summary.md` tu trung vi so do Q2.

## Sinh CSV ngoai DB

Hai script nay phuc vu `COPY`/Neo4j import va kiem tra du lieu doc lap:

```powershell
python benchmark/scripts/gen_tree_data.py --sizes 1000 10000 100000
python benchmark/scripts/gen_graph_data.py --all
```

File cay: `comment`, `comment_path`, `comment_ns`, `comment_closure`.
File do thi: CSV PostgreSQL (`users`, `friendship`) va CSV Neo4j (`neo4j_users`, `neo4j_friendship`).
