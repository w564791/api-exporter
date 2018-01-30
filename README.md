
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
		},
		"info": {
			"copyrights": ["PXSJ Navgation", "Jingheqiangcheng"],
			"took": 1
		},
		"paths": [{
			"ascend": 0,
			"bbox": [1215.0748, -511.51904, -1031.2197, -1046.1915],
			"descend": 0,
			"distance": 2955.904,
			"instructions": [{
				"distance": 348.972,
				"interval": [0, 2],
				"sign": 0,
				"street_name": "小南街",
				"text": "继续行驶到 小南街",
				"time": 17945
			}, {
				"distance": 1764.278,
				"interval": [2, 9],
				"sign": 3,
				"street_name": "少城路",
				"text": "右急转 到  少城路",
				"time": 90729
			}, {
				"distance": 181.044,
				"interval": [9, 10],
				"sign": -2,
				"street_name": "西沟头巷",
				"text": "左转 到  西沟头巷",
				"time": 9310
			}, {
				"distance": 256.793,
				"interval": [10, 12],
				"sign": 3,
				"street_name": "提督街",
				"text": "右急转 到  提督街",
				"time": 13205
			}, {
				"distance": 404.818,
				"interval": [12, 14],
				"sign": -2,
				"street_name": "署袜北二街",
				"text": "左转 到  署袜北二街",
				"time": 20817
			}, {
				"distance": 0,
				"interval": [14, 14],
				"sign": 4,
				"street_name": "署袜北二街",
				"text": "终点到达",
				"time": 0
			}],
			"legs": [],
			"points": {
				"coordinates": [
					[1215.0748, -511.51904],
					[1169.111, -661.15875],
					[1111.2856, -848.9587],
					[917.7929, -635.2183],
					[842.91644, -607.99164],
					[678.3364, -607.1341],
					[431.46646, -612.06494],
					[339.5389, -610.993],
					[-417.3808, -624.2848],
					[-580.4781, -625.5711],
					[-577.5127, -808.6546],
					[-655.35455, -782.7142],
					[-813.2624, -699.1046],
					[-967.46344, -947.57513],
					[-1031.2197, -1046.1915]
				],
				"type": "LineString"
			},
			"points_encoded": false,
			"snapped_waypoints": {
				"coordinates": [
					[1215.0748, -511.51904],
					[-1031.2197, -1046.1915]
				],
				"type": "LineString"
			},
			"time": 152006,
			"transfers": 0,
			"weight": 152.013408
		}]
	},
	"string": "",
	"traceId": ""
}
```
返回值为json，需要监控的为code字段，正常值为0,http code正常值为200
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
###如监控返回值非json格式，为str时配置时，例如返回值为pong
```angular2html
internet: True 
program: program  
project: test
projectCode: "pong"  配置不同的为子处为匹配项目，而非返回值为json时的key值,当返回值是图片时，此处配置无效，根据Header是否存在“image/png”自动置1。
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
