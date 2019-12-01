import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        pixmap = QPixmap("img/background.png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(1000,500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())
