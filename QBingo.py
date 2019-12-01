import sys
import threading
import time
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.initUI()
        #thread = threading.Thread(target=self.run)
        #thread.start()

    def initUI(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.resize(1000,500)

    def paintEvent(self, event):
        pass
        #painter = QPainter(self)
        #painter.begin(self)
        #painter.setPen(Qt.red)
        #painter.setFont(QFont('Times',30))
        #painter.drawText(250,250,50)
        #painter.drawText(250,5*self.counter,str(self.counter))
        #painter.end()

    def run(self):
        self.counter = 0
        while(True):
            self.update()
            time.sleep(1/60)
            self.counter +=1
            if self.counter > 60:
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
