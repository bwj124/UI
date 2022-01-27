import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from last import *
from creat_task import Ui_Dialog as CT_Dialog
from all_tasks import Ui_Dialog as AT_Dialog
from all_models import Ui_Dialog as AM_Dialog
from dev_mana import Ui_Dialog as DM_Dialog
from settings import Ui_Dialog as ST_Dialog


class MyCTDialog(CT_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyCTDialog, self).__init__(parent=None)
        self.setupUi(self)


class MyATDialog(AT_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyATDialog, self).__init__(parent=None)
        self.setupUi(self)


class MyAMDialog(AM_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyAMDialog, self).__init__(parent=None)
        self.setupUi(self)


class MyDMDialog(DM_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyDMDialog, self).__init__(parent=None)
        self.setupUi(self)


class MySTDialog(ST_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MySTDialog, self).__init__(parent=None)
        self.setupUi(self)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(parent=None)
        self.setupUi(self)
        self.showMainWindow()
        self.action_10.triggered.connect(self.showMainWindow)
        self.action_17.triggered.connect(self.showHistory)
        self.action_18.triggered.connect(self.showTasks)
        self.action_13.triggered.connect(self.showNewModel)

        self.ct_dialog = MyCTDialog()
        self.at_dialog = MyATDialog()
        self.am_dialog = MyAMDialog()
        self.dm_dialog = MyDMDialog()
        self.st_dialog = MySTDialog()

        self.ct_dialog.setVisible(False)
        self.at_dialog.setVisible(False)
        self.am_dialog.setVisible(False)
        self.dm_dialog.setVisible(False)
        self.st_dialog.setVisible(False)

        self.action.triggered.connect(self.dialog_create_task)
        self.action_3.triggered.connect(self.dialog_all_tasks)
        self.action_4.triggered.connect(self.dialog_all_models)
        self.action_15.triggered.connect(self.dialog_dev_mana)
        self.action_16.triggered.connect(self.dialog_settings)

    def showMainWindow(self):
        self.stackedWidget.setCurrentIndex(0)

    def showHistory(self):
        self.stackedWidget.setCurrentIndex(1)

    def showTasks(self):
        self.stackedWidget.setCurrentIndex(2)

    def showNewModel(self):
        self.stackedWidget.setCurrentIndex(3)

    def dialog_create_task(self):
        self.ct_dialog.setVisible(True)

    def dialog_all_tasks(self):
        self.at_dialog.setVisible(True)

    def dialog_all_models(self):
        self.am_dialog.setVisible(True)

    def dialog_dev_mana(self):
        self.dm_dialog.setVisible(True)

    def dialog_settings(self):
        self.st_dialog.setVisible(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ct_dialog.setVisible(False)
        self.at_dialog.setVisible(False)
        self.am_dialog.setVisible(False)
        self.dm_dialog.setVisible(False)
        self.st_dialog.setVisible(False)


if __name__=='__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
