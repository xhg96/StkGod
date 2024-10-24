import sys
import os

# 使用调色板等
from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSlot
from PyQt5.QtGui import QIcon
# 导入QT,其中包含一些常量，例如颜色等
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
# 导入QWebChannel
from PyQt5.QtWebChannel import QWebChannel


# 定义一个类，其中包含一个槽函数，供JS代码调用来计算阶乘
class Factorial(QObject):
    # 将其定义为一个槽函数，参数类型为int，返回值类型为int
    @pyqtSlot(int, result=int)
    def factorial(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            return self.factorial(n - 1) * n


# 定义一个channel全局对象，用于注册一些对象提供给html页面中的JS代码调用
channel = QWebChannel()
# 定义一个对象，其中包含槽函数，注册到channel可以传递给JS代码
factorial = Factorial()


class DemoWin(QWidget):
    count = 0

    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()

    def initUI(self):
        # 将窗口设置为动图大小
        self.resize(500, 200)
        self.browser = QWebEngineView()
        url = os.getcwd() + '/test.html'
        # 加载test.html
        self.browser.load(QUrl.fromLocalFile(url))

        # 将factorial对象注册到channel中，名字为obj，JS中使用这个名字来调用函数
        channel.registerObject("obj", factorial)
        # 将channel传递给html中的JS
        self.browser.page().setWebChannel(channel)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        # 添加窗口标题
        self.setWindowTitle("JSDemo")

    def getFullName(self):
        # 传递参数value到JS函数
        value = "Hello World"
        # 调用JS中的fullName函数
        self.browser.page().runJavaScript('fullName("' + value + '");')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/icon.ico"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())