import argparse

from bot_engine import PlotsGenerator
from storage import create_database, db_session, DataCollector, DataSender


parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Run a special container")
args = parser.parse_args()


if args.mode == "db":
    create_database()

if args.mode == "sender":
    test_groups = [
        "xdalte",
        "sonya_prosti",
        "wowwownow",
        "makcum.makcum.makcum",
        "olovo",
        "samcyband",
    ]

    # Тест внесения данных к текущей версии данных
    for group in test_groups:
        DataCollector.add_new_group(group, db_session)

if args.mode == "getter":
    test_groups = [
        "sonya_prosti",
        "wowwownow",
        "makcum.makcum.makcum",
        "olovo",
        "samcyband",
    ]

    for group in test_groups:
        group_d = DataSender.get_groups_data(group, db_session)
        print(group_d)

        PlotsGenerator.visualization1(
            group_d["all_ages_dict"].keys(),
            group_d["all_ages_dict"].values(),
            f'All subs {group_d["title"]}',
        )
