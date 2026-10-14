# NHAT KY BENCHMARK

Tao mot file moi cho moi lan chay, vi du `docs/experiment_log/benchmark_2026-10-14_1000.md`.

## Moi truong

- **Ngay chay:** `YYYY-MM-DD`
- **Nguoi chay:** Quynh (TV5)
- **May:** CPU / RAM / SSD
- **He dieu hanh:**
- **PostgreSQL:** `SELECT version();`
- **Cau hinh lien quan:** `shared_buffers`, `work_mem`, `effective_cache_size`
- **Commit:** `git rev-parse --short HEAD`
- **Lenh seed:** `psql -d <db> -v bench_size=<N> -f database/seed_bench.sql`
- **Lenh benchmark:** `python benchmark/scripts/run_benchmark.py --dataset-size <N> --repeats 5 --mode both`

## Ket qua

| Mo hinh | Index | Q2 median (ms) | Planning (ms) | Hit | Read | Plan goc | Nhan xet |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Adjacency List | Khong/Co |  |  |  |  |  |  |
| Path Enumeration | Khong/Co |  |  |  |  |  |  |
| Nested Set | Khong/Co |  |  |  |  |  |  |
| Closure Table | Khong/Co |  |  |  |  |  |  |

## Ket luan

- Chi dung so lieu trong `benchmark/results/benchmark_results.csv`.
- Ghi ro neu cold cache, loi ket noi, hoac plan khong dung index.
- Khong ket luan mo hinh nao luon nhanh hon; ket luan theo N, query, index, va chi phi ghi.