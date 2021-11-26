from timeseries import last_pot

import json

import falcon
import hug
from prometheus_client import Counter, CollectorRegistry, Gauge, exposition

KILTIS = CollectorRegistry()

class Metrics():
    def __init__(self, registry):
        self.count = Counter("kiltis_kahviot_count", "Number of measurements received", ["id"], registry=registry)
        self.temperature = Gauge("kiltis_kahviot_temperature", "Temperature in Celsius", ["id"], registry=registry)
        self.millis = Gauge("kiltis_kahviot_millis", "Milliseconds since sensor restart", ["id"], registry=registry)
        self.bad_http_responses = Gauge("kiltis_kahviot_bad_http_responses", "Number of bad http resonses received by the sensor", ["id"], registry=registry)

metrics = Metrics(KILTIS)

@hug.exception(json.decoder.JSONDecodeError)
def invalid_json(response):
    response.status = falcon.HTTP_400
    return {"errors": {"body": "invalid json"}}

@hug.get('/metrics', version=1, output=hug.output_format.text)
def get_metrics(response):
    """Prometheus endpoint"""
    content = exposition.generate_latest(KILTIS)
    # application debug info generated separately
    content += exposition.generate_latest()
    return content.decode("utf-8")

@hug.post('/metrics/new', version=1, output=hug.output_format.text)
def new_metrics(response, id: hug.types.number, temperature: hug.types.float_number, millis: hug.types.number, bad_http_responses: hug.types.number, charset='ascii'):
    """Submit a measurement"""

    if not 0 < id < 10:
        response.status = falcon.HTTP_400
        return {"errors": {"id": "Must supply an id between 1..9"}}
    
    # filter out -127 C
    # BUGBUG
    if temperature == -127.:
        print(f"-127 C ignored from {id}")
        return "OK (ignored based on temperature)"

    metrics.count.labels(id).inc()
    metrics.temperature.labels(id).set(temperature)
    metrics.millis.labels(id).set(millis)
    metrics.bad_http_responses.labels(id).set(bad_http_responses)
    return "OK"

@hug.get('/pot/last', version=1, examples="id=1").cache(max_age=300)
def get_last_pot(response, id: hug.types.number):
    """ISO timestamp of the last pot brewed"""
    if not 0 < id < 10:
        response.status = falcon.HTTP_400
        return {"errors": {"id", "Must supply an id between 1..9"}}
    return {"date": last_pot(id)}