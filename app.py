'''
SEPTA arrivals, departures, etc. by station
'''
# externals
from flask import Flask, render_template, request, jsonify

# internals
from utils import utils
from utils import septa

# initialize the flask app
app = Flask(__name__)

# initialize the connector for septa client
septa_client = septa.SeptaAPIClient()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    station_start = request.form.get('station_start')  # Get data from the form
    station_end = request.form.get('station_end')  # Get data from the form

    septa_data = septa_client.get_next_arrivals(
        depart_station=station_start,
        arrive_station=station_end,
        num_results=3
    )
    septa_cleaned = utils.deconstruct_arrivals(septa_data)

    response = {
        "path": f"{station_start} - {station_end}",
        "trains": septa_cleaned
    }

    return jsonify(response)  # Respond with JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)