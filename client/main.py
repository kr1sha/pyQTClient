import json
import sys
import datetime
import requests
from requests.exceptions import HTTPError

from PyQt6 import uic, QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    server_address = "http://localhost:5000"
    messanger_address = "/api/Messanger"
    message_id = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('messanger.ui', self)
        self.pushButton.clicked.connect(self.push_button_clicked)

    def push_button_clicked(self):
        self.send_message()

    def send_message(self):
        user_name = self.lineEdit.text()
        message_text = self.lineEdit_2.text()
        time_stamp = str(datetime.datetime.today())

        message = f"{{\"UserName\": \"{user_name}\", \"MessageText\": \"{message_text}\", \"TimeStamp\": \"{time_stamp}\"}}"
        print("Отправлено сообщение: " + message)

        url = self.server_address + self.messanger_address
        data = json.loads(message)
        r = requests.post(url, json=data)

    def get_message(self, message_id: int) -> (str, None):
        url = self.server_address + self.messanger_address + "/" + str(message_id)

        try:
            response = requests.get(url)
            response.raise_for_status()

        except HTTPError as error_message:
            #print(f'HTTP error occurred: {error_message}')
            return None
        except Exception as error_message:
            #print(f'nonHTTP error occurred: {error_message}')
            return None

        else:
            return response.text

    def timer_event(self):
        message = self.get_message(self.message_id)

        while message is not None:
            message = json.loads(message)
            user_name = message['UserName']
            message_text = message['MessageText']
            time_stamp = message['TimeStamp']
            full_message_text = f"{time_stamp}: <{user_name}>: {message_text}"
            print(full_message_text)

            self.listWidget.insertItem(self.message_id, full_message_text)

            self.message_id += 1
            message = self.get_message(self.message_id)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timer_event)
    timer.start(5000)

    sys.exit(app.exec())
