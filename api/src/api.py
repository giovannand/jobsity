import os 

from flask import Flask
from flask import request

import redis

app = Flask(__name__)

REDIS_LIST="trips"
    
def send_trip_to_list(list, message):
    r = redis.Redis(host='redis', port=6379, db=0)
    r.lpush(list, message)


@app.route("/trips", methods=['POST'])
def get_data():
    try:

        data = request.data
        send_trip_to_list(REDIS_LIST, data)
        return (f"Data was send to redis ", 201)
    except Exception as ex:
        return (ex, 500)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))