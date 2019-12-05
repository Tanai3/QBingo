#!/use/bin/python3

"""
Sceneだけはself外すな！
memory leak 
"""

import os
import sys
import time
import random
import threading
#from ui_bingo import Ui_MainWindow
from QBingoUI import Ui_MainWindow
from PySide2.QtWidgets import * 
from PySide2.QtGui import *

# pixmap.height
FRAMESIZE = 1200
OBJECTSNUM = 5

class MovingItem():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 1
        self.number = 0
    
    def setNumber(self,number):
        self.number = str(number)

    def initXY(self,x,y):
        self.x = x
        self.y = y
    
    def initDXDY(self,dx,dy):
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def releaseNumber(self):
        if self.y > FRAMESIZE:
            self.y = 0
            self.sendTeams()
    
    def sendTeams(self):
        # sendTeams
        pass

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lock = threading.Lock()
        self.resize(1900,1200)
        self.move(0,0)
        self.scene = QGraphicsScene()

        self.counter = 0
        self.movingItemList = []
        for i in range(OBJECTSNUM):
            self.movingItem = MovingItem()
            self.movingItem.setNumber(int(random.random() * 75))
            self.movingItem.initXY(250,100*i)
            self.movingItem.initDXDY(0,5)
            self.movingItemList.append(self.movingItem)
        
    def paint(self):
        self.scene.clear()
        pixmap = QPixmap("./background.png")
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QColor(255.255,0,150))
        painter.setFont(QFont('Times', 50))
        if self.lock.locked():
            for i in range(OBJECTSNUM):
                painter.drawText(self.movingItemList[i].x, self.movingItemList[i].y, self.movingItemList[i].number)
                # ヒストリリストからヒストリを表示するコードを書く
        painter.end()
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)

    def run(self):
        self.counter = 0
        while(True):
            self.counter += 1
            time.sleep(1/30)
            self.update()
            for i in range(OBJECTSNUM):
                self.movingItemList[i].move()
                self.movingItemList[i].releaseNumber()
            if self.counter > 500:
                print("bingo stop")
                self.lock.release()
                break
                # ここに演出とヒストリリストへ数値登録を入れる


    def paintEvent(self, event):
        self.paint()

    def mousePressEvent(self, event):
        print("clicked")
        if self.lock.locked():
            # スレッド停止用の命令を入れる
            return
        thread = threading.Thread(target=self.run)
        thread.start()
        self.lock.acquire()
        

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.CustomizeWindowHint)
    window.show()
    sys.exit(app.exec_())