# QUY TRINH THIET KE VAT LY VA BENCHMARK

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

## Sinh CSV ngoai DB

Hai script nay phuc vu `COPY`/Neo4j import va kiem tra du lieu doc lap:

```powershell
python benchmark/scripts/gen_tree_data.py --sizes 1000 10000 100000
python benchmark/scripts/gen_graph_data.py --all
```

File cay: `comment`, `comment_path`, `comment_ns`, `comment_closure`.
File do thi: CSV PostgreSQL (`users`, `friendship`) va CSV Neo4j (`neo4j_users`, `neo4j_friendship`).