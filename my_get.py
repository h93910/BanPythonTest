import time
import os


def download():
    url = ''
    with open('download_list.txt', 'r') as my_list:
        url = my_list.readline()
    if url != '':
        # os.system('you-get --ff %s' % url)
        for i in range(3):
            print('吃' * (i+1))
            time.sleep(1)
        with open('download_list.txt', 'r+') as my_list:
            d = my_list.read().splitlines()
            for s in d:
                del d[0]
                print('下载完成:%s 已经删除' % s)
                output = ''
                for s2 in d:
                    output += (s2 + '\n')
                output = output[0:-1]
                my_list.truncate(0)
                my_list.seek(0)
                my_list.write(output)
                return True
    return False


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(BASE_DIR)
    while download():
        time.sleep(1)
        print('=========================')
