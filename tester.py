import datetime
import os

#
# save_path_test = r'C:\StellaBotOutputCsv3'
# create_path_of_user_prefs = os.path.join(save_path_test, "user_settings.txt")
# path_of_report_csv = os.path.join(save_path_test, "report.csv")
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from requests_html import HTMLSession

list_of_urls = ['', '', '', '', '']
first_url = "https://books.toscrape.com/catalogue/private-paris-private-10_958/index.html"
second_url = "https://books.toscrape.com/catalogue/bridget-joness-diary-bridget-jones-1_10/index.html"
third_url = "https://books.toscrape.com/catalogue/something-blue-darcy-rachel-2_223/index.html"
fourth_url = "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"

f = HTMLSession()
s = HTMLSession()
item1_is_running = False
item2_is_running = False




