import pika
from config import RMQ_CONNECTION_STR


class RabbitClient:
    DEFAULT_QUEUE = "default_queue"

    def __init__(self, queue_name: str, connection_str: str = RMQ_CONNECTION_STR):
        self.connection = pika.BlockingConnection(pika.URLParameters(connection_str))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def get_connection(self):
        """Возвращает соединение с брокером"""

        return self.connection

    def publish(self, message_body: str, queue_name: str):
        """
        Общий интерфейс для отправки сообщений.

        :param message_body: сообщение.
        :param queue_name: очередь брокера.
        """

        self.channel.basic_publish(
            exchange="", routing_key=queue_name, body=message_body.encode()
        )

        print(" [CONSUMER] Message", message_body, "is sent!")

    def consume(self, handler, queue_name: str):
        """
        Общий интерфейс для отправки сообщений.

        :param handler: функция для обработки сообщений (описаны в .message_processing.py).
        :param queue_name: очередь брокера.
        """

        def callback(
            ch,
            method: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body,
        ):
            message_body = body.decode()
            print(" [WORKER] Received message:", message_body)

            handler(message_body)

            # Явно сообщаем брокеру, что ОДНО сообщение обработано
            ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

        # Ограничиваем поток сообщений для потребителя
        self.channel.basic_qos(prefetch_count=1)

        # Ставим слушателя на очередь новых слов,
        # передаем логику принятия сообщений и автоматически не подтверждаем обработку
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=False
        )

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def __del__(self):
        # Явно закрываем канал
        self.channel.close()
        # Явно закрываем соединение
        self.connection.close()
