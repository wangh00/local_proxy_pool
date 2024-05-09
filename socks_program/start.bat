@echo off
chcp 65001
socks_program\socks_pool_start.exe  -f ./config_old.yaml
echo Starting command line service...
start /min