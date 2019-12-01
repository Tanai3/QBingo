# -*- coding: utf-8 -*-
import sys
import time
import random
import threading
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

"""
MovingItemを3つ生成する。
selfをつけてクラス変数とする
それぞれが履歴の出力と座標を管理するものとする

動く速度はメインループのスリープで管理する

"""

class MovingItem():
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def initLocation(self,x,y):
        self.x = x
        self.y = y

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QVBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, -1))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.resize(1900,1200)
        self.counter = 0
        mainThread = threading.Thread(target=self.run)
    
    def paintEvent(self, event):
        pixmap = QPixmap('background.png')
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(Qt.red)
        painter.setFont(QFont('Times', 30))
        painter.drawText(0,2*self.counter,"Test")
        painter.end()

        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)
        

    def run(self):
        self.counter = 0
        while(True):
            self.update()
            time.sleep(1)
            self.counter +=1
            if self.counter > 60:
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())