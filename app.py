from flask import Flask, jsonify, render_template
import pandas as pd
import random
from shapely.geometry import Point, Polygon
# from consumer import generate_random_point

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







# strona będzie wysyłać dane do serwera i pobierać dane z serwera
@app.route('/', methods=['GET', 'POST'])
def index():
    # na stronie głównej też zwracam jakoś wynik losowania z producenta
    random_point = generate_random_point() 
    # coordinates = {"latitude": random_point.y, "longitude": random_point.x }

    # Example dataframe
    data = {
        'Column1': ['A', 'B', 'C', 'D'],
        'Column2': [1, 2, 3, 4],
        'Column3': [10.1, 20.2, 30.3, 40.4]
    }
    df = pd.DataFrame(data)

    dataframe_html = df.to_html(classes='table table-striped table-bordered', index=False)

    return render_template('index.html', latitude=random_point.y, longitude= random_point.x, dataframe=dataframe_html)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5000, debug = True)
