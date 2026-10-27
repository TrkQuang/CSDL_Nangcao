"""Verify FD checks reject malformed data using rollback-only temporary tables."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import psycopg2
from psycopg2 import sql

ROOT = Path(__file__).resolve().parents[2]


def validate(dsn: str) -> list[dict[str, str]]:
    script = (ROOT / "normalization/fd_check.sql").read_text(encoding="utf-8")
    cases = (
        ("comment", "parent_id", 999999, "f1"),
        ("comment", "content", "Changed content", "f1"),
        ("comment", "created_at", "2000-01-01T00:00:00Z", "f1"),
        ("post", "group_id", 999999, "f2"),
        ("study_group", "topic", "Changed topic", "f3"),
        ("users", "full_name", "Changed name", "f4"),
        ("users", "user_id", 999999, "f5"),
    )
    outcomes = []
    with psycopg2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SET statement_timeout = '30s'")
            cursor.execute(script)
            outcomes.append({"test": "valid seed", "status": "passed"})
            for relation, attribute, value, label in cases:
                cursor.execute("SAVEPOINT malformed_fd")
                cursor.execute(sql.SQL("CREATE TEMP TABLE {} AS SELECT * FROM public.{}").format(
                    sql.Identifier(relation), sql.Identifier(relation)))
                cursor.execute(sql.SQL(
                    "INSERT INTO pg_temp.{} SELECT (jsonb_populate_record(NULL::pg_temp.{}, "
                    "to_jsonb(source) || jsonb_build_object(%s, %s))).* FROM public.{} AS source LIMIT 1"
                ).format(sql.Identifier(relation), sql.Identifier(relation), sql.Identifier(relation)),
                    (attribute, value))
                try:
                    cursor.execute(script)
                except psycopg2.Error as error:
                    if error.pgcode != "P0001" or f"FD violation: {label}:" not in str(error):
                        raise
                    outcomes.append({"test": f"{label}: reject changed {relation}.{attribute}", "status": "passed"})
                else:
                    raise AssertionError(f"FD checker accepted malformed {relation}.{attribute}")
                finally:
                    cursor.execute("ROLLBACK TO SAVEPOINT malformed_fd")
            cursor.execute("SAVEPOINT malformed_counter")
            cursor.execute("UPDATE users SET friend_count = friend_count + 1 WHERE user_id = (SELECT MIN(user_id) FROM users)")
            try:
                cursor.execute(script)
            except psycopg2.Error as error:
                if error.pgcode != "P0001" or "Business integrity violation" not in str(error):
                    raise
                outcomes.append({"test": "BR9: reject incorrect friend_count", "status": "passed"})
            else:
                raise AssertionError("FD checker accepted incorrect friend_count")
            finally:
                cursor.execute("ROLLBACK TO SAVEPOINT malformed_counter")
            cursor.execute(script)
            outcomes.append({"test": "valid seed after rollback", "status": "passed"})
        connection.rollback()
    return outcomes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dsn", default=os.getenv("DATABASE_URL"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.dsn:
        parser.error("pass --dsn or set DATABASE_URL")
    outcomes = validate(args.dsn)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"status": "passed", "tests": outcomes}, indent=2), encoding="utf-8")
    print(f"Passed {len(outcomes)} FD regression checks")


if __name__ == "__main__":
    main()
