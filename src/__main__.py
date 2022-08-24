import argparse

from storage import create_database, db_session
from clients import DataCollector


parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Run a special container")
args = parser.parse_args()


if args.mode == "db":
    create_database()
    DataCollector.create_default_version_marker(db_session)

if args.mode == "sender":
    test_groups = [
        "ex.princess_band",
        "sonya_prosti",
        "wowwownow",
        "makcum.makcum.makcum",
        "olovo",
        "samcyband",
    ]

    # Тест внесения данных к текущей версии данных
    for group in test_groups:
        DataCollector.add_new_group(group, db_session)
