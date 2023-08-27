import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,  QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QMainWindow, QDialog

class ToDoList(QMainWindow):
    def __init__(self):
        super(ToDoList,self).__init__()
        uic.loadUi("todo.ui", self)

        self.task_edit = self.findChild(QLineEdit,"lineEdit")
        self.add_button = self.findChild(QPushButton, "pushButton")
        self.table = self.findChild(QTableWidget,"tableWidget")

        self.task_edit.returnPressed.connect(self.add_task)
        self.add_button.clicked.connect(self.add_task)

        self.show()
        self.initUI()


    def initUI(self):

        self.table.setColumnWidth(0,10)
        self.table.setColumnWidth(1,  QHeaderView.Stretch)
        self.table.setColumnWidth(2, 10)
        self.table.setColumnWidth(3, 10)
        self.table.setHorizontalHeaderLabels(['done', 'Task', 'edit', 'del'])
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)


    def add_task(self):
        task = self.task_edit.text()
        if task:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            check = QCheckBox()
            check.setStyleSheet("QCheckBox  {padding-left:10px}")
            check.stateChanged.connect(self.task_completed)
            self.table.setCellWidget(rowPosition, 0, check)
            item = QTableWidgetItem(task)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(rowPosition, 1, item)
            edit_button = QPushButton()
            edit_button.setIcon(QIcon('edit.png'))
            edit_button.setStyleSheet("QPushButton { background-color: transparent }")
            edit_button.setToolTip('Edit Task')
            edit_button.clicked.connect(self.edit_row)
            self.table.setCellWidget(rowPosition, 2, edit_button)
            bin_button = QPushButton()
            bin_button.setIcon(QIcon('bin.png'))
            bin_button.setStyleSheet("QPushButton { background-color: transparent }")
            bin_button.setToolTip('Delete Task')
            bin_button.clicked.connect(self.delete_task)
            self.table.setCellWidget(rowPosition, 3, bin_button)
            self.task_edit.setText('')
        else:
            QMessageBox.warning(self, 'Error', 'Task cannot be empty.')


    def task_completed(self, state):
        check = self.sender()
        row = self.table.indexAt(check.pos()).row()
        if state == Qt.Checked:
            font = QFont()
            font.setStrikeOut(True)
            self.table.item(row,1).setFont(font)

        else:
            self.table.item(row, 1).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)


    def delete_task(self):
        button = self.sender()
        row = self.table.indexAt(button.pos()).row()

        mbox = QMessageBox.question(self, 'Message', "Do you want to delete?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            print("this task will be deleted!")
            self.table.removeRow(row)


    def edit_row(self):
        # get the selected row
        button = self.sender()
        row = self.table.indexAt(button.pos()).row()
        if row == -1:
            return

        # create the edit dialog
        dialog = EditRowDialog(self)
        name_item = self.table.item(row, 1)
        dialog.name_edit.setText(name_item.text())

        # show the dialog and get the new data
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_data()
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item)


class EditRowDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon('edit.png'))
        self.setWindowTitle('Edit')
        name_label = QLabel('Task:')
        self.name_edit = QLineEdit()
        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')

        # layout the widgets
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_edit)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # connect the signals for the buttons
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)


    def get_data(self):
        name = self.name_edit.text()
        return name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = ToDoList()
    app.exec_()

