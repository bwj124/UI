import json
import os
import sys
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QLabel
from last import *
from creat_task import Ui_Dialog as CT_Dialog
from all_tasks import Ui_Dialog as AT_Dialog
from all_models import Ui_Dialog as AM_Dialog
from dev_mana import Ui_Dialog as DM_Dialog
from settings import Ui_Dialog as ST_Dialog
from picture_preview import Ui_Dialog as PV_Dialog

# global info
dict = {"task": "",
        "batch": -1,
        "name": '',
        "batch_name": [],
        "model": ""}
tasks_path = 'tasks/'
data_path = 'data/'
models_path = 'models/'
input_path = data_path+'input/'
out_path = data_path + 'output/'
camera1_path = input_path + 'camera1/'
camera2_path = input_path + 'camera2/'
camera3_path = input_path + 'camera3/'
camera4_path = input_path + 'camera4/'
camera5_path = input_path + 'camera5/'
camera6_path = input_path + 'camera6/'
camera7_path = input_path + 'camera7/'
camera8_path = input_path + 'camera8/'

def save_task():
    tasks_file = open(tasks_path + 'all_tasks.json', 'r', encoding='utf-8')
    try:
        all_tasks = json.load(tasks_file)
        tasks_file.close()
        num = all_tasks.values()[-1].split('task').split('.json')
        num = int(num)
        while f'task{num + 1}.json' in all_tasks.values():
            num += 1
        all_tasks[dict["task"]] = f'task{num + 1}.json'
    except:
        all_tasks = {}
        num = 0
        all_tasks[dict["task"]] = f'task{num + 1}.json'
    tasks_file = open(tasks_path + 'all_tasks.json', 'w', encoding='utf-8')
    json.dump(all_tasks, tasks_file, ensure_ascii=False)
    tasks_file.close()
    json.dump(dict, open(tasks_path + f'task{num + 1}.json', 'w', encoding='utf-8'), ensure_ascii=False)


class MyCTDialog(CT_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyCTDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.upload_file)
        self.pushButton_2.clicked.connect(self.create_task)
        self.pushButton_3.clicked.connect(self.cancel)
        self.radioButton.clicked.connect(self.update_config)
        self.lineEdit.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

    def update_config(self):
        if self.radioButton.isChecked():
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
        else:
            self.lineEdit.setEnabled(True)
            self.pushButton.setEnabled(False)
            self.lineEdit_2.setEnabled(False)

    def upload_file(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, '上传批处理文件', '', '*.txt')
        self.lineEdit_2.setText(fileName)

    def create_task(self):
        dict['task'] = self.lineEdit_3.text()
        dict["batch"] = 1 if self.radioButton.isChecked() else 0

        dict['name'] = self.lineEdit.text()
        if self.lineEdit_2.text() and os.path.exists(self.lineEdit_2.text()):
            with open(self.lineEdit_2.text(), 'r', encoding='utf-8') as f:
                dict['batch_name'] = f.read().split('\n')
        dict['model'] = self.comboBox.itemText(self.comboBox.currentIndex())
        print(dict)
        save_task()
        self.setVisible(False)

    def cancel(self):
        self.setVisible(False)


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


