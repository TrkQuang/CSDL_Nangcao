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
    from psycopg2 import sql
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
            SELECT comment_id, parent_id, post_id
            FROM comment
            WHERE comment_id = %s
            UNION ALL
            SELECT child.comment_id, child.parent_id, child.post_id
            FROM comment child
            JOIN subtree ON child.parent_id = subtree.comment_id
                        AND child.post_id = subtree.post_id
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
        "plan_document": plan_document,
    }


def execute_sql_file(connection: Any, sql_path: Path) -> None:
    with sql_path.open(encoding="utf-8") as handle, connection.cursor() as cursor:
        cursor.execute(handle.read())


def drop_secondary_indexes(connection: Any) -> None:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ns.nspname, idx.relname
            FROM pg_index info
            JOIN pg_class tab ON tab.oid = info.indrelid
            JOIN pg_class idx ON idx.oid = info.indexrelid
            JOIN pg_namespace ns ON ns.oid = idx.relnamespace
            WHERE tab.oid IN ('comment'::regclass, 'comment_path'::regclass,
                'comment_ns'::regclass, 'comment_closure'::regclass, 'friendship'::regclass)
              AND NOT EXISTS (SELECT 1 FROM pg_constraint con WHERE con.conindid = info.indexrelid)
        """)
        for schema_name, index_name in cursor.fetchall():
            cursor.execute(sql.SQL("DROP INDEX {}.{}").format(sql.Identifier(schema_name), sql.Identifier(index_name)))
        cursor.execute("ANALYZE comment, comment_path, comment_ns, comment_closure, friendship;")


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
    plan_dir: Path | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with connection.cursor() as cursor:
        for case in CASES:
            explain(cursor, case, node_id)  # warm-up; excluded from output
            measurements = [explain(cursor, case, node_id) for _ in range(repeats)]
            if plan_dir is not None:
                plan_dir.mkdir(parents=True, exist_ok=True)
                (plan_dir / f"{experiment_prefix}-{case.model[:3].upper()}.json").write_text(
                    json.dumps(measurements[-1]["plan_document"], indent=2), encoding="utf-8"
                )
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


def snapshot_storage(connection: Any, dataset_size: int, has_index: bool, output: Path) -> None:
    with connection.cursor() as cursor:
        cursor.execute((ROOT_DIR / "benchmark" / "storage_sizes.sql").read_text(encoding="utf-8"))
        columns = [column.name for column in cursor.description]
        records = [dict(zip(columns, values)) for values in cursor.fetchall()]
        cursor.execute("""
            SELECT tab.relname, idx.relname, pg_get_indexdef(idx.oid)
            FROM pg_index info JOIN pg_class tab ON tab.oid = info.indrelid
            JOIN pg_class idx ON idx.oid = info.indexrelid
            WHERE tab.oid IN ('comment'::regclass, 'comment_path'::regclass,
                'comment_ns'::regclass, 'comment_closure'::regclass, 'friendship'::regclass)
            ORDER BY tab.relname, idx.relname
        """)
        indexes = cursor.fetchall()
    output.mkdir(parents=True, exist_ok=True)
    (output / f"storage_{dataset_size}_{int(has_index)}.json").write_text(
        json.dumps({"dataset_size": dataset_size, "has_index": has_index, "relations": records,
                    "indexes": indexes}, indent=2), encoding="utf-8"
    )


def run_writes(connection: Any, size: int, repeats: int, has_index: bool, prefix: str,
               plan_dir: Path) -> list[dict[str, Any]]:
    rows = []
    with connection.cursor() as cursor:
        for case in CASES:
            for code, query, params in (
                ("INSERT_Leaf", "SELECT benchmark_insert_leaf(%s, %s)", (case.model, 2)),
                ("UPDATE_MoveLeaf", "SELECT benchmark_move_leaf(%s, %s, %s)", (case.model, size, 2)),
            ):
                measurements = []
                for repeat in range(repeats + 1):
                    cursor.execute("SAVEPOINT measured_write")
                    cursor.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + query, params)
                    document = cursor.fetchone()[0]
                    if isinstance(document, str):
                        document = json.loads(document)
                    if repeat == 0:
                        cursor.execute("SELECT MAX(comment_id) FROM comment")
                        changed_node = cursor.fetchone()[0] if code == "INSERT_Leaf" else size
                        cursor.execute("SELECT benchmark_assert_leaf(%s, %s, %s)", (case.model, changed_node, 2))
                    cursor.execute("ROLLBACK TO SAVEPOINT measured_write")
                    cursor.execute("RELEASE SAVEPOINT measured_write")
                    if repeat:
                        root = document[0]
                        measurements.append({
                            "execution_time_ms": root["Execution Time"],
                            "planning_time_ms": root["Planning Time"],
                            "shared_hit_blocks": root["Plan"].get("Shared Hit Blocks", 0),
                            "shared_read_blocks": root["Plan"].get("Shared Read Blocks", 0),
                            "plan_node_type": root["Plan"]["Node Type"],
                        })
                plan_dir.mkdir(parents=True, exist_ok=True)
                (plan_dir / f"{prefix}-{case.model[:3].upper()}-{code}.json").write_text(
                    json.dumps(document, indent=2), encoding="utf-8"
                )
                for repeat_no, metric in enumerate(measurements, 1):
                    rows.append({
                        "experiment_id": f"{prefix}-{case.model[:3].upper()}-{code}-{repeat_no:02d}",
                        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "target_model": case.model, "query_code": code, "dataset_size": size,
                        "has_index": str(has_index).lower(), "repeat_no": repeat_no, **metric,
                        "notes": "parent=2; move leaf=N; savepoint rollback; warm cache; includes model metadata maintenance",
                    })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark four tree storage models with EXPLAIN ANALYZE.")
    parser.add_argument("--dsn", default=os.getenv("DATABASE_URL"), help="PostgreSQL DSN; default: DATABASE_URL")
    parser.add_argument("--dataset-size", type=int, required=True, choices=(1000, 10000, 100000))
    parser.add_argument("--node-id", type=int, default=2, help="Subtree root; use non-root node for selective query.")
    parser.add_argument("--repeats", type=int, default=5, help="Measured runs after one warm-up.")
    parser.add_argument("--mode", choices=("without-index", "with-index", "both"), default="both")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--artifacts-dir", type=Path, default=ROOT_DIR / "benchmark" / "results" / "artifacts")
    parser.add_argument("--include-writes", action="store_true")
    args = parser.parse_args()

    if psycopg2 is None:
        raise SystemExit(f"Missing dependency psycopg2-binary: {PSYCOPG_IMPORT_ERROR}")
    if not args.dsn:
        raise SystemExit("Pass --dsn or set DATABASE_URL.")
    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1.")

    connection = psycopg2.connect(args.dsn)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET statement_timeout = '180s'")
            cursor.execute("SELECT COUNT(*) FROM comment")
            if cursor.fetchone()[0] != args.dataset_size:
                raise ValueError("Actual comment count differs from --dataset-size; seed matching dataset first")
            expected = []
            for case in CASES:
                cursor.execute(case.query, (args.node_id,))
                expected.append(cursor.fetchone()[0])
            if not expected[0] or len(set(expected)) != 1:
                raise ValueError(f"Four models disagree on subtree counts: {expected}")
        if args.include_writes:
            execute_sql_file(connection, ROOT_DIR / "benchmark" / "write_workloads.sql")
        all_rows: list[dict[str, Any]] = []
        if args.mode in ("without-index", "both"):
            drop_secondary_indexes(connection)
            all_rows.extend(
                run_one_mode(connection, args.dataset_size, args.node_id, args.repeats, False, f"N{args.dataset_size}-NOIDX", args.artifacts_dir)
            )
            snapshot_storage(connection, args.dataset_size, False, args.artifacts_dir)
        if args.mode in ("with-index", "both"):
            execute_sql_file(connection, INDEX_SQL)
            all_rows.extend(
                run_one_mode(connection, args.dataset_size, args.node_id, args.repeats, True, f"N{args.dataset_size}-IDX", args.artifacts_dir)
            )
            snapshot_storage(connection, args.dataset_size, True, args.artifacts_dir)
        if args.include_writes:
            if args.mode in ("without-index", "both"):
                drop_secondary_indexes(connection)
                all_rows.extend(run_writes(connection, args.dataset_size, args.repeats, False,
                                          f"N{args.dataset_size}-NOIDX", args.artifacts_dir))
            if args.mode in ("with-index", "both"):
                execute_sql_file(connection, INDEX_SQL)
                all_rows.extend(run_writes(connection, args.dataset_size, args.repeats, True,
                                          f"N{args.dataset_size}-IDX", args.artifacts_dir))
        append_rows(args.output, all_rows)
        print(f"Wrote {len(all_rows)} measurements to {args.output}")
    finally:
        connection.rollback()
        connection.close()


if __name__ == "__main__":
    main()
