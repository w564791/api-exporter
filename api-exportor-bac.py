#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: how_bjl@live.cn
file: prometheus-test
time: 17-12-25 上午10:27
"""
from prometheus_client import start_http_server,Gauge,Summary,CollectorRegistry
from prometheus_client.core import GaugeMetricFamily
import sys
import time
import yaml,json,requests
ConnectTimeout = requests.exceptions.ConnectTimeout
ScannerError=yaml.scanner.ScannerError
registry = CollectorRegistry()
try:
    args = int(sys.argv[1])
except ValueError as e:
    print(e.args)
    exit(2)

def http_ok(url,result,data,resbonse,projectCode):
    """当获取resbonse成功时，为result赋值"""
    print("%s get OK! %s" % (url,resbonse.status_code))
    for i in data['metrics']:
        if i == "http_code":
            result[i] = resbonse.status_code
        elif i == "program_code":
            result[i] = resbonse.json()[projectCode]
    return result
def http_timeout(url,result,data):
    """当获取resbonse超时时，为result赋值为0"""
    print("%s get Error! " % url)
    for i in data['metrics']:
        if i == "http_code":
            result[i] = 0
        elif i == "program_code":
            result[i] = 0
    return result

def Scan_conf():
    """读取yaml文件的内容"""
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
    '''格式化yaml中的metrics为字典（原为list）'''
    for metrics in data:
        print(metrics['project'],metrics['metrics'])
        metrics_data = {}
        for  metrics_format in metrics['metrics']:
            metrics_data[metrics_format] = metrics_format
        metrics['metrics'] = metrics_data

    return data
data_list = Scan_conf()

def Result(data_list):
    """获取url的返回值"""
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
                    http_ok(url,result,data, resbonse, projectCode)
                except  :

                    http_timeout(url,result, data)

                    # continue
            elif method == "GET":
                try:
                    resbonse = requests.get(url=url,headers=header,timeout=2)
                    http_ok(url,result,data, resbonse, projectCode)
                except :
                    http_timeout(url,result, data)

                    # continue
            get_code.append(result)
    return get_code




REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST2 = Gauge('cluster_current_time', 'kubernetes pods  current time', ['dates'])

RESOULT = {}
result = Result(data_list)
for data in result:
    """初始化RESOULT字典，Gauge无法重复赋值"""
    for monitor_metrics in data["metrics"]:
        metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)
        annotations = "program of %s, and project of %s ,metrics %s" % (data["program"], data["project"], monitor_metrics)
        ENV = data['env']

        RESOULT[metrics] = {"Gauge": Gauge(metrics, annotations, ['env']), "data": data[monitor_metrics],"ENV": data['env']}

@REQUEST_TIME.time()
def get_REQUEST(RESOULT,args):
    REQUEST2.labels(dates='date').set(time.time())
    result = Result(data_list)
    for data in result:
        print(data)
        for monitor_metrics in data["metrics"]:
            metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)

            RESOULT[metrics]["data"] = data[monitor_metrics]
    # print(result,244)
    print(RESOULT)
    for key,value in RESOULT.items():
        value["Gauge"].labels(env=value["ENV"]).set(value["data"])
    time.sleep(args)

if __name__ == '__main__':
#     # Start up the server to expose the metrics.
    start_http_server(8000)
#     # Generate some requests.
    while True:

        get_REQUEST(RESOULT,args)


