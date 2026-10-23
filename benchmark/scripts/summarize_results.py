"""Build a Markdown benchmark table from real CSV measurements."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_results.csv"
DEFAULT_OUTPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_summary.md"
MODELS = ("Adjacency List", "Path Enumeration", "Nested Set", "Closure Table")


def median(values: list[float]) -> str:
    return f"{statistics.median(values):.3f}" if values else "-"


def load_rows(input_path: Path) -> dict[tuple[int, str, bool], dict[str, list[float]]]:
    rows: dict[tuple[int, str, bool], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    with input_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("query_code") != "Q2_Subtree":
                continue
            key = (int(row["dataset_size"]), row["target_model"], row["has_index"].lower() == "true")
            for column in ("execution_time_ms", "planning_time_ms", "shared_hit_blocks", "shared_read_blocks"):
                rows[key][column].append(float(row[column]))
    return rows


def build_markdown(rows: dict[tuple[int, str, bool], dict[str, list[float]]]) -> str:
    lines = [
        "# Benchmark Summary",
        "",
        "Generated from real Q2_Subtree rows in `benchmark_results.csv`.",
        "Each value is median of recorded repeats. Empty CSV produces no result.",
        "",
    ]
    for size in sorted({key[0] for key in rows}):
        lines.extend([
            f"## Dataset {size:,} nodes",
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
    args = parser.parse_args()

    rows = load_rows(args.input)
    if not rows:
        raise SystemExit("No Q2_Subtree measurements found. Run run_benchmark.py first.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
