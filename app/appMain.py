import sqlite3
from app.appConfig import RESULT_BASE_PATH, UI_PATH
from bot.botMain import stopBot, startBot
import sys
import threading

from PyQt5 import uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QMainWindow, QPushButton, QLabel, QTimeEdit, QListWidget
from PyQt5.QtWidgets import QCalendarWidget, QFileDialog, QTableWidgetItem, QMessageBox


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.con = sqlite3.connect(RESULT_BASE_PATH)
        self.cur = self.con.cursor()
        self.bot_thread = None
        
        self.upload.clicked.connect(self.selectData)
        self.restart.clicked.connect(self.botRestart)
        self.stop.clicked.connect(self.botStop)
        
        self.names = ['id', 'Имя', 'Фамилия', 'Класс', 'Процент решения', 'Оценка', 'TG id', 'Вариант', 'Начало решения', 'Время решения', 'Ответы']
        self.selectData()

    def selectData(self):
        self.res = self.cur.execute(f"""SELECT * from base""").fetchall()
        self.res.sort(key=lambda x: x[0], reverse=True)
        self.view()

    def view(self):
        # self.tableWidget.setColumnCount(11)
        # self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def botStop(self):
        stopBot()

    def botRestart(self):
        stopBot()
        if self.bot_thread is not None: self.bot_thread.join() # Ожидаем завершения потока
        self.bot_thread = threading.Thread(target=startBot)
        self.bot_thread.start()

    def closeEvent(self, event):
        if self.bot_thread is not None:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            buttonAceptar = msg.addButton('Да', QMessageBox.YesRole)
            buttonCancelar = msg.addButton('Нет', QMessageBox.RejectRole)
            msg.setDefaultButton(buttonAceptar)
            msg.setText("Сейчас запущен бот, вы хотите его остановить перед закрытием?")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            
            if msg.clickedButton() == buttonAceptar:
                stopBot()
                self.bot_thread.join()  # Ожидаем завершения потока
                self.con.close()
            elif msg.clickedButton() == buttonCancelar:
                event.accept()

def openApp():
    appConfig = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(appConfig.exec_())
    