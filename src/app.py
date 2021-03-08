from os import popen, environ, listdir
from os.path import isfile, join
from flask import Flask, render_template, request, Response
from time import time
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import json

startTime = time()

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)

hostname = popen("cat /etc/hostname").read().strip()
timestampMessage = environ.get("TIMESTAMP_MESSAGE", "Automate all the things!")
contentPath = environ.get("CONTENT_PATH", ".")

contentFileNames = [f for f in listdir(
    contentPath) if isfile(join(contentPath, f))]
contentFiles = {}

for fileName in contentFileNames:
    contentFiles[fileName] = open(
        f"{contentPath}/{fileName}", "r").read()


@app.route("/")
def index():
    return render_template("index.html", hostname=hostname, contentFiles=contentFiles, envvars=environ)

@app.route("/timestamp")
def timestamp():
    return JsonResponse({"message": timestampMessage, "timestamp": int(time())}, status=200, addHostname=False, indent=2)

@app.route("/<path:path>")
def catchAll(path):
    delay = request.args.get("d", -1, type=int)
    fail = request.args.get("f", -1, type=int)

    timeDelta = time() - startTime

    if timeDelta < delay:
        return JsonResponse({"message": "too soon!"}, status=503)

    if fail > 0 and timeDelta > fail:
        return JsonResponse({"message": "catastrophic failure!"}, status=500)

    return JsonResponse({"message": "ok!"}, status=200)


class JsonResponse(Response):
    def __init__(self, messageObj, status, addHostname=True, indent=None):
        if addHostname:
            messageObj["hostname"] = hostname

        message = json.dumps(messageObj, indent=indent) + '\n'
        Response.__init__(self, message, status=status,
                          mimetype="application/json")


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
