"""Publish a completed benchmark run, preserving older local measurements."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "benchmark" / "results"
MODELS = ("Adjacency List", "Path Enumeration", "Nested Set", "Closure Table")


def write_markdown(path: Path, content: str) -> None:
    patch = "*** Begin Patch\n"
    if path.exists():
        patch += f"*** Delete File: {path.as_posix()}\n"
    patch += f"*** Add File: {path.as_posix()}\n"
    patch += "\n".join("+" + line for line in content.splitlines()) + "\n*** End Patch\n"
    subprocess.run(["apply_patch", patch], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    if not run_dir.is_relative_to((RESULTS / "runs").resolve()):
        parser.error("--run-dir must be inside benchmark/results/runs")
    completion = json.loads((run_dir / "completion.json").read_text(encoding="utf-8"))
    if completion["status"] != "passed":
        raise SystemExit("Cannot publish incomplete run")
    with (run_dir / "benchmark_results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 360:
        raise SystemExit("Publication requires full run: 3 sizes x 4 models x 2 index modes x 3 queries x 5 repeats")
    groups = defaultdict(list)
    for row in rows:
        key = (int(row["dataset_size"]), row["query_code"], row["target_model"], row["has_index"] == "true")
        groups[key].append(float(row["execution_time_ms"]))
    if len(groups) != 72 or any(len(values) != 5 for values in groups.values()):
        raise SystemExit("Run has missing or duplicate measurement groups")
    medians = {key: statistics.median(values) for key, values in groups.items()}
    environment = json.loads((run_dir / "environment.json").read_text(encoding="utf-8"))
    archive = RESULTS / "archive"
    archive.mkdir(exist_ok=True)
    existing = RESULTS / "benchmark_results.csv"
    if existing.exists() and existing.read_bytes() != (run_dir / "benchmark_results.csv").read_bytes():
        backup = archive / f"benchmark_results_before_{run_dir.name}.csv"
        if not backup.exists():
            shutil.copy2(existing, backup)
    shutil.copy2(run_dir / "benchmark_results.csv", existing)
    subprocess.run([sys.executable, str(ROOT / "benchmark/scripts/summarize_results.py"),
                    "--input", str(existing), "--output", str(RESULTS / "benchmark_summary.md"),
                    "--artifacts-dir", str(run_dir / "artifacts")], check=True)
    subprocess.run([sys.executable, str(ROOT / "benchmark/scripts/plot_results.py"),
                    "--input", str(existing), "--output-dir", str(RESULTS / "charts")], check=True)

    def table(code: str) -> str:
        lines = ["| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |",
                 "| ---: | --- | ---: | ---: | ---: |"]
        for size in (1000, 10000, 100000):
            for model in MODELS:
                before = medians[(size, code, model, False)]
                after = medians[(size, code, model, True)]
                ratio = f"{before / after:.2f}" if after else "n/a"
                lines.append(f"| {size:,} | {model} | {before:.3f} | {after:.3f} | {ratio} |")
        return "\n".join(lines)

    relative_run = run_dir.relative_to(ROOT).as_posix()
    date = completion["completed_at_utc"][:10]
    read_table = table("Q2_Subtree")
    insert_table = table("INSERT_Leaf")
    update_table = table("UPDATE_MoveLeaf")
    storage = ["| Số node | Bảng | Index trước (byte) | Index sau (byte) | Tăng (byte) |",
               "| ---: | --- | ---: | ---: | ---: |"]
    for size in (1000, 10000, 100000):
        snapshots = [json.loads((run_dir / f"artifacts/storage_{size}_{mode}.json").read_text(encoding="utf-8"))
                     for mode in (0, 1)]
        baseline = {item["relation_name"]: item for item in snapshots[0]["relations"]}
        for item in snapshots[1]["relations"]:
            before = baseline[item["relation_name"]]["index_bytes"]
            storage.append(f"| {size:,} | {item['relation_name']} | {before} | {item['index_bytes']} | {item['index_bytes'] - before} |")
    storage_table = "\n".join(storage)
    fastest = min(MODELS, key=lambda model: medians[(100000, "Q2_Subtree", model, True)])
    slowest_insert = max(MODELS, key=lambda model: medians[(100000, "INSERT_Leaf", model, True)])
    slowest_update = max(MODELS, key=lambda model: medians[(100000, "UPDATE_MoveLeaf", model, True)])
    config = "\n".join(f"- `{name}`: `{value}` {unit or ''}".rstrip() for name, value, unit in environment["settings"])
    methodology = """- Dữ liệu sinh, không dùng SNAP: cây tam phân breadth-first; đồ thị SQL dạng vòng, mỗi user nối 5 user kế tiếp, cạnh lưu một lần.
- CSV đồ thị dùng bộ sinh ngẫu nhiên seed 42; đây là corpus riêng để import/đối chiếu Neo4j, không phải đồ thị vòng SQL.
- Ba quy mô: 1.000, 10.000, 100.000 node. Mỗi trường hợp làm nóng 1 lần, đo 5 lần, báo cáo trung vị.
- Q2 lấy subtree node 2, gồm chính node; cả 4 mô hình phải trả cùng số lượng trước khi đo.
- Baseline giữ index PK/UNIQUE. Chỉ bỏ index phụ không gắn ràng buộc, không vô hiệu hóa PK/FK và không ép planner dùng index.
- Pha có index thêm toàn bộ `benchmark/indexes.sql`. Index `(post_id,parent_id)` khớp cả hai điều kiện JOIN trong CTE.
- Đo đọc và dung lượng trước pha ghi, tránh dung lượng bị phình bởi các UPDATE rollback.
- INSERT thêm lá dưới node 2; UPDATE chuyển lá cuối N dưới node 2. Mỗi mô hình tính cả cập nhật `comment` và bảng biểu diễn riêng.
- Mỗi phép ghi dùng SAVEPOINT/ROLLBACK. Kiểm chứng kết quả ghi ở lượt warm-up ngoài khoảng đo; sau benchmark kiểm chứng lại toàn bộ dataset.
- Ghi trong transaction rollback vẫn tạo WAL/dirty buffers/dead tuples. Kết quả là workload ghi ấm, không phải latency COMMIT hay chuyển subtree lớn.
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` lưu raw plan; root thường là Aggregate/Result, muốn biết index thực dùng phải xem node con.
- Lưu dung lượng bảng/index/total và danh sách index thực tế theo từng pha. Tất cả thay đổi index trong runner được rollback khi đóng kết nối.
- Cụm PostgreSQL tạm dùng SCRAM, chỉ nghe loopback, mật khẩu sinh ngẫu nhiên không ghi repo; tự dừng/xóa sau chạy, không thay đổi DB người dùng."""
    conclusions = f"""- Ở 100.000 node, pha thêm index, Q2 nhanh nhất trong lần đo này: **{fastest}**.
- Chi phí INSERT cao nhất trong cùng pha: **{slowest_insert}**; UPDATE chuyển lá cao nhất: **{slowest_update}**.
- Tỉ số trước/sau > 1 là giảm thời gian; < 1 là chậm hơn. Index không bảo đảm tăng tốc mọi truy vấn.
- Closure Table đã có PK `(ancestor,descendant)`, nên baseline vẫn có đường truy cập theo ancestor; không được gọi đây là quét bảng hoàn toàn không index.
- Kết luận chỉ áp dụng cấu trúc cây, node truy vấn, máy và trạng thái cache này. Chưa đo cold-cache, cây dây chuyền, subtree lớn khi ghi hoặc throughput đồng thời.
- Phần pgbench/deadlock và Neo4j do thành viên khác phụ trách; Task 5 cung cấp corpus và số liệu PostgreSQL, không tự nhận đã chạy thay họ."""
    validation = f"""- Seed nhỏ: nạp schema, constraints, seed_test và Q9–Q12; `sql_advanced/validate_task3.sql` chạy thành công.
- Chạy CRUD và Q1–Q10 của cả 4 mô hình trên seed nhỏ, sau mỗi file kiểm chứng dữ liệu không đổi sau rollback.
- Ground truth: subtree(1) = {{1,2,3}}, ancestors(3) = {{1,2}}.
- `normalization/fd_check.sql`: mọi SELECT trả 0 dòng trên seed nhỏ và ba dataset lớn. Đây là kiểm chứng dữ liệu, không phải chứng minh FD từ lý thuyết; FD tình cờ vẫn không được coi là quy tắc nghiệp vụ.
- `benchmark/validate_dataset.sql`: so toàn bộ cặp closure với CTE, đường dẫn ltree, khoảng Nested Set, số node, post cha-con và friend_count.
- Kiểm chứng dataset trước và sau benchmark ở từng quy mô; {len(rows)} lượt đo hoàn tất, 72 nhóm, mỗi nhóm 5 lượt.
- Corpus CSV: 24 file cây/đồ thị đã kiểm tra nội dung, số dòng và SHA-256 trong `benchmark/results/generated_data_manifest.json`.
- Log gốc và kế hoạch thực thi: `{relative_run}/`."""
    report = f"""# Task 5 — Dữ liệu, chỉ mục và benchmark

Ngày thực nghiệm: {date}. Người phụ trách: Quỳnh.

## Môi trường

- OS: {environment['platform']}
- CPU: {environment['processor']}; {environment['logical_cpus']} logical CPU.
- RAM: {environment.get('memory', {}).get('TotalPhysicalMemory', 'not recorded')} byte.
- Python: {environment['python']}
- PostgreSQL: {environment['postgresql']}
{config}

## Thiết kế thực nghiệm

{methodology}

## Kiểm chứng đúng đắn

{validation}

## Kết quả Q2 đọc subtree — trung vị ms

{read_table}

## Chi phí INSERT lá — trung vị ms

{insert_table}

## Chi phí UPDATE chuyển lá — trung vị ms

{update_table}

## Dung lượng index

{storage_table}

Dung lượng bảng, index và tổng đầy đủ có trong `benchmark/results/benchmark_summary.md` và raw JSON; bảng trên chỉ hiển thị index.

## Phân tích và giới hạn

{conclusions}

## Tái lập

```powershell
python -m pip install -r benchmark/requirements.txt
python benchmark/scripts/run_complete.py --postgres-bin "C:\\Program Files\\PostgreSQL\\16\\bin"
python benchmark/scripts/gen_tree_data.py --sizes 1000 10000 100000
python benchmark/scripts/gen_graph_data.py --all
python benchmark/scripts/verify_generated_data.py
```

Runner in đường dẫn run mới khi hoàn tất. Chạy `publish_results.py --run-dir <đường_dẫn_run>` để cập nhật bảng, biểu đồ, log và tài liệu. Không cần mật khẩu DB đang dùng vì tạo cụm riêng.

## Minh chứng bàn giao

- CSV chuẩn: `benchmark/results/benchmark_results.csv`.
- Bảng tổng hợp: `benchmark/results/benchmark_summary.md`.
- Biểu đồ: `benchmark/results/charts/`, gồm Q2, INSERT, UPDATE cho cả ba quy mô.
- Nhật ký: `docs/experiment_log/task5_completed.md`.
- Slide nội dung: `slides/task5_benchmark.md`.
- Run gốc: `{relative_run}/`; dữ liệu 1k cũ được giữ riêng trong `benchmark/results/archive/`, không gộp vào lần đo này.
"""
    log = f"""# Nhật ký thực nghiệm Task 5

- Ngày: {date}; run ID: `{run_dir.name}`.
- Trạng thái: hoàn tất {len(rows)} lượt đo, không điền số mẫu.
- Môi trường và config: `{relative_run}/environment.json`.
- Commit nền: `{(run_dir / 'commit.txt').read_text().strip()}`. Có thay đổi chưa commit; xem manifest nguồn công bố.
- Seed và kiểm chứng: `seed_*.txt`, `validate_*.txt`, `validation.txt`, `fd_*.txt`, `tree_queries.txt` trong run gốc.
- Đầu ra: CSV, 9 biểu đồ, summary và 78 JSON (72 plan + 6 snapshot dung lượng/index).

## Quy trình

{methodology}

## Kiểm chứng

{validation}

## Kết quả và nhận xét

Xem số đầy đủ ở `report/task5_benchmark_results.md` và `benchmark/results/benchmark_summary.md`.

{conclusions}
"""
    slides = f"""# Task 5 — Nội dung slide benchmark

## Slide 1 — Dữ liệu và kiểm chứng
- Dữ liệu sinh: cây tam phân 1k/10k/100k, đồ thị SQL tương ứng 5k/50k/500k cạnh.
- 4 mô hình dùng cùng cây; seed nhỏ có đáp án tính tay.
- FD/BR và cấu trúc cây kiểm chứng trước/sau đo; 24 CSV có SHA-256.

## Slide 2 — Thiết kế chỉ mục và phương pháp
- Baseline giữ PK/UNIQUE; pha sau thêm B-tree, GiST và composite theo mô hình.
- 1 warm-up, 5 repeats, lấy median; EXPLAIN ANALYZE BUFFERS JSON.
- Đo đọc/dung lượng trước ghi. Ghi rollback, không phải COMMIT latency.
- INSERT lá dưới 2, UPDATE chuyển lá N dưới 2; không suy rộng sang chuyển subtree lớn.

## Slide 3 — Q2 tại 100k
- Chèn ảnh `benchmark/results/charts/q2_subtree_100000.png`.
- Mô hình nhanh nhất trong pha thêm index của lần đo: {fastest}.
- Xem bảng tại `report/task5_benchmark_results.md`; không nói index luôn nhanh hơn.

## Slide 4 — Chi phí ghi và dung lượng
- Chèn ảnh `benchmark/results/charts/insert_leaf_100000.png` và `update_moveleaf_100000.png`.
- INSERT cao nhất: {slowest_insert}; UPDATE chuyển lá cao nhất: {slowest_update}.
- Bảng dung lượng index ở báo cáo; dung lượng total ở summary và raw snapshot.
- Chốt đánh đổi đọc/ghi/dung lượng, giới hạn warm-cache và một cấu trúc cây.

## Demo
Mở `benchmark/results/benchmark_summary.md`, biểu đồ 100k và một raw plan trong `{relative_run}/artifacts/`.
"""
    documents = {
        ROOT / "report/task5_benchmark_results.md": report,
        ROOT / "docs/experiment_log/task5_completed.md": log,
        ROOT / "slides/task5_benchmark.md": slides,
    }
    for path, content in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    source_files = [*ROOT.glob("benchmark/scripts/*.py"), *ROOT.glob("benchmark/*.sql"),
                    ROOT / "database/seed_bench.sql"]
    (RESULTS / "published_run.json").write_text(json.dumps({
        "run_dir": relative_run, "rows": len(rows), "source_state_at_publication": {
            path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_files}},
        indent=2), encoding="utf-8")
    print(f"Published {len(rows)} measurements, report, slides and experiment log")


if __name__ == "__main__":
    main()
