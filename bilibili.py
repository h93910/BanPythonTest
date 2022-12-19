import time
import requests
import os
import json
import subprocess


def download(url):
    print("下载:%s" % url)
    output = subprocess.check_output("you-get -i %s" % url, shell=False)
    format = str(output, encoding="utf-8").split("\r\n")[8].split(" ")[-2]
    while True:
        r = os.system('you-get %s %s' % (format, url))
        if r == 0:
            break
        time.sleep(1)
        print('============重试=============')


def vlist():
    pn = 1
    while True:
        url = "https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=0&pn=%s&keyword=&order=pubdate&order_avoided=true&jsonp=jsonp" \
              % (up_id, pn)
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        d = json.loads(resp.text)
        vl = d["data"]["list"]["vlist"]
        if len(vl) == 0:
            break
        for l in vl:
            download("https://www.bilibili.com/video/%s/" % l["bvid"])
        print('============第%s页完成=============' % pn)
        pn += 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ArgUtils')
    # parser.add_argument('-a', type=str, default=None, help="agent_id_from_platform id")
    parser.add_argument('-up', type=str, help="up主的id")
    args = parser.parse_args()

    up_id = args.up
    vlist()
    print('============完成=============')

    # "https://www.bilibili.com/video/%s/" % bvid

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(BASE_DIR)
    # while download():
    #     time.sleep(1)
    #     print('=========================')
