from datetime import date

from PyQt5.QtWidgets import QWidget, QListWidgetItem, QCheckBox
from PyQt5.QtCore import Qt

from UI.py.addTakWindow import Ui_AddTaskWindow

from data import db_session
from data.tasks import Tasks
from data.categories import Categories


# Создаём объект 'Задача', наследуя QCheckBox, немного дополняя QCheckBox
class TaskCheckBox(QCheckBox):
    def __init__(self, id, category_id, second_parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.category_id = category_id
        # Переменная self.second_parent должна содержать родитель MainWindow для прямого обращения к MainWindow
        self.second_parent = second_parent
        self.stateChanged.connect(self.on_state_changed)

    # Функция завершающая задачу, которая срабатывает смене состояния QTaskCheckBox
    def on_state_changed(self, state):
        dbs = db_session.create_session()
        current_task = dbs.query(Tasks).filter(Tasks.id == self.id).one()
        if state == Qt.Checked:
            current_task.finished = True
            dbs.commit()
            # Напрямую удаляем (переносим в завершенные) задачу из списка задач из MainWindow
            self.second_parent.list_tasks.takeItem(self.second_parent.list_tasks.currentRow())

    # Функция удалении задачи самой себя
    def delete_self(self):
        # Удаляем из базы данных
        dbs = db_session.create_session()
        current_task = dbs.query(Tasks).filter(Tasks.id == self.id).one()
        dbs.delete(current_task)
        dbs.commit()
        # Напрямую удаляем задачу из списка задач из MainWindow
        self.second_parent.list_tasks.takeItem(self.second_parent.list_tasks.currentRow())

    # Функция блокировки смены состояния, нужна чтобы пользователь не смог убрать галочку с отмеченной задачи
    def on_clicked(self):
        self.blockSignals(True)
        if self.checkState() == Qt.Unchecked:
            self.setCheckState(Qt.Checked)
        self.blockSignals(False)


# Окно добавлении задачи
class AddTaskWindow(QWidget, Ui_AddTaskWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # Переменная self.parent должна содержать родитель MainWindow для прямого обращения к MainWindow
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(460, 190)
        self.setWindowTitle('Добавить задачу')
        self.btn_add_edit.clicked.connect(self.add_task)
        self.load_categories()

    # Функция добавлении задачи
    def add_task(self):
        if not self.lineEdit_task.text():
            return
        dbs = db_session.create_session()
        # Получаем id выбранного категория
        category = dbs.query(Categories).filter(Categories.name == self.comboBox_categories.currentText()).one()
        # Создаём задачу в базе
        task = Tasks()
        task.category_id = category.id
        task.task_description = self.lineEdit_task.text()
        task.date = date.today()
        dbs.add(task)
        dbs.commit()

        # Создаём задачу виджетом и добавляем список задач
        check_box = TaskCheckBox(task.id, task.category_id, self.parent, task.task_description)
        check_box.setStyleSheet("QCheckBox { color: white; }")
        item = QListWidgetItem()
        # Также идёт прямое обращение к MainWindow
        self.parent.list_tasks.insertItem(0, item)
        self.parent.list_tasks.setItemWidget(item, check_box)
        self.close()

    # Функция загрузки категорий
    def load_categories(self):
        self.comboBox_categories.clear()
        dbs = db_session.create_session()
        categories = dbs.query(Categories).all()
        for element in categories:
            self.comboBox_categories.addItem(element.name)

    # Событие, при закрытии окна добавлении задач, удаляет себя из списка открытых окон
    def closeEvent(self, event):
        del self.parent.open_windows[self.objectName()]


# Окно редактирования задач
class EditTaskWindow(QWidget, Ui_AddTaskWindow):
    def __init__(self, task, parent=None):
        super().__init__()
        self.setupUi(self)
        # Переменная self.parent должна содержать родитель MainWindow для прямого обращения к MainWindow
        self.parent = parent
        self.dbs = db_session.create_session()
        # Берём данные о выбранной задаче
        self.task_checkbox = task
        self.current_task = self.dbs.query(Tasks).filter(Tasks.id == task.id).one()
        self.category_id = self.current_task.category_id
        self.task_text = self.current_task.task_description
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(460, 190)
        self.setWindowTitle('Изменить задачу')
        self.btn_add_edit.setText('Изменить')
        self.btn_delete.setVisible(True)
        self.btn_delete.setEnabled(True)
        # Подгружаем полученные данные о выбранной задаче
        self.label_date.setText(f'Создано: {self.current_task.date}')
        self.label_date.setVisible(True)
        self.lineEdit_task.setText(self.task_text)

        self.btn_add_edit.clicked.connect(self.edit_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.load_categories()

    # Функция редактирования задач
    def edit_task(self):
        if not self.lineEdit_task.text():
            return
        # Передаём обновлённые данные выбранной задаче
        category = self.dbs.query(Categories).filter(Categories.name == self.comboBox_categories.currentText()).one()
        self.current_task.category_id = category.id
        self.current_task.task_description = self.lineEdit_task.text()
        self.dbs.add(self.current_task)
        self.dbs.commit()

        # Также передаём обновлённые данные в виджет задачи
        check_box = self.parent.list_tasks.itemWidget(self.parent.list_tasks.currentItem())
        check_box.category_id = self.current_task.category_id
        check_box.setText(self.current_task.task_description)
        self.parent.load_tasks()
        self.close()

    # Функция загрузки категории
    def load_categories(self):
        self.comboBox_categories.clear()
        categories = self.dbs.query(Categories).all()
        for element in categories:
            self.comboBox_categories.addItem(element.name)
        self.comboBox_categories.setCurrentIndex(self.category_id - 1)

    # Функция удалении задачи
    def delete_task(self):
        # Вызываем функцию удалении самой себя у задачи
        self.task_checkbox.delete_self()
        self.close()

    # Событие, при закрытии окна добавлении задач, удаляет себя из списка открытых окон
    def closeEvent(self, event):
        del self.parent.open_windows[self.objectName()]