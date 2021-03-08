from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import os

def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(os.environ["METRICS_PORT"])

def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)