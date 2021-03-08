from os import popen, environ, listdir
from os.path import isfile, join
from flask import Flask, render_template, request, Response
from time import time
import json

startTime = time()

app = Flask(__name__)

hostname = popen("cat /etc/hostname").read().strip()

contentFileNames = [f for f in listdir(
    environ["CONTENT_PATH"]) if isfile(join(environ["CONTENT_PATH"], f))]
contentFiles = {}

for fileName in contentFileNames:
    contentFiles[fileName] = open(
        f"{environ['CONTENT_PATH']}/{fileName}", "r").read()

timestampMessage = environ.get("TIMESTAMP_MESSAGE", default="Automate all the things!")

@app.route("/")
def index():
    return render_template("index.html", hostname=hostname, contentFiles=contentFiles, envvars=environ)

@app.route("/timestamp")
def timestamp():
    return JsonResponse({"message": timestampMessage, "timestamp": time()}, status=200, addHostname=False)

@app.route("/<path:path>")
def catchAll(path):
    delay = request.args.get("d", default=-1, type=int)
    fail = request.args.get("f", default=-1, type=int)

    timeDelta = time() - startTime

    if timeDelta < delay:
        return JsonResponse({"message": "too soon!"}, status=503)

    if fail > 0 and timeDelta > fail:
        return JsonResponse({"message": "catastrophic failure!"}, status=500)

    return JsonResponse({"message": "ok!"}, status=200)


class JsonResponse(Response):
    def __init__(self, messageObj, status, addHostname=True):
        if addHostname:
            messageObj["hostname"] = hostname

        message = json.dumps(messageObj, indent=2) + '\n'
        Response.__init__(self, message, status=status,
                          mimetype="application/json")


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
