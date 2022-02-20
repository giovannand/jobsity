import os 

from flask import Flask
from flask import request

import psycopg2
import json 

app = Flask(__name__)

def get_connection():
    PGHOST='db'
    PGDATABASE='jobsity'
    PGUSER='postgres'
    PGPASSWORD='postgres_password'

    conn_string = f"host={PGHOST} port=5432 dbname={PGDATABASE} user={PGUSER} password={PGPASSWORD}"
    return psycopg2.connect(conn_string)


def insert_trip(trip_data):
    region = trip_data.get('region')
    origin = trip_data.get('origin_coord')
    destination = trip_data.get('destination_coord')
    trip_datetime = trip_data.get('datetime')
    datasource = trip_data.get('datasource')

    sql = "INSERT INTO trips(region,origin_coord,destination_coord,trip_datetime,datasource) "
    sql += f"VALUES('{region}','{origin}','{destination}','{trip_datetime}','{datasource}') "
    sql += "RETURNING id;"
    trips_id = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (trip_data,))
        trips_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

    return trips_id


@app.route("/trips", methods=['POST'])
def get_data():
    try:

        data = request.data
        trip = json.loads(data)
        trips_id = insert_trip(trip)
        print(f'Data war insert succesfully {trips_id}')
        return (f"Data was received. Trips id [{trips_id}] ", 201)
    except Exception as ex:
        return (ex, 500)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))