import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QDialog, QAbstractItemView, QMessageBox
from PyQt6.QtCore import Qt


def get_all_coffee():
    con = get_connection()
    cur = con.cursor()
    data = cur.execute("SELECT * FROM coffee").fetchall()
    con.close()
    return data


def get_connection():
    con = sqlite3.connect("coffee.sqlite")
    return con


def db_add_card(name, roast, types, taste_description, price, volume):
    con = get_connection()
    cur = con.cursor()
    request = """INSERT INTO coffee (name, roast, type, 
        taste_description, price, package_volume) 
        VALUES (?, ?, ?, ?, ?, ?)"""
    cur.execute(request, (name, roast, types,
                taste_description, price, volume))
    con.commit()
    con.close()


def db_edit_card(coffee_id, name, roast, types, taste_description, price, volume):
    con = get_connection()
    cur = con.cursor()
    request = """UPDATE coffee SET name = ?, roast = ?, type = ?, 
        taste_description = ?, price = ?, package_volume = ? WHERE id = ?"""
    cur.execute(request, (name, roast, types,
                taste_description, price, volume, coffee_id))
    con.commit()
    con.close()


def db_get_data_coffee(coffee_id):
    con = get_connection()
    cur = con.cursor()
    coffee = cur.execute("""SELECT name, roast, type, taste_description, 
    price, package_volume FROM coffee WHERE id = ?""", (coffee_id,)).fetchone()
    con.close()
    return coffee


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.fill_table()

    def fill_table(self):
        data = get_all_coffee()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            "Название",
            "Обжарка",
            "Вид",
            "Описание вкуса",
            "Цена",
            "Объём упаковки"
        ])
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.load_coffee(data)

    def load_coffee(self, data):
        self.tableWidget.setRowCount(len(data))
        for row, coffee in enumerate(data):
            for col, value in enumerate(coffee[1:]):
                item = QTableWidgetItem(str(value))
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, coffee[0])
                self.tableWidget.setItem(row, col, item)

    def add_coffee(self):
        dialog = CoffeeDialog(self)
        if dialog.exec():
            name, roast, types, taste_description, price, volume = dialog.coffee_data

            db_add_card(name, roast, types,
                        taste_description, price, volume)
            self.load_coffee(get_all_coffee())

    def edit_coffee(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Ничего не выделено!")
            return
        coffee_id = self.tableWidget.item(
            row, 0).data(Qt.ItemDataRole.UserRole)
        dialog = CoffeeDialog(self, coffee_id)
        if dialog.exec():
            name, roast, types, taste_description, price, volume = dialog.coffee_data
            db_edit_card(coffee_id, name, roast, types,
                         taste_description, price, volume)
            self.load_coffee(get_all_coffee())


class CoffeeDialog(QDialog):
    def __init__(self, parent=None, id_coffee=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.saveButton.clicked.connect(self.save_coffee)

        self.id_coffee = id_coffee
        if id_coffee is not None:
            self.saveButton.setText("Отредактировать")
            self.setWindowTitle("Редактирование кофе")
            self.get_data_coffee()

    def get_data_coffee(self):
        name, roast, types, taste_description, price, volume = db_get_data_coffee(
            self.id_coffee)
        self.nameLineEdit.setText(name)
        self.roastLineEdit.setText(roast)
        self.typeLineEdit.setText(types)
        self.taste_descriptionLineEdit.setText(taste_description)
        self.prcieLineEdit.setText(str(price))
        self.volumeLineEdit.setText(str(volume))

    def save_coffee(self):
        name = self.nameLineEdit.text().strip()
        roast = self.roastLineEdit.text().strip()
        types = self.typeLineEdit.text().strip()
        taste_description = self.taste_descriptionLineEdit.text().strip()
        try:
            price = float(self.prcieLineEdit.text().strip())
            volume = int(self.volumeLineEdit.text().strip())
        except ValueError as e:
            QMessageBox.warning(
                self, "Ошибка", str(e))
            return
        self.coffee_data = (name, roast, types,
                            taste_description, price, volume)
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
