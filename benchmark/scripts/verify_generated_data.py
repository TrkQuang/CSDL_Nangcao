"""Validate deterministic CSV datasets and record row counts and SHA-256 hashes."""

from __future__ import annotations

import csv
import hashlib
import json
from itertools import zip_longest
from pathlib import Path

from gen_graph_data import DEFAULT_DATASETS, generate_edges
from gen_tree_data import DEFAULT_SIZES, parent_for

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "benchmark" / "data"


def verify_rows(path: Path, expected: object) -> dict[str, object]:
    count = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        for actual, wanted in zip_longest(reader, expected):
            if actual is None or wanted is None or actual != [str(value) for value in wanted]:
                raise ValueError(f"Unexpected row {count + 1} in {path.name}")
            count += 1
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"file": path.relative_to(ROOT).as_posix(), "rows": count,
            "bytes": path.stat().st_size, "header": header, "sha256": digest.hexdigest()}


def main() -> None:
    manifest = []
    for size in DEFAULT_SIZES:
        paths = {1: [1]}
        children = {node: [] for node in range(1, size + 1)}
        for node in range(2, size + 1):
            parent = parent_for(node, 3)
            paths[node] = paths[parent] + [node]
            children[parent].append(node)
        bounds = {}
        boundary = 0
        stack = [(1, False)]
        while stack:
            node, closing = stack.pop()
            boundary += 1
            if closing:
                bounds[node][1] = boundary
            else:
                bounds[node] = [boundary, 0]
                stack.append((node, True))
                stack.extend((child, False) for child in reversed(children[node]))
        manifest.append(verify_rows(DATA / f"comment_{size}.csv", (
            (node, 1, node, parent_for(node, 3) or "", f"Benchmark comment {node}")
            for node in range(1, size + 1))))
        manifest.append(verify_rows(DATA / f"comment_path_{size}.csv", (
            (node, 1, ".".join(f"n{part}" for part in paths[node])) for node in range(1, size + 1))))
        manifest.append(verify_rows(DATA / f"comment_ns_{size}.csv", (
            (node, 1, *bounds[node]) for node in range(1, size + 1))))
        manifest.append(verify_rows(DATA / f"comment_closure_{size}.csv", (
            (ancestor, node, depth) for node in range(1, size + 1)
            for depth, ancestor in enumerate(reversed(paths[node])))))
        print(f"Tree {size}: all four CSV models verified", flush=True)

    for users, edges in DEFAULT_DATASETS:
        pairs = generate_edges(users, edges)
        suffix = f"{users}_users_{edges}_edges"
        manifest.append(verify_rows(DATA / f"users_{suffix}.csv", (
            (node, f"Graph User {node}", f"graph_user_{node}@sgu.vn") for node in range(1, users + 1))))
        manifest.append(verify_rows(DATA / f"friendship_{suffix}.csv", pairs))
        manifest.append(verify_rows(DATA / f"neo4j_users_{suffix}.csv", (
            (node, f"Graph User {node}", "User") for node in range(1, users + 1))))
        manifest.append(verify_rows(DATA / f"neo4j_friendship_{suffix}.csv", (
            (first, second, "FRIEND") for first, second in pairs)))
        print(f"Graph {users}/{edges}: PostgreSQL/Neo4j CSVs verified", flush=True)

    output = ROOT / "benchmark" / "results" / "generated_data_manifest.json"
    output.write_text(json.dumps({"status": "passed", "graph_random_seed": 42,
        "tree": "deterministic breadth-first ternary tree", "files": manifest}, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
