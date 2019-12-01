#!/use/bin/python3

"""
Sceneだけはself外すな！
memory leak 
"""

import sys
import time
import random
import threading
from ui_bingo import Ui_MainWindow
from PySide2.QtWidgets import * 
from PySide2.QtGui import *

FRAMESIZE = 500
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
            print("release")
            self.y = 0
            self.sendTeams()
            #self.setNumber(0)
    
    def sendTeams(self):
        # sendTeams
        pass

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setProperty("value", 50)
        self.scene = QGraphicsScene()

        self.counter = 0
        self.movingItemList = []
        for i in range(OBJECTSNUM):
            self.movingItem = MovingItem()
            self.movingItem.setNumber(int(random.random() * 75))
            self.movingItem.initXY(250,100*i)
            self.movingItem.initDXDY(0,5)
            self.movingItemList.append(self.movingItem)
        thread = threading.Thread(target=self.run)
        thread.start()
        
    def paint(self):
        self.scene.clear()
        pixmap = QPixmap("./background.png")
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QColor(255.255,0,150))
        painter.setFont(QFont('Times', 50))
        for i in range(OBJECTSNUM):
            painter.drawText(self.movingItemList[i].x, self.movingItemList[i].y, self.movingItemList[i].number)
        painter.end()
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)

    def run(self):
        while(True):
            self.counter += 1
            time.sleep(1/30)
            self.update()
            for i in range(OBJECTSNUM):
                self.movingItemList[i].move()
                self.movingItemList[i].releaseNumber()
            if self.counter > 500:
                print("break")
                break

    def paintEvent(self, event):
        self.paint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())