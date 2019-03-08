from flask import request
import time
import sys

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)

INTERNAL_ERROR_COUNT = Counter(
    'internal_error_count', 'Internal error Count',
    ['app_name', 'method', 'endpoint', 'error_label']
)

REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
                            ['app_name', 'method', 'endpoint']
                            )


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('key_value_app', request.method, request.path).observe(resp_time)
    return response


def record_request_data(response):
    sys.stdout.write("Request path: %s Request method: %s with status code %s\n" %
                     (request.path, request.method, response.status_code))
    REQUEST_COUNT.labels('key_value_app', request.method, request.path,
                         response.status_code).inc()
    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
