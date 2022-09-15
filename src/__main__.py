import argparse

from bot_engine import create_bot
from clients import RabbitClient
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

if args.mode == 'test':
    pass
