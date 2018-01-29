#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: how_bjl@live.cn
file: prometheus-test
time: 17-12-25 上午10:27
"""
from prometheus_client import start_http_server,Gauge,Summary
import sys
import time,datetime
import yaml,json,requests
import re
ConnectTimeout = requests.exceptions.ConnectTimeout
ReadTimeout = requests.exceptions.ReadTimeout
ConnectionError = requests.exceptions.ConnectionError
ScannerError=yaml.scanner.ScannerError

# registry = CollectorRegistry()
args_list = sys.argv[1:]

def print_red(arg):
    print("\033[0;31;10m%s\033[0m"%arg)
def print_green(arg):
    print("\033[0;32;10m%s\033[0m"%arg)
def print_yellow(arg):
    print("\033[0;33;10m%s\033[0m" %arg)


def get_args(args_list):
    """获取脚本参数"""
    args = 30
    cluster_env = 'swarm'
    config_file = '/tmp/config.yml'
    for Arg in args_list:
        Arg=re.split("[=]",Arg)
        # print(Arg)
        if "-i" in Arg:
            try:
                args = int(Arg[1])
            except ValueError as e:
                print(datetime.datetime.now(),e.args)
                exit(1)
            except IndexError as e:
                print(datetime.datetime.now(),e.args)
                exit(2)
        elif "-e" in Arg:
            try:
                cluster_env = Arg[1]
            except IndexError as e:
                cluster_env = 'swarm'
                print(datetime.datetime.now(),e.args)
                exit(3)
        elif "-f" in Arg:
            try:
                config_file = Arg[1]
            except IndexError as e:
                config_file = 'config.yml'
                print(datetime.datetime.now(),e.args)
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
print_green("%s: args list ----> %s"%(datetime.datetime.now(),args_list))
print_green("%s: config file ----> %s"%(datetime.datetime.now(),config_file))
print_green("%s cluster env ----> %s"%(datetime.datetime.now(),cluster_env))

def http_ok(url,result,data,resbonse,projectCode):
    """当获取resbonse成功时，为result赋值"""
    print("%s: %s get [\033[0;32;10mOK\033[0m]! %s" % (datetime.datetime.now(),url,resbonse.status_code))
    try:
        response = json.loads(resbonse.text)
    except json.decoder.JSONDecodeError:
        if resbonse.headers['Content-Type'] == 'image/png':
            response = "1"
        else:
            response = resbonse.text


    # match_code = re.match(projectCode,resbonse)
    # print(type(match_code),"------------------------>")
    for i in data['metrics']:
        if i == "http_code":
            result[i] = resbonse.status_code
        elif i == "program_code":
            if isinstance(response,dict):
                result[i] = response[projectCode]

            elif isinstance(response,str):
                if re.match(projectCode,response):
                    result[i] = 1
                else:
                    result[i] = -1
                # break
            # elif not match_code:
            #     result[i] = 1
            # elif match_code:
            #     result[i] = -1
    return result
def http_timeout(url,result,data):
    """当获取resbonse超时时，为result赋值为0"""
    print("%s: %s get [\033[0;31;10mError\033[0m]! " % (datetime.datetime.now(),url))
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
            print_red("%s: %s"%(datetime.datetime.now(),scanner_error.problem_mark))
            break
        except StopIteration as stop_err:

            # print(stop_err.value)
            break

    return data
data_list = Scan_conf(config_file)
def re_data(method,uri,result, datas,*args,**kwargs):
    try:
        resbonse = requests.request(method,**kwargs)

        http_ok(uri,result, datas,resbonse,*args)

    except ConnectTimeout:

        http_timeout(uri,result, datas)
        resbonse = None
    except   ConnectionError:
        http_timeout(uri, result, datas)
        resbonse = None
    except ReadTimeout:
        http_timeout(uri, result, datas)
        resbonse = None


    return resbonse

def get_key(data,key,type=False):
    if type:
        try:
            get_data = type(data[key])
        except:
            get_data = False
    else:
        try:
            get_data = data[key]
        except:
            get_data = False
    return get_data

def Result(data_list,cluster_env):
    """获取url的返回值"""
    get_code = []

    for data in data_list:
        for host in data['host']:

            auth = get_key(data,'authData',type=tuple)
            internet = get_key(data,'internet')

            if data:
                try:
                    """判断环境，读URL进行叠加"""
                    if cluster_env == "k8s":
                        if internet:
                            url = "%s://%s:%s%s" % (data["protocol"],
                                                    host,
                                                    data["port"],
                                                    data["url"])
                        else:
                            url = "%s://%s.%s:%s%s" % (data["protocol"],
                                                       host,
                                                       data['namespace'],
                                                       data["port"],
                                                       data["url"])
                    elif cluster_env == "swarm":
                        if internet:
                            url = "%s://%s:%s%s" % (data["protocol"],
                                                    host,
                                                    data["port"],
                                                    data["url"])
                        else:
                            url = "%s://%s:%s%s" % (data["protocol"],
                                                    host,
                                                data["port"],
                                                data["url"])
                    elif cluster_env == "local":
                        if internet:
                            url = "%s://%s:%s%s" % (data["protocol"],
                                                    host,
                                                    data["port"],
                                                    data["url"])
                        else:
                            url = "%s://192.168.31.233:%s%s" % (data["protocol"],
                                                            data["port"],
                                                            data["url"])
                    else:
                        print("""
                                -e=[swarm|k8s|local] 设置cluster环境，当前支持k8s或者swarm,local，默认swarm
                            
                              """)
                        exit(7)
                    metadata = data['data']
                    method = data['method'].lower()
                    header = data['header']
                    projectCode = data['projectCode']
                    result = {}
                    result['program'] = data['program']
                    result['env'] = cluster_env
                    result['project'] = data['project']
                    result['metrics'] = data['metrics']
                    result['hosts'] = host
                    # auth = data['auth']
                    # print(data)
                except KeyError as e:
                    print_red("Key Error, Lost config: [ \"%s\" ]"%e.args)
                    exit(5)

                re_data(method,url,result,data,
                        projectCode,url=url,
                        data=json.dumps(metadata),
                        headers=header,
                        timeout=2,
                        auth=auth
                        )



                get_code.append(result)

    return get_code


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST2 = Gauge('cluster_current_time', 'kubernetes pods  current time', ['dates'])
UP_STATUS = Gauge('upapi',"api status",['env','labels'])
RESOULT = {}
result = Result(data_list,cluster_env)

for data in result:
    """初始化RESOULT字典，Gauge无法重复赋值"""
    for monitor_metrics in data["metrics"]:
        host = re.sub("[\.-]","_",data['hosts'])
        metrics = "%s_%s_%s__%s" % (data["program"], data["project"], monitor_metrics,host)
        annotations = "program of %s, and project of %s ,metrics %s" % (data["program"], data["project"], monitor_metrics)
        ENV = cluster_env

        RESOULT[metrics] = {"resbonse_data": data[monitor_metrics],"ENV": cluster_env}


@REQUEST_TIME.time()
def get_REQUEST(RESOULT,args,cluster_env,STATUS):
    REQUEST2.labels(dates='date').set(time.time())
    """再次获取值并重新为RESOULT[metrics]["data"]赋值"""
    result = Result(data_list,cluster_env)

    for data in result:
        # print(data,"----->")
        for monitor_metrics in data["metrics"]:
            host = re.sub("[.-]","_",data['hosts'])
            metrics = "%s_%s_%s__%s" % (data["program"], data["project"], monitor_metrics,host)

            RESOULT[metrics]["metrics"] = monitor_metrics
            RESOULT[metrics]["resbonse_data"] = data[monitor_metrics]
            RESOULT[metrics]["default"] = data['metrics'][monitor_metrics]

            # RESOULT
    # print(result,244)
    """重新为Gauge赋值"""
    print(datetime.datetime.now(),RESOULT)
    for key,value in RESOULT.items():
        # print(key,value,"========>")
        # value["Gauge"].labels(env=value["ENV"]).set(value["resbonse_data"])
        # STATUS.labels(value["ENV"],key).set(value["resbonse_data"])
        print_yellow("%s: %-50s %s"%(datetime.datetime.now(),key,value))
        if value["resbonse_data"] == value["default"]:
            STATUS.labels(value["ENV"],key).set(1)
        else:
            STATUS.labels(value["ENV"], key).set(value["resbonse_data"])
        # STATUS.labels(labels=key).set(value["data"])
    time.sleep(args)

if __name__ == '__main__':

#     # Start up the server to expose the metrics.
    start_http_server(8000)
#     # Generate some requests.
    print("%s: start server at port [\033[0;32;10m8000\033[0m]"%datetime.datetime.now())
    while True:

        get_REQUEST(RESOULT,args,cluster_env,UP_STATUS)

