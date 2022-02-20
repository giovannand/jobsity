import os
import pandas as pd

import time
import requests

STATUS = os.environ['STATUS']

if STATUS=='Online':
    df = pd.read_csv('data/trips.csv')

    for i in df.index:
        data = df.loc[i].to_json()
        r = requests.post('http://api:8080/trips',data = data) 
        time.sleep(0.5)


            