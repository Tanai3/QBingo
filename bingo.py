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
import requests
import json
from QBingoUI import Ui_MainWindow
from PySide2.QtWidgets import * 
from PySide2.QtGui import *

# pixmap.height
FRAMESIZE = 1280
OBJECTSNUM = 5

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
    
    def sendTeams(self, bingo_number):
        textList = ["そろそろリーチになりましたか？", ""]
        #uri = ""
        text = "当選番号は{}です\r\n".format(bingo_number)
        text += textList[int(random.random()*len(textList))]
        title = "GS_BINGO!!!!!!!"
        payload = {"text":text, "title":title}
        upload_data = json.dumps(payload)
        #response = requests.post(uri, data=upload_data)
        response = "DEBUG MODE"
        print(response)
        

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
            self.movingItemList.append(MovingItem(i))
            self.movingItemList[i].initXY(222, -400+340*i)
        
        if os.path.exists("HistoryFile"):
            self.historyFileDiscripter = open("HistoryFile", "r")
            for s in self.historyFileDiscripter.read().split('\n')[:-1]:
               self.historyItemList.append(MovingItem(int(s)))
            for i,num in enumerate(self.queueItemList):
                for j in self.historyItemList:
                    if  num == j:
                        self.queueItemList.pop(i)
        #        print(s)
        self.historyFileDiscripter = open("HistoryFile", "w")

        self.number_pixmap = QPixmap("img/75.png")
        self.frame_pixmap = QPixmap("img/12040.png")

    def paint(self):
        self.scene.clear()
        # pixmap = QPixmap("./background.png")
        pixmap = QPixmap("img/background.png")
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QColor(0,0,0,250))
        painter.setFont(QFont('Times', 300))
        
        # number_pixmap = QPixmap("./12020.png")
        
        for i in range(len(self.movingItemList)):
            painter.drawPixmap(self.movingItemList[i].x, self.movingItemList[i].y, self.number_pixmap)
            # painter.drawText(self.movingItemList[i].x, self.movingItemList[i].y, str(self.movingItemList[i].number))
            # ヒストリリストからヒストリを表示するコードを書く
        # print(frame_pixmap)
        #painter.drawPixmap(0,0, self.frame_pixmap)

        painter.setPen(QColor(100,100,0,250))
        #painter.setFont(QFont('Times', 80))
        painter.setFont(QFont('Times', 40))
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
                #print(bingo_number)
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
            self.movingItemList[i].initXY(222, -400+340*i)
            self.movingItemList[i].initDXDY(0,10)
        for i in range(len(self.historyItemList)):
            #print(100+50*int(i/3))
            self.historyItemList[i].initXY(1170+145*(i%4), 280+168*(int(i/4)))
            self.historyItemList[i].initDXDY(0,0)
        # --------------------------------------------------
        # print(sorted(self.queueItemList))
        # print(len(self.queueItemList))
        # print(len(self.movingItemList))

        speed = int(random.random() * 100)
        print("speed="+str(speed))
        while(True):
            self.counter += 1
            time.sleep(1/60)
            self.update()

            for i in range(len(self.movingItemList)):
                self.movingItemList[i].move()
                self.movingItemList[i].initDXDY(0,speed)

                if self.movingItemList[i].y > FRAMESIZE:
                    self.queueItemList.append(self.movingItemList[i].number)
                    self.movingItemList[i].y = -400
                    self.movingItemList[i].setNumber(self.queueItemList.pop(0))

            if self.counter > 600:
                # 流れる数字の中央判定部分-----------------------------------------------------------------------------
                y_list = []
                for x in self.movingItemList:
                    y_list.append(x.y)
                y_list = sorted(y_list)
                middle_number_axis = y_list[3]
                middle_number_arg = 0
                for i, item in enumerate(self.movingItemList):
                    print("i={}, y={}, num={}".format(i, item.y, item.number), end="  ")
                    if item.y == middle_number_axis:
                        middle_number_arg = i
                    print()
                middle_number = self.movingItemList[middle_number_arg].number
                print("y_list="+str(y_list))
                # print("middle_number_axis="+str(middle_number_axis))
                # ----------------------------------------------------------------------------------------------------

                if middle_number_axis != 720:
                    if speed > 3:
                        if int(random.random() * 100) < 30:
                            speed -= 1
                    if self.counter > 1120:
                        speed = 1
                    print("speed="+str(speed))
                    continue
                    
                # 事後処理----------------------------------------------------------------------------------------------------
                self.lock.release()
                self.historyItemList.append(MovingItem(self.movingItemList[middle_number_arg].number))
                self.movingItemList[2].sendTeams(self.movingItemList[middle_number_arg].number)
                #self.historyFileDiscripter.write("{}\n".format(self.movingItemList[middle_number_arg].number))
                
                for addQueue in self.movingItemList:
                    if not(addQueue.number == middle_number):
                        self.queueItemList.append(addQueue.number)

                print("movingItemListLen="+str(len(self.movingItemList)))
                print("historyItemListLen="+str(len(self.historyItemList)))
                print("queueItemListLen="+str(len(self.queueItemList)))
                print("SUM={}".format(len(self.historyItemList) + len(self.queueItemList)))
                break
                # ここに演出入れる


    def paintEvent(self, event):
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
