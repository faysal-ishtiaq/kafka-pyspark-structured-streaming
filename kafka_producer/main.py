from kafka import KafkaProducer
from log_generator.RFC5434 import RFC5434
import multiprocessing as mp
import random
import time
import faker
import json
import syslog_rfc5424_parser


def send_log_to_kafka(_hostname):
    syslog_generator = RFC5434()
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    while True:
        message = json.dumps(syslog_rfc5424_parser.SyslogMessage.parse(syslog_generator.generate(_hostname)).as_dict()).encode('utf-8')
        print(f"[info] sending message: {message}")
        producer.send(topic="syslog", value=message)
        time.sleep(1/random.randint(2, 6))


if __name__ == "__main__":
    fake = faker.Faker()
    hostnames = [fake.hostname() for x in range(100)]
    processes = []
    for hostname in hostnames:
        p = mp.Process(target=send_log_to_kafka, args=(hostname,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
