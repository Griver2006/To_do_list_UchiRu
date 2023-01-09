# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/ui/addTaskWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddTaskWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 190)
        Form.setStyleSheet("")
        application_icon = QtGui.QIcon()
        application_icon.addPixmap(QtGui.QPixmap(r"UI/icons/toDoList_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(application_icon)
        self.comboBox_categories = QtWidgets.QComboBox(Form)
        self.comboBox_categories.setGeometry(QtCore.QRect(130, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_categories.setFont(font)
        self.comboBox_categories.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox_categories.setStyleSheet("background-color: #666;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.comboBox_categories.setFrame(True)
        self.comboBox_categories.setObjectName("comboBox_categories")
        self.comboBox_categories.addItem("")
        self.label_date = QtWidgets.QLabel(Form)
        self.label_date.setGeometry(QtCore.QRect(10, 170, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_date.setFont(font)
        self.label_date.setStyleSheet("color: white;\n"
"background-color: transparent;")
        self.label_date.setText("")
        self.label_date.setObjectName("label_date")
        self.lineEdit_task = QtWidgets.QLineEdit(Form)
        self.lineEdit_task.setGeometry(QtCore.QRect(30, 50, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_task.setFont(font)
        self.lineEdit_task.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    padding-left: 20px;\n"
"    padding-right: 20px\n"
"}")
        self.lineEdit_task.setText("")
        self.lineEdit_task.setObjectName("lineEdit_task")
        self.btn_add_edit = QtWidgets.QPushButton(Form)
        self.btn_add_edit.setGeometry(QtCore.QRect(110, 90, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_add_edit.setFont(font)
        self.btn_add_edit.setStyleSheet("QPushButton {\n"
"    border-radius: 10px;\n"
"    background-color: #666;\n"
"    color: white;\n"
"    transition: transform 0.2s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  cursor: pointer;\n"
"  background-color: gray;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  transform: scale(0.5);\n"
"  background-color: darkgray;\n"
"}")
        self.btn_add_edit.setObjectName("btn_add_edit")
        self.label_category = QtWidgets.QLabel(Form)
        self.label_category.setGeometry(QtCore.QRect(40, 10, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_category.setFont(font)
        self.label_category.setStyleSheet("color: white;\n"
"background-color: transparent;")
        self.label_category.setObjectName("label_category")
        self.btn_delete = QtWidgets.QPushButton(Form)
        self.btn_delete.setGeometry(QtCore.QRect(410, 140, 41, 41))
        self.btn_delete.setStyleSheet("background-color: transparent;")
        self.btn_delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI/ui\\../icons/addTaskWindow/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon)
        self.btn_delete.setIconSize(QtCore.QSize(41, 41))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setVisible(False)
        self.btn_delete.setEnabled(False)

        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(-30, -10, 511, 211))
        self.frame.setStyleSheet("background-color: rgb(33, 33, 33);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.comboBox_categories.raise_()
        self.label_date.raise_()
        self.lineEdit_task.raise_()
        self.btn_add_edit.raise_()
        self.label_category.raise_()
        self.btn_delete.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox_categories.setItemText(0, _translate("Form", "Все задачи"))
        self.btn_add_edit.setText(_translate("Form", "Добавить"))
        self.label_category.setText(_translate("Form", "Категория:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_AddTaskWindow()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
