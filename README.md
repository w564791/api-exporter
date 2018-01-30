
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

### 举例
如过需要监控www.xxx.com/path/to/somewhere的返回值和http code，配置文件应该怎么写，返回值如下
```angular2html
{
	"code": "0",
	"response": {
		"hints": {
			"visited_nodes.average": "130.0",
			"visited_nodes.sum": "130"
...
}
```
#### 返回值为json，需要监控的为code字段，正常值为0,http code正常值为200
```angular2html
internet: True 
program: program  
project: test
projectCode: code
metrics:
 http_code: 200 
 program_code: "0"   #这里一定要注意返回值十int还是str类型
auth: False 
authData: 
  - hello
  - 895712
data: ""  
method: GET
namespace: "" #此处可以留空
header:
  Content-Type: "application/json" 
url: "/path/to/somewhere"    
host:  
 - "www.xxx.com"

port: "80" 
protocol: "http"  
```
#### 如监控返回值非json格式，为str时配置时，例如返回值为pong
```angular2html
internet: True 
program: program  
project: test
projectCode: "pong"  配置不同的为此处，而非返回值为json时的key值,当返回值是图片时，此处配置无效，根据Header是否存在“image/png”自动置1。
metrics:
 http_code: 200 
 program_code: "pong"   
auth: False 
authData: 
  - hello
  - 895712
data: ""  
method: GET
namespace: "" #此处可以留空
header:
  Content-Type: "application/json" 
url: "/path/to/somewhere"    
host:  
 - "www.xxx.com"

port: "80" 
protocol: "http"  
```
