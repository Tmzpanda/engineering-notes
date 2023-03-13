from kafka import KafkaProducer
import json
import uuid
import datetime
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def generate_event(sequence_number):
    return {
        "eventID": str(uuid.uuid4()),
        "eventTimestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "eventSequence": sequence_number
    }


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))

if __name__ == "__main__":
    for i in range(1, 101):
        message = generate_event(i)
        logging.info(f"Sending #{i} message: {message}")
        producer.send("stackpath-interview-homework", message)

    producer.flush()
    producer.close()
