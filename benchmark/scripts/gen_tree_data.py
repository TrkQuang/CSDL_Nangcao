"""Generate reproducible tree benchmark CSV files for all four relational models."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

SEED = 42
DEFAULT_SIZES = (1_000, 10_000, 100_000)


def parent_for(node_id: int, branching_factor: int) -> int | None:
    """Return deterministic parent for a breadth-first k-ary tree."""
    if node_id == 1:
        return None
    return (node_id - 2) // branching_factor + 1


def write_tree_data(num_nodes: int, output_dir: Path, branching_factor: int) -> dict[str, int]:
    """Write CSV input for comment, ltree, nested-set, and closure tables."""
    if num_nodes < 1:
        raise ValueError("num_nodes must be positive")
    if branching_factor < 2:
        raise ValueError("branching_factor must be at least 2")

    output_dir.mkdir(parents=True, exist_ok=True)
    parents: list[int | None] = [None] * (num_nodes + 1)
    children: list[list[int]] = [[] for _ in range(num_nodes + 1)]
    paths: list[list[int] | None] = [None] * (num_nodes + 1)

    paths[1] = [1]
    for node_id in range(2, num_nodes + 1):
        parent_id = parent_for(node_id, branching_factor)
        parents[node_id] = parent_id
        children[parent_id].append(node_id)
        paths[node_id] = paths[parent_id] + [node_id]

    bounds: list[tuple[int, int] | None] = [None] * (num_nodes + 1)
    counter = 1
    stack: list[tuple[int, bool]] = [(1, False)]
    while stack:
        node_id, exiting = stack.pop()
        if not exiting:
            left = counter
            counter += 1
            bounds[node_id] = (left, 0)
            stack.append((node_id, True))
            for child_id in reversed(children[node_id]):
                stack.append((child_id, False))
        else:
            left, _ = bounds[node_id]
            bounds[node_id] = (left, counter)
            counter += 1

    files = {
        "comment": output_dir / f"comment_{num_nodes}.csv",
        "path": output_dir / f"comment_path_{num_nodes}.csv",
        "nested_set": output_dir / f"comment_ns_{num_nodes}.csv",
        "closure": output_dir / f"comment_closure_{num_nodes}.csv",
    }

    with files["comment"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["comment_id", "post_id", "author_id", "parent_id", "content"])
        for node_id in range(1, num_nodes + 1):
            writer.writerow([node_id, 1, node_id, parents[node_id] or "", f"Benchmark comment {node_id}"])

    with files["path"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["comment_id", "post_id", "path"])
        for node_id in range(1, num_nodes + 1):
            path = ".".join(f"n{part}" for part in paths[node_id])
            writer.writerow([node_id, 1, path])

    with files["nested_set"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["comment_id", "post_id", "lft", "rgt"])
        for node_id in range(1, num_nodes + 1):
            left, right = bounds[node_id]
            writer.writerow([node_id, 1, left, right])

    closure_rows = 0
    with files["closure"].open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["ancestor", "descendant", "depth"])
        for node_id in range(1, num_nodes + 1):
            lineage = paths[node_id]
            for depth, ancestor_id in enumerate(reversed(lineage)):
                writer.writerow([ancestor_id, node_id, depth])
                closure_rows += 1

    return {"nodes": num_nodes, "closure_rows": closure_rows, **{key: value.stat().st_size for key, value in files.items()}}


def parse_sizes(values: Iterable[str]) -> tuple[int, ...]:
    return tuple(int(value) for value in values)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate tree CSV data for benchmark imports.")
    parser.add_argument("--sizes", nargs="+", default=[str(size) for size in DEFAULT_SIZES])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--branching-factor", type=int, default=3)
    args = parser.parse_args()

    for size in parse_sizes(args.sizes):
        result = write_tree_data(size, args.output_dir, args.branching_factor)
        print(f"tree={size} nodes, closure_rows={result['closure_rows']}, output={args.output_dir}")


if __name__ == "__main__":
    main()