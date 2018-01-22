program: 项目名称

project: 工程名

projectCode: 从resbonse中需要获取的字段（resbonse需要为json格式）

env: swarm 环境

data: ""   post时的data，可以留空

method: GET   方法

metrics:   监控项目，除http_code以为，其他都是从resbonse中获取

 - http_code

 - program_code

header:  头信息

  Content-Type: "application/json"

  Accept: "application/json"

url: "/v1/sms/template.get"  一下4列会在code中格式化

host: "sms-service"

port: "8301"

protocol: "http"