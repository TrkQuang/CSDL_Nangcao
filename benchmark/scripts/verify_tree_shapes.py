"""Generate and cross-check extra tree shapes without changing benchmark results."""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

from gen_tree_data import DEFAULT_SIZES, write_tree_data
from verify_generated_data import verify_rows

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "benchmark/data"


def verify_shape(size: int, shape: str) -> dict[str, object]:
    directory = DATA / shape
    write_tree_data(size, directory, 3, shape)
    with (directory / f"comment_{size}.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    parents = {int(row["comment_id"]): int(row["parent_id"]) if row["parent_id"] else None for row in rows}
    if set(parents) != set(range(1, size + 1)) or parents[1] is not None:
        raise ValueError("Tree IDs or root invalid")
    children = {node: [] for node in parents}
    paths = {1: [1]}
    for node in range(2, size + 1):
        parent = parents[node]
        if parent is None or not 1 <= parent < node:
            raise ValueError("Parent must precede child")
        if shape == "chain" and parent != node - 1:
            raise ValueError("Invalid chain")
        children[parent].append(node)
        paths[node] = paths[parent] + [node]
    bounds = {}
    clock = 0
    stack = [(1, False)]
    while stack:
        node, closing = stack.pop()
        clock += 1
        if closing:
            bounds[node][1] = clock
        else:
            bounds[node] = [clock, 0]
            stack.append((node, True))
            stack.extend((child, False) for child in reversed(children[node]))
    files = [verify_rows(directory / f"comment_{size}.csv", (
        (node, 1, node, parents[node] or "", f"Benchmark comment {node}")
        for node in range(1, size + 1))),
        verify_rows(directory / f"comment_path_{size}.csv", (
            (node, 1, ".".join(f"n{part}" for part in paths[node])) for node in range(1, size + 1))),
        verify_rows(directory / f"comment_ns_{size}.csv", (
            (node, 1, *bounds[node]) for node in range(1, size + 1))),
        verify_rows(directory / f"comment_closure_{size}.csv", (
            (ancestor, node, depth) for node in range(1, size + 1)
            for depth, ancestor in enumerate(reversed(paths[node]))))]
    with tempfile.TemporaryDirectory(prefix="detai17_shape_") as temporary:
        repeat = Path(temporary)
        write_tree_data(size, repeat, 3, shape)
        for original in directory.glob(f"*_{size}.csv"):
            if original.read_bytes() != (repeat / original.name).read_bytes():
                raise ValueError("Tree generation is not deterministic")
    return {"shape": shape, "nodes": size, "max_depth": max(map(len, paths.values())), "files": files}


def main() -> None:
    cases = [verify_shape(size, "random") for size in DEFAULT_SIZES]
    cases.append(verify_shape(1000, "chain"))
    output = ROOT / "benchmark/results/tree_shapes_manifest.json"
    output.write_text(json.dumps({"status": "passed", "seed": 42, "cases": cases}, indent=2), encoding="utf-8")
    print(f"Verified {len(cases)} additional datasets: {output}")


if __name__ == "__main__":
    main()
