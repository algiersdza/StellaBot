import os
from notifypy import Notify
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import datetime
import csv
import pandas as pd
from requests_html import HTMLSession

StyleSheet = """
QProgressBar {
                background-color: grey;
                color: black;
                border-style: solid;
                border-radius: 19px;
                text-align: center;
}

QProgressBar::chunk {
    background-color: rgb(200, 255, 255);
}

QLabel {
    font-family: Shanti;
    font-size: 12px;
    color: #FFF;                               
}

QLineEdit {
    border: 2px solid rgb(37, 39, 48);
    border-radius: 10px;
    color: #FFF;
    padding-left: 3px;
    background-color: rgb(34, 36, 44);
}

QCheckBox {
    color: #FFF
}

QPushButton{
        border: 2px solid rgb(37, 39, 48);
        border-radius: 10px;
        font-size: 12px;
        color: #FFF;
        
               
}
QPushButton:hover{
        background: '#BC006C';
}

QTextEdit{
        border: 2px solid rgb(37, 39, 48);
        border-radius: 10px;
        color: #FFF;
        font-family: Shanti;
        font-size: 11px;
        padding-left: 3px;
        background-color: rgb(34, 36, 44);
}

QComboBox{
        border: 2px solid rgb(37, 39, 48);
        font-size: 12px;
        color: #FFF;
        cursor: pointer;
}

QComboBox:hover{
        background: '#BC006C';
}

QListView{
        display: none;
        position: absolute;
        background: '#BC006C';
        color: #FFF;
        min-width: 10px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}

"""

#global variables
WINDOW_SIZE = 800, 800
VERSION_NUMBER_STR = ("Version: " + str(1))
nnnn = 0 # background colour int for signals, 0 is eggplant default colour

item1_is_running = False
item2_is_running = False
item3_is_running = False
item4_is_running = False
item5_is_running = False

save_path = 'C:\StellaBotSettings'
path_of_user_prefs = os.path.join(save_path, "user_settings.txt")
path_of_report_csv = os.path.join(save_path, r"Reports\report.csv")

f = HTMLSession()   # first item instance
s = HTMLSession()   # second item instance
t = HTMLSession()   # third item instance
ff = HTMLSession()  # fourth item instance
fff = HTMLSession() # fifth item instance

first_item_url = ""
second_item_url = ""
third_item_url = ""
fourth_item_url = ""
fifth_item_url = ""


# create files on start up if not exist already
if os.path.exists(save_path):
    print("directory exists, not first time launch")
    if os.path.exists(path_of_user_prefs):
        print("user_settings.txt exists as well in the directory")
    else:
        print("user_settings.txt does not exist")
        with open(path_of_user_prefs, 'w') as wf:   # create the file and write loop
                create_file = wf.writelines(["email=example222@email.com", "\ncsv_location=C:\\StellaBotOutputCsv\\Reports"])
                print("created file")
else:
    print(str(save_path)+" does not exist, first time launch")
    os.mkdir(os.path.dirname(path_of_user_prefs))  # create the directory and file
    with open(path_of_user_prefs, 'w') as wf:      # write loop
        create_dir = wf.writelines(["email=example222@email.com", "\ncsv_location=C:\\StellaBotOutputCsv\\Reports"])
    print("created file")

# 5 worker subclasses of QObject to be added to Qthread class, to work concurrently without hanging the GUI
class WorkerOne(QObject):
    global item1_is_running, first_item_url

    # the signal objects below are used to display the status, indicate a 200 code response
    # and send an alert if item is in stock

    # create a signal and emit it, 3 arguments strings for updating the items status
    parsed_signal = pyqtSignal(str, str, str)
    # create a signal and emit it, 2 arugments ints for
    # indicating track is happening or code 404 (not found, 403 (forbidden)
    tracking_or_nah = pyqtSignal(int, int)
    # create a signal and emit it, 3 arguments, if item is found
    item_is_found = pyqtSignal(str, int, str)

    # run worker 1
    def run(self):
            try:
                r = f.get(first_item_url)
                while item1_is_running:
                    self.tracking_or_nah.emit(1, 1)  # 1 for item 1,  1 = ON
                    r = f.get(first_item_url)
                    title = str(r.html.find('title', first=True).text)
                    price = str(r.html.find('p.price_color', first=True).text)
                    availability = str(r.html.find('p.instock.availability', first=True).text)
                    self.parsed_signal.emit(title, price, availability)
                    if "In stock" in availability:
                        self.item_is_found.emit(title, 1, availability)
                        break
                    time.sleep(60)
                self.tracking_or_nah.emit(1, 0)
            except:
                print("Cant GET response from first link")
                self.tracking_or_nah.emit(1, 0)
                #first_item_url = ""

class WorkerTwo(QObject):
    global item2_is_running, second_item_url
    parsed_signal2 = pyqtSignal(str, str, str)
    tracking_or_nah2 = pyqtSignal(int, int)
    item_is_found2 = pyqtSignal(str, int, str)
    # run worker 2
    def run(self):
        try:
            r = s.get(second_item_url)
            while item2_is_running:
                r = s.get(second_item_url)
                self.tracking_or_nah2.emit(2, 1)    # 2 for item 1,  1 = ON
                title = str(r.html.find('title', first=True).text)
                price = str(r.html.find('p.price_color', first=True).text)
                availability = str(r.html.find('p.instock.availability', first=True).text)
                self.parsed_signal2.emit(title, price, availability)
                if "In stock" in availability:
                    self.item_is_found2.emit(title, 2, availability)
                    break
                time.sleep(60)
            self.tracking_or_nah2.emit(2, 0)
        except:
            print("Cant GET response from second link")
            self.tracking_or_nah2.emit(2, 0)

class WorkerThree(QObject):
    global item3_is_running, third_item_url
    parsed_signal3 = pyqtSignal(str, str, str)
    tracking_or_nah3 = pyqtSignal(int, int)
    item_is_found3 = pyqtSignal(str, int, str)
    # run worker 3
    def run(self):
        try:
            r = t.get(third_item_url)
            while item3_is_running:
                r = t.get(third_item_url)
                self.tracking_or_nah3.emit(3, 1)
                title = str(r.html.find('title', first=True).text)
                price = str(r.html.find('p.price_color', first=True).text)
                availability = str(r.html.find('p.instock.availability', first=True).text)
                self.parsed_signal3.emit(title, price, availability)
                if "In stock" in availability:
                    self.item_is_found3.emit(title, 3, availability)
                    break
                time.sleep(60)
            self.tracking_or_nah3.emit(3, 0)
        except:
            print("Cant GET response from Third link")
            self.tracking_or_nah3.emit(3, 0)

class WorkerFour(QObject):
    global item4_is_running, fourth_item_url
    parsed_signal4 = pyqtSignal(str, str, str)
    tracking_or_nah4 = pyqtSignal(int, int)
    item_is_found4 = pyqtSignal(str, int, str)
    # run worker 4
    def run(self):
        try:
            r = ff.get(fourth_item_url)
            while item4_is_running:
                r = ff.get(fourth_item_url)
                self.tracking_or_nah4.emit(4, 1)
                title = str(r.html.find('title', first=True).text)
                price = str(r.html.find('p.price_color', first=True).text)
                availability = str(r.html.find('p.instock.availability', first=True).text)
                self.parsed_signal4.emit(title, price, availability)
                if "In stock" in availability:
                    self.item_is_found4.emit(title, 4, availability)
                    break
                time.sleep(60)
            self.tracking_or_nah4.emit(4, 0)
        except:
            print("Cant GET response from Fourth link")
            self.tracking_or_nah4.emit(4, 0)

class WorkerFive(QObject):
    global item5_is_running, fifth_item_url
    parsed_signal5 = pyqtSignal(str, str, str)
    tracking_or_nah5 = pyqtSignal(int, int)
    item_is_found5 = pyqtSignal(str, int, str)
    # run worker 5
    def run(self):
        try:
            r = fff.get(fifth_item_url)
            while item5_is_running:
                r = fff.get(fifth_item_url)
                self.tracking_or_nah5.emit(5, 1)
                title = str(r.html.find('title', first=True).text)
                price = str(r.html.find('p.price_color', first=True).text)
                availability = str(r.html.find('p.instock.availability', first=True).text)
                self.parsed_signal5.emit(title, price, availability)
                if "In stock" in availability:
                    self.item_is_found5.emit(title, 5, availability)
                    break
                time.sleep(60)
            self.tracking_or_nah5.emit(5, 0)
        except:
            print("Cant GET response from fifth link")
            self.tracking_or_nah5.emit(5, 0)

