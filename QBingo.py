import sys
import threading
import time
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.initUI()
        thread = threading.Thread(target=self.run)
        thread.start()

    def initUI(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.resize(1000,500)
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setPen(Qt.red)
        self.setFont(QFont('Times',30))
        self.painter.drawText(250,5*self.counter,str(self.counter))
        self.painter.end()

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
