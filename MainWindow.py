# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtGui import QWidget,QSystemTrayIcon,QIcon,QCloseEvent,QMenu,QAction,QInputDialog,QMessageBox,\
    QFileDialog,QTableWidgetItem
from PyQt4.QtCore import QDir
from PyQt4 import QtGui
from ui_MainWindow import Ui_MainWindow
from Process import Process
import os

def QString2str(qstring):
    return str(qstring.toUtf8()).decode('utf-8')
    #return str(qstring.toUtf8())

class MainWindow(QWidget):

    def __init__(self):
        super(QWidget,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.systemTray = QSystemTrayIcon(self)
        self.systemTray.setIcon(QIcon(':/images/icon.png'))
        act_setting = QAction('设置',self)
        act_setting.triggered.connect(self.on_settings)
        act_exit = QAction('退出',self)
        act_exit.triggered.connect(self.on_exit)
        self.menu_run = QMenu('运行',self)
        menu = QMenu('菜单',self)
        menu.addMenu(self.menu_run)
        menu.addSeparator()
        menu.addAction(act_setting)
        menu.addAction(act_exit)
        self.systemTray.setContextMenu(menu)
        self.systemTray.show()
        self.showMessage('启动工具正在运行')

        self.ui.btn_add.clicked.connect(self.on_add)
        self.ui.btn_delete.clicked.connect(self.on_delete)
        self.ui.btn_apply.clicked.connect(self.on_apply)
        self.ui.btn_env_add.clicked.connect(self.on_env_add)
        self.ui.btn_env_del.clicked.connect(self.on_env_del)
        self.ui.btn_open.clicked.connect(self.on_open)
        self.ui.btn_run.clicked.connect(self.on_run)
        self.ui.le_args.textEdited.connect(self.on_edited)
        self.ui.le_desc.textEdited.connect(self.on_edited)
        self.ui.le_exe.textEdited.connect(self.on_edited)
        self.ui.cb_process.currentIndexChanged.connect(self.on_index_changed)
        self.init()

    def showMessage(self,msg):
        self.systemTray.showMessage('Launcher',msg,QSystemTrayIcon.Information,10000)

    def config_dir(self):
        confd = os.getcwd() + os.sep + 'configs'
        dir = QDir(confd)
        dir.mkpath(confd)
        return confd

    def on_settings(self):
        self.show()

    def on_exit(self):
        QtGui.qApp.quit()

    def on_edited(self):
        self.modify = True

    def on_apply(self):
        if self.currentProcess is None:
            return
        args = self.ui.le_args.text()
        exe = self.ui.le_exe.text()
        desc = self.ui.le_desc.text()
        self.currentProcess.setArgs(QString2str(args))
        self.currentProcess.setExe(QString2str(exe))
        self.currentProcess.setDesc(QString2str(desc))
        envs = {}
        for i in range(self.ui.tw_envs.rowCount()):
            key = self.ui.tw_envs.item(i,0).text()
            value = self.ui.tw_envs.item(i,1).text()
            envs[QString2str(key)] = QString2str(value)
        self.currentProcess.setEnvs(envs)
        self.processDict[self.currentProcess.getName()] = self.currentProcess
        configDir = self.config_dir()
        configFilePath = configDir + os.sep + self.currentProcess.getName() + '.json'
        with open(configFilePath, 'w+') as f:
            f.write(self.currentProcess.save())
        self.modify = False

    def on_add(self):
        ret = QInputDialog.getText(self,'请输入启动项目名称','名称')
        if not ret[1]:
            return
        name = ret[0]
        if name.isEmpty():
            return
        if self.processDict.has_key(QString2str(name)):
            QMessageBox.warning(self,'提示','该启动项已存在！')
            return
        curProcess = Process()
        curProcess.setName(QString2str(name))
        configDir = self.config_dir()
        configFilePath = configDir + os.sep + QString2str(name) + '.json'
        with open(configFilePath,'w+') as f:
            f.write(curProcess.save())
        self.add_item(curProcess)
        self.ui.cb_process.setCurrentIndex(self.ui.cb_process.count()-1)

    def on_delete(self):
        name = self.ui.cb_process.currentText()
        index = self.ui.cb_process.currentIndex()
        process = self.processDict.pop(QString2str(name))
        self.ui.cb_process.removeItem(index)
        configFilePath = self.config_dir() + os.sep + QString2str(name) + '.json'
        os.remove(configFilePath)

    def on_index_changed(self,index):
        if self.modify and QMessageBox.question(self, '提示', '启动项已修改，是否保存？',QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.on_apply()
        name = self.ui.cb_process.itemText(index)
        self.reset()
        if self.processDict.has_key(QString2str(name)):
            process = self.processDict[QString2str(name)]
            self.currentProcess = process
            self.display(process)

    def on_env_add(self):
        self.ui.tw_envs.setRowCount(self.ui.tw_envs.rowCount()+1)
        self.modify = True

    def on_env_del(self):
        index = self.ui.tw_envs.currentRow()
        self.ui.tw_envs.removeRow(index)
        self.modify = True

    def on_run(self):
        if self.modify and QMessageBox.question(self,'提示','启动项已修改，是否保存？',QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.on_apply()
        name = self.ui.cb_process.currentText()
        if self.processDict.has_key(QString2str(name)):
            process = self.processDict[QString2str(name)]
            if process.start():
                self.showMessage(u'%s启动项已执行' % process.getName())
            else:
                self.showMessage(u'%s启动项执行失败，请检查配置' % process.getName())

    def on_action_run(self):
        name = self.sender().text()
        if self.processDict.has_key(QString2str(name)):
            process = self.processDict[QString2str(name)]
            if process.start():
                self.showMessage(u'%s启动项已执行' % process.getName())
            else:
                self.showMessage(u'%s启动项执行失败，请检查配置' % process.getName())

    def on_open(self):
        filePath = QFileDialog.getOpenFileName(self,'选择程序')
        self.ui.le_exe.setText(filePath)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def add_item(self,process):
        self.processDict[process.getName()] = process
        self.ui.cb_process.addItem(process.getName())
        act = self.menu_run.addAction(process.getName())
        act.triggered.connect(self.on_action_run)

    def init(self):
        self.modify = False
        self.currentProcess = None
        self.processDict = {}
        items = os.listdir(self.config_dir())
        for item in items:
            currentPath = self.config_dir()  + os.sep + item
            if not os.path.isdir(currentPath) and os.path.exists(currentPath):
                with open(currentPath,'r') as f:
                    content = f.read()
                    process = Process()
                    if process.load(content):
                        self.add_item(process)
        self.ui.cb_process.setCurrentIndex(0)

    def reset(self):
        self.ui.le_args.setText('')
        self.ui.le_exe.setText('')
        self.ui.le_desc.setText('')
        self.ui.tw_envs.clear()
        self.ui.tw_envs.setRowCount(0)
        self.modify = False

    def display(self,process):
        self.ui.le_args.setText(process.getArgs())
        self.ui.le_exe.setText(process.getExe())
        self.ui.le_desc.setText(process.getDesc())
        envs = process.getEnvs()
        for key in envs.keys():
            row = self.ui.tw_envs.rowCount()
            self.ui.tw_envs.setRowCount(row+1)
            self.ui.tw_envs.setItem(row,0,QTableWidgetItem(key))
            self.ui.tw_envs.setItem(row, 1, QTableWidgetItem(envs[key]))