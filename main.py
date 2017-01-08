# coding:utf-8

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTextCodec
from MainWindow import MainWindow
import sys,os

pwd = './'

def main():
    app = QApplication(sys.argv)
    textCodec = QTextCodec.codecForName('utf-8')
    QTextCodec.setCodecForCStrings(textCodec)
    QTextCodec.setCodecForLocale(textCodec)
    QTextCodec.setCodecForTr(textCodec)

    pwd = os.getcwd().decode('utf-8')
    mainWindow = MainWindow()
    #mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()