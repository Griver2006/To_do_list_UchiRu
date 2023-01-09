import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt

from tasks_w import AddTaskWindow, EditTaskWindow, TaskCheckBox
from categories_w import AddCategoryWindow, EditCategoryWindow

from UI.py.mainWindow import Ui_MainWindow

from data import db_session
from data.tasks import Tasks
from data.categories import Categories


# Основное окно приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ToDoList')
        self.finished_tasks = False  # Проверка переключения к списку завершённым задачам
        self.open_windows = {}
        self.init_ui()

    def init_ui(self):
        # Подключаем функции кнопкам и событиям
        self.btn_add_task.clicked.connect(self.open_add_task_window)
        self.btn_add_category.clicked.connect(self.open_add_category_window)
        self.btn_edit.clicked.connect(self.open_edit_category_window)
        self.list_tasks.itemClicked.connect(self.open_edit_task_window)
        self.buttonGroup.buttonClicked.connect(self.switch_tasks)

        self.load_categories()
        self.comboBox_categories.currentTextChanged.connect(self.load_tasks)
        self.load_tasks()

    # Функция загрузки задач
    def load_tasks(self):
        self.list_tasks.clear()
        dbs = db_session.create_session()
        tasks = dbs.query(Tasks).all()
        # Получаем id выбранного категория
        current_category_id = dbs.query(Categories).filter(Categories.name ==
                                                           self.comboBox_categories.currentText()).one().id
        if not self.finished_tasks:  # Проверка, нужно ли показывать завершённые задачи
            for t in reversed(tasks):
                if t.finished:  # Проверка, не завершена ли задачи
                    continue
                # Проверка, совпадает ли категория задачи с выбранной категорией
                if t.category_id != current_category_id and current_category_id != 1:
                    continue
                # Создаём задачу и добавляем в список задач
                task = TaskCheckBox(t.id, t.category_id, self, t.task_description)
                task.setStyleSheet("QCheckBox { color: white; }")
                item = QListWidgetItem()
                self.list_tasks.addItem(item)
                self.list_tasks.setItemWidget(item, task)
        else:
            for t in reversed(tasks):
                # Проверка завершена ли задача и проверка совпадает ли категория задачи с выбранной категорией
                if t.finished and (t.category_id == current_category_id or current_category_id == 1):
                    # Создаём задачу и добавляем в список задач
                    task = TaskCheckBox(t.id, t.category_id, self, t.task_description)
                    task.setStyleSheet('color: rgb(111,115,118); text-decoration: line-through;')
                    # Отмечаем задачу и отключаем возможность смены состояния checkbox
                    task.setChecked(True)
                    task.setAttribute(Qt.WA_TransparentForMouseEvents)
                    task.setFocusPolicy(Qt.NoFocus)
                    task.clicked.connect(task.on_clicked)
                    item = QListWidgetItem()
                    self.list_tasks.addItem(item)
                    self.list_tasks.setItemWidget(item, task)

    # Функция смены списка обычных задач на список завершённых задач
    def switch_tasks(self):
        if self.buttonGroup.checkedButton().text() == 'Завершённые':
            self.finished_tasks = True
            self.load_tasks()
        else:
            self.list_tasks.setEnabled(True)
            self.finished_tasks = False
            self.load_tasks()

    # Функция добавления категорий в comboBox
    def load_categories(self):
        self.comboBox_categories.clear()
        dbs = db_session.create_session()
        categories = dbs.query(Categories).all()
        for element in categories:
            self.comboBox_categories.addItem(element.name)

    # Функция открытия окна добавлении задачи
    def open_add_task_window(self):
        if self.buttonGroup.checkedButton().text() == 'Завершённые':
            self.radBtn_not_finished.setChecked(True)
            self.load_tasks()
        add_task_window = AddTaskWindow(parent=self)
        self.open_windows[add_task_window.objectName()] = add_task_window
        add_task_window.show()

    # Функция открытия окна редактирования задачи
    def open_edit_task_window(self):
        # Получаем выбранную задачу
        selected_item = self.list_tasks.currentItem()
        task = self.list_tasks.itemWidget(selected_item)

        # Для окна редактировании задачи необходима выбранная задача
        edit_category_window = EditTaskWindow(task, parent=self)
        self.open_windows[edit_category_window.objectName()] = edit_category_window
        edit_category_window.show()

    # Функция открытия окна добавлении категории
    def open_add_category_window(self):
        add_category_window = AddCategoryWindow(parent=self)
        self.open_windows[add_category_window.objectName()] = add_category_window
        add_category_window.show()

    # Функция открытия окна редактирования категории
    def open_edit_category_window(self):
        # Берём выбранную категорию
        category = {'id': self.comboBox_categories.currentIndex(),
                    'name': self.comboBox_categories.currentText()}
        if category['name'] == 'Все задачи':  # Категория 'Все задачи' это константа, так что её изменять нельзя
            return
        # Для окна редактирования категории необходима выбранная категория
        edit_category_window = EditCategoryWindow(category, parent=self)
        self.open_windows[edit_category_window.objectName()] = edit_category_window
        edit_category_window.show()

    # Функция закрытия всех окон при закрытии основного окна
    def closeEvent(self, event):
        windows = self.open_windows.copy()
        for w in windows.values():
            w.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_session.global_init("db/To_do_list.db")
    window = MainWindow()
    window.setFixedSize(800, 600)
    window.show()
    app.exec()