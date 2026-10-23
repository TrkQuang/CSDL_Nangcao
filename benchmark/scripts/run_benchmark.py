"""Run repeatable PostgreSQL tree benchmarks and export EXPLAIN ANALYZE metrics."""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

try:
    import psycopg2
except ImportError as error:  # pragma: no cover - CLI dependency guard
    psycopg2 = None
    PSYCOPG_IMPORT_ERROR = error
else:
    PSYCOPG_IMPORT_ERROR = None

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT_DIR / "benchmark" / "results" / "benchmark_results.csv"
INDEX_SQL = ROOT_DIR / "benchmark" / "indexes.sql"
DROP_INDEXES = (
    "idx_bench_comment_post_parent",
    "idx_bench_comment_path_gist",
    "idx_bench_comment_path_post",
    "idx_bench_comment_ns_post_lft_rgt",
    "idx_bench_closure_ancestor_depth_descendant",
    "idx_bench_closure_descendant_ancestor",
    "idx_bench_friendship_user_b",
)
FIELDNAMES = (
    "experiment_id",
    "run_at_utc",
    "target_model",
    "query_code",
    "dataset_size",
    "has_index",
    "repeat_no",
    "execution_time_ms",
    "planning_time_ms",
    "shared_hit_blocks",
    "shared_read_blocks",
    "plan_node_type",
    "notes",
)


@dataclass(frozen=True)
class BenchmarkCase:
    model: str
    query_code: str
    query: str
    notes: str


CASES = (
    BenchmarkCase(
        "Adjacency List",
        "Q2_Subtree",
        """
        WITH RECURSIVE subtree AS (
            SELECT comment_id, parent_id
            FROM comment
            WHERE comment_id = %s
            UNION ALL
            SELECT child.comment_id, child.parent_id
            FROM comment child
            JOIN subtree ON child.parent_id = subtree.comment_id
        )
        SELECT COUNT(*) FROM subtree;
        """,
        "WITH RECURSIVE parent_id traversal",
    ),
    BenchmarkCase(
        "Path Enumeration",
        "Q2_Subtree",
        """
        SELECT COUNT(*)
        FROM comment_path child
        JOIN comment_path root ON root.comment_id = %s
        WHERE child.path <@ root.path;
        """,
        "ltree descendant operator <@",
    ),
    BenchmarkCase(
        "Nested Set",
        "Q2_Subtree",
        """
        SELECT COUNT(*)
        FROM comment_ns child
        JOIN comment_ns root ON root.comment_id = %s
        WHERE child.post_id = root.post_id
          AND child.lft BETWEEN root.lft AND root.rgt;
        """,
        "lft/rgt range scan",
    ),
    BenchmarkCase(
        "Closure Table",
        "Q2_Subtree",
        "SELECT COUNT(*) FROM comment_closure WHERE ancestor = %s;",
        "ancestor lookup",
    ),
)


def get_plan_metric(plan: dict[str, Any], key: str) -> int:
    """Read top-level buffer metric; PostgreSQL root contains aggregate values."""
    return int(plan.get(key, 0))


def explain(cursor: Any, case: BenchmarkCase, node_id: int) -> dict[str, Any]:
    cursor.execute(
        "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + case.query,
        (node_id,),
    )
    result = cursor.fetchone()[0]
    plan_document = json.loads(result) if isinstance(result, str) else result
    root = plan_document[0]
    plan = root["Plan"]
    return {
        "execution_time_ms": float(root["Execution Time"]),
        "planning_time_ms": float(root["Planning Time"]),
        "shared_hit_blocks": get_plan_metric(plan, "Shared Hit Blocks"),
        "shared_read_blocks": get_plan_metric(plan, "Shared Read Blocks"),
        "plan_node_type": plan.get("Node Type", "unknown"),
    }


def execute_sql_file(connection: Any, sql_path: Path) -> None:
    with sql_path.open(encoding="utf-8") as handle, connection.cursor() as cursor:
        cursor.execute(handle.read())
    connection.commit()


def drop_secondary_indexes(connection: Any) -> None:
    with connection.cursor() as cursor:
        for index_name in DROP_INDEXES:
            cursor.execute(f"DROP INDEX IF EXISTS {index_name};")
        cursor.execute("ANALYZE comment, comment_path, comment_ns, comment_closure, friendship;")
    connection.commit()


def append_rows(output_path: Path, rows: Sequence[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not output_path.exists() or output_path.stat().st_size == 0
    with output_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def run_one_mode(
    connection: Any,
    dataset_size: int,
    node_id: int,
    repeats: int,
    has_index: bool,
    experiment_prefix: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with connection.cursor() as cursor:
        for case in CASES:
            explain(cursor, case, node_id)  # warm-up; excluded from output
            measurements = [explain(cursor, case, node_id) for _ in range(repeats)]
            execution_median = statistics.median(item["execution_time_ms"] for item in measurements)
            for repeat_no, metric in enumerate(measurements, start=1):
                rows.append(
                    {
                        "experiment_id": f"{experiment_prefix}-{case.model[:3].upper()}-{repeat_no:02d}",
                        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "target_model": case.model,
                        "query_code": case.query_code,
                        "dataset_size": dataset_size,
                        "has_index": str(has_index).lower(),
                        "repeat_no": repeat_no,
                        "execution_time_ms": metric["execution_time_ms"],
                        "planning_time_ms": metric["planning_time_ms"],
                        "shared_hit_blocks": metric["shared_hit_blocks"],
                        "shared_read_blocks": metric["shared_read_blocks"],
                        "plan_node_type": metric["plan_node_type"],
                        "notes": f"{case.notes}; median_execution_ms={execution_median:.3f}",
                    }
                )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark four tree storage models with EXPLAIN ANALYZE.")
    parser.add_argument("--dsn", default=os.getenv("DATABASE_URL"), help="PostgreSQL DSN; default: DATABASE_URL")
    parser.add_argument("--dataset-size", type=int, required=True, choices=(1000, 10000, 100000))
    parser.add_argument("--node-id", type=int, default=2, help="Subtree root; use non-root node for selective query.")
    parser.add_argument("--repeats", type=int, default=5, help="Measured runs after one warm-up.")
    parser.add_argument("--mode", choices=("without-index", "with-index", "both"), default="both")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if psycopg2 is None:
        raise SystemExit(f"Missing dependency psycopg2-binary: {PSYCOPG_IMPORT_ERROR}")
    if not args.dsn:
        raise SystemExit("Pass --dsn or set DATABASE_URL.")
    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1.")

    connection = psycopg2.connect(args.dsn)
    try:
        all_rows: list[dict[str, Any]] = []
        if args.mode in ("without-index", "both"):
            drop_secondary_indexes(connection)
            all_rows.extend(
                run_one_mode(connection, args.dataset_size, args.node_id, args.repeats, False, f"N{args.dataset_size}-NOIDX")
            )
        if args.mode in ("with-index", "both"):
            execute_sql_file(connection, INDEX_SQL)
            all_rows.extend(
                run_one_mode(connection, args.dataset_size, args.node_id, args.repeats, True, f"N{args.dataset_size}-IDX")
            )
        append_rows(args.output, all_rows)
        print(f"Wrote {len(all_rows)} measurements to {args.output}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()