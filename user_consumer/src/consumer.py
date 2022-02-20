import os 
import time 
import logging
import redis

logging.basicConfig(
    level=logging.INFO,
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

REDIS_CHANNEL="trips"

r = redis.Redis(host='redis', port=6379, db=0)
subscriber = r.pubsub()
subscriber.psubscribe(REDIS_CHANNEL)

while (True):
    message = subscriber.get_message()

    if message:
        logger.info(f'{message["data"]}')
    else:
        time.sleep(0.5)