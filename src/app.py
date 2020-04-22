import os
from flask import Flask, render_template

app = Flask(__name__)

hostname = os.popen("cat /etc/hostname").read().strip()

contentBase = "/usr/local/etc/content"
contentFileNames = os.listdir(contentBase)
contentFiles = {}

for fileName in contentFileNames:
    contentFiles[fileName] = open(f"{contentBase}/{fileName}", "r").read()


@app.route("/")
def index():
    return render_template("index.html", hostname=hostname, contentFiles=contentFiles, envvars=os.environ)


@app.route("/plain")
def plain():
    return hostname + "\n"


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
