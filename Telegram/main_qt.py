import sqlite3
from config import RESULT_BASE_PATH

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDockWidget, QApplication, QMainWindow, QPushButton, QLabel, QTimeEdit, QListWidget
from PyQt5.QtWidgets import QCalendarWidget, QFileDialog, QTableWidgetItem
from ui_untitled import Ui_MainWindow
from config import UI_PATH

class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.con = sqlite3.connect(RESULT_BASE_PATH)
        self.cur = self.con.cursor()
        self.upload.clicked.connect(self.select_data)
        self.names = ['id', 'Имя', 'Фамилия', 'Класс', 'Процент решения', 'Оценка', 'TG id', 'Вариант', 'Начало решения', 'Время решения']
        self.select_data()

    def select_data(self):
        self.res = self.cur.execute(f"""SELECT * from base""").fetchall()
        self.res.sort(key=lambda x: x[0], reverse=True)
        self.view()

    def view(self):
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec_())
    