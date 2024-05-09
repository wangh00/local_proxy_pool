import re
import subprocess
import socket
import psutil


def get_network_connections_by_pid(pid):
    command = f"netstat -nao | findstr {pid}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    output_lines = result.stdout.split('\n')
    return output_lines


# 替换 YOUR_PID 为您要查找的进程的 PID
# your_pid = "14220"


def get_proxy_port(pid_list):
    proxy_port_list = []
    for pid in pid_list:
        connections = get_network_connections_by_pid(pid)
        for line in connections:
            # print(line)
            if 'UDP' in line and '[::]' in line:
                # print(line)
                match = re.search(r'UDP\s{1,4}(\S+):(\d+)', line)
                one = match.group(2)
                print(one)
                proxy_port_list.append(one)
    return proxy_port_list


# get_proxy_port(['20968',"7944"])

def find_udp_ports_in_range(start: int = 39000, end: int = 54000) -> list:
    udp_ports = []
    for conn in psutil.net_connections(kind='udp'):
        if start <= conn.laddr.port <= end:
            udp_ports.append(conn.laddr.port)
    return list(set(udp_ports))

def get_local_ip():
    try:
        # 创建一个 UDP 套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到一个公共的 IP 地址
        local_ip = s.getsockname()[0]  # 获取本地 IP 地址
        s.close()
        return local_ip
    except Exception as e:
        print("获取本地 IP 地址失败:", e)
        return None
