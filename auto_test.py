import asyncio
import inspect
import os

import pack.pyChrome as chrome
import time
import socket

# 获取本机电脑名
pcname = socket.getfqdn(socket.gethostname())

# 设置
base_url = 'http://local.api.hzsgz.com/account/'  # 服务器地址
test_account_name = 'test'  # 帐号列表名称,服务器上有
test_id = '1'  # 测试id号,随意,测一次改一次
count = 5  # 每台电脑测试数量

# 初始化全局参数
os.system(r'C:\Windows\System32\taskkill /f /t /im chrome.exe')
test_account_data = {}
web = chrome.WebBrowser(False, is_load_img=False)
test_webs = []
command2fun = {}


def ini_data():
    for i in range(count):
        rt = web.GetJson(base_url + 'get_new?id=%s&account_name=%s' % (test_id, test_account_name))
        if rt['code'] == 200:
            test_account_data[rt['data'][0]] = rt['data'][1]
        else:
            break
    update_log('获取帐号%d/%d' % (len(test_account_data), count))
    global test_webs
    test_webs = [(chrome.WebBrowser(True, is_load_img=False), (account, test_account_data[account])) for account in
                 test_account_data]
    update_log('启动完成')


def update_log(log: str):
    rt = web.GetJson(base_url + 'update_log?id=%s&pcname=%s&log=%s' % (test_id, pcname, log))
    print(log)
    return rt['code'] == 200


def do_action():
    success_action = ''
    while True:
        rt = web.GetJson(base_url + 'get_action?id=%s' % test_id)
        if rt['code'] != 200:
            print(rt['msg'])
            time.sleep(1)
        else:
            if rt['data'] == 'end':
                [end(test_web[0], test_web[1]) for test_web in test_webs]
                update_log('结束测试')
                os.system(r'C:\Windows\System32\taskkill /f /t /im python.exe')
            elif rt['data'] == success_action:
                time.sleep(1)
            elif rt['data'] in command2fun:
                print(rt['data'])
                data = asyncio.run(__run_action(rt['data']))
                success_action = rt['data']
                update_log('执行%s命令,结果:%s' % (rt['data'], str(data)))
            else:
                print('无对应函数')
                time.sleep(1)


async def __run_action(fun: str):
    if inspect.iscoroutinefunction((command2fun[fun])):
        task = [asyncio.ensure_future(command2fun[fun](test_web[0], test_web[1])) for test_web in test_webs]
        data = [await t for t in task]
    else:
        data = [command2fun[fun](test_web[0], test_web[1]) for test_web in test_webs]
    return data


def reg_fun(func):
    command2fun[func.__name__] = func
    return func


@reg_fun
def end(web: chrome.WebBrowser, account):
    try:
        web.Chrome.close()
    except Exception as e:
        print(e)
