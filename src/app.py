import os
from flask import Flask, render_template

app = Flask(__name__)

hostname = os.popen("cat /etc/hostname").read().strip()


@app.route("/")
def index():
    return render_template("index.html", hostname=hostname)


@app.route("/plain")
def plain():
    return hostname


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
