import os.path
import subprocess
import psutil
import pygetwindow as gw


def close_cmd_window_by_title(keyword):
    windows = gw.getWindowsWithTitle("cmd.exe")
    for window in windows:
        print(window.title)
        if keyword in window.title:
            print('---Closing--->', window.close())


def find_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pid = proc.info['pid']
            # print(pid)
            # startupinfo = subprocess.STARTUPINFO()
            # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # startupinfo.wShowWindow = subprocess.SW_HIDE
            # subprocess.Popen(['taskkill', '/F', '/T', '/PID', str(pid)], startupinfo=startupinfo)
            # subprocess.Popen(['taskkill', '/F', '/PID', str(pid)], creationflags=subprocess.CREATE_NO_WINDOW)
            return pid
    return False


def kill_process(pid):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(['taskkill', '/F', '/T', '/PID', str(pid)], startupinfo=startupinfo)


def start_or_stop_background_service(start_or_stop):
    # 启动.bat文件
    bat_file = 'socks_program/start.bat'
    if start_or_stop == 'start':
        file_folder = os.path.abspath(bat_file)
        print(file_folder)
        subprocess.Popen(f'start {file_folder}', shell=True)
    elif start_or_stop == 'stop':
        close_cmd_window_by_title(bat_file)
    else:
        raise AttributeError


if __name__ == '__main__':
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc)
    # start_background_service()
    # find_and_kill_process('socks_pool_start.exe')
