import os 

from flask import Flask
from flask import request

import json


app = Flask(__name__)

@app.route("/trips", methods=['POST'])
def get_data():
    try:

        data = request.data
        print(data)
        #send request para enfileirar o dado
  
        return (f"Data was received ", 201)
    except Exception as ex:
        return (ex, 500)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))