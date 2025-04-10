from flask import Flask
import logging
import os
from common.versionDIs import selectVersion
from countries.countryEndpoints import countryRouter
from scripts.scriptEndpoints import scriptRouter

flaskPort = int(os.environ["FLASK_PORT"]) if os.environ["FLASK_PORT"] else 3000

app = Flask(__name__)
app.config["APPLICATION_ROOT"] = "."
app.config["FLASK_DEBUG"] = 1
app.logger.setLevel(logging.INFO)

app.register_blueprint(countryRouter)
app.register_blueprint(scriptRouter)


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/version")
def version():
    return {"version": selectVersion()["version"]}


if __name__ == "__main__":
    # TODO: Add env check to set debug=True
    app.run(host="0.0.0.0", port=flaskPort)
