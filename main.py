import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.fill_table()

    def fill_table(self):
        con = self.get_connection()
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID",
            "Название",
            "Обжарка",
            "Вид",
            "Описание вкуса",
            "Цена",
            "Объём упаковки"
        ])
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setRowCount(len(data))

        for row, coffee in enumerate(data):
            for col, value in enumerate(coffee):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, col, item)

    def get_connection(self):
        con = sqlite3.connect("coffee.sqlite")
        return con


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
