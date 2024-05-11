import os
import subprocess
import time
from sys import stdout
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
        f'https://clashgithub.com/wp-content/uploads/rss/{formatted_date}.txt',
        #    'https://freenode.me/wp-content/uploads/2024/03/0321.yaml',
        'https://tt.vg/freeclash',
        'https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2',
        'https://proxy.v2gh.com/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub',
        'https://cainiao164.top/api/v1/client/subscribe?token=5d7dc49e53b48b7fa46a9791f8ab2d21',
    ]
    for index, u in enumerate(url):
        log_console(u)
        try:
            res = requests_cuff.get(u, impersonate='chrome104', headers=headers)
        except Exception:
            res = requests_cuff.get(u, impersonate='chrome104', verify=False, headers=headers,
                                    proxies={'https': 'http://127.0.0.1:1090'})
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
