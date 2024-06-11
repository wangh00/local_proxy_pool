import os
import subprocess
import time
from sys import stdout
from traceback import print_exc

import curl_cffi
import execjs
import urllib.parse
from curl_cffi import requests as requests_cuff
import requests


def log_console(info):
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stdout.write(f'{local_time}\t{info}\r\n')


def update_agent():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    from datetime import datetime
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')
    # print(formatted_date)
    url = [
        # f'https://clashgithub.com/wp-content/uploads/rss/{formatted_date}.txt',
        #    'https://freenode.me/wp-content/uploads/2024/03/0321.yaml',
        'https://tt.vg/freeclash',
        'https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2',
        'https://proxy.v2gh.com/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub',
    ]
    for index, u in enumerate(url):
        log_console(u)
        try:
            res = requests.get(u, headers=headers)
        except TimeoutError as e:
            print(u,'请求报错,需要获取的链接可能被墙了,设置代理重试:',e)
            res = requests.get(u, headers=headers,verify=False,proxies={'http':'http://127.0.0.1:1090','https':'http://127.0.0.1:1090'})
        except Exception as e:
            print_exc()
            continue
        if res.status_code != 200:
            print(f'{u} 当前订阅地址无效返回:{res.status_code}')
            continue
        path = f'merge/yaml_list/{index + 1}.yaml'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(res.text)


def merge_yaml():
    process = subprocess.Popen(['subconverter_win64/subconverter/subconverter.exe'])
    time.sleep(1)
    folder_path = 'merge/yaml_list'
    pathlist = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        absolute_path = os.path.abspath(item_path)
        pathlist.append('\"' + absolute_path + '\"')
        print(absolute_path)
    # input('enter')
    pathlist = '|'.join(pathlist)
    encoded_filepath = urllib.parse.quote(pathlist)
    url = f'http://127.0.0.1:25500/sub?target=clash&url={encoded_filepath}&insert=false'
    print(url)
    res = requests.get(url)
    with open(r'clash_proxy\before_conversion.txt', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print('Converting to yaml file')
    time.sleep(1)
    result = subprocess.run(['node', 'clash_proxy/format_conversion.js'], capture_output=True, text=True,
                            encoding='utf-8')
    print(result.stdout)
    process.terminate()
    process.wait()


if __name__ == '__main__':
    update_agent()
    merge_yaml()
