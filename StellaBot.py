import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import requests

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
        padding-left: 3px;
        background-color: rgb(34, 36, 44);
}
"""

WINDOW_SIZE = 800, 800
BACKGROUND_APP_MAIN = 255, 255, 255
BACKGROUND_APP_ALT = 58, 57, 57
VERSION_NUMBER_STR = ("Version: " + str(0.6))
OFFSET_X = 50
OFFSET_Y = 30


# Help & tutorial of the application, will add more items to the class when getting close to version 1.0
class HelpWindow(QDialog):
    def __init__(self):
        super(HelpWindow, self).__init__()
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon('Images/info.ico'))
        self.setStyleSheet("background: #161219;")
        width = 600
        height = 600
        self.resize(width, height)

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
        self.first_item_button.clicked.connect(self.btn_clicked)

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
        self.second_item_button.clicked.connect(self.btn_clicked)

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
        self.third_item_button.clicked.connect(self.btn_clicked)

        # forth item options
        self.forth_item_label = QLabel("Forth URL:", self)
        self.forth_item_label.setStyleSheet(StyleSheet)
        self.forth_item_label.move(140, 345)

        self.forth_item_input = QLineEdit(self)
        self.forth_item_input.resize(250, 30)
        self.forth_item_input.move(50, 375)
        self.forth_item_input.setStyleSheet(StyleSheet)
        self.forth_item_input.setPlaceholderText("Enter forth URL item")

        self.forth_item_check_desktop = QCheckBox(self)
        self.forth_item_check_desktop.setText("Notify to Desktop?")
        self.forth_item_check_desktop.setStyleSheet(StyleSheet)
        self.forth_item_check_desktop.move(50, 410)
        self.forth_item_check_desktop.resize(110, 30)

        self.forth_item_check_email = QCheckBox(self)
        self.forth_item_check_email.setText("Notify to Email?")
        self.forth_item_check_email.setStyleSheet(StyleSheet)
        self.forth_item_check_email.move(195, 410)
        self.forth_item_check_email.resize(110, 30)

        self.forth_item_button = QPushButton(self)
        self.forth_item_button.setText("Track Item Four")
        self.forth_item_button.setStyleSheet(StyleSheet)
        self.forth_item_button.move(320, 375)
        self.forth_item_button.clicked.connect(self.btn_clicked)

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
        self.fifth_item_button.clicked.connect(self.btn_clicked)

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
        self.create_top_banner()  # start the top banner scene
        self.center()  # call function to center the window
        self.show()  # show the QMainWindow

    # button functions placeholders for now
    def btn_clicked(self):
        print("clicked!")

    # button function, produce report
    def produce_report(self):
        print("place holder, produced report")

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

        welcome_label = QGraphicsSimpleTextItem('StellaBot Version 0.6')
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

    # function to get system time and update time by 1 second
    def get_sys_time(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_and_display_time)
        timer.start(1000)

    # function to display the time on the window
    def update_and_display_time(self):
        time_oki = QDateTime.currentDateTime()
        # timeDisplay = time_oki.toString('dddd MM-dd-yyyy hh:mm:ss')
        timeDisplay = time_oki.toString(Qt.DefaultLocaleLongDate)
        self.system_date.setText(timeDisplay)

    # not used
    def create_mid_scene(self):
        scene = QGraphicsScene()
        # scene.setSceneRect(QRectF(0, 0, 1200-30, 755-20))
        scene.setSceneRect(QRectF(0, 0, 1200, 755))
        scene.setBackgroundBrush(QBrush(QColor(32, 32, 32)))
        mid_view = QGraphicsView(self)
        mid_view.setScene(scene)
        mid_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mid_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mid_view.setGeometry(0, 45, 1200, 755)

        welcome_label = QGraphicsSimpleTextItem('Enter URL of the desired Item: ')
        welcome_label.setFont(QFont('Fantasy', 10))
        welcome_label.setBrush(QColor('purple'))
        welcome_label.setPos(10, 725)
        scene.addItem(welcome_label)

        input_url = QGraphicsSimpleTextItem('This is where it goes: ')
        input_url.setFont(QFont('Fantasy', 10))
        input_url.setBrush(QColor('purple'))
        input_url.setPos(190, 10)
        scene.addItem(input_url)

    # opens window for user to enter preferences
    def preferences_app(self):
        pass

    # quit app function
    def quit_app(self):
        self.close()

    # opens another window to display help
    def show_help(self):
        self.helpwindow = HelpWindow()

    def setbackground_app_main(self):
        # background = QBrush(QColor(*BACKGROUND_APP_MAIN))
        self.setStyleSheet("background-color: rgb(58, 48, 48);")

    def setbackground_app_alt(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255)")

    # function to center window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication([])

    splash = SplashScreen()
    splash.show()
    splash.progress()

    window = MainWindow()
    splash.finish(window)

    app.exec_()
