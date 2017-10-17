from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.msg()

    def msg(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "标题",
                                        "消息",
                                        QMessageBox.Yes)


def fun_s():
    import tkinter.messagebox
    tkinter.messagebox.showwarning('提示', '这是一个消息框')

if __name__ == "__main__":
    import threading
    import datetime

    now = datetime.datetime.now()
    剩下时间 = 14 * 60 * 60 + 50 * 60 - (now.hour * 60 * 60 + now.minute * 60+now.second)
    print("%d秒 后提示" % (剩下时间))
    if 剩下时间 > 0:
        timer = threading.Timer(5, fun_s)
        timer.start()
    else:
        print("已经过了 14：50了")
    input()
