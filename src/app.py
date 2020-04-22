from os import popen, environ, listdir
from os.path import isfile, join
from flask import Flask, render_template

app = Flask(__name__)

hostname = popen("cat /etc/hostname").read().strip()

contentFileNames = [f for f in listdir(
    environ["CONTENT_PATH"]) if isfile(join(environ["CONTENT_PATH"], f))]
contentFiles = {}

for fileName in contentFileNames:
    contentFiles[fileName] = open(
        f"{environ['CONTENT_PATH']}/{fileName}", "r").read()


@app.route("/")
def index():
    return render_template("index.html", hostname=hostname, contentFiles=contentFiles, envvars=environ)


@app.route("/plain")
def plain():
    return hostname + "\n"


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
