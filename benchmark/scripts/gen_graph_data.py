"""Generate reproducible graph CSV files for PostgreSQL and Neo4j imports."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

SEED = 42
DEFAULT_DATASETS = ((1_000, 5_000), (10_000, 50_000), (100_000, 500_000))


def generate_edges(num_users: int, num_edges: int, seed: int = SEED) -> list[tuple[int, int]]:
    """Generate unique undirected edges, stored canonically as (smaller, larger)."""
    if num_users < 2:
        raise ValueError("num_users must be at least 2")
    if not 0 <= num_edges <= num_users * (num_users - 1) // 2:
        raise ValueError("num_edges exceeds possible undirected edges")

    randomizer = random.Random(seed)
    edges: set[tuple[int, int]] = set()
    while len(edges) < num_edges:
        first_user = randomizer.randint(1, num_users)
        second_user = randomizer.randint(1, num_users)
        if first_user == second_user:
            continue
        edges.add((min(first_user, second_user), max(first_user, second_user)))
    return sorted(edges)


def write_graph_data(num_users: int, num_edges: int, output_dir: Path) -> None:
    """Write user and edge CSVs with headers usable by COPY and neo4j-admin import."""
    output_dir.mkdir(parents=True, exist_ok=True)
    edges = generate_edges(num_users, num_edges)
    suffix = f"{num_users}_users_{num_edges}_edges"

    postgres_users = output_dir / f"users_{suffix}.csv"
    postgres_edges = output_dir / f"friendship_{suffix}.csv"
    neo4j_users = output_dir / f"neo4j_users_{suffix}.csv"
    neo4j_edges = output_dir / f"neo4j_friendship_{suffix}.csv"

    with postgres_users.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["user_id", "full_name", "email"])
        for user_id in range(1, num_users + 1):
            writer.writerow([user_id, f"Graph User {user_id}", f"graph_user_{user_id}@sgu.vn"])

    with postgres_edges.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["user_a", "user_b"])
        writer.writerows(edges)

    with neo4j_users.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["user_id:ID(User)", "full_name", ":LABEL"])
        for user_id in range(1, num_users + 1):
            writer.writerow([user_id, f"Graph User {user_id}", "User"])

    with neo4j_edges.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([":START_ID(User)", ":END_ID(User)", ":TYPE"])
        for user_a, user_b in edges:
            writer.writerow([user_a, user_b, "FRIEND"])

    print(f"users={num_users}, edges={num_edges}, output={output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate graph CSV data for benchmark imports.")
    parser.add_argument("--users", type=int)
    parser.add_argument("--edges", type=int)
    parser.add_argument("--all", action="store_true", help="Generate 1k/5k, 10k/50k, and 100k/500k datasets.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    args = parser.parse_args()

    if args.all:
        datasets = DEFAULT_DATASETS
    elif args.users is not None and args.edges is not None:
        datasets = ((args.users, args.edges),)
    else:
        parser.error("pass --all or both --users and --edges")

    for num_users, num_edges in datasets:
        write_graph_data(num_users, num_edges, args.output_dir)


if __name__ == "__main__":
    main()