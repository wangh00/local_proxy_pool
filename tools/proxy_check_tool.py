import time
from queue import Queue
from sys import stdout
from tools.get_port import find_udp_ports_in_range, get_local_ip
import requests
from concurrent.futures import ThreadPoolExecutor, wait

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}


def log_console(info):
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stdout.write(f'{local_time}\t{info}\r\n')


class ThreadPool:
    def __init__(self, thread_num, queue_add_number=3):
        self.pool = ThreadPoolExecutor(max_workers=thread_num)
        self.queue = Queue(thread_num + queue_add_number)
        self.future_list = []
        for _ in range(thread_num):
            future = self.pool.submit(self._run)
            self.future_list.append(future)

    def _run(self):
        while True:
            signal, function, args, kwargs = self.queue.get()
            if signal is True:
                break
            function(*args, **kwargs)

    def _add_close_signal(self):
        for _ in range(len(self.future_list) + 5):
            self.queue.put((True, None, None, None))

    def add_task(self, function, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.queue.put((False, function, args, kwargs))

    def wait_done(self):
        self._add_close_signal()
        done, not_done=wait(self.future_list,timeout=60*10)
        print('error task:',len(not_done))


def check_task(pro_list, d):
    # print(f'{pro_list}+{d}')
    def get():
        res = requests.get('https://api.ip.sb/ip', headers=head, proxies={'https': d}, timeout=20).text
        #https://api.ip.sb/geoip
        # print(res.text)
        return res

    count = pro_list[d]['count']
    try:
        while True:
            try:
                myip = get()
                if 'api.ip.sb' in myip:
                    raise AttributeError
                else:
                    print(f'{d}:{myip}')
                    # result = f'{ip} {country1}'
                    count += 1
                    break
            except AttributeError as e_e:
                print(d, '重试', e_e)
                time.sleep(5)
        pro_list.update({d: {'count': count, 'IpAddress': myip}})
    except Exception as e:
        print(d, e)
        del pro_list[d]
    time.sleep(1)


def check(proxy_result):
    pool = ThreadPool(8)
    ports = find_udp_ports_in_range()
    my_ip = get_local_ip()
    my_ip = my_ip if my_ip else '127.0.0.1'
    for d in ports:
        proxy = f'socks5://{my_ip}:{d}'
        if proxy_result.get(proxy):
            pass
            # proxy_result[proxy][0] += 1
        else:
            proxy_result.update({proxy: {'count': 0, 'IpAddress': ''}})
    log_console(f'开始检测{len(proxy_result.keys())}个代理')
    for d in dict(proxy_result):
        pool.add_task(check_task, args=(proxy_result, d))
    pool.wait_done()
    log_console(('END:', proxy_result))
    return proxy_result
    
def check_no_queue(proxy_result):
    ports=find_udp_ports_in_range()
    my_ip = get_local_ip()
    my_ip = my_ip if my_ip else '127.0.0.1'
    for d in ports:
        proxy = f'{my_ip}:{d}'
        if proxy_result.get(proxy):
            pass
            # proxy_result[proxy][0] += 1
        else:
            proxy_result.update({proxy: {'count': 0, 'IpAddress': ''}})
    with ThreadPoolExecutor(16) as pool:
        log_console(f'开始检测{len(proxy_result.keys())}个代理')
        for d in proxy_result:
            pool.submit(check_task, proxy_result, d)
    log_console(('END:', proxy_result))
    return proxy_result

def main():
    proxys = ['socks5://192.168.1.190:1089', 'socks5://192.168.1.190:1091', 'socks5://192.168.1.190:7897',
              'socks5://192.168.1.190:10808',
              'socks5://192.168.1.102:10808',
              'socks5://192.168.1.131:10808', 'socks5://192.168.1.190:10810']
    format_proxy_result = {x: [0, ''] for x in proxys}
    proxy_result = check(format_proxy_result)
    print(proxy_result)


if __name__ == '__main__':
    main()
