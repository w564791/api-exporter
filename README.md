
```
internet: True   是否为internet项目（True时不会在host后添加命名空间）
program: flannel  
project: "k8s"
projectCode: "flanneld is running"  “当返回值是json时，此值为key，当为str时，为match对象”
metrics:
 http_code: 200  “http code和其默认值”
 program_code: "flanneld is running" “http参数 其默认值”
auth: False “是否需要验证”
authData:  “验证参数”
  - hello
  - 895712
data: ""  “post数据”
method: GET
namespace: pxsj  “K8S命名空间”
header:
  Content-Type: "application/json"  “header”
url: "/healthz"    
host:     “host， list格式”
 - "10.10.5.85"
 - "10.10.6.90"
 - "10.10.4.159"
 - "10.10.4.151"
 - "10.10.4.50"
 - "10.10.7.229"
 - "10.10.7.38"
 - "10.10.6.201"
 - "10.10.4.12"
 - "10.10.5.105"
port: "10752"  “通信端口”
protocol: "http"  “通信协议”

```
