import json
import time
import logging
import socket
from datetime import datetime
from numpy.random import uniform, choice, randn
import random
import pandas as pd
from confluent_kafka import Producer

 
KAFKA_BROKER = 'broker:9092'
TRANSACTION_TOPIC = 'project_streaming'
LAG = 10

# tworzy producenta
def create_producer():
    try:
        producer = Producer({
            "bootstrap.servers": KAFKA_BROKER,
            "client.id": socket.gethostname(),
            "enable.idempotence": True,
            "batch.size": 64000,
            "linger.ms": 10,
            "acks": "all",
            "retries": 5,
            "delivery.timeout.ms": 1000
        })
    except Exception as e:
        logging.exception("Nie mogę utworzyć producenta")
        producer = None
    return producer
 
def bike_random(row):
    bike_number = random.randint(0, row['Number of slots'])
    e_bike_number = random.randint(0, row['Number of slots'] - bike_number)
    empty_slots = row['Number of slots'] - bike_number - e_bike_number
    return bike_number, e_bike_number, empty_slots
 
def generate_json(df):
    # generate json generuje tablicę danych jedną słowników 
    all_messages = []
    current_time_iso = datetime.utcnow().isoformat()
    current_dt = datetime.fromisoformat(current_time_iso)

    # Convert timestamp to a more visually appealing format
    current_time = current_dt.strftime("%H:%M:%S %d-%m-%Y")
    
    
    for index, row in df.iterrows():
        # w pętli losuje wiersz danych i dodaję do ramki 
        bike_number, e_bike_number, empty_slots = bike_random(row)
        message = {
            "station_name": row['Station Name'],
            "latitude": row['Latitude'],
            "longitude": row['Longitude'],
            "number_of_slots": row['Number of slots'],
            "number_of_free_bikes": bike_number,
            "number_of_e_bikes": e_bike_number,
            "number_of_empty_slots": empty_slots,
            "update_time": current_time
        }
        all_messages.append(message)
    return all_messages
# wysyłaj wiadomości do producenta o argumencie messages
def send_messages(producer, messages):
    try:
        producer.produce(topic=TRANSACTION_TOPIC, value=json.dumps(messages).encode("utf-8"))
        producer.flush()
    except Exception as e:
        logging.exception("Błąd podczas wysyłania wiadomości do Kafka")


# tworze instancję producenta  
producer = create_producer()

# inicjacja działania producenta nr 1
if producer is not None:
    # ładuje dane zczytane z api z excela, imitacja procesu produkowania strumienia danych 
    df = pd.read_excel("bike.xlsx")
    # _id = 0
    try:
        while True:
            all_messages = generate_json(df)
            send_messages(producer, all_messages) 
            print(all_messages)         
            time.sleep(LAG)
    except KeyboardInterrupt:
        producer.close()
else:
    print("Producer not created")
    