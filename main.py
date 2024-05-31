import os
import time

import requests
from tool.proxy_check_tool import check_no_queue
from flask import Flask, jsonify, request
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
from socks_program.socks_pool import find_process, start_or_stop_background_service
from merge.merge_yaml import update_agent, merge_yaml


app = Flask(__name__)
proxys = ['socks5://192.168.1.190:1089'
          'socks5://192.168.1.190:10808',
          'socks5://192.168.1.102:10808',
          'socks5://192.168.1.131:10808', 'socks5://192.168.1.190:10810']
format_proxy_result = {x:{'count': 0, 'IpAddress': ''} for x in proxys}
if not find_process('socks_pool_start.exe'):
    print('start pool--')
    start_or_stop_background_service(start_or_stop='start')
    time.sleep(2)
proxy_result = check_no_queue(format_proxy_result)
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
start_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


def shutdown_scheduler():
    global scheduler
    if scheduler.running:
        scheduler.shutdown()


def scheduled_task():
    global proxy_result, formatted_time
    for d in proxys:
        if proxy_result.get(d):
            pass
        else:
            proxy_result.update({d: {'count': 0, 'IpAddress': ''}})
    proxy_result = check_no_queue(proxy_result)
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def update_proxy():
    global proxy_result, current_time
    check_yaml_path_is_update = 'merge/yaml_list/0.yaml'
    mtime = os.path.getmtime(check_yaml_path_is_update)
    update_time = datetime.fromtimestamp(mtime)
    if update_time.date() == datetime.now().date():
        print('Get a new yaml file')
        update_agent()
        print('Synthesize yaml files')
        merge_yaml()
        time.sleep(3)
        print('Find the running proxy pool and close it')
        pid = find_process('socks_pool_start.exe')
        if pid:
            start_or_stop_background_service(start_or_stop='stop')
            print('Successfully closed proxy pool')
        else:
            print('Process not found, start socks proxy pool directly')
        time.sleep(3)
        print('Start the bat program')
        start_or_stop_background_service(start_or_stop='start')
        proxy_result = check_no_queue(format_proxy_result)
        current_time = datetime.now()


scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, trigger=IntervalTrigger(minutes=30))
scheduler.add_job(update_proxy, 'cron', hour=16, minute=55)
scheduler.start()
atexit.register(lambda: shutdown_scheduler())


@app.route('/')
def get_proxy_result():
    global proxy_result
    seen_values = set()
    keys_to_remove = []
    for key, value in proxy_result.items():
        if value['IpAddress'] in seen_values:
            keys_to_remove.append(key)
        else:
            seen_values.add(value['IpAddress'])
    if len(keys_to_remove) != 0:
        print(f'Number of duplicate nodes:{len(keys_to_remove)}')
    for key in keys_to_remove:
        del proxy_result[key]
    return jsonify({'proxy_pool': proxy_result, '最后一次更新时间': current_time.strftime("%Y-%m-%d %H:%M:%S"), '程序开始运行时间': current_time.strftime("%Y-%m-%d %H:%M:%S")})


@app.route('/sort')
def sorted_proxy():
    res = requests.get('http://127.0.0.1:8000').json()
    pool = res['proxy_pool']
    data_list = []
    for key, value in pool.items():
        # print(d)
        number, ip = value['count'], value['IpAddress']
        data = {key: number}
        data_list.append(data)
    sorted_data_list = sorted(data_list, key=lambda x: list(x.values())[0], reverse=True)
    # print(sorted_data_list)
    return jsonify(sorted_data_list)


@app.route('/update', methods=['GET', 'POST'])
def update_proxy():
    global proxys
    if request.method == 'GET':
        proxy = request.args.get('proxy', '')
        if proxy:
            if 'socks' or 'http' in proxy:
                if len(proxy.split(':')) == 3:
                    proxys.append(proxy)
                    return '添加成功!!!'
                else:
                    return '请添加ip或者端口!!'
            else:
                return '请指定代理协议!!(socks,http)'
        else:
            return '添加失败!!!请检查格式'
    else:
        received_data = request.json
        checked_proxy = received_data.get('proxys', [])
        for d in checked_proxy:
            if d not in proxys:
                print(d)
                proxys.append(d)
        print(proxys)
        return '已添加到代理列表,下次检测会带上'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    # threading.Thread(target=app.run, kwargs={'debug': True}).start()
