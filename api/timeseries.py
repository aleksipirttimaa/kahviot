from datetime import datetime

from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime

PROMETHEUS_URL = "http://localhost:9090"
STEP = 30

def prometheus():
    return PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)

def last_pot(id):
    prom = prometheus()

    query = '(deriv(kiltis_kahviot_temperature{{id="{0}"}}[10m]) > bool 0.02) * (kiltis_kahviot_temperature{{id="{0}"}} > bool 43 )'.format(id)

    timeserieses = prom.custom_query_range(
        query=query,
        start_time=parse_datetime("18h"),
        end_time=parse_datetime("now"),
        step=str(STEP)
    )

    if len(timeserieses) != 1 :
        return None
    covfes = [covfe for covfe in timeserieses[-1]["values"] if float(covfe[1]) > 0.]
    timestamp = covfes[-1][0]
    timestamp = timestamp - (timestamp % (2 * STEP)) # round down to two times step
    covfetime = datetime.fromtimestamp(timestamp).astimezone()
    return covfetime