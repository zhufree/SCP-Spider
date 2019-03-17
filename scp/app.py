from flask import Flask, jsonify
from .latest_spy import get_latest_article

app = Flask(__name__)


@app.route("/")
def hello():
    result_list = get_latest_article(0, 0)
    return jsonify(result_list)


if __name__ == '__main__':
    app.run()
