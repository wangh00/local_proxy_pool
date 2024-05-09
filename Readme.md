# 本地socks代理
## 本项目是为了爬虫而在本地启动的代理池,从网上搜集的[订阅节点合成](https://github.com/tindy2013/subconverter/releases)，每一个节点起一个代理端口

### [订阅转换工具](https://github.com/tindy2013/subconverter/releases)
### [v2rayN中的clash-mata内核](https://github.com/2dust/v2rayN)(避免进程名冲突重命名为socks_pool_start.exe)



### 运行  127.0.0.1:8000

>python.exe main.py
> 
>main.py文件中的定时任务时间
>> - 每30分钟检查一次
>> - 每天指定时间定时重新获取一次节点并重启内核
>> - tool/proxy_check_tool.py可更换检测的api

仅供学习使用。
