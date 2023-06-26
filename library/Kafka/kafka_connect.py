import json

from confluent_kafka import Producer

from core import settings


class KafkaConnect(object):
    _kafka_client = None

    @classmethod
    def get_kafka_client(cls):
        if not cls._kafka_client:
            cls._kafka_client = Producer({'bootstrap.servers': settings.KAFKA_BROKERS})
        return cls._kafka_client

    @classmethod
    def delivery_report(cls, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    @classmethod
    def write_data_to_kafka(cls, kafka_topic, messages, batch_size=50):
        """
        :param kafka_topic:
        :type kafka_topic:
        :param messages: (key, data)
        :param batch_size: default is 50
        :return:
        """
        for index in range(0, len(messages), batch_size):
            batch_messages = messages[index:index + batch_size]
            for batch_message in batch_messages:
                cls.get_kafka_client().poll(0)
                cls.get_kafka_client().produce(kafka_topic, json.dumps(batch_message).encode('utf-8'),
                                               callback=cls.delivery_report)
            cls.get_kafka_client().flush()
