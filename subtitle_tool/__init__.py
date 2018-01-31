if __name__ == '__main__':
    import os
    import time

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(BASE_DIR)
    requirements = list()
    result = os.popen('pip freeze').read()
    print('已安装的列表:\n%s' % result)
    install = False
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
        for s in requirements:
            if result in s:
                print('%s 已安装' % s)
            else:
                print('%s 未安装' % s)
                install = True
        print()
    if install:
        os.system('pip install -r requirements.txt')
        time.sleep(5)
        os.system('python first.py')
