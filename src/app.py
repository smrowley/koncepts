from os import popen, environ, listdir
from os.path import isfile, join
from flask import Flask, render_template, request, Response
import time

startTime = time.time()

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


@app.route("/<path:path>")
def catchAll(path):
    delay = request.args.get("d", default=-1, type=int)
    fail = request.args.get("f", default=-1, type=int)

    timeDelta = time.time() - startTime

    if timeDelta < delay:
        return Response('{"message":"service is not ready"}', status=503, mimetype="application/json")

    if fail > 0 and timeDelta > fail:
        return Response('{"message":"catastrophic failure!"}', status=500, mimetype="application/json")

    print(path)
    return "ok"


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