class MyPVDialog(PV_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyPVDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.label.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.isKeyPress = False

    def eventFilter(self, object, event):
        print('鼠标事件：', event.type())
        # 释放鼠标左键和释放空格时关闭窗口
        # QtCore.QEvent
        if event.type() == 3:
            self.setVisible(False)
            return True
        return False

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.isKeyPress = True

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.isVisible() and self.isKeyPress:
            if a0.key() == QtCore.Qt.Key_Space:
                self.setVisible(False)
        self.isKeyPress = False

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if self.isVisible():
            if a0.angleDelta().y() > 0:
                self.resize(QtCore.QSize(self.width()+10, self.height()+10))
            else:
                self.resize(QtCore.QSize(self.width() - 10, self.height() - 10))


# 自定义可点击的Label类
class MyQLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    # signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyQLabel, self).__init__(parent)
        # self.signal.connect(self.signalCall)

    # def mousePressEvent(self, ev: QtGui.QMouseEvent):
    #     self.signal.emit()

    # def signalCall(self):
    #
    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    # def mousePressEvent(self, ev):
    #     self.clicked.emit()

    # 可在外部与槽函数连接
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(parent=None)
        self.setupUi(self)
        self.statusBar().showMessage('正在初始化...', )
        self.showMainWindow()
        self.ct_dialog = MyCTDialog()
        self.at_dialog = MyATDialog()
        self.am_dialog = MyAMDialog()
        self.dm_dialog = MyDMDialog()
        self.st_dialog = MySTDialog()
        self.preview_dialog = MyPVDialog()

        self.action_10.triggered.connect(self.showMainWindow)
        self.action_17.triggered.connect(self.showHistory)
        self.action_18.triggered.connect(self.showTasks)
        self.action_13.triggered.connect(self.showNewModel)

        self.action.triggered.connect(self.dialog_create_task)
        self.action_3.triggered.connect(self.dialog_all_tasks)
        self.action_4.triggered.connect(self.dialog_all_models)
        self.action_15.triggered.connect(self.dialog_dev_mana)
        self.action_16.triggered.connect(self.dialog_settings)

        self.action_20.triggered.connect(self.blue_theme)
        self.action_21.triggered.connect(self.black_theme)
        self.action_22.triggered.connect(self.white_theme)
        self.action_23.triggered.connect(self.purple_theme)

        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_15.clicked.connect(self.stop)
        self.statusbar.showMessage('初始化完成')

        # self.label_15 = MyQLabel(self.scrollArea)
        # self.label_15.connect_customized_slot(self.showHistory)
        # self.label_15.signal

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_statusbar)
        self.timer.start(2000)
        self.count_fault = 0
        self.count_object = 1
        # self.timer2 = QTimer()
        # self.time.time

        self.listWidget.setIconSize(QtCore.QSize(200, 253))
        self.listWidget.itemSelectionChanged.connect(self.show_bigPicture)
        self.fault_pictures = []
        self.currentImgIdx = 0
        # 创建异常图片的列表
        # self.list_widget = QtWidgets.QListWidget()
        # self.list_widget.setFlow(0)
        # self.list_widget(QTCore.QSize(150, 143))
        # self.list_widget.itemSelectionChanged.connect(self.show_bigPicture)
        # self.fault_pictures = []
        # self.currentImgIdx = 0
        # self.currentImg = None

    def showMainWindow(self):
        self.stackedWidget.setCurrentIndex(0)

    def showHistory(self):
        self.stackedWidget.setCurrentIndex(1)

    def showTasks(self):
        self.stackedWidget.setCurrentIndex(2)

    def showNewModel(self):
        self.stackedWidget.setCurrentIndex(3)

    # 显示异常图片大图
    def show_bigPicture(self):
        self.currentImgIdx = self.listWidget.currentIndex().row()
        self.listWidget.clearSelection()
        if self.currentImgIdx in range(len(self.fault_pictures)):
            currentImg = QPixmap(self.fault_pictures[self.currentImgIdx]).scaledToHeight(400)
            self.preview_dialog.label.setPixmap(currentImg)
            self.preview_dialog.label.setScaledContents(True)
            self.preview_dialog.setVisible(True)

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

    def blue_theme(self):
        self.setStyleSheet("background-color:rgb(26, 29, 37)")
        self.stackedWidget.setStyleSheet("background-color: rgb(30, 37, 48);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(125, 253, 255);\n"
                                         "border-style: solid;\n"
                                         "border-width: 2px;border-radius:5px;")
        self.page.setStyleSheet("background-color: rgb(30, 37, 48);\n")
        self.widget.setStyleSheet("background-color: rgb(30, 37, 48);border-width:0px")
        self.label_2.setStyleSheet("background-color: rgb(49, 58, 75);broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(65, 97, 136);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(49, 58, 75);\n"
                                      "border-color: rgb(125, 253, 255);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_10.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_12.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_5.setStyleSheet("background-color: rgb(49, 58, 75);")
        self.label_9.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_11.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_8.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_7.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.groupBox.setStyleSheet("background-color: rgb(49, 58, 75);\n"
                                    "border-color: rgb(125, 253, 255);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color:rgb(26, 29, 37);\n"
                                        "color: rgb(255, 255, 255);")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet("background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
                                       "255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb("
                                       "125, 253, 255);")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
            "255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(125, 253, 255);")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet("background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
                                         "255);border-radius:5px;border-style:solid;border-width:2px;border-color: "
                                         "rgb(125, 253, 255);")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color:rgb(26, 29, 37);\n"
                                        "color:rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_18.setStyleSheet("border-width:1px;")
        self.label_19.setStyleSheet("border-width:1px;")
        # self.line.setStyleSheet("background-color: rgb(105, 137, 187);")
        self.widget_4.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_24.setStyleSheet("border-width:1px;")
        self.label_25.setStyleSheet("border-width:1px;")
        # self.line_4.setStyleSheet("background-color: rgb(105, 137, 187);")
        self.widget_5.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_26.setStyleSheet("border-width:1px;")
        self.label_27.setStyleSheet("border-width:1px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    def black_theme(self):
        self.setStyleSheet("background-color:rgb(36, 36, 36)")
        self.stackedWidget.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(134, 89, 52);\n"
                                         "border-style: solid;\n"
                                         "border-width: 3px;border-radius:5px;")
        self.page.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color:rgb(59, 61, 65);")
        self.label_2.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(68, 70, 74);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(59, 61, 65);\n"
                                      "border-color: rgb(134, 89, 52);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_10.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_12.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_5.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_9.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_11.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_8.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_7.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.groupBox.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                    "border-color: rgb(134, 89, 52);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color:rgb(59, 61, 65);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color: rgb(36, 36, 36);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(59, 61, 65)")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color: rgb(36, 36, 36);color: rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(59, 61, 65);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_18.setStyleSheet("border-width:2px;")
        self.label_19.setStyleSheet("border-width:2px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_24.setStyleSheet("border-width:2px;")
        self.label_25.setStyleSheet("border-width:2px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_26.setStyleSheet("border-width:2px;")
        self.label_27.setStyleSheet("border-width:2px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    def white_theme(self):
        self.setStyleSheet("background-color:rgb(240, 240, 240)")
        self.stackedWidget.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                         "/*color: rgb(255,255,255);*/\n"
                                         "border-color: rgb(113, 120, 126);\n"
                                         "border-style: solid;\n"
                                         "border-width: 2px;border-radius:5px;")
        self.page.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(220, 220, 220);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                      "border-color: rgb(113, 120, 126);;\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_10.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_12.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_5.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_9.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_11.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_8.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_7.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.groupBox.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                    "border-color: rgb(113, 120, 126);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color:rgba(240, 240, 240,0);\n"
                                        "/*color: rgb(255, 255, 255);*/\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(230, 230, 230);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_19.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_21.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_20.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color:rgba(240, 240, 240, 0);\n"
                                        "/*color:rgb(255,255,255);*/")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_18.setStyleSheet("border-width:1px;")
        self.label_19.setStyleSheet("border-width:1px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_24.setStyleSheet("border-width:1px;")
        self.label_25.setStyleSheet("border-width:1px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_26.setStyleSheet("border-width:1px;")
        self.label_27.setStyleSheet("border-width:1px;")
        self.pushButton.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")

    def purple_theme(self):
        self.setStyleSheet("background-color:rgb(105, 105, 157)")
        self.stackedWidget.setStyleSheet("background-color: rgb(103, 139, 183);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(129, 242, 255);\n"
                                         "border-style: solid;\n"
                                         "border-width: 3px;border-radius:5px;")
        self.page.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color:rgb(94, 125, 165);")
        self.label_2.setStyleSheet("background-color: rgb(103, 140, 184);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(163, 201, 214);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(163, 201, 214);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(103, 140, 184);\n"
                                      "border-color: rgb(129, 242, 255);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_10.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_12.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_5.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_9.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_11.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_8.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_7.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.groupBox.setStyleSheet("background-color: rgb(157, 183, 220);\n"
                                    "border-color: rgb(129, 242, 255);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(157, 183, 220);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color: rgb(61, 98, 136);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(105, 105, 157)")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(163, 201, 214, 150);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet("background-color: rgb(163, 201, 214, 150);\n"
                                         "border-color: rgb(123, 180, 232);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(163, 201, 214, 150);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color: rgb(61, 98, 136);color: rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(105, 105, 157);\n"
                                                "border-color: rgb(123, 180, 232);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_18.setStyleSheet("border-width:2px;")
        self.label_19.setStyleSheet("border-width:2px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_24.setStyleSheet("border-width:2px;")
        self.label_25.setStyleSheet("border-width:2px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_26.setStyleSheet("border-width:2px;")
        self.label_27.setStyleSheet("border-width:2px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    def start(self):
        self.camera1 = self.join_path(self.all_photos(camera1_path))
        self.camera2 = self.join_path(self.all_photos(camera2_path))
        self.camera3 = self.join_path(self.all_photos(camera3_path))
        self.camera4 = self.join_path(self.all_photos(camera4_path))
        self.camera5 = self.join_path(self.all_photos(camera5_path))
        self.camera6 = self.join_path(self.all_photos(camera6_path))
        self.camera7 = self.join_path(self.all_photos(camera7_path))
        self.camera8 = self.join_path(self.all_photos(camera8_path))

        self.max_i = len(self.camera8)
        self.i = 0
        self.timer_control = QTimer()
        self.timer_control.timeout.connect(self.setPhoto)
        self.timer_control.start(1000)
        self.find_fault()
        self.new_fault = []

    def join_path(self, tur):
        root, files = tur
        full_path = []
        for file in files:
            file = root + file
            full_path.append(file)
        return full_path

    def setPhoto(self):
        if self.i == self.max_i:
            self.timer_control.stop()
            self.statusbar.showMessage('任务：' + dict['task']+' 检测完成！')
            self.i = 0
            return
        print('设置图片', self.i)
        self.label_5.setPixmap(QPixmap(self.camera1[self.i]))
        if os.path.getsize(self.camera1_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera1_outpath[self.i].split('.')[0])

        self.label_6.setPixmap(QPixmap(self.camera2[self.i]))
        if os.path.getsize(self.camera2_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera2_outpath[self.i].split('.')[0])

        self.label_7.setPixmap(QPixmap(self.camera3[self.i]))
        if os.path.getsize(self.camera3_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera3_outpath[self.i].split('.')[0])

        self.label_8.setPixmap(QPixmap(self.camera4[self.i]))
        if os.path.getsize(self.camera4_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera4_outpath[self.i].split('.')[0])

        self.label_9.setPixmap(QPixmap(self.camera5[self.i]))
        if os.path.getsize(self.camera5_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera5_outpath[self.i].split('.')[0])

        self.label_10.setPixmap(QPixmap(self.camera6[self.i]))
        if os.path.getsize(self.camera6_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera6_outpath[self.i].split('.')[0])

        self.label_11.setPixmap(QPixmap(self.camera7[self.i]))
        if os.path.getsize(self.camera7_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera7_outpath[self.i].split('.')[0])

        self.label_12.setPixmap(QPixmap(self.camera8[self.i]))
        if os.path.getsize(self.camera8_outpath[self.i].split('.')[0]+'.txt') != 0:
            self.show_fault(self.camera8_outpath[self.i].split('.')[0])

        self.i += 1

    def all_photos(self, path):
        for root, dirs, files in os.walk(path):
            print('读取', path, '成功', root, files)
            return root, files

    def stop(self):
        self.timer_control.stop()

    def find_fault(self):
        _, self.camera1_out = self.all_photos(camera1_path)
        _, self.camera2_out = self.all_photos(camera2_path)
        _, self.camera3_out = self.all_photos(camera3_path)
        _, self.camera4_out = self.all_photos(camera4_path)
        _, self.camera5_out = self.all_photos(camera5_path)
        _, self.camera6_out = self.all_photos(camera6_path)
        _, self.camera7_out = self.all_photos(camera7_path)
        _, self.camera8_out = self.all_photos(camera8_path)
        self.camera1_outpath = self.join_path((out_path, self.camera1_out))
        self.camera2_outpath = self.join_path((out_path, self.camera2_out))
        self.camera3_outpath = self.join_path((out_path, self.camera3_out))
        self.camera4_outpath = self.join_path((out_path, self.camera4_out))
        self.camera5_outpath = self.join_path((out_path, self.camera5_out))
        self.camera6_outpath = self.join_path((out_path, self.camera6_out))
        self.camera7_outpath = self.join_path((out_path, self.camera7_out))
        self.camera8_outpath = self.join_path((out_path, self.camera8_out))

    def show_fault(self, filename):
        self.fault_pictures.append(filename+'.jpg')
        item = QtWidgets.QListWidgetItem(QtGui.QIcon(filename+'.jpg'), '')
        self.listWidget.addItem(item)
        self.count_fault += 1
        if self.count_fault < 4:
            # index_fault_img = [self.label_15, self.label_16, self.label_17]
            index_fault_tasks = [self.textBrowser, self.textBrowser_2, self.textBrowser_3]
            index_fault_tasks_button = [self.pushButton_19, self.pushButton_21, self.pushButton_20]
            index_fault_warn = [self.label_18, self.label_24, self.label_26]
            index_fault_percent = [self.label_19, self.label_25, self.label_27]
        #
        #     # index_fault_img[self.count_fault-1].setPixmap(QPixmap(filename+'.jpg'))
        #
            with open(filename+'.txt', 'r', encoding='utf-8') as f:
                info_list = f.read().split()
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            print(current_time)
        #
            index_fault_tasks[self.count_fault-1].setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">铸件编号：{}</p>\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常编号：{}</p>\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常类别：{}</p>\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">检测时间：{}</p></body></html>".format(dict['name'], self.count_fault, info_list[0], current_time))
            index_fault_tasks_button[self.count_fault-1].setText('待处理')
            index_fault_warn[self.count_fault-1].setText(f'异常{self.count_fault}')
            index_fault_percent[self.count_fault-1].setText(f'{int(float(info_list[1])*10000)/100.0}%')
        # else:
        #     # my_push_button = QtWidgets.QPushButton(self.scrollArea)
        #     # my_push_button.setIcon(QtGui.QIcon(filename+'.jpg'))
        #     # my_push_button.setMinimumSize(150, 143)
        #     # my_push_button.setMaximumSize(150, 143)
        #     # my_push_button.setIconSize(QtCore.QSize(150, 143))
        #     # my_push_button.clicked.connect(self.showHistory)
        #     # self.horizontalLayout_6.addWidget(my_push_button)
        #     label_new = QLabel(self.scrollArea)
        #     label_new.setObjectName("label_new")
        #     label_new.setMinimumSize(150, 143)
        #     # label_new.setMaximumSize(150, 143)
        #     label_new.setScaledContents(True)
        #     label_new.setPixmap(QPixmap(filename+'.jpg'))
        #     self.horizontalLayout_6.addWidget(label_new)

        self.label_14.setText(f'已检测 产品{self.count_object}件 异常{self.count_fault}处')
        print('有缺陷', filename)

    def update_statusbar(self):
        if dict['batch'] == -1:
            self.statusbar.showMessage('请选择或创建一个任务以运行')
        else:
            self.statusbar.showMessage('当前任务为：' + dict['task'])

    # 点击异常图片放大效果
    def enlarge_img(self):
        self.groupBox.setVisible(False)
        # self.groupBox_2.setVisible(False)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ct_dialog.setVisible(False)
        self.at_dialog.setVisible(False)
        self.am_dialog.setVisible(False)
        self.dm_dialog.setVisible(False)
        self.st_dialog.setVisible(False)


def main():
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

