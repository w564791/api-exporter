#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: how_bjl@live.cn
file: prometheus-test
time: 17-12-25 上午10:27
"""
from prometheus_client import start_http_server,Gauge
from prometheus_client.core import GaugeMetricFamily
import time
import yaml,json,requests
ConnectTimeout = requests.exceptions.ConnectTimeout
ScannerError=yaml.scanner.ScannerError
# def Scan_conf():
#
#     stream = open('config.yml','r')
#     ff= yaml.load_all(stream)
#     data=[]
#     while True:
#         try:
#             data.append(next(ff))
#         except ScannerError    as scanner_error:
#             print(scanner_error.problem_mark)
#             break
#         except StopIteration as stop_err:
#             # print(stop_err.value)
#             break
#     return data
# data_list = Scan_conf()
# '''
# for data in data_list:
#     if data:
#         url = "%s//:%s:%s%s"%(data["protocol"],data["host"],data["port"],data["url"])
#
#         print(url)
#         '''
# def Result(data_list):
#     get_code = []
#     for data in data_list:
#         if data:
#             url = "%s://%s:%s%s" % (data["protocol"], data["host"], data["port"], data["url"])
#             metadata = data['data']
#             method = data['method']
#             header = data['header']
#             projectCode = data['projectCode']
#             result = {}
#             result['program'] = data['program']
#             result['env'] = data['env']
#             result['project'] = data['project']
#             result['metrics'] = data['metrics']
#             if method == 'POST':
#                 try:
#                     resbonse = requests.post(url=url, data=json.dumps(metadata), headers=header,timeout=2)
#                     result['http_code'] = resbonse.status_code
#                     result['program_code'] = resbonse.json()[projectCode]
#                 except ConnectTimeout:
#                     result['http_code'] = 0
#                     result['program_code'] = 0
#                     continue
#             elif method == "GET":
#                 try:
#                     resbonse = requests.get(url=url,headers=header,timeout=2)
#                     result['http_code'] = resbonse.status_code
#                     result['program_code'] = resbonse.json()[projectCode]
#                 except ConnectTimeout:
#                     result['http_code'] = 0
#                     result['program_code'] = 0
#                     continue
#             get_code.append(result)
#     return get_code
#
# result = Result(data_list)
# print(result)


GaugeMetricFamily("cluster_current_time","cluster current time",labels=['host_name']).add_metric("hosts","100")
GaugeMetricFamily("cluster_current_time","cluster current time",labels=['host_name']).add_metric("hosts","100")

# REQUEST = Gauge('cluster_current_time', 'kubernetes pods  current time',)
# REQUEST.set_to_current_time()
# def get_REQUEST(result):
#     for data in result:
#         for monitor_metrics in data["metrics"]:
#             metrics = "%s_%s_%s_%s"%(data["program"],data["env"],data["project"],monitor_metrics)
#             Gauge(metrics, metrics).set(data[monitor_metrics])
#             REQUEST.set(data[monitor_metrics])

# REQUEST.track_inprogress()
# get_REQUEST(result)

#
# REQUEST = Gauge('cluster_current_time', 'kubernetes pods  current time',)
#
#
#
#
# REQUEST = Gauge('cluster_current_time', 'kubernetes pods  current time', )
# if __name__ == '__main__':
# #     # Start up the server to expose the metrics.
#     start_http_server(8000)
# #     # Generate some requests.
#     while True:
# #     #     process_request()
# #         time.sleep(3)
#
# #         REQUEST.set_to_current_time()
#         REQUEST.dec()
#
#
#
#         # for data in result:
#         #     for monitor_metrics in data["metrics"]:
#         #         metrics = "%s_%s_%s_%s" % (data["program"], data["env"], data["project"], monitor_metrics)
#         #         Gauge(metrics, metrics).set(data[monitor_metrics])
#
#         REQUEST.track_inprogress()

