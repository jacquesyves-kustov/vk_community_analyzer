import argparse

from bot_engine import create_bot
from clients import RabbitClient, VkApiClient
from storage import create_database
from worker import WorkerMessageHandler

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

# if args.mode == 'test':
    # # Get list of members dict
    # test_users = VkApiClient.get_total_members_list('wowwownow')
    #
    # # Collect data on their subs
    # found_groups = dict()
    # for user in test_users:
    #     r = VkApiClient.send_get_request(VkApiClient.VK_USERS_GET_SUBS, user_id=user['true_user_id'])
    #     r = r.json()
    #     print(r)
    #
    #     if 'error' in r:
    #         continue
    #
    #     for group_id in r['response']['groups']['items']:
    #         found_groups[group_id] = found_groups.setdefault(group_id, 0) + 1
    #
    # # Sorted by value
    # found_groups = dict(sorted(found_groups.items(), key=lambda item: item[1]))
    #
    # # define
    # sorted_values = sorted(found_groups.values())
    # sorted_values.reverse()
    # print(sorted_values)
    #
    # if len(sorted_values) > 10:
    #     sorted_values = sorted_values[:10]
    #
    # for popular_group in found_groups:
    #     if found_groups[popular_group] in sorted_values:
    #         print(f'{popular_group}: {found_groups[popular_group]}')
    #
