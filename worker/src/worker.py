import os 

import psycopg2
import json 
import time

import redis
import logging

logging.basicConfig(
    level=logging.INFO,
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

REDIS_LIST="trips"
REDIS_CHANNEL="trips"

def get_trip(list):
    r = redis.Redis(host='redis', port=6379, db=0)
    return r.rpop(list)


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
    conn=None
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
    
def publish_to_topic(message):
    r = redis.Redis(host='redis', port=6379, db=0)
    r.publish(REDIS_CHANNEL,message)

def publish_message_processed(trips_id):
    message=""
    if trips_id != None: 
        message += f"The message was saved. Trips Id: [{trips_id}] "
    else:
        message += f"We get an error to save the massage."
    
    publish_to_topic(message)

def save_trips():
    try:
        data = get_trip(REDIS_LIST)
        trip = json.loads(data)
        logger.info(f'Trip received')
        trips_id = insert_trip(trip)
        logger.info(f"Data was processed. Trips id [{trips_id}]")
    except Exception as ex:
        logger.error(f'Error: {ex}')

    publish_message_processed(trips_id)

time.sleep(10)

while (True):
    r = redis.Redis(host='redis', port=6379, db=0)
    if r.llen(REDIS_LIST) > 0:
        save_trips()
    else:
        time.sleep(1)

