from flask import Flask
from flask_cors import CORS
from src.eggeliste_crawler.API.PlayerAPI import get_player_stats
from flask import request
from src.server.DataObjects import *

app = Flask(__name__)
CORS(app)


@app.route('/<name>')
def example(name):
    res = get_player_stats(name).to_json()
    print(res)
    return res


if __name__ == '__main__':
    app.run()