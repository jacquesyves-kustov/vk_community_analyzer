import argparse
from storage import create_database, db_session, DataCollector


parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Run a special container")
args = parser.parse_args()


if args.mode == "db":
    create_database()
    DataCollector.create_default_version_marker(db_session)

if args.mode == "sender":
    # Тест внесения данных к текущей версии данных
    for group in ["huskytunes", "xdlate"]:
        DataCollector.add_new_group(group, db_session)