# Help & tutorial of the application, will add more items to the class when getting close to version 1.0
class HelpWindow(QDialog):
    def __init__(self):
        super(HelpWindow, self).__init__()
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon('Images/info.ico'))
        self.setStyleSheet("background: #161219;")
        width = 600
        height = 600
        self.setFixedSize(width, height)

        # load picture asset
        self.pic_label = QLabel(self)
        self.pixmap = QPixmap('Images/help-1.png')
        self.pic_label.setPixmap(self.pixmap)
        self.pic_label.move(0, 0)

        # next page button
        self.nextpage = QPushButton(self)
        self.nextpage.setText("Next Page")
        self.nextpage.setStyleSheet(StyleSheet)
        self.nextpage.move(535, 575)
        self.nextpage.clicked.connect(self.next_page)

        self.center()
        self.show()

    # to display next page of help
    def next_page(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# user preferences class
class UserPreferences(QDialog):
    send_signal = pyqtSignal(int)
    def __init__(self):
        super(UserPreferences, self).__init__()
        self.setWindowIcon(QIcon("Images/StellaBot-Icon.ico"))
        self.setWindowTitle("Preferences")
        self.setFixedSize(300, 300)
        self.setStyleSheet(str(self.set_style_sheet(nnnn)))



        combolist = ["Eggplant", "Iris", "Santa Grey"]
        self.background_combo_box = QComboBox(self)
        self.background_combo_box.setStyleSheet(StyleSheet)
        self.background_combo_box.addItems(combolist)
        self.background_combo_box.setGeometry(100, 30, 95, 40)
        self.background_combo_box.currentIndexChanged.connect(self.selectionchange)

        self.choose_label = QLabel("Background Color", self)
        self.choose_label.setStyleSheet(StyleSheet)
        self.choose_label.move(100, 10)

        self.email_label = QLabel("Email Address", self)
        self.email_label.setStyleSheet(StyleSheet)
        self.email_label.move(110, 100)

        self.email_edit_line = QLineEdit(self)
        self.email_edit_line.resize(250, 30)
        self.email_edit_line.move(25, 120)
        self.email_edit_line.setStyleSheet(StyleSheet)
        reg_ex = QRegExp("[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}")
        input_validator = QRegExpValidator(reg_ex, self.email_edit_line)
        self.email_edit_line.setValidator(input_validator)

        self.save_csv_label = QLabel("CSV File Location", self)
        self.save_csv_label.setStyleSheet(StyleSheet)
        self.save_csv_label.move(100, 190)

        self.save_csv_edit_line = QLineEdit(self)
        self.save_csv_edit_line.resize(250, 30)
        self.save_csv_edit_line.move(25, 210)
        self.save_csv_edit_line.setStyleSheet(StyleSheet)

        self.save_preferences_button = QPushButton(self)
        self.save_preferences_button.setText("Save")
        self.save_preferences_button.setStyleSheet(
            '''
                QPushButton{
                    border: 2px solid rgb(37, 39, 48);
                    border-radius: 10px;
                    font-size: 12px;
                    color: #FFF;
                }
                QPushButton:hover{
                    background: '#BC006C';
                }
            ''')
        self.save_preferences_button.move(260, 276)
        self.save_preferences_button.clicked.connect(self.save_user_prefs)
        self.current_combo_index(nnnn)
        self.get_users_settings()
        self.show()

    # load user settings back as placeholders
    def get_users_settings(self):
        with open(path_of_user_prefs, 'r') as rf:
            rf_email_of_user = rf.readline()
            rf_loc = rf.readline()
        self.email_edit_line.setPlaceholderText(str(rf_email_of_user.split("=")[1]))
        self.save_csv_edit_line.setPlaceholderText(str(rf_loc.split("=")[1]))

    # check if used did indeed change the colour, display the combo box item on next open
    def current_combo_index(self, i):
        self.background_combo_box.setCurrentIndex(i)

    # check if user changed background colour
    def selectionchange(self, i):
        n = i
        self.current_combo_index(n)
        self.send_signal.emit(i)
        self.setStyleSheet(str(self.set_style_sheet(n)))

    # check if
    def save_user_prefs(self):
        with open(path_of_user_prefs, 'r') as read:
            lines = read.readlines()

        if self.email_edit_line.text():
            newemail = str(self.email_edit_line.text())  # get the new email
            lines[0] = f"email={newemail}\n"
            with open(path_of_user_prefs, 'w') as write_email:  #   do write operation
                write_email.writelines(lines)

        if self.save_csv_edit_line.text():
            new_csv_loc = str(self.save_csv_edit_line.text())
            lines[1] = f"csv_location={new_csv_loc}"
            with open(path_of_user_prefs, 'w') as write_email:  #   do write operation
                write_email.writelines(lines)

        print("Saved any changes!")
        self.close()

    def set_style_sheet(self, n):
        global nnnn
        if n == 0:
            nnnn = n
            return "background: #161219;"
        elif n == 1:
            nnnn = n
            return "background: #571B7E;"
        else:
            nnnn = n
            return "background: #9FA0B1;"

# splash/loading screen for the application
class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.pxmap = QPixmap('Images/SplashScreen.png')
        self.setPixmap(self.pxmap)
        self.resize(500, 210)
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(0, 200, 500, 11)
        self.progressBar.setStyleSheet(StyleSheet)

        self.center()
        self.setWindowFlag(Qt.FramelessWindowHint)

    # progress bar for splash
    def progress(self):
        for i in range(100):
            time.sleep(0.02)
            self.progressBar.setValue(i)

    # function to center the window to the middle of the user's screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# main window of the application
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.app_ui()

    # function that holds all the GUI assets (widgets and graphic things)
    def app_ui(self):
        # main window assets
        self.setFixedSize(*WINDOW_SIZE)
        self.setWindowTitle("StellaBot")
        self.setWindowIcon(QIcon("Images/StellaBot-Icon.ico"))
        self.setStyleSheet("background: #161219;")

        # first item options
        self.first_item_label = QLabel("First URL:", self)
        self.first_item_label.setStyleSheet(StyleSheet)
        self.first_item_label.move(140, 45)

        self.first_item_input = QLineEdit(self)
        self.first_item_input.resize(250, 30)
        self.first_item_input.move(50, 75)
        self.first_item_input.setStyleSheet(StyleSheet)
        self.first_item_input.setPlaceholderText("Enter first URL item")

        self.first_item_check_desk = QCheckBox(self)
        self.first_item_check_desk.setText("Notify to Desktop?")
        self.first_item_check_desk.setStyleSheet(StyleSheet)
        self.first_item_check_desk.move(50, 110)
        self.first_item_check_desk.resize(110, 30)

        self.first_item_check_email = QCheckBox(self)
        self.first_item_check_email.setText("Notify to Email?")
        self.first_item_check_email.setStyleSheet(StyleSheet)
        self.first_item_check_email.move(195, 110)
        self.first_item_check_email.resize(110, 30)

        self.first_item_button = QPushButton(self)
        self.first_item_button.setText("Track Item One")
        self.first_item_button.setStyleSheet(StyleSheet)
        self.first_item_button.move(320, 75)
        self.first_item_button.clicked.connect(self.first_btn_track_clicked)

        self.first_item_button_stop = QPushButton(self)
        self.first_item_button_stop.setEnabled(False)
        self.first_item_button_stop.setText("Stop Tracking")
        self.first_item_button_stop.setStyleSheet(StyleSheet)
        self.first_item_button_stop.move(430, 75)
        self.first_item_button_stop.clicked.connect(self.first_item_track_stop_clicked)

        # LED indicator, if web server response code 200 = very good
        # if web server response code 404, 403 = not very good
        self.first_item_indicator = QLabel(self)
        self.first_item_indicator.move(540, 75)

        # second item options
        self.second_item_label = QLabel("Second URL:", self)
        self.second_item_label.setStyleSheet(StyleSheet)
        self.second_item_label.move(140, 145)

        self.second_item_input = QLineEdit(self)
        self.second_item_input.resize(250, 30)
        self.second_item_input.move(50, 175)
        self.second_item_input.setStyleSheet(StyleSheet)
        self.second_item_input.setPlaceholderText("Enter second URL item")

        self.second_item_check_desktop = QCheckBox(self)
        self.second_item_check_desktop.setText("Notify to Desktop?")
        self.second_item_check_desktop.setStyleSheet(StyleSheet)
        self.second_item_check_desktop.move(50, 210)
        self.second_item_check_desktop.resize(110, 30)

        self.second_item_check_email = QCheckBox(self)
        self.second_item_check_email.setText("Notify to Email?")
        self.second_item_check_email.setStyleSheet(StyleSheet)
        self.second_item_check_email.move(195, 210)
        self.second_item_check_email.resize(110, 30)

        self.second_item_button = QPushButton(self)
        self.second_item_button.setText("Track Item Two")
        self.second_item_button.setStyleSheet(StyleSheet)
        self.second_item_button.move(320, 175)
        self.second_item_button.clicked.connect(self.two_btn_track_clicked)

        self.second_item_button_stop = QPushButton(self)
        self.second_item_button_stop.setEnabled(False)
        self.second_item_button_stop.setText("Stop Tracking")
        self.second_item_button_stop.setStyleSheet(StyleSheet)
        self.second_item_button_stop.move(430, 175)
        self.second_item_button_stop.clicked.connect(self.two_item_track_stop_clicked)

        self.second_item_indicator = QLabel(self)
        self.second_item_indicator.move(540, 175)

        # third item options
        self.third_item_label = QLabel("Third URL:", self)
        self.third_item_label.setStyleSheet(StyleSheet)
        self.third_item_label.move(140, 245)

        self.third_item_input = QLineEdit(self)
        self.third_item_input.resize(250, 30)
        self.third_item_input.move(50, 275)
        self.third_item_input.setStyleSheet(StyleSheet)
        self.third_item_input.setPlaceholderText("Enter third URL item")

        self.third_item_check_desktop = QCheckBox(self)
        self.third_item_check_desktop.setText("Notify to Desktop?")
        self.third_item_check_desktop.setStyleSheet(StyleSheet)
        self.third_item_check_desktop.move(50, 310)
        self.third_item_check_desktop.resize(110, 30)

        self.third_item_check_email = QCheckBox(self)
        self.third_item_check_email.setText("Notify to Email?")
        self.third_item_check_email.setStyleSheet(StyleSheet)
        self.third_item_check_email.move(195, 310)
        self.third_item_check_email.resize(110, 30)

        self.third_item_button = QPushButton(self)
        self.third_item_button.setText("Track Item Three")
        self.third_item_button.setStyleSheet(StyleSheet)
        self.third_item_button.move(320, 275)
        self.third_item_button.clicked.connect(self.three_btn_track_clicked)

        self.third_item_button_stop = QPushButton(self)
        self.third_item_button_stop.setEnabled(False)
        self.third_item_button_stop.setText("Stop Tracking")
        self.third_item_button_stop.setStyleSheet(StyleSheet)
        self.third_item_button_stop.move(430, 275)
        self.third_item_button_stop.clicked.connect(self.three_item_track_stop_clicked)

        self.third_item_indicator = QLabel(self)
        self.third_item_indicator.move(540, 275)

        # forth item options
        self.fourth_item_label = QLabel("Forth URL:", self)
        self.fourth_item_label.setStyleSheet(StyleSheet)
        self.fourth_item_label.move(140, 345)

        self.fourth_item_input = QLineEdit(self)
        self.fourth_item_input.resize(250, 30)
        self.fourth_item_input.move(50, 375)
        self.fourth_item_input.setStyleSheet(StyleSheet)
        self.fourth_item_input.setPlaceholderText("Enter fourth URL item")

        self.fourth_item_check_desktop = QCheckBox(self)
        self.fourth_item_check_desktop.setText("Notify to Desktop?")
        self.fourth_item_check_desktop.setStyleSheet(StyleSheet)
        self.fourth_item_check_desktop.move(50, 410)
        self.fourth_item_check_desktop.resize(110, 30)

        self.fourth_item_check_email = QCheckBox(self)
        self.fourth_item_check_email.setText("Notify to Email?")
        self.fourth_item_check_email.setStyleSheet(StyleSheet)
        self.fourth_item_check_email.move(195, 410)
        self.fourth_item_check_email.resize(110, 30)

        self.fourth_item_button = QPushButton(self)
        self.fourth_item_button.setText("Track Item Four")
        self.fourth_item_button.setStyleSheet(StyleSheet)
        self.fourth_item_button.move(320, 375)
        self.fourth_item_button.clicked.connect(self.four_btn_track_clicked)

        self.fourth_item_button_stop = QPushButton(self)
        self.fourth_item_button_stop.setEnabled(False)
        self.fourth_item_button_stop.setText("Stop Tracking")
        self.fourth_item_button_stop.setStyleSheet(StyleSheet)
        self.fourth_item_button_stop.move(430, 375)
        self.fourth_item_button_stop.clicked.connect(self.four_item_track_stop_clicked)

        self.fourth_item_indicator = QLabel(self)
        self.fourth_item_indicator.move(540, 375)

        # fifth item options
        self.fifth_item_label = QLabel("Fifth URL:", self)
        self.fifth_item_label.setStyleSheet(StyleSheet)
        self.fifth_item_label.move(140, 445)

        self.fifth_item_input = QLineEdit(self)
        self.fifth_item_input.resize(250, 30)
        self.fifth_item_input.move(50, 475)
        self.fifth_item_input.setStyleSheet(StyleSheet)
        self.fifth_item_input.setPlaceholderText("Enter fifth URL item")

        self.fifth_item_check_desktop = QCheckBox(self)
        self.fifth_item_check_desktop.setText("Notify to Desktop?")
        self.fifth_item_check_desktop.setStyleSheet(StyleSheet)
        self.fifth_item_check_desktop.move(50, 510)
        self.fifth_item_check_desktop.resize(110, 30)

        self.fifth_item_check_email = QCheckBox(self)
        self.fifth_item_check_email.setText("Notify to Email?")
        self.fifth_item_check_email.setStyleSheet(StyleSheet)
        self.fifth_item_check_email.move(195, 510)
        self.fifth_item_check_email.resize(110, 30)

        self.fifth_item_button = QPushButton(self)
        self.fifth_item_button.setText("Track Item Five")
        self.fifth_item_button.setStyleSheet(StyleSheet)
        self.fifth_item_button.move(320, 475)
        self.fifth_item_button.clicked.connect(self.five_btn_track_clicked)

        self.fifth_item_button_stop = QPushButton(self)
        self.fifth_item_button_stop.setEnabled(False)
        self.fifth_item_button_stop.setText("Stop Tracking")
        self.fifth_item_button_stop.setStyleSheet(StyleSheet)
        self.fifth_item_button_stop.move(430, 475)
        self.fifth_item_button_stop.clicked.connect(self.five_item_track_stop_clicked)

        self.fifth_item_indicator = QLabel(self)
        self.fifth_item_indicator.move(540, 475)

        # Status of items display, QLabel and QTextEdit
        self.status_items_label = QLabel("Items Status", self)
        self.status_items_label.move(350, 570)
        self.status_items_label.setStyleSheet(
            '''
            QLabel{
                font-size: 12px;
                color: #FFF;
            }
            '''
        )

        self.status_items_display = QTextEdit(self)
        self.status_items_display.setStyleSheet(StyleSheet)
        self.status_items_display.move(10, 600)
        self.status_items_display.resize(780, 185)
        self.status_items_display.setDisabled(True)
        self.status_items_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Additional buttons and functions to be displayed here
        # help button
        self.show_help_button = QPushButton(self)
        self.show_help_button.setStyleSheet(
            '''
                QPushButton {
                    border: 2px solid rgb(37, 39, 48);
                    border-radius: 10px;
                    font-size: 15px;
                    color: #FFF;
                }
                QPushButton:hover{
                    background: '#BC006C';
                }
            '''
        )
        self.show_help_button.move(700, 26)
        self.show_help_button.setText("Help")
        self.show_help_button.clicked.connect(self.show_help)

        # Export tracking results to csv
        self.produce_report_button = QPushButton(self)
        self.produce_report_button.setStyleSheet(
            '''
                QPushButton {
                    border: 2px solid rgb(37, 39, 48);
                    border-radius: 10px;
                    font-size: 12px;
                    color: #FFF;
                }
                QPushButton:hover{
                    background: '#BC006C';
                }
            '''
        )
        self.produce_report_button.setText("Produce Report")
        self.produce_report_button.move(700, 60)
        self.produce_report_button.clicked.connect(self.produce_report)

        self.open_user_prefs = QPushButton(self)
        self.open_user_prefs.setText("Settings")
        self.open_user_prefs.setStyleSheet(StyleSheet)
        self.open_user_prefs.move(700, 95)
        self.open_user_prefs.clicked.connect(self.open_user_preferences)

        self.close_app_btn = QPushButton(self)
        self.close_app_btn.setText("Exit")
        self.close_app_btn.setStyleSheet(StyleSheet)
        self.close_app_btn.move(700, 130)
        self.close_app_btn.clicked.connect(self.quit_app)

        self.initial_indicator()
        self.create_top_banner()  # start the top banner scene
        self.center()  # call function to center the window
        self.show()  # show the QMainWindow

    # First tracking button function
    def first_btn_track_clicked(self):
        global item1_is_running, first_item_url
        if self.first_item_input.text():    # check if input has text inside
            item1_is_running = True
            first_item_url = str(self.first_item_input.text())  # get the text(hopefully a URL)
            self.thread = QThread()
            self.worker = WorkerOne()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.parsed_signal.connect(self.update_items_status)
            self.worker.tracking_or_nah.connect(self.track_or_nah)
            self.worker.item_is_found.connect(self.desktop_push)
            self.thread.start()

    # First tracking button stop
    def first_item_track_stop_clicked(self):
        global item1_is_running
        item1_is_running = False
        self.first_item_button.setEnabled(True)
        self.first_item_button_stop.setEnabled(False)
        self.track_or_nah(1,0)
        self.thread.quit()


    # Second tracking button function
    def two_btn_track_clicked(self):
        global item2_is_running, second_item_url
        if self.second_item_input.text():    # check if input has text inside
            item2_is_running = True
            second_item_url = str(self.second_item_input.text())  # get the text(hopefully a URL)
            self.thread2 = QThread()
            self.worker2 = WorkerTwo()
            self.worker2.moveToThread(self.thread2)
            self.thread2.started.connect(self.worker2.run)
            self.worker2.parsed_signal2.connect(self.update_items_status)
            self.worker2.tracking_or_nah2.connect(self.track_or_nah)
            self.worker2.item_is_found2.connect(self.desktop_push)
            self.thread2.start()

    # Second tracking button stop
    def two_item_track_stop_clicked(self):
        global item2_is_running
        item2_is_running = False
        self.second_item_button.setEnabled(True)
        self.second_item_button_stop.setEnabled(False)
        self.track_or_nah(2,0)
        self.thread2.quit()

    # Third tracking button function
    def three_btn_track_clicked(self):
        global item3_is_running, third_item_url
        if self.third_item_input.text():    # check if input has text inside
            item3_is_running = True
            third_item_url = str(self.third_item_input.text())  # get the text(hopefully a URL)
            self.thread3 = QThread()
            self.worker3 = WorkerThree()
            self.worker3.moveToThread(self.thread3)
            self.thread3.started.connect(self.worker3.run)
            self.worker3.parsed_signal3.connect(self.update_items_status)
            self.worker3.tracking_or_nah3.connect(self.track_or_nah)
            self.worker3.item_is_found3.connect(self.desktop_push)
            self.thread3.start()

    # Third tracking button stop
    def three_item_track_stop_clicked(self):
        global item3_is_running
        item3_is_running = False
        self.third_item_button.setEnabled(True)
        self.third_item_button_stop.setEnabled(False)
        self.track_or_nah(3,0)
        self.thread3.quit()

    # Fourth tracking button function
    def four_btn_track_clicked(self):
        global item4_is_running, fourth_item_url
        if self.fourth_item_input.text():    # check if input has text inside
            item4_is_running = True
            fourth_item_url = str(self.fourth_item_input.text())  # get the text(hopefully a URL)
            self.thread4 = QThread()
            self.worker4 = WorkerFour()
            self.worker4.moveToThread(self.thread4)
            self.thread4.started.connect(self.worker4.run)
            self.worker4.parsed_signal4.connect(self.update_items_status)
            self.worker4.tracking_or_nah4.connect(self.track_or_nah)
            self.worker4.item_is_found4.connect(self.desktop_push)
            self.thread4.start()

    # Fourth tracking button to stop
    def four_item_track_stop_clicked(self):
        global item4_is_running
        item4_is_running = False
        self.fourth_item_button_stop.setEnabled(False)
        self.fourth_item_button.setEnabled(True)
        self.track_or_nah(4,0)
        self.thread4.quit()

    # Fifth tracking button function
    def five_btn_track_clicked(self):
        global item5_is_running, fifth_item_url
        if self.fifth_item_input.text():    # check if input has text inside
            item5_is_running = True
            fifth_item_url = str(self.fifth_item_input.text())  # get the text(hopefully a URL)
            self.thread5 = QThread()
            self.worker5 = WorkerFive()
            self.worker5.moveToThread(self.thread5)
            self.thread5.started.connect(self.worker5.run)
            self.worker5.parsed_signal5.connect(self.update_items_status)
            self.worker5.tracking_or_nah5.connect(self.track_or_nah)
            self.worker5.item_is_found5.connect(self.desktop_push)
            self.thread5.start()

    # Fifth tracking button stop
    def five_item_track_stop_clicked(self):
        global item5_is_running
        item5_is_running = False
        self.fifth_item_button.setEnabled(True)
        self.fifth_item_button_stop.setEnabled(False)
        self.track_or_nah(5,0)
        self.thread5.quit()

    # update the status display to show items that are tracking
    # slot for a signal
    # (60 seconds interval to lower the chance of an IP ban, timer found at Worker subclasses)
    def update_items_status(self, title, price, availability):
        titlez = title.split("|")[0]
        pricez = price.split("£")[1]
        availabilities = availability
        datenowthx = QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate)
        reportingz = str(f'Item: {titlez}, Price: {pricez}, Availability: {availabilities}, Date: {datenowthx}\n')
        # reportingz = str({
        #         'Item': titlez,
        #         'Price': pricez,
        #         'Availability': availabilities,
        #         'Date': datenowthx
        # })
        # print(reportingz)
        self.status_items_display.append(reportingz)

    # button function, produce report
    def produce_report(self):
        test_text = self.status_items_display.toPlainText()
        # find the path of the csv_save_path
        with open(path_of_user_prefs, "r") as find_path:
            csv_path_is = find_path.readlines()
            directory = csv_path_is[1].split("=")[1]
            x = datetime.datetime.now()
            file = f"{x.year}_{x.month}_{x.day}.csv"
            path_csv = os.path.join(directory, file)

        # check if directory exists,
        if os.path.exists(path_csv):
            # write to csv
            with open(path_csv, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(test_text)
        else:
            # create the dir
            os.mkdir(os.path.dirname(path_csv))
            # write to csv
            with open(path_csv, 'w') as f:
                 writer = csv.writer(f)
                 writer.writerows(test_text)

    # function to create the top banner to display time and version
    def create_top_banner(self):
        scene = QGraphicsScene()
        scene.setSceneRect(QRectF(0, 0, 800, 50))
        scene.setBackgroundBrush(QBrush(QColor(204, 204, 255)))

        top_view = QGraphicsView(self)
        top_view.setScene(scene)
        top_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        top_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        top_view.setGeometry(0, 0, 800, 25)

        welcome_label = QGraphicsSimpleTextItem('StellaBot Version 1.0')
        welcome_label.setFont(QFont('Times New Roman', 12))
        welcome_label.setBrush(QColor(153, 51, 255))
        welcome_label.setPos(5, 15)
        scene.addItem(welcome_label)

        self.system_date = QGraphicsSimpleTextItem('')
        self.system_date.setFont(QFont('OldEnglish', 12))
        self.system_date.setBrush(QColor(153, 51, 255))
        self.system_date.setPos(500, 15)
        scene.addItem(self.system_date)

        self.get_sys_time()

    # function using signals and slots to change the colour of the background
    def change_background_colour(self, the_signal):
        if the_signal == 0:
            self.setStyleSheet("background: #161219;")
        elif the_signal == 1:
            self.setStyleSheet("background: #571B7E;")
        else:
            self.setStyleSheet("background: #9FA0B1;")

    # function to get system time and update time by 1 second
    def get_sys_time(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_and_display_time)
        timer.start(1000)

    # function to display the time on the window and also changes background color (poor way to do it
    # but calling a function from Qdialog to Qmainwindow will create another window)
    def update_and_display_time(self):
        time_oki = QDateTime.currentDateTime()
        timeDisplay = time_oki.toString(Qt.DefaultLocaleLongDate)
        self.system_date.setText(timeDisplay)

    def open_user_preferences(self):    # opens window for user to enter preferences, and assigns slot for signal emits
        self.pref = UserPreferences()
        self.pref.send_signal.connect(self.change_background_colour)

    # quit app function
    def quit_app(self):
        self.quitmsg = QMessageBox(self)
        self.quitmsg.setStyleSheet("QLabel{ color: white}")
        reply = self.quitmsg.question(self,"Close StellaBot", "Are you sure you want to close StellaBot?",
                                      self.quitmsg.Yes | self.quitmsg.No)
        if reply == self.quitmsg.Yes:
            self.close()

    # opens another window to display help
    def show_help(self):
        self.helpwindow = HelpWindow()

    # function to center window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # function to alternate between enabled or disabled buttons
    def track_or_nah(self, item, on_or_off):
        target_button = item
        status = on_or_off  # 1 for tracking, 0 for non tracking
        self.RED_LED = QPixmap("Images/red_led4.png")
        self.GREEN_LED = QPixmap("Images/green_led.png")
        if target_button == 1:
            if status == 1:
                self.first_item_button.setEnabled(False)
                self.first_item_button_stop.setEnabled(True)
                self.first_item_indicator.setPixmap(self.GREEN_LED)
            else:
                self.first_item_button.setEnabled(True)
                self.first_item_button_stop.setEnabled(False)
                self.first_item_indicator.setPixmap(self.RED_LED)
        elif target_button == 2:
            if status == 1:
                self.second_item_button.setEnabled(False)
                self.second_item_button_stop.setEnabled(True)
                self.second_item_indicator.setPixmap(self.GREEN_LED)
            else:
                self.second_item_button.setEnabled(True)
                self.second_item_button_stop.setEnabled(False)
                self.second_item_indicator.setPixmap(self.RED_LED)
        elif target_button == 3:
            if status == 1:
                self.third_item_button.setEnabled(False)
                self.third_item_button_stop.setEnabled(True)
                self.third_item_indicator.setPixmap(self.GREEN_LED)
            else:
                self.third_item_button.setEnabled(True)
                self.third_item_button_stop.setEnabled(False)
                self.third_item_indicator.setPixmap(self.RED_LED)
        elif target_button == 4:
            if status == 1:
                self.fourth_item_button.setEnabled(False)
                self.fourth_item_button_stop.setEnabled(True)
                self.fourth_item_indicator.setPixmap(self.GREEN_LED)
            else:
                self.fourth_item_button.setEnabled(True)
                self.fourth_item_button_stop.setEnabled(False)
                self.fourth_item_indicator.setPixmap(self.RED_LED)
        elif target_button == 5:
            if status == 1:
                self.fifth_item_button.setEnabled(False)
                self.fifth_item_button_stop.setEnabled(True)
                self.fifth_item_indicator.setPixmap(self.GREEN_LED)
            else:
                self.fifth_item_button.setEnabled(True)
                self.fifth_item_button_stop.setEnabled(False)
                self.fifth_item_indicator.setPixmap(self.RED_LED)
        else:
            print("nothing happened!")

    def initial_indicator(self):
        self.RED_LEDs = QPixmap("Images/red_led4.png")
        self.first_item_indicator.setPixmap(self.RED_LEDs)
        self.second_item_indicator.setPixmap(self.RED_LEDs)
        self.third_item_indicator.setPixmap(self.RED_LEDs)
        self.fourth_item_indicator.setPixmap(self.RED_LEDs)
        self.fifth_item_indicator.setPixmap(self.RED_LEDs)

    # Alerts management, either desktop or email
    def desktop_push(self, titlez, item_number, avail):     # item_number is the n item that is being tracked, 1-5
        if item_number == 1 and self.first_item_check_desk.isChecked():
            ttt = str(titlez).split("|")[0]
            amount = str(avail).split("(")[1]
            amount2 = str(amount).split(")")[0]
            notification = Notify()
            notification.title = ttt
            notification.message = f"Item found with {amount2}"   #heres the link {url}"
            notification.application_name = "StellaBot"
            notification.send()

        elif item_number == 2 and self.second_item_check_desktop.isChecked():
            ttt = str(titlez).split("|")[0]
            amount = str(avail).split("(")[1]
            amount2 = str(amount).split(")")[0]
            notification = Notify()
            notification.title = ttt
            notification.message = f"Item found with {amount2}"   #heres the link {url}"
            notification.application_name = "StellaBot"
            notification.send()
        elif item_number == 3 and self.third_item_check_desktop.isChecked():
            ttt = str(titlez).split("|")[0]
            amount = str(avail).split("(")[1]
            amount2 = str(amount).split(")")[0]
            notification = Notify()
            notification.title = ttt
            notification.message = f"Item found with {amount2}"   #heres the link {url}"
            notification.application_name = "StellaBot"
            notification.send()
        elif item_number == 4 and self.fourth_item_check_desktop.isChecked():
            ttt = str(titlez).split("|")[0]
            amount = str(avail).split("(")[1]
            amount2 = str(amount).split(")")[0]
            notification = Notify()
            notification.title = ttt
            notification.message = f"Item found with {amount2}"   #heres the link {url}"
            notification.application_name = "StellaBot"
            notification.send()
        elif item_number == 5 and self.fifth_item_check_desktop.isChecked():
            ttt = str(titlez).split("|")[0]
            amount = str(avail).split("(")[1]
            amount2 = str(amount).split(")")[0]
            notification = Notify()
            notification.title = ttt
            notification.message = f"Item found with {amount2}"   #heres the link {url}"
            notification.application_name = "StellaBot"
            notification.send()
        else:
            print("Item found but no desktop checkboxes were checked!")


if __name__ == '__main__':
    app = QApplication([])

    splash = SplashScreen()
    splash.show()
    splash.progress()
    window = MainWindow()
    splash.finish(window)

    app.exec_()
