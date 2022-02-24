import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from guide import Ui_Frame as guideWin
from pointcloud import Ui_Form as pointCloudWin
from demo import MyWindow
from OCR import Ui_Form as ocrWin


class MyPointCloud(pointCloudWin, QtWidgets.QDialog):
    def __init__(self):
        super(MyPointCloud, self).__init__(parent=None)
        self.setupUi(self)


class MyOCR(ocrWin, QtWidgets.QDialog):
    def __init__(self):
        super(MyOCR, self).__init__(parent=None)
        self.setupUi(self)


class MyGuide(guideWin, QtWidgets.QDialog):
    def __init__(self):
        super(MyGuide, self).__init__(parent=None)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openDection)
        self.pushButton_2.clicked.connect(self.openPointCloud)
        self.pushButton_3.clicked.connect(self.openOCR)

    def openDection(self):
        self.dection = MyWindow()
        self.dection.setVisible(True)
        self.setVisible(False)

    def openPointCloud(self):
        self.pointCloud = MyPointCloud()
        self.pointCloud.setVisible(True)
        self.setVisible(False)

    def openOCR(self):
        self.ocr = MyOCR()
        self.ocr.setVisible(True)
        self.setVisible(False)


def main_this():
    app = QApplication(sys.argv)
    myBegin = MyGuide()
    qssStyle = '''
            QPushButton {
                background-color:red
            }
        '''
    myBegin.show()
    # myBegin.setStyle()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_this()
