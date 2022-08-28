import argparse

from bot_engine import create_bot
from clients import RabbitClient, VkApiClient
from storage import create_database, db_session, DatabaseInterface
from worker import WorkerMessageHandler, PlotsGenerator, ReportGenerator


parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Run a special container")
args = parser.parse_args()


if args.mode == "db":
    create_database()

if args.mode == "bot":
    create_bot()

if args.mode == "worker":
    rabbitmq_client = RabbitClient(RabbitClient.DEFAULT_QUEUE)
    rabbitmq_client.consume(
        WorkerMessageHandler.worker_message_handler, RabbitClient.DEFAULT_QUEUE
    )
    rabbitmq_client.__del__()

# Тестовые группы
# test_groups = [
#     "xdlate",
#     "sonya_prosti",
#     "wowwownow",
#     "makcum.makcum.makcum",
#     "olovo",
#     "samcyband",
# ]

# if args.mode == "sender":
#     # Тест внесения данных к текущей версии данных
#     for group in test_groups:
#         DatabaseInterface.add_new_group(group, db_session)

# if args.mode == "getter":
#     for group in test_groups:
#         group_d = DatabaseInterface.get_groups_data(group, db_session)
#         print(group_d, '\n')
#
#         print(ReportTextGenerator.get_report_text(group_d))
#
#         PlotsGenerator.visualization1(
#             group_d["all_ages_dict"].keys(),
#             group_d["all_ages_dict"].values(),
#             f'All subs {group_d["title"]}',
#         )
#
#         PlotsGenerator.two_plots_visualisation(
#             group_d["title"],
#             group_d["men_ages_dict"].keys(),
#             group_d["men_ages_dict"].values(),
#             group_d["women_ages_dict"].keys(),
#             group_d["women_ages_dict"].values(),
#         )
#         print(type(group_d["men_ages_dict"])[0], group_d["men_ages_dict"][0])
#
#         PlotsGenerator.two_plots_in_one(
#             group_d["title"],
#             group_d["men_ages_dict"],
#             group_d["women_ages_dict"]
#         )

if args.mode == "test":
    WorkerMessageHandler.worker_message_handler(
        "xdlate" + WorkerMessageHandler.MESSAGE_DATA_SEP + "344371646"
    )
