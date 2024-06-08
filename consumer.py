import json
import os
import time 
import numpy as np
import socket
import logging
from datetime import datetime
from joblib import load
import pandas as pd
from confluent_kafka import Producer, Consumer
from multiprocessing import Process
from app import generate_random_point
from shapely.geometry import Point
from pyproj import Transformer

 
KAFKA_BROKER = 'broker:9092'
FIRST_TOPIC = 'project_streaming'
FIRST_CG = 'project_streaming'
SECOND_TOPIC = 'output_streaming'
SECOND_CG = 'output_streaming'
LAG = 5

 

# implementacja producenta
def create_producer():
    try:
        producer = Producer({
        "bootstrap.servers":KAFKA_BROKER,
        "client.id": socket.gethostname(),
        "enable.idempotence": True,
        "batch.size": 64000,
        "linger.ms":10,
        "acks": "all",
        "retries": 5,
        "delivery.timeout.ms":1000
        })
    except Exception as e:
        logging.exception("nie mogę utworzyć producenta")
        producer = None
    return producer

# implementacja konsumenta
def create_consumer(topic, group_id):
    try:
 
        consumer = Consumer({
          "bootstrap.servers": KAFKA_BROKER,
          "group.id": group_id,
          "client.id": socket.gethostname(),
          "isolation.level":"read_committed",
          "default.topic.config":{
                    "auto.offset.reset":"latest",
                    "enable.auto.commit": False
            }
        })
        consumer.subscribe([topic])
    except Exception as e:
        logging.exception("nie mogę utworzyć konsumenta")
        consumer = None
    return consumer



# napisz funkcję, która przy pomocy zczytywanych danych z konsumenta nr 1 
# wybierze 5 najbliższych stacji i będzie je przetwarzać w nowym topicu przy pomocy producenta 2

# na start napisz funkcje która przesyła dane do nowego topicu i wyświetlaj działanie producenta


consumer = create_consumer(topic = FIRST_TOPIC, group_id = FIRST_CG)
producer = create_producer()
generated_point = generate_random_point()
# stały wygenerowany punkt względem którego liczymy odległość
print("Punkt wygenerowany: ", generated_point)

# tworze transformację, która zmienia współrzędne punktu na współrzędne geograficzne 
transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
generated_point = Point(transformer.transform(generated_point.x, generated_point.y))

        
try:
    while True:
        # biorę w pętli dane konsumenta
        message = consumer.poll()
        # print(message)
        if message is None:
            continue
        if message.error():
            logging.error(f"CONSUMER error: {message.error()}")
            continue
        # deserializacja żeby móc ją przetwarzać
        
        # serializacja wiadomości żeby wczytać do kafki, wewnatrz do modyfikacji
        data = message.value().decode("utf-8") # string
        data_json = json.loads(data) # zamiana stringa na json
        
        # zamiana - reguła decyzyjna w postaci 5 najbliższych stacji i ich stanu 
        
        df_data = pd.DataFrame(data_json)
        df_data.set_index('station_name', inplace=True)
        # współrzędne punktu każdej stacji
        df_data['point'] = df_data[["longitude", "latitude"]].apply(Point, axis=1)
        # dystans of wygenerowanego punktu - w metrach 
        df_data['point'] = df_data['point'].apply(lambda point: Point(transformer.transform(point.x, point.y)))
        df_data['distance_meters'] = df_data['point'].apply(lambda point: generated_point.distance(point))
        
        # sortuj po najmniejszym distansie i zwracaj 5 najbliższych                           
        df_data = df_data.sort_values(by='distance_meters', ascending=True)
        # 5 najmniejszych wartości odległości 
        df_smallest = df_data.nsmallest(5, 'distance_meters')
        df_smallest['distance_meters'] = df_smallest['distance_meters'].round(2)
        df_smallest_cleaned = df_smallest.drop(columns=['point', 'latitude', 'longitude'])

        df_sm_cleaned_json = df_smallest_cleaned.reset_index().to_json(orient='records')
        # producent produkujący nowe dane 
        if producer is not None:
            try:
                producer.produce(topic=SECOND_TOPIC, value=df_sm_cleaned_json.encode("utf-8"))
                producer.flush()
                print(df_smallest_cleaned)
                # message to dane które powinien produkować
                time.sleep(LAG)
            except KeyboardInterrupt:
                producer.close()
        else:
            print("Producer not created")            

except KeyboardInterrupt:
    consumer.close()
        

