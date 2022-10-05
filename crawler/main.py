from crawler import flask
from config.app import App

app = App()
flask.config["rq"] = app.rq

if __name__ == "__main__":
  flask.run(host="0.0.0.0", port=5000, debug=True)
