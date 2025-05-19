import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLineEdit, QMessageBox
)
import os

os.environ["QT_OPENGL"] = "software"

SERVER_URL = "http://127.0.0.1:5000"

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 + Flask + PostgreSQL")
        self.setGeometry(100, 100, 300, 450)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.load_users_button = QPushButton("Загрузить пользователей")
        self.name_input = QLineEdit()
        self.add_user_button = QPushButton("Добавить пользователя")
        self.edit_user_button = QPushButton("Изменить имя")
        self.delete_user_button = QPushButton("Удалить пользователя")

        layout.addWidget(self.list_widget)
        layout.addWidget(self.load_users_button)
        layout.addWidget(self.name_input)
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.edit_user_button)
        layout.addWidget(self.delete_user_button)

        self.setLayout(layout)

        self.load_users_button.clicked.connect(self.load_users)
        self.add_user_button.clicked.connect(self.add_user)
        self.edit_user_button.clicked.connect(self.edit_user)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.list_widget.itemClicked.connect(self.fill_input_from_selection)

    def load_users(self):
        try:
            response = requests.get(f"{SERVER_URL}/users")
            if response.status_code == 200:
                self.list_widget.clear()
                users = response.json()
                for user in users:
                    self.list_widget.addItem(f"{user['id']}: {user['name']}")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить пользователей")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу")

    def add_user(self):
        name = self.name_input.text().strip()
        if name:
            try:
                response = requests.post(f"{SERVER_URL}/users", json={"name": name})
                if response.status_code == 201:
                    QMessageBox.information(self, "Успех", "Пользователь добавлен!")
                    self.name_input.clear()
                    self.load_users()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось добавить пользователя")
            except requests.exceptions.RequestException:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу")

    def get_selected_user_id(self):
        selected = self.list_widget.currentItem()
        if selected:
            return int(selected.text().split(":")[0])
        return None

    def fill_input_from_selection(self):
        selected = self.list_widget.currentItem()
        if selected:
            name = selected.text().split(": ", 1)[1]
            self.name_input.setText(name)

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if user_id is not None:
            confirm = QMessageBox.question(
                self, "Подтверждение",
                f"Удалить пользователя с ID {user_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                try:
                    response = requests.delete(f"{SERVER_URL}/users/{user_id}")
                    if response.status_code == 200:
                        QMessageBox.information(self, "Успех", "Пользователь удалён!")
                        self.load_users()
                    else:
                        QMessageBox.critical(self, "Ошибка", "Не удалось удалить пользователя")
                except requests.exceptions.RequestException:
                    QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу")

    def edit_user(self):
        user_id = self.get_selected_user_id()
        new_name = self.name_input.text().strip()
        if user_id is not None and new_name:
            try:
                response = requests.put(f"{SERVER_URL}/users/{user_id}", json={"name": new_name})
                if response.status_code == 200:
                    QMessageBox.information(self, "Успех", "Имя пользователя обновлено!")
                    self.name_input.clear()
                    self.load_users()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить имя")
            except requests.exceptions.RequestException:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec())