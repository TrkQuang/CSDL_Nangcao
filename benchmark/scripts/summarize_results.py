"""Build a Markdown benchmark table from real CSV measurements."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_results.csv"
DEFAULT_OUTPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_summary.md"
MODELS = ("Adjacency List", "Path Enumeration", "Nested Set", "Closure Table")


def median(values: list[float]) -> str:
    return f"{statistics.median(values):.3f}" if values else "-"


def load_rows(input_path: Path, query_code: str = "Q2_Subtree") -> dict[tuple[int, str, bool], dict[str, list[float]]]:
    rows: dict[tuple[int, str, bool], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    with input_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("query_code") != query_code:
                continue
            key = (int(row["dataset_size"]), row["target_model"], row["has_index"].lower() == "true")
            for column in ("execution_time_ms", "planning_time_ms", "shared_hit_blocks", "shared_read_blocks"):
                rows[key][column].append(float(row[column]))
    return rows


def build_markdown(rows: dict[tuple[int, str, bool], dict[str, list[float]]], query_code: str = "Q2_Subtree") -> str:
    lines = [
        f"## {query_code}",
        "",
        "Generated from actual rows in `benchmark_results.csv`.",
        "Each value is median of recorded repeats. Empty CSV produces no result.",
        "",
    ]
    for size in sorted({key[0] for key in rows}):
        lines.extend([
            f"### Dataset {size:,} nodes",
            "",
            "| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ])
        for model in MODELS:
            for has_index in (False, True):
                metrics = rows.get((size, model, has_index))
                if metrics is None:
                    continue
                lines.append(
                    f"| {model} | {'Yes' if has_index else 'No'} | "
                    f"{median(metrics['execution_time_ms'])} | {median(metrics['planning_time_ms'])} | "
                    f"{median(metrics['shared_hit_blocks'])} | {median(metrics['shared_read_blocks'])} |"
                )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize actual benchmark CSV rows as Markdown.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--artifacts-dir", type=Path)
    args = parser.parse_args()

    sections = ["# Benchmark Summary", "",
        "Index No = constraint-backed indexes retained. Index Yes = benchmark secondary indexes added.",
        "Warm cache; one warm-up and recorded repeats. Writes rolled back to savepoints.",
        "INSERT adds a child of node 2; UPDATE moves leaf N below node 2, not a whole subtree.", ""]
    found = False
    for query_code in ("Q2_Subtree", "INSERT_Leaf", "UPDATE_MoveLeaf"):
        rows = load_rows(args.input, query_code)
        if rows:
            sections.append(build_markdown(rows, query_code))
            found = True
    if not found:
        raise SystemExit("No measurements found. Run run_benchmark.py first.")
    if args.artifacts_dir:
        sections.extend(["## Storage", "",
            "Table bytes exclude indexes and TOAST; total bytes include auxiliary storage.", "",
            "| Nodes | Secondary index | Relation | Table bytes | Index bytes | Total bytes |",
            "| ---: | --- | --- | ---: | ---: | ---: |"])
        snapshots = [json.loads(path.read_text(encoding="utf-8"))
                     for path in args.artifacts_dir.glob("storage_*.json")]
        for snapshot in sorted(snapshots, key=lambda item: (item["dataset_size"], item["has_index"])):
            for relation in snapshot["relations"]:
                sections.append(f"| {snapshot['dataset_size']} | {snapshot['has_index']} | "
                    f"{relation['relation_name']} | {relation['table_bytes']} | "
                    f"{relation['index_bytes']} | {relation['total_bytes']} |")
        sections.append("")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
