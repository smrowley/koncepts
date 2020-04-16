import os
from flask import Flask, render_template

application = Flask(__name__)

hostname = os.popen("cat /etc/hostname").read().strip()


@application.route("/")
def index():
    return render_template("index.html", hostname=hostname)


@application.route("/plain")
def plain():
    return hostname


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
