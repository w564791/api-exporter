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
import re
ConnectTimeout = requests.exceptions.ConnectTimeout
ScannerError=yaml.scanner.ScannerError
registry = CollectorRegistry()
args_list = sys.argv[1:]
print(args_list)
def get_args(args_list):
    """获取脚本参数"""
    args = 30
    cluster_env = 'swarm'
    config_file = '/tmp/config.yml'
    for Arg in args_list:
        Arg=re.split("[=]",Arg)
        print(Arg)
        if "-i" in Arg:
            try:
                args = int(Arg[1])
            except ValueError as e:
                print(e.args)
                exit(1)
            except IndexError as e:
                print(e.args)
                exit(2)
        elif "-e" in Arg:
            try:
                cluster_env = Arg[1]
            except IndexError as e:
                cluster_env = 'swarm'
                print(e.args)
                exit(3)
        elif "-f" in Arg:
            try:
                config_file = Arg[1]
            except IndexError as e:
                config_file = 'config.yml'
                print(e.args)
                exit(4)
        elif "help" or "-h" in Arg:
            print(
                """
                -i=int 设置监控时间间隔,默认30s
                -e=[swarm|k8s] 设置cluster环境，当前支持k8s或者swarm，默认swarm
                -f=path 指定配置文件,默认为./config.yml
                --help or -h 查看帮助
                """
            )
            exit(0)

    return args,cluster_env,config_file

args,cluster_env,config_file = get_args(args_list)
print("config","---->",config_file)
print("cluster_env","---->",cluster_env)

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
            result[i] = -1
        elif i == "program_code":
            result[i] = -1
    return result

def Scan_conf(config_file):
    """读取yaml文件的内容"""
    stream = open(config_file,'r')
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
        try:
            print(metrics['project'],metrics['metrics'])
            metrics_data = {}
            for  metrics_format in metrics['metrics']:
                metrics_data[metrics_format] = metrics_format
            metrics['metrics'] = metrics_data
        except TypeError:
            pass

    return data
data_list = Scan_conf(config_file)

def Result(data_list,cluster_env):
    """获取url的返回值"""
    get_code = []
    for data in data_list:
        # print(data)
        if data:
            if cluster_env == "k8s":
                url = "%s://%s.%s:%s%s" % (data["protocol"], data["host"], data['namespace'],data["port"], data["url"])
            elif cluster_env == "swarm":
                url = "%s://%s:%s%s" % (data["protocol"], data["host"], data["port"], data["url"])
            elif cluster_env == "local":
                url = "%s://192.168.31.233:%s%s" % (data["protocol"],data["port"], data["url"])
            metadata = data['data']
            method = data['method']
            header = data['header']
            projectCode = data['projectCode']
            result = {}
            result['program'] = data['program']
            result['env'] = cluster_env
            result['project'] = data['project']
            result['metrics'] = data['metrics']
            """尝试获取resbonse"""
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
result = Result(data_list,cluster_env)
for data in result:
    """初始化RESOULT字典，Gauge无法重复赋值"""
    for monitor_metrics in data["metrics"]:
        metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)
        annotations = "program of %s, and project of %s ,metrics %s" % (data["program"], data["project"], monitor_metrics)
        ENV = cluster_env

        RESOULT[metrics] = {"Gauge": Gauge(metrics, annotations, ['env']), "data": data[monitor_metrics],"ENV": cluster_env}

@REQUEST_TIME.time()
def get_REQUEST(RESOULT,args,cluster_env):
    REQUEST2.labels(dates='date').set(time.time())
    """再次获取值并重新为RESOULT[metrics]["data"]赋值"""
    result = Result(data_list,cluster_env)

    for data in result:
        print(data)
        for monitor_metrics in data["metrics"]:
            metrics = "%s_%s_%s" % (data["program"], data["project"], monitor_metrics)

            RESOULT[metrics]["data"] = data[monitor_metrics]
    # print(result,244)
    """重新为Gauge赋值"""
    print(RESOULT)
    for key,value in RESOULT.items():
        value["Gauge"].labels(env=value["ENV"]).set(value["data"])
    time.sleep(args)

if __name__ == '__main__':
#     # Start up the server to expose the metrics.
    start_http_server(8000)
#     # Generate some requests.
    while True:

        get_REQUEST(RESOULT,args,cluster_env)

