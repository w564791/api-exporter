#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: how_bjl@live.cn
file: prometheus-test
time: 17-12-25 上午10:27
"""
from prometheus_client import start_http_server,Gauge,Summary,CollectorRegistry
from prometheus_client.core import GaugeMetricFamily

import time
import yaml,json,requests
ConnectTimeout = requests.exceptions.ConnectTimeout
ScannerError=yaml.scanner.ScannerError
registry = CollectorRegistry()
def Scan_conf():

    stream = open('/tmp/config.yml','r')
    ff= yaml.load_all(stream)
    data=[]
    while True:
        try:
            data.append(next(ff))
        except ScannerError    as scanner_error:
            print(scanner_error.problem_mark)
            break
        except StopIteration as stop_err:
            # print(stop_err.value)
            break
    return data
data_list = Scan_conf()

def Result(data_list):
    get_code = []
    for data in data_list:
        if data:
            url = "%s://%s:%s%s" % (data["protocol"], data["host"], data["port"], data["url"])
            metadata = data['data']
            method = data['method']
            header = data['header']
            projectCode = data['projectCode']
            result = {}
            result['program'] = data['program']
            result['env'] = data['env']
            result['project'] = data['project']
            result['metrics'] = data['metrics']
            if method == 'POST':
                try:
                    resbonse = requests.post(url=url, data=json.dumps(metadata), headers=header,timeout=2)
                    result['http_code'] = resbonse.status_code
                    result['program_code'] = resbonse.json()[projectCode]
                except :
                    result['http_code'] = 0
                    result['program_code'] = 0
                    # continue
            elif method == "GET":
                try:
                    resbonse = requests.get(url=url,headers=header,timeout=2)
                    result['http_code'] = resbonse.status_code
                    result['program_code'] = resbonse.json()[projectCode]
                except :
                    result['http_code'] = 0
                    result['program_code'] = 0
                    # continue
            get_code.append(result)
    return get_code




REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST2 = Gauge('cluster_current_time', 'kubernetes pods  current time', ['dates'])
RESOULT = {}
result = Result(data_list)
for data in result:
    for monitor_metrics in data["metrics"]:
        metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)
        ENV = data['env']

        RESOULT[metrics] = [Gauge(metrics, metrics, ['env']), data[monitor_metrics],data['env']]

@REQUEST_TIME.time()
def get_REQUEST():
    result = Result(data_list)
    for data in result:
        for monitor_metrics in data["metrics"]:
            metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)

            RESOULT[metrics][1] = data[monitor_metrics]
    print(result)
    print(RESOULT)
    for key,value in RESOULT.items():
        value[0].labels(env=value[2]).set(value[1])
    time.sleep(30)

if __name__ == '__main__':
#     # Start up the server to expose the metrics.
    start_http_server(8000)
#     # Generate some requests.
    while True:

        get_REQUEST()


