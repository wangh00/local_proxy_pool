import re
import time
from sys import stdout
from typing import Union, List, Dict
from tools.get_port import find_udp_ports_in_range
import requests
from lxml import etree
from redis import Redis, ConnectionPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait



head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    # "cookie":"EUID=e9716db7-1acb-4e52-aba8-8356497ba934; id_ab=AEG; mboxes=%7B%22header-sign-in%22%3A%7B%22variation%22%3A%22%231%22%2C%22enabled%22%3Afalse%7D%7D; __gads=ID=437ac4993291c005:T=1698129367:RT=1701161161:S=ALNI_MbSrZGcxWrFxfy7bM6fxFB4HHbBWA; mbox=session%23c5e7a1355e4b4eceb64f5d6ab77e067d%231701163024%7CPC%23884c7daad7a6491b80549f100ba59e64.34_0%231764405964; __cf_bm=hUVih04zP9pysHsj6CZfGvnpuWQaZxpyXoheonC0N5M-1701326317-0-Abj1de6lnkkbAiY3YG2U7d5bSkB2m0PmGkHjb3JNyupkHoTJ+194UEL+vjM+81WTG60t10oL4nN36Uk95i0LSK7Oj2rxVLfdmErW9FBx1AWf; cf_clearance=NkULiB.CvRmiCXSZfTb_j3mWrhzK.Idz66l5nOwtyaw-1701326324-0-1-dadd55.df54065b.57db82b5-0.2.1701326324; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19692%7CMCMID%7C79880518574593793854008400437633522387%7CMCAAMLH-1701931127%7C7%7CMCAAMB-1701931127%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1701333527s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1660478464%7CvVersion%7C5.5.0; s_pers=%20v8%3D1701326327457%7C1795934327457%3B%20v8_s%3DLess%2520than%25207%2520days%7C1701328127457%3B%20c19%3Dsd%253Aerror%253Awafblocked%7C1701328127460%3B%20v68%3D1701326325183%7C1701328127462%3B; s_sess=%20e41%3D1%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B"
}


def log_console(info):
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stdout.write(f'{local_time}\t{info}\r\n')


DictWithNumericString = Dict[str, List[Union[int, str]]]


def check_task(pro_list, d):
    def get1():
        res = requests.get('https://www.ipaddress.my/?lang=zh_CN', headers=head, proxies={'https': d}, timeout=20)
        # print(res.text)
        resp = etree.HTML(res.text)
        ipaddress = ''.join(re.findall(r'www.ip2location.com/demo/(.*?)" target="_blank">', res.text))
        country = ''.join(resp.xpath('//ul[@class="list-inline text-center"]//img/@alt')).replace('国旗', '').strip()
        return ipaddress, country
    count = pro_list[d][0]
    try:
        while True:
            try:
                ip, country1 = get1()
                if not ip and not country1:
                    raise AttributeError
                else:
                    print(f'{d}端口IP地址:{ip} 国家:{country1}')
                    result = f'{ip} {country1}'
                    count += 1
                    break
            except AttributeError as e_e:
                print(d, '重试', e_e)
                time.sleep(5)
        pro_list.update({d: [count, result]})
    except Exception as e:
        print(d, e)
        del pro_list[d]
    time.sleep(1)


def check(proxy_result):
    ports=find_udp_ports_in_range(start=11000,end=12000)
    for d in ports:
        proxy = f'socks5://192.168.1.190:{d}'
        if proxy_result.get(proxy):
            pass
            # proxy_result[proxy][0] += 1
        else:
            proxy_result.update({proxy: [0, '']})
    with ThreadPoolExecutor(16) as pool:
        log_console(f'开始检测{len(proxy_result.keys())}个代理')
        for d in proxy_result:
            pool.submit(check_task, proxy_result, d)
    log_console(('END:', proxy_result))
    return proxy_result

# 42042 42058 42060 42062 42063 42066 42034
# d=42201
# res = requests.get('https://www.ipaddress.my/?lang=zh_CN', headers=head,proxies={'https': f'socks5h://127.0.0.1:{d}'})
# resp=etree.HTML(res.text)
# # print(res.text)
# # print(res.status_code)  # IP地址 <a href="https://www.ip2location.com/demo
# result = ''.join(re.findall(r'www.ip2location.com/demo/(.*?)" target="_blank">', res.text))
# country=''.join(resp.xpath('//ul[@class="list-inline text-center"]//img/@alt')).replace('国旗','').strip()
# print(f'{d}端口IP地址:', result)
# print('国家:',country)
# print(res.text)
# your_string = """
# proxies:
#   - {name: 🇻🇳 越南_Telegram@kxswa, server: 103.154.63.16, port: 443, type: trojan, password: 5bae27f5-3b8e-48f3-b91f-30fc680ea78f, sni: lienquan.garena.vn, skip-cert-verify: true}
#   - {name: 🇻🇳 越南_Telegram@kxswa 2, server: vn18.4gchill.com, port: 80, type: vmess, uuid: 67d5296e-a2ee-4a9f-89e6-365da540c55d, alterId: 0, cipher: auto, tls: false, skip-cert-verify: true, network: ws, ws-opts: {path: /4gchill.com, headers: {Host: dl.ks.freefiremobile.com}}}
#   - {name: 🇻🇳 越南_Telegram@kxswa 3, server: 103.163.218.2, port: 989, type: ss, cipher: aes-256-cfb, password: f8f7aCzcPKbsF8p3}
# proxy-groups
# """
# matches = re.findall(r'server: (\S+),', your_string)
# print(matches)
# print(get_sum('before_conversion.txt'))