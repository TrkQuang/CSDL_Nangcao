"""Reproduce Task 5 using a private, password-protected PostgreSQL cluster."""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import secrets
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import psycopg2

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "benchmark" / "scripts"
RESULTS = ROOT / "benchmark" / "results"


def run(command: list[str], environment: dict[str, str], log: Path, input_text: str | None = None) -> None:
    with log.open("a", encoding="utf-8") as handle:
        result = subprocess.run(command, env=environment, input=input_text, text=True,
                                encoding="utf-8", errors="replace", stdout=handle,
                                stderr=subprocess.STDOUT,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}); inspect {log}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--postgres-bin", type=Path, required=True)
    parser.add_argument("--sizes", nargs="+", type=int, choices=(1000, 10000, 100000), default=[1000, 10000, 100000])
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    suffix = ".exe" if os.name == "nt" else ""
    programs = {name: args.postgres_bin / (name + suffix) for name in ("initdb", "pg_ctl", "psql")}
    for executable in programs.values():
        if not executable.is_file():
            parser.error(f"Missing executable: {executable}")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = RESULTS / "runs" / run_id
    output.mkdir(parents=True)
    artifacts = output / "artifacts"
    data_file = output / "benchmark_results.csv"
    environment = dict(os.environ)
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PGCLIENTENCODING"] = "UTF8"
    environment["MPLBACKEND"] = "Agg"
    password = secrets.token_urlsafe(32)
    environment["PGPASSWORD"] = password
    with socket.socket() as port_probe:
        port_probe.bind(("127.0.0.1", 0))
        port = port_probe.getsockname()[1]

    with tempfile.TemporaryDirectory(prefix="detai17_task5_") as temporary:
        temporary_path = Path(temporary)
        cluster = temporary_path / "cluster"
        password_file = temporary_path / "init_password"
        password_file.write_text(password, encoding="utf-8")
        started = False
        try:
            run([str(programs["initdb"]), "-D", str(cluster), "-U", "benchmark_runner",
                 "--auth=scram-sha-256", f"--pwfile={password_file}", "--encoding=UTF8", "--locale=C"],
                environment, output / "setup.txt")
            password_file.unlink()
            run([str(programs["pg_ctl"]), "-D", str(cluster), "-l", str(temporary_path / "server.txt"),
                 "-o", f"-h 127.0.0.1 -p {port}", "-w", "start"], environment, output / "setup.txt")
            started = True
            environment.update(PGHOST="127.0.0.1", PGPORT=str(port), PGUSER="benchmark_runner", PGDATABASE="postgres")
            environment["DATABASE_URL"] = f"host=127.0.0.1 port={port} user=benchmark_runner dbname=postgres"

            def psql_file(relative: str, log_name: str, *variables: str) -> None:
                command = [str(programs["psql"]), "-X", "-w", "-v", "ON_ERROR_STOP=1"]
                for variable in variables:
                    command.extend(["-v", variable])
                command.extend(["-f", str(ROOT / relative)])
                run(command, environment, output / log_name)

            for filename in ("schema.sql", "constraints.sql", "seed_test.sql"):
                psql_file(f"database/{filename}", "validation.txt")
            for filename in ("q09_trigger.sql", "q10_procedure.sql", "q11_function.sql", "q12_dynamic.sql"):
                psql_file(f"sql_advanced/{filename}", "validation.txt")
            psql_file("sql_advanced/validate_task3.sql", "validation.txt")
            psql_file("normalization/fd_check.sql", "fd_seed.txt")
            psql_file("benchmark/validate_dataset.sql", "validation.txt")
            for model in ("adjacency_list", "path_enumeration", "nested_set", "closure_table"):
                psql_file(f"tree_models/{model}/crud.sql", "tree_queries.txt")
                psql_file(f"tree_models/{model}/queries_q1_q10.sql", "tree_queries.txt")
                psql_file("benchmark/validate_dataset.sql", "validation.txt")

            with psycopg2.connect(environment["DATABASE_URL"], password=password) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    cursor.execute("SELECT name, setting, unit FROM pg_settings WHERE name IN "
                                   "('shared_buffers','work_mem','effective_cache_size','max_connections','jit') ORDER BY name")
                    settings = cursor.fetchall()
                run(["git", "rev-parse", "HEAD"], environment, output / "commit.txt")
                hardware = {"platform": platform.platform(), "processor": platform.processor(),
                            "logical_cpus": os.cpu_count(), "python": sys.version,
                            "postgresql": version, "settings": settings, "run_id": run_id,
                            "sizes": args.sizes, "repeats": args.repeats,
                            "cluster": "fresh isolated SCRAM cluster; loopback only; stopped and removed after run"}
                if os.name == "nt":
                    result = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory | ConvertTo-Json"],
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if result.returncode == 0:
                        hardware["memory"] = json.loads(result.stdout)
                (output / "environment.json").write_text(json.dumps(hardware, indent=2), encoding="utf-8")

            for size in args.sizes:
                print(f"Seeding and validating {size:,} nodes", flush=True)
                psql_file("database/seed_bench.sql", f"seed_{size}.txt", f"bench_size={size}")
                psql_file("benchmark/validate_dataset.sql", f"validate_{size}.txt")
                psql_file("normalization/fd_check.sql", f"fd_{size}.txt")
                print(f"Measuring reads, writes, indexes: {size:,}", flush=True)
                run([sys.executable, str(SCRIPTS / "run_benchmark.py"), "--dataset-size", str(size),
                     "--repeats", str(args.repeats), "--mode", "both", "--include-writes",
                     "--output", str(data_file), "--artifacts-dir", str(artifacts)],
                    environment, output / f"benchmark_{size}.txt")
                psql_file("benchmark/validate_dataset.sql", f"validate_{size}.txt")

            with data_file.open(newline="", encoding="utf-8") as handle:
                measurements = list(csv.DictReader(handle))
            expected = len(args.sizes) * 4 * 2 * 3 * args.repeats
            if len(measurements) != expected:
                raise RuntimeError(f"Expected {expected} measurements, found {len(measurements)}")
            run([sys.executable, str(SCRIPTS / "plot_results.py"), "--input", str(data_file),
                 "--output-dir", str(output / "charts")], environment, output / "reporting.txt")
            run([sys.executable, str(SCRIPTS / "summarize_results.py"), "--input", str(data_file),
                 "--output", str(output / "benchmark_summary.md"), "--artifacts-dir", str(artifacts)],
                environment, output / "reporting.txt")
            (output / "completion.json").write_text(json.dumps({"status": "passed", "rows": expected,
                "completed_at_utc": datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
            print(f"Complete: {expected} measurements. Results: {output}", flush=True)
        finally:
            if started:
                run([str(programs["pg_ctl"]), "-D", str(cluster), "-m", "fast", "-w", "stop"],
                    environment, output / "setup.txt")


if __name__ == "__main__":
    main()
