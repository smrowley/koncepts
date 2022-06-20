from os import popen, environ, listdir
from os.path import isfile, join
from flask import Flask, render_template, request, Response
from time import time
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import json
import dns.resolver

startTime = time()

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)

hostname = popen("cat /etc/hostname").read().strip()
timestamp_message = environ.get("TIMESTAMP_MESSAGE", "Automate all the things!")
content_path = environ.get("CONTENT_PATH", ".")

content_file_names = [f for f in listdir(
    content_path) if isfile(join(content_path, f))]
content_files = {}

for file_name in content_file_names:
    content_files[file_name] = open(
        f"{content_path}/{file_name}", "r").read()

discovery_hostname = environ.get("DISCOVERY_HOSTNAME", None)

pods = [("pod1", "172.1.1.1"), ("pod2", "172.1.1.2")]

@app.route("/")
def index():
    return render_template("index.html", hostname=hostname, content_files=content_files, envvars=environ, pods=pods)

@app.route("/timestamp")
def timestamp():
    return JsonResponse({"message": timestamp_message, "timestamp": int(time())}, status=200, add_hostname=False, indent=2)

@app.route("/discover")
def discover():
    pods = []

    #if discovery_hostname != None:
    #    dns.resolver.

    return JsonResponse({"pods": pods}, status=200, add_hostname=True, indent=2)

@app.route("/<path:path>")
def catch_all(path):
    startup_delay = request.args.get("startup_delay", -1, type=int)
    failure_delay = request.args.get("failure_delay", -1, type=int)
    readiness_period = request.args.get("readiness_period", 1, type=int)
    readiness_duration = request.args.get("readiness_duration", 1, type=int)

    time_delta = int(time() - startTime)

    if time_delta < startup_delay:
        return JsonResponse({"message": "too soon!"}, status=503, running_time=time_delta)

    if failure_delay > -1 and time_delta > failure_delay:
        return JsonResponse({"message": "catastrophic failure!"}, status=500, running_time=time_delta)

    if time_delta % readiness_period >= readiness_duration:
        return JsonResponse({"message": "unready!"}, status=503, running_time=time_delta)

    return JsonResponse({"message": "ok!"}, status=200, running_time=time_delta)


class JsonResponse(Response):
    def __init__(self, message_obj, status, add_hostname=True, indent=None, running_time=None):
        if add_hostname:
            message_obj["hostname"] = hostname
        if running_time != None:
            message_obj["running_time"] = running_time

        message = json.dumps(message_obj, indent=indent) + '\n'
        Response.__init__(self, message, status=status,
                          mimetype="application/json")


# used only for debugging when not using gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
