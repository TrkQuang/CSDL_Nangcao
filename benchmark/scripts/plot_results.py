"""Create benchmark charts from real rows exported by run_benchmark.py."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

try:
    import matplotlib.pyplot as pyplot
except ImportError as error:  # pragma: no cover - CLI dependency guard
    pyplot = None
    MATPLOTLIB_IMPORT_ERROR = error
else:
    MATPLOTLIB_IMPORT_ERROR = None

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_results.csv"
MODEL_ORDER = ("Adjacency List", "Path Enumeration", "Nested Set", "Closure Table")
COLORS = {False: "#9ca3af", True: "#2563eb"}


def load_medians(input_path: Path) -> dict[tuple[int, str, bool], float]:
    values: dict[tuple[int, str, bool], list[float]] = defaultdict(list)
    with input_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("query_code") != "Q2_Subtree":
                continue
            key = (int(row["dataset_size"]), row["target_model"], row["has_index"].lower() == "true")
            values[key].append(float(row["execution_time_ms"]))
    return {key: statistics.median(items) for key, items in values.items()}


def draw_size_chart(medians: dict[tuple[int, str, bool], float], size: int, output_dir: Path) -> Path:
    labels = [model for model in MODEL_ORDER if (size, model, False) in medians or (size, model, True) in medians]
    if not labels:
        raise ValueError(f"No Q2_Subtree rows for dataset size {size}.")

    positions = list(range(len(labels)))
    width = 0.38
    figure, axis = pyplot.subplots(figsize=(10, 5.5))
    for offset, has_index, label in ((-width / 2, False, "Khong index"), (width / 2, True, "Co index")):
        heights = [medians.get((size, model, has_index), 0) for model in labels]
        bars = axis.bar([position + offset for position in positions], heights, width, label=label, color=COLORS[has_index])
        axis.bar_label(bars, fmt="%.3f", padding=3, fontsize=8)

    axis.set_title(f"Q2 Subtree: thoi gian trung vi ({size:,} node)")
    axis.set_ylabel("Execution time (ms)")
    axis.set_xticks(positions, labels, rotation=12, ha="right")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    output_path = output_dir / f"q2_subtree_{size}.png"
    figure.savefig(output_path, dpi=180)
    pyplot.close(figure)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw Q2 charts from actual CSV measurements.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=ROOT_DIR / "benchmark" / "results" / "charts")
    args = parser.parse_args()

    if pyplot is None:
        raise SystemExit(f"Missing dependency matplotlib: {MATPLOTLIB_IMPORT_ERROR}")
    medians = load_medians(args.input)
    if not medians:
        raise SystemExit("No Q2_Subtree measurements found. Run run_benchmark.py first.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for size in sorted({size for size, _, _ in medians}):
        print(f"Wrote {draw_size_chart(medians, size, args.output_dir)}")


if __name__ == "__main__":
    main()
