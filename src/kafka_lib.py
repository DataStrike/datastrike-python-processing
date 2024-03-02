import kafka.errors
from kafka import KafkaConsumer, KafkaProducer
import threading
import uuid
import queue
import json
import math
import time



class ProducerThread(threading.Thread):

    def __init__(self, url, date=None, nb_try_connection=30):

        threading.Thread.__init__(self)

        self.date = date
        self.nb_try_connection = nb_try_connection

        self.init_producer_ok, self.producer = self.init_producer(url)
        self.queue_sender = queue.Queue(2)

        self.finished = False


        print('[ProducerThread] Kafka Producer has been initiated...')

    def init_producer(self, url):

        count = 0
        while count < self.nb_try_connection:
            try:
                producer = KafkaProducer(bootstrap_servers=url,
                                         value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                         max_request_size=15728640)
                print('[ProducerThread] Connection with broker : OK')
                return True, producer

            except kafka.errors.NoBrokersAvailable:
                print(
                    "[ProducerThread] Impossible to connect with brokers, waiting kafka launch or check if kafka exist.")
                time.sleep(1)
                count += 1

        return False, None

    def run(self):

        while not self.finished:

            try:
                msg = self.queue_sender.get(timeout=1)
                topic = msg['topic']
                data = msg['data']

                if type(msg['data']) is dict:
                    msg['data'] = json.dumps(msg['data'])


                future = self.producer.send(topic, data)
                result = future.get(timeout=10)


            except queue.Empty as error:
                pass

        print("[ProducerThread][run] Finish.")



    def send(self, topic, data):

        msg = {"topic": topic, "data": data}
        self.queue_sender.put(msg)

    def stop(self):
        self.finished = True
        

class ConsumerThread(threading.Thread):
    def __init__(self, url,  date=None, nb_try_connection=30):

        threading.Thread.__init__(self)

        self.date = date
        self.nb_try_connection = nb_try_connection

        self.callback = {}
        self.topics = []
        self.finished = False

        self.message_split = {}

        self.init_consumer_ok, self.consumer = self.init_consumer(url)

        print('[ConsumerThread] Kafka Consumer has been initiated...')

    def init_consumer(self, url):

        count = 0
        while count < self.nb_try_connection:
            try:
                producer = KafkaConsumer(bootstrap_servers=url, max_partition_fetch_bytes=15728640,
                                         receive_buffer_bytes=(15 * 1024 * 1024), enable_auto_commit=False, auto_offset_reset='latest')
                print('[ConsumerThread] Connection with broker : OK')
                return True, producer

            except kafka.errors.NoBrokersAvailable:
                print(
                    "[ConsumerThread] Impossible to connect with brokers, waiting kafka launch or check if kafka exist.")
                time.sleep(1)
                count += 1
        return False, None


    def add_topics(self, topic, callback):

        self.callback[topic] = callback
        self.topics.append(topic)

    def run(self):

        if self.topics != [] :
        
            self.consumer.subscribe(self.topics)

            try:
                while not self.finished:
                    msg = self.consumer.poll(timeout_ms=100, max_records=200)
                    if not msg:
                        continue
                    else:
                        for topic_partition, messages in msg.items():
                            topic = topic_partition.topic

                            for message in messages:
                                data = message.value.decode('UTF-8')
                                print(data)
                                try:
                                    data = json.loads(data)
                                except json.decoder.JSONDecodeError:
                                    pass
                                self.callback[topic](topic, data)

                print("[ConsumerThread][run] Finish.")
            finally:
                self.consumer.close()
                print("[ConsumerThread][run] Close.")

    def stop(self):
        self.finished = True