import os
import shutil
from typing import Dict
from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="stackpath-consumer",
    enable_auto_commit=True,
    auto_offset_reset='latest',
    consumer_timeout_ms=10000
)


def transform(info: Dict):
    eventID = info['eventID']
    eventTimestamp = info['eventTimestamp']
    eventSequence = info['eventSequence']

    if (eventSequence % 3 == 0) & (eventSequence % 5 == 0):
        translatedEventSequence = 'FizzBuzz'
    elif eventSequence % 3 == 0:
        translatedEventSequence = 'Fizz'
    elif eventSequence % 5 == 0:
        translatedEventSequence = 'Buzz'
    else:
        translatedEventSequence = eventSequence

    return ','.join([eventID, eventTimestamp, str(eventSequence), str(translatedEventSequence)])


def append_to_file(msg, file):
    with open(f"temp/{file}", 'a') as f:
        f.write(msg + '\n')

    f.close()


if __name__ == "__main__":
    consumer.subscribe(["stackpath-interview-homework"])
    for message in consumer:
        logging.info(f"Receiving message: {message}")
        append_to_file(transform(message.value), 'stackpath-homework-output.txt')

    consumer.close()
