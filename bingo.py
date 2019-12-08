#!/use/bin/python3

"""
Sceneだけはself外すな！
memory leak 
MovingListはオブジェクト毎回生成してリストに挿入
historyListは生成したオブジェクト持越し
待ち行列作って画面表示20個、画面外に出たものは待ち行列に並びなおす
判定している段階ではどの数字が出るのか分からないようにする
数字を60フレームごとに変えながら下に流す

・ランダムに数字を表示できるようにする
・位置調整する(イライラするから最後)

"""

import os
import sys
import time
import random
import threading
from QBingoUI import Ui_MainWindow
from PySide2.QtWidgets import * 
from PySide2.QtGui import *

# pixmap.height
FRAMESIZE = 1200
OBJECTSNUM = 10

class MovingItem():
    def __init__(self, number=0):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.number = number
    
    def setNumber(self,number):
        self.number = number

    def initXY(self,x,y):
        self.x = x
        self.y = y
    
    def initDXDY(self,dx,dy):
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    #def releaseNumber(self):
    #    if self.y > FRAMESIZE:
    #        self.y = 0
    
    def sendTeams(self):
        # sendTeams
        pass

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lock = threading.Lock()

        self.queueItemList = [i for i in range(1,76)]
        self.movingItemList = [] # 流れている数字のリスト
        self.historyItemList = []

        self.resize(1920,1280)
        self.move(0,0)
        self.scene = QGraphicsScene()

        self.counter = 0
        self.movingItemList = []
        for i in range(OBJECTSNUM):
            #self.movingItem = MovingItem()
            #self.movingItem.setNumber(int(random.random() * 75))
            #self.movingItem.initXY(250,5*i)
            #self.movingItem.initDXDY(0,5)
            self.movingItemList.append(MovingItem())
        
    def paint(self):
        self.scene.clear()
        pixmap = QPixmap("./background.png")
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QColor(255,255,255,150))
        painter.setFont(QFont('Times', 100))
        #if self.lock.locked():
        for i in range(len(self.movingItemList)):
            painter.drawText(self.movingItemList[i].x, self.movingItemList[i].y, str(self.movingItemList[i].number))
            # ヒストリリストからヒストリを表示するコードを書く
        painter.setPen(QColor(255,255,0,150))
        for i in range(len(self.historyItemList)):
            painter.drawText(self.historyItemList[i].x, self.historyItemList[i].y, str(self.historyItemList[i].number))
        painter.end()
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)

    def getBingoNumber(self):
        #print(self.historyItemList)
        while(True):
            bingo_number = int(random.random() * 74) + 1
            flag = True
            for item in self.historyItemList:
                if bingo_number == item.number:
                    flag = False
            if flag == True:
                print(bingo_number)
                break
        return bingo_number

    def run(self):
        # Initialize----------------------------------------
        self.counter = 0
        # MovingListとQueueを決める処理を入れる
        random.shuffle(self.queueItemList)
        bingo_num = self.getBingoNumber()
        for i in range(len(self.movingItemList)):
            self.movingItemList[i].setNumber(self.queueItemList.pop(0))
            self.movingItemList[i].initXY(222, 120*i)
            self.movingItemList[i].initDXDY(0,5)
        for i in range(len(self.historyItemList)):
            #print(100+50*int(i/3))
            self.historyItemList[i].initXY(1152+150*(i%5), 180+150*(int(i/5)))
            self.historyItemList[i].initDXDY(0,0)    
        # --------------------------------------------------

        while(True):
            self.counter += 1
            time.sleep(1/60)
            self.update()
            for i in range(OBJECTSNUM):
                self.movingItemList[i].move()
                #self.movingItemList[i].loopNumber()
                if self.movingItemList[i].y > FRAMESIZE:
                    self.queueItemList.append(self.movingItemList[i].number)
                    self.movingItemList[i].y = 0
                    self.movingItemList[i].setNumber(self.queueItemList.pop(0))


            if self.counter > 500:
                self.lock.release()
                #self.historyItemList.append(bingo_num)
                self.historyItemList.append(MovingItem(bingo_num))
                break
                # ここに演出入れる


    def paintEvent(self, event):
        #if self.lock.locked():
        self.paint()

    def mousePressEvent(self, event):
        if self.lock.locked():
            self.counter = 1000
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
