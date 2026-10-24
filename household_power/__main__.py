import argparse

import pandas as pd

from . import data, db, report


def build(force):
    if db.DB_PATH.exists() and not force:
        print(f"{db.DB_PATH.name} already exists; use --force to rebuild it.")
        return

    raw = data.load_raw()
    quality = data.check_quality(raw)
    blocks = quality["missing_blocks"]
    print(f"Rows: {quality['rows']:,}")
    print(f"Duplicate rows: {quality['duplicate_rows']}, duplicate timestamps: {quality['duplicate_timestamps']}")
    print(f"Rows with a missing value: {quality['missing_rows']:,} in {len(blocks)} blocks "
          f"(longest {blocks.max():,} minutes)")

    cleaned = data.clean(raw)
    left = int(cleaned[data.SENSOR_COLS].isna().any(axis=1).sum())
    print(f"Filled gaps of up to {data.MAX_FILL_MINUTES} minutes; {left:,} rows still have a missing value")

    db.save_to_sqlite(cleaned)
    print(f"Wrote {db.DB_PATH}")


def main():
    parser = argparse.ArgumentParser(prog="household_power")
    commands = parser.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build", help="clean the data and build power.db")
    build_parser.add_argument("--force", action="store_true", help="rebuild even if power.db exists")

    commands.add_parser("report", help="save charts to figures/")

    query_parser = commands.add_parser("query", help="run a query from queries/")
    query_parser.add_argument("name", nargs="?", help="query file name without .sql; omit to list them")

    args = parser.parse_args()

    needs_db = args.command == "report" or (args.command == "query" and args.name)
    if needs_db and not db.DB_PATH.exists():
        parser.exit(1, f"{db.DB_PATH.name} not found. Run: python -m household_power build\n")

    if args.command == "build":
        build(args.force)
    elif args.command == "report":
        for path in report.make_all(db.DB_PATH):
            print(f"Wrote {path.relative_to(db.ROOT)}")
    elif args.command == "query":
        if args.name is None:
            print("\n".join(db.query_names()))
        else:
            with pd.option_context("display.max_rows", 40, "display.width", 120):
                print(db.run_query(args.name))


if __name__ == "__main__":
    main()
