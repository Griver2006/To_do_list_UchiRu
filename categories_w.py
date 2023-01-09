from PyQt5.QtWidgets import QWidget
from UI.py.addCategoryWindow import Ui_AddCategoryWindow

from data import db_session
from data.categories import Categories


# Окно добавлении категории
class AddCategoryWindow(QWidget, Ui_AddCategoryWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # Переменная self.parent должна содержать родитель MainWindow для прямого обращения к MainWindow
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(460, 190)
        self.setWindowTitle('Добавить категорию')
        self.btn_add_edit.clicked.connect(self.add_category)

    # Функция добавлении категории
    def add_category(self):
        category_name = self.lineEdit_category.text().strip()
        # Проверка, нет ли такой категории уже в списке
        if not category_name or self.parent.comboBox_categories.findText(category_name) != -1:
            return
        # Добавляем категорию в базу данных
        dbs = db_session.create_session()
        category = Categories()
        category.name = category_name
        dbs.add(category)
        dbs.commit()
        # Также добавляем категорию в список категорий
        self.parent.comboBox_categories.addItem(category.name)
        self.close()

    # Событие, при закрытии окна добавлении задач, удаляет себя из списка открытых окон
    def closeEvent(self, event):
        del self.parent.open_windows[self.objectName()]


# Окно редактировании категории
class EditCategoryWindow(QWidget, Ui_AddCategoryWindow):
    def __init__(self, category, parent=None):
        super().__init__()
        self.setupUi(self)
        # Переменная self.parent должна содержать родитель MainWindow для прямого обращения к MainWindow
        self.parent = parent
        # Берём данные о выбранной категории
        self.category = category
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(460, 190)
        self.setWindowTitle('Изменить категорию')
        self.btn_add_edit.setText('Изменить')
        self.btn_add_edit.setEnabled(True)
        self.btn_delete.setVisible(True)
        self.btn_delete.setEnabled(True)

        # Подгружаем полученные данные о выбранной категории
        self.lineEdit_category.setText(self.category['name'])

        self.btn_add_edit.clicked.connect(self.edit_category)
        self.btn_delete.clicked.connect(self.delete_category)

    # Функция редактировании категории
    def edit_category(self):
        category = self.lineEdit_category.text().strip()
        # Проверка, не пытается ли пользователь изменить категорию, на тоже самую категорию
        if self.parent.comboBox_categories.currentText() == category:
            self.close()
            return
        # Проверка, нет ли такой категории уже в списке
        if not category or self.parent.comboBox_categories.findText(category) != -1:
            return
        # Передаём обновлённые данные об изменённой категории
        dbs = db_session.create_session()
        current_category = dbs.query(Categories).filter(Categories.name == self.category['name']).one()
        current_category.name = category
        dbs.commit()

        # Также передаём обновлённые данные в виджет категории
        self.parent.comboBox_categories.setItemText(self.category['id'], current_category.name)
        self.close()

    # Функция удалении категории
    def delete_category(self):
        # Удаляем из базы данных
        dbs = db_session.create_session()
        current_category = dbs.query(Categories).filter(Categories.name == self.category['name']).one()
        dbs.delete(current_category)
        dbs.commit()

        # Напрямую удаляем категорию из списка категорий из MainWindow
        self.parent.comboBox_categories.removeItem(self.category['id'])
        self.parent.comboBox_categories.setCurrentIndex(0)
        self.close()

    # Событие, при закрытии окна добавлении задач, удаляет себя из списка открытых окон
    def closeEvent(self, event):
        del self.parent.open_windows[self.objectName()]