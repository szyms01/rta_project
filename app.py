from flask import Flask, jsonify, render_template
import pandas as pd
import random
from shapely.geometry import Point, Polygon
from confluent_kafka import Consumer, KafkaException, KafkaError
import socket
import logging
import json



# napisac konsumenta wewnątrz aplikacji flask - kopiowanie z consumer.py
KAFKA_BROKER = 'broker:9092'
SECOND_TOPIC = 'output_streaming'
SECOND_CG = 'output_streaming'
LAG = 10


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

# funkcja nasłuchująca topic
def consumer_message():    
    consumer = create_consumer(topic = SECOND_TOPIC, group_id = SECOND_CG)
    last_message = None
    try:
        # nasłuchuj konsumenta jednorazowo 
        message = consumer.poll()
        if message and not message.error():
            data = message.value().decode("utf-8") # string
            data_json = json.loads(data) # zamiana stringa na json
            df_data = pd.DataFrame(data_json)
            # df_data = df_data.reset_index()
            last_message = df_data.copy()
        elif message and message.error():
            if message.error().code() != KafkaError._PARTITION_EOF:
                raise KafkaException(msg.error())
    except Exception as e:
        print(f"Error: {e}")       
    finally:
        consumer.close()
    return last_message
    


app = Flask(__name__)

def generate_random_point():
    # random.seed(42)
    # Define a more detailed polygon for the boundaries of Paris
    paris_boundaries = Polygon([
    (2.224100, 48.815573), (2.229700, 48.817719), (2.235300, 48.819865), (2.240900, 48.822011),
    (2.246500, 48.824157), (2.252100, 48.826303), (2.257700, 48.828449), (2.263300, 48.830595),
    (2.268900, 48.832741), (2.274500, 48.834887), (2.280100, 48.837033), (2.285700, 48.839179),
    (2.291300, 48.841325), (2.296900, 48.843471), (2.302500, 48.845617), (2.308100, 48.847763),
    (2.313700, 48.849909), (2.319300, 48.852055), (2.324900, 48.854201), (2.330500, 48.856347),
    (2.336100, 48.858493), (2.341700, 48.860639), (2.347300, 48.862785), (2.352900, 48.864931),
    (2.358500, 48.867077), (2.364100, 48.869223), (2.369700, 48.871369), (2.375300, 48.873515),
    (2.380900, 48.875661), (2.386500, 48.877807), (2.392100, 48.879953), (2.397700, 48.882099),
    (2.403300, 48.884245), (2.408900, 48.886391), (2.414500, 48.888537), (2.420100, 48.890683),
    (2.425700, 48.892829), (2.431300, 48.894975), (2.436900, 48.897121), (2.442500, 48.899267),
    (2.448100, 48.901413), (2.453700, 48.903559), (2.459300, 48.905705), (2.464900, 48.907851),
    (2.469920, 48.902144),
    (2.469920, 48.815573),
    (2.224199, 48.815573),
    (2.224100, 48.815573)
    ])
    min_x, min_y, max_x, max_y = paris_boundaries.bounds
    while True:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if paris_boundaries.contains(random_point):
            return random_point




# napisać funkcję która zwraca wynik kafki 


# strona będzie wysyłać dane do serwera i pobierać dane z serwera
@app.route('/', methods=['GET', 'POST'])
def index():
    # na stronie głównej też zwracam jakoś wynik losowania z producenta
    random_point = generate_random_point() 
    # tu  df
    message_df = consumer_message()
    message_df = message_df.rename(columns={'station_name': 'Stacja', 'number_of_slots': 'Wszystkich', 'number_of_free_bikes': 'Wolnych rowerów', 'number_of_e_bikes': 'Wolnych rowerów elektrycznych', 'number_of_empty_slots': 'Miejsc', 'update_time': 'Godzina', 'distance_meters': 'Dystans [m]'})
    dataframe_html_message = message_df.to_html(classes='table table-bordered table-centered', index=False)
    # coordinates = {"latitude": random_point.y, "longitude": random_point.x }
    return render_template('index.html', latitude=random_point.y, longitude=random_point.x, 
                           message = dataframe_html_message)


        
            

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5000, debug = True)
