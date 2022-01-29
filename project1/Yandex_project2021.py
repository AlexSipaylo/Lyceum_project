import sqlite3
import sys
from random import sample
import datetime
import time
import mouse

from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QFrame, QAbstractItemView, QScrollArea
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.container = QWidget()
        self.main_window = MainWindowWidget()
        self.practice_window = PracticeWindowWidget()
        self.chart_window = ChartWindowWidget()
        self.glossary_window = GlossaryWindowWidget()
        self.statistics_window = StatisticsWindowWidget()
        self.read_window = ReadWindowWidget()
        self.select_number_of_questions1 = NumberOfQuestionsWidget1()
        self.select_number_of_questions2 = NumberOfQuestionsWidget2()
        self.write_window = WriteWindowWidget()
        self.game_over_window1 = GameOverWindowWidget1()
        self.game_over_window2 = GameOverWindowWidget2()

        self.spisok_slov_i_zvukov = [('sleep', 'sliːp'), ('me', 'miː'), ('happy', 'ˈhæpɪ'), ('recipe', 'ˈresɪpɪ'),
                                     ('pin', 'pɪn'), ('dinner', 'ˈdɪnə'), ('foot', 'fʊt'), ('could', 'kʊd'),
                                     ('pull', 'pʊl'), ('casual', 'ˈkæʒʊəl'), ('do', 'duː'), ('shoe', 'ʃuː'),
                                     ('through', 'θruː'), ('red', 'red'), ('head', 'hed'), ('said', 'sed'),
                                     ('arrive', 'əˈraɪv'), ('father', 'ˈfɑːðə'), ('colour', 'ˈkʌlə'),
                                     ('walk', 'wɔːk'), ('turn', 'tɜːn'), ('bird', 'bɜːd'), ('work', 'wɜːk'),
                                     ('sort', 'sɔːt'), ('thought', 'θɔːt'), ('cat', 'kæt'), ('black', 'blæk'),
                                     ('sun', 'sʌn'), ('enough', 'ɪˈnʌf'), ('wonder', 'ˈwʌndə'), ('got', 'gɒt'),
                                     ('watch', 'wɒʧ'), ('sock', 'sɒk'), ('part', 'pɑːt'), ('heart', 'hɑːt'),
                                     ('laugh', 'lɑːf'), ('name', 'neɪm'), ('late', 'leɪt'), ('aim', 'eɪm'),
                                     ('my', 'maɪ'), ('idea', 'aɪˈdɪə'), ('time', 'taɪm'), ('boy', 'bɔɪ'),
                                     ('noise', 'nɔɪz'), ('pair', 'peə'), ('where', 'weə'), ('bear', 'beə'),
                                     ('hear', 'hɪə'), ('cheers', 'ˈʧɪəz'), ('go', 'gəʊ'), ('home', 'həʊm'),
                                     ('show', 'ʃəʊ'), ('out', 'aʊt'), ('cow', 'kaʊ'), ('pure', 'pjʊə'),
                                     ('fewer', 'ˈfjuːər')]

        self.r = self.spisok_slov_i_zvukov[:]
        self.question = 1
        self.score = 0
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.container)
        self.setStyleSheet("background-color: #524f59")
        self.setWindowTitle('Sounds')

        self.setGeometry(350, 150, 1000, 620)
        layout = QVBoxLayout(self.container)
        layout.setSpacing(0)

        self.practice_window.hide()
        self.chart_window.hide()
        self.glossary_window.hide()
        self.statistics_window.hide()
        self.read_window.hide()
        self.select_number_of_questions1.hide()
        self.select_number_of_questions2.hide()
        self.write_window.hide()
        self.game_over_window1.hide()
        self.game_over_window2.hide()

        layout.addWidget(self.main_window)
        layout.addWidget(self.practice_window)
        layout.addWidget(self.glossary_window)
        layout.addWidget(self.select_number_of_questions1)
        layout.addWidget(self.select_number_of_questions2)
        layout.addWidget(self.chart_window)
        layout.addWidget(self.statistics_window)
        layout.addWidget(self.read_window)
        layout.addWidget(self.write_window)
        layout.addWidget(self.game_over_window1)
        layout.addWidget(self.game_over_window2)

        self.main_window.tester_button.clicked.connect(self.run_practice_window)
        self.main_window.chart_button.clicked.connect(self.run_chart_window)
        self.main_window.glossary_button.clicked.connect(self.run_glossary_window)
        self.main_window.statistics_button.clicked.connect(self.run_statistics_window)

        self.practice_window.back_button.clicked.connect(self.back_to_main_window1)
        self.practice_window.read_button.clicked.connect(self.run_select_window1)
        self.practice_window.write_button.clicked.connect(self.run_select_window2)

        self.chart_window.back_button.clicked.connect(self.back_to_main_window2)
        self.statistics_window.back_button.clicked.connect(self.back_to_main_window4)
        self.glossary_window.back_button.clicked.connect(self.back_to_main_window3)
        self.statistics_window.clean_button.clicked.connect(self.clean_data_base)

        self.select_number_of_questions1.back_button.clicked.connect(self.back_to_practice_window1)
        self.select_number_of_questions1.select_button1.clicked.connect(self.run_read_window)
        self.select_number_of_questions1.select_button2.clicked.connect(self.run_read_window)
        self.select_number_of_questions1.select_button3.clicked.connect(self.run_read_window)
        self.select_number_of_questions2.back_button.clicked.connect(self.back_to_practice_window2)
        self.select_number_of_questions2.select_button1.clicked.connect(self.run_write_window)
        self.select_number_of_questions2.select_button2.clicked.connect(self.run_write_window)
        self.select_number_of_questions2.select_button3.clicked.connect(self.run_write_window)

        self.read_window.check_button.clicked.connect(self.check1)
        self.read_window.back_button.clicked.connect(self.back_to_practice_from_read_window)
        self.read_window.next_button.clicked.connect(self.next1)
        self.read_window.show_button.clicked.connect(self.show1)

        self.write_window.back_button.clicked.connect(self.back_to_practice_from_write_window)
        self.write_window.check_button.clicked.connect(self.check2)
        self.write_window.next_button.clicked.connect(self.next2)
        self.write_window.show_button.clicked.connect(self.show2)

        self.game_over_window1.back_button.clicked.connect(self.back_to_practice_from_game_over_window1)
        self.game_over_window1.ok_button.clicked.connect(self.insert1)
        self.game_over_window2.back_button.clicked.connect(self.back_to_practice_from_game_over_window2)
        self.game_over_window2.ok_button.clicked.connect(self.insert2)

    def insert1(self):
        now = datetime.datetime.now().replace(microsecond=0)
        if self.game_over_window1.name.text() != '' and self.game_over_window1.surname.text() != '' and \
                self.game_over_window1.age.text() != '':
            con = sqlite3.connect("Results.db")
            cur1 = con.cursor()
            result1 = """INSERT INTO Users
                (Name, Surname, Age) 
                VALUES (?, ?, ?)"""
            data1 = (self.game_over_window1.name.text(), self.game_over_window1.surname.text(), \
                     self.game_over_window1.age.text())
            cur1.execute(result1, data1)
            cur1.close()

            cur2 = con.cursor()
            result2 = """SELECT * FROM Users"""
            cur2.execute(result2)
            records = cur2.fetchall()
            cur2.close()

            cur3 = con.cursor()
            result3 = """INSERT INTO Results
                            (User, Task, Result, Date) 
                            VALUES (?, ?, ?, ?)"""

            data2 = (records[-1][0], 'Read', f'{self.score}/{self.number1}', str(now))
            cur3.execute(result3, data2)
            cur3.close()
            con.commit()
            con.close()
        self.game_over_window1.ok_button.setEnabled(False)
        self.game_over_window1.name.setEnabled(False)
        self.game_over_window1.surname.setEnabled(False)
        self.game_over_window1.age.setEnabled(False)

    def insert2(self):
        now = datetime.datetime.now().replace(microsecond=0)
        if self.game_over_window2.name.text() != '' and self.game_over_window2.surname.text() != '' and \
                self.game_over_window2.age.text() != '':
            con = sqlite3.connect("Results.db")
            cur1 = con.cursor()
            result1 = """INSERT INTO Users
                (Name, Surname, Age) 
                VALUES (?, ?, ?)"""
            data1 = (self.game_over_window2.name.text(), self.game_over_window2.surname.text(), \
                     self.game_over_window2.age.text())
            cur1.execute(result1, data1)
            cur1.close()

            cur2 = con.cursor()
            result2 = """SELECT * FROM Users"""
            cur2.execute(result2)
            records = cur2.fetchall()
            cur2.close()

            cur3 = con.cursor()
            result3 = """INSERT INTO Results
                            (User, Task, Result, Date) 
                            VALUES (?, ?, ?, ?)"""

            data2 = (records[-1][0], 'Write', f'{self.score}/{self.number2}', str(now))
            cur3.execute(result3, data2)
            cur3.close()
            con.commit()
            con.close()
        self.game_over_window2.ok_button.setEnabled(False)
        self.game_over_window2.name.setEnabled(False)
        self.game_over_window2.surname.setEnabled(False)
        self.game_over_window2.age.setEnabled(False)

    def clean_data_base(self):
        warning = QMessageBox(QMessageBox.Warning, 'Warning', 'Are you sure you want to clear statistics?',
                              QMessageBox.Yes | QMessageBox.No)
        warning.exec()
        reply = warning.standardButton(warning.clickedButton())
        if reply == QMessageBox.Yes:
            con = sqlite3.connect("Results.db")
            cur = con.cursor()
            result1 = """DELETE FROM Users"""
            result2 = """DELETE FROM Results"""
            cur.execute(result1)
            cur.execute(result2)
            con.commit()
            cur.close()
            con.close()
            self.statistics_window.table.setRowCount(0)

    def run_practice_window(self):
        self.main_window.hide()
        self.setWindowTitle('Practice')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def back_to_main_window1(self):
        self.practice_window.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 620)
        self.main_window.show()

    def run_chart_window(self):
        self.main_window.hide()
        self.setWindowTitle('Chart')
        self.setGeometry(350, 150, 1000, 840)
        self.chart_window.text_output.clear()
        self.chart_window.show()

    def run_glossary_window(self):
        self.main_window.hide()
        self.setWindowTitle('Glossary')
        self.setGeometry(350, 150, 1000, 620)
        con = sqlite3.connect("Glossary.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM School""").fetchall()
        cur.close()
        con.close()
        self.glossary_window.statistics_button.setText(' ' * 5 + result[0][0] + ' ' * 10 + result[0][1])
        self.glossary_window.show()

    def back_to_main_window2(self):
        self.chart_window.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 620)
        self.main_window.show()

    def back_to_main_window3(self):
        self.glossary_window.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 620)
        self.main_window.show()

    def run_statistics_window(self):
        self.main_window.hide()
        self.setWindowTitle('Statistics')
        self.setGeometry(350, 150, 1000, 580)
        con = sqlite3.connect("Results.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Users
                                    INNER JOIN Results
                                    ON Users.UserId = Results.User""").fetchall()
        cur.close()
        con.close()
        new_result = []
        score = []
        for elem in result:
            elem1 = elem[1:4] + elem[6:]
            elem2 = elem1[4].split('/')
            new_result.append(elem1)
            score.append(elem2)
        self.statistics_window.table.setRowCount(len(new_result))
        for i in range(len(new_result)):
            for j in range(6):
                self.statistics_window.table.setItem(i, j, QTableWidgetItem(str(new_result[i][j])))
                if int(score[i][0]) >= int(score[i][1]) * 0.7:
                    self.statistics_window.table.item(i, j).setBackground(QColor(37, 212, 2))
                else:
                    self.statistics_window.table.item(i, j).setBackground(QColor(181, 0, 0))
        self.statistics_window.show()

    def back_to_main_window4(self):
        self.statistics_window.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 620)
        self.main_window.show()

    def run_select_window1(self):
        self.practice_window.hide()
        self.setWindowTitle('Number of questions')
        self.setGeometry(350, 150, 800, 500)
        self.select_number_of_questions1.show()

    def back_to_practice_window1(self):
        self.select_number_of_questions1.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def run_read_window(self):
        self.select_number_of_questions1.hide()
        self.setWindowTitle('Read')
        self.setGeometry(350, 150, 800, 500)
        self.read_window.show()
        self.el = sample(self.r, 1)
        self.read_window.label1.setText(self.el[0][1])
        self.number1 = self.select_number_of_questions1.sender().text()
        self.read_window.label3.setText(f'QUESTION: {self.question}/{self.number1}')
        self.r.remove(*self.el)

    def check1(self):
        if self.read_window.text_input.text().lower() == self.el[0][0] and self.read_window.label2.text() == '':
            self.score += 1
            self.read_window.label4.setText(f'SCORE: {self.score}')
            self.read_window.znak.setPixmap(self.read_window.pixmap1)
        else:
            self.read_window.znak.setPixmap(self.read_window.pixmap2)
        self.read_window.check_button.setEnabled(False)

    def show1(self):
        self.read_window.label2.setText(self.el[0][0])

    def next1(self):
        self.question += 1
        if self.question == int(self.number1) + 1:
            self.open_game_over_window1()
        self.read_window.check_button.setEnabled(True)
        self.read_window.znak.clear()
        self.read_window.text_input.clear()
        self.read_window.label2.clear()
        self.el = sample(self.r, 1)
        self.read_window.label1.setText(self.el[0][1])
        self.read_window.label3.setText(f'QUESTION: {self.question}/{self.number1}')
        self.r.remove(*self.el)

    def open_game_over_window1(self):
        self.read_window.hide()
        self.setWindowTitle('Game Over')
        self.setGeometry(350, 150, 800, 700)
        self.game_over_window1.label1.setText(f'You have earned {self.score} points.')
        self.game_over_window1.ok_button.setEnabled(True)
        self.game_over_window1.name.setEnabled(True)
        self.game_over_window1.surname.setEnabled(True)
        self.game_over_window1.age.setEnabled(True)
        self.game_over_window1.name.clear()
        self.game_over_window1.surname.clear()
        self.game_over_window1.age.clear()
        self.game_over_window1.show()

    def back_to_practice_from_read_window(self):
        self.question = 1
        self.score = 0
        self.read_window.znak.clear()
        self.read_window.text_input.clear()
        self.read_window.label2.clear()
        self.read_window.label4.setText('SCORE: 0')
        self.read_window.check_button.setEnabled(True)
        self.read_window.hide()
        self.r = self.spisok_slov_i_zvukov[:]
        self.setWindowTitle('Practice')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def back_to_practice_from_game_over_window1(self):
        self.question = 1
        self.score = 0
        self.r = self.spisok_slov_i_zvukov[:]
        self.read_window.label4.setText('SCORE: 0')
        self.game_over_window1.hide()
        self.setWindowTitle('Practice')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def run_select_window2(self):
        self.practice_window.hide()
        self.setWindowTitle('Number of questions')
        self.setGeometry(350, 150, 800, 500)
        self.select_number_of_questions2.show()

    def back_to_practice_window2(self):
        self.select_number_of_questions2.hide()
        self.setWindowTitle('Sounds')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def run_write_window(self):
        self.select_number_of_questions2.hide()
        self.setWindowTitle('Write')
        self.setGeometry(350, 150, 800, 850)
        self.write_window.show()
        self.el = sample(self.r, 1)
        self.write_window.label1.setText(self.el[0][0])
        self.number2 = self.select_number_of_questions2.sender().text()
        self.write_window.label3.setText(f'QUESTION: {self.question}/{self.number2}')
        self.r.remove(*self.el)

    def check2(self):
        if "ˈ" in self.el[0][1]:
            new_el = self.el[0][1].replace("ˈ", "")
        else:
            new_el = self.el[0][1]
        if self.write_window.text_input.text().lower() == new_el and self.write_window.label2.text() == '':
            self.score += 1
            self.write_window.label4.setText(f'SCORE: {self.score}')
            self.write_window.znak.setPixmap(self.write_window.pixmap1)
        else:
            self.write_window.znak.setPixmap(self.write_window.pixmap2)
            self.write_window.check_button.setEnabled(False)

    def show2(self):
        self.write_window.label2.setText(self.el[0][1])

    def next2(self):
        self.question += 1
        if self.question == int(self.number2) + 1:
            self.open_game_over_window2()
        self.write_window.check_button.setEnabled(True)
        self.write_window.znak.clear()
        self.write_window.text_input.clear()
        self.write_window.label2.clear()
        self.el = sample(self.r, 1)
        self.write_window.label1.setText(self.el[0][0])
        self.write_window.label3.setText(f'QUESTION: {self.question}/{self.number2}')
        self.r.remove(*self.el)

    def open_game_over_window2(self):
        self.write_window.hide()
        self.setWindowTitle('Game Over')
        self.setGeometry(350, 150, 800, 700)
        self.game_over_window2.label1.setText(f'You have earned {self.score} points.')
        self.game_over_window2.ok_button.setEnabled(True)
        self.game_over_window2.name.setEnabled(True)
        self.game_over_window2.surname.setEnabled(True)
        self.game_over_window2.age.setEnabled(True)
        self.game_over_window2.name.clear()
        self.game_over_window2.surname.clear()
        self.game_over_window2.age.clear()
        self.game_over_window2.show()

    def back_to_practice_from_write_window(self):
        self.question = 1
        self.score = 0
        self.write_window.znak.clear()
        self.write_window.text_input.clear()
        self.write_window.label2.clear()
        self.write_window.label4.setText('SCORE: 0')
        self.write_window.check_button.setEnabled(True)
        self.write_window.hide()
        self.r = self.spisok_slov_i_zvukov[:]
        self.setWindowTitle('Practice')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()

    def back_to_practice_from_game_over_window2(self):
        self.question = 1
        self.score = 0
        self.r = self.spisok_slov_i_zvukov[:]
        self.write_window.label4.setText('SCORE: 0')
        self.game_over_window2.hide()
        self.setWindowTitle('Practice')
        self.setGeometry(350, 150, 1000, 500)
        self.practice_window.show()


class MainWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label1 = QLabel(self)
        self.label1.setText('Welcome to the Sounds!')
        self.label1.setStyleSheet('color: #FF7A00')
        self.label1.setFont(QFont('Arial', 20))
        self.label1.move(20, 10)

        self.label2 = QLabel(self)
        self.label2.setText('You can improve your phonetic and grammar skills and have a good time here.')
        self.label2.setStyleSheet('color: #FF7A00')
        self.label2.setFont(QFont('Arial', 20))
        self.label2.move(20, 45)

        self.chart_button = QPushButton('CHART', self)
        self.chart_button.setStyleSheet("QPushButton { border: none }"
                                        "QPushButton { text-align: left }"
                                        "QPushButton { color: white }"
                                        "QPushButton:hover { background-color: white } "
                                        "QPushButton:hover {color: black}")
        self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.chart_button.setFont(QFont('Arial', 20))
        self.chart_button.resize(350, 70)
        self.chart_button.move(90, 140)
        self.pixmap1 = QPixmap('images/zvuk.png')
        self.zvuk = QLabel(self)
        self.zvuk.move(25, 148)
        self.zvuk.resize(55, 55)
        self.zvuk.setPixmap(self.pixmap1)

        self.tester_button = QPushButton('PRACTICE TESTER', self)
        self.tester_button.setStyleSheet("QPushButton { border: none }"
                                         "QPushButton { text-align: left }"
                                         "QPushButton { color: white }"
                                         "QPushButton:hover { background-color: white } "
                                         "QPushButton:hover {color: black}")
        self.tester_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.tester_button.setFont(QFont('Arial', 20))
        self.tester_button.resize(350, 71)
        self.tester_button.move(90, 214)
        self.pixmap2 = QPixmap('images/galka.png')
        self.galka = QLabel(self)
        self.galka.move(30, 223)
        self.galka.resize(55, 55)
        self.galka.setPixmap(self.pixmap2)

        self.quiz_tester_button = QPushButton('QUIZ TESTER', self)
        self.quiz_tester_button.setStyleSheet("QPushButton { border: none }"
                                              "QPushButton { text-align: left }"
                                              "QPushButton { color: white }"
                                              "QPushButton:hover { background-color: white } "
                                              "QPushButton:hover {color: black}")
        self.quiz_tester_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.quiz_tester_button.setFont(QFont('Arial', 20))
        self.quiz_tester_button.resize(350, 71)
        self.quiz_tester_button.move(90, 290)
        self.pixmap3 = QPixmap('images/quiz.png')
        self.galka = QLabel(self)
        self.galka.move(15, 296)
        self.galka.resize(65, 59)
        self.galka.setPixmap(self.pixmap3)

        self.glossary_button = QPushButton('GLOSSARY', self)
        self.glossary_button.setStyleSheet("QPushButton { border: none }"
                                           "QPushButton { text-align: left }"
                                           "QPushButton { color: white }"
                                           "QPushButton:hover { background-color: white } "
                                           "QPushButton:hover {color: black}")
        self.glossary_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.glossary_button.setFont(QFont('Arial', 20))
        self.glossary_button.resize(350, 70)
        self.glossary_button.move(90, 365)
        self.pixmap4 = QPixmap('images/glossary.png')
        self.glossary = QLabel(self)
        self.glossary.move(22, 372)
        self.glossary.resize(55, 55)
        self.glossary.setPixmap(self.pixmap4)

        self.statistics_button = QPushButton('STATISTICS', self)
        self.statistics_button.setStyleSheet("QPushButton { border: none }"
                                             "QPushButton { text-align: left }"
                                             "QPushButton { color: white }"
                                             "QPushButton:hover { background-color: white } "
                                             "QPushButton:hover {color: black}")
        self.statistics_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.statistics_button.setFont(QFont('Arial', 20))
        self.statistics_button.resize(350, 70)
        self.statistics_button.move(90, 440)
        self.pixmap5 = QPixmap('images/statistics.png')
        self.statistics = QLabel(self)
        self.statistics.move(26, 447)
        self.statistics.resize(55, 55)
        self.statistics.setPixmap(self.pixmap5)

        self.exit_button = QPushButton('EXIT', self)
        self.exit_button.setStyleSheet("QPushButton { border: none }"
                                       "QPushButton { text-align: left }"
                                       "QPushButton { color: white }"
                                       "QPushButton:hover { background-color: white } "
                                       "QPushButton:hover {color: black}")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.setFont(QFont('Arial', 20))
        self.exit_button.resize(350, 70)
        self.exit_button.move(90, 515)
        self.exit_button.clicked.connect(self.close_window)
        self.pixmap6 = QPixmap('images/exit.png')
        self.exit = QLabel(self)
        self.exit.move(30, 522)
        self.exit.resize(50, 55)
        self.exit.setPixmap(self.pixmap6)
        self.pixmap7 = QPixmap('images/sounds.png')
        self.sounds = QLabel(self)
        self.sounds.move(570, 218)
        self.sounds.resize(400, 272)
        self.sounds.setPixmap(self.pixmap7)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(107, 107, 107), 3)
        qp.setPen(pen1)
        qp.drawLine(50, 211, 500, 211)
        qp.drawLine(50, 287, 500, 287)
        qp.drawLine(50, 362, 500, 362)
        qp.drawLine(50, 437, 500, 437)
        qp.drawLine(50, 512, 500, 512)
        qp.drawLine(50, 587, 500, 587)
        pen2 = QPen(QColor(107, 107, 107), 8)
        qp.setPen(pen2)
        qp.drawLine(0, 90, 10000, 90)

    def close_window(self):
        sys.exit(app.exec())


class GlossaryWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.statistics_button = QPushButton(self)
        self.statistics_button.setStyleSheet("QPushButton { border: none }"
                                             "QPushButton { text-align: left }"
                                             "QPushButton { color: white }"
                                             "QPushButton:hover { background-color: white } "
                                             "QPushButton:hover {color: black}")
        self.statistics_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.statistics_button.setFont(QFont('Arial', 20))
        self.statistics_button.resize(350, 70)
        self.statistics_button.move(90, 440)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)


class PracticeWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.practice_label = QLabel('PRACTICE', self)
        self.practice_label.setFont(QFont('Arial', 25))
        self.practice_label.setStyleSheet('color: white')
        self.practice_label.move(400, 85)

        self.pixmap1 = QPixmap('images/galka2.png')
        self.galka = QLabel(self)
        self.galka.move(310, 75)
        self.galka.resize(70, 56)
        self.galka.setPixmap(self.pixmap1)

        self.read_button = QPushButton('READ', self, )
        self.read_button.setStyleSheet("QPushButton { border: none }"
                                       "QPushButton { text-align: left }"
                                       "QPushButton { color: white }"
                                       "QPushButton:hover { background-color: white } "
                                       "QPushButton:hover {color: black}")
        self.read_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.read_button.setFont(QFont('Arial', 20))
        self.read_button.resize(350, 80)
        self.read_button.move(100, 207)
        self.pixmap2 = QPixmap('images/book.png')
        self.book = QLabel(self)
        self.book.move(20, 221)
        self.book.resize(65, 56)
        self.book.setPixmap(self.pixmap2)

        self.write_button = QPushButton('WRITE', self, )
        self.write_button.setStyleSheet("QPushButton { border: none }"
                                        "QPushButton { text-align: left }"
                                        "QPushButton { color: white }"
                                        "QPushButton:hover { background-color: white } "
                                        "QPushButton:hover {color: black}")
        self.write_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.write_button.setFont(QFont('Arial', 20))
        self.write_button.resize(350, 80)
        self.write_button.move(100, 291)
        self.pixmap3 = QPixmap('images/pero.png')
        self.pero = QLabel(self)
        self.pero.move(40, 293)
        self.pero.resize(36, 74)
        self.pero.setPixmap(self.pixmap3)

        self.listen_button = QPushButton('LISTEN', self, )
        self.listen_button.setStyleSheet("QPushButton { border: none }"
                                         "QPushButton { text-align: left }"
                                         "QPushButton { color: white }"
                                         "QPushButton:hover { background-color: white } "
                                         "QPushButton:hover {color: black}")
        self.listen_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.listen_button.setFont(QFont('Arial', 20))
        self.listen_button.resize(350, 80)
        self.listen_button.move(100, 374)
        self.pixmap4 = QPixmap('images/headphones.png')
        self.headphones = QLabel(self)
        self.headphones.move(25, 385)
        self.headphones.resize(56, 56)
        self.headphones.setPixmap(self.pixmap4)
        self.pixmap5 = QPixmap('images/english.png')
        self.sounds = QLabel(self)
        self.sounds.move(590, 148)
        self.sounds.resize(368, 282)
        self.sounds.setPixmap(self.pixmap5)

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)
        pen2 = QPen(QColor(107, 107, 107), 3)
        qp.setPen(pen2)
        qp.drawLine(50, 288, 530, 288)
        qp.drawLine(50, 372, 530, 372)
        qp.drawLine(50, 456, 530, 456)


class NumberOfQuestionsWidget1(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.label1 = QLabel(self)
        self.label1.setText('Please select number of questions:')
        self.label1.setStyleSheet('color: white')
        self.label1.setFont(QFont('Arial', 25))
        self.label1.move(40, 120)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.select_button1 = QPushButton('10', self)
        self.select_button1.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button1.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button1.setFont(QFont('Arial', 35))
        self.select_button1.move(130, 250)

        self.select_button2 = QPushButton('25', self)
        self.select_button2.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button2.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button2.setFont(QFont('Arial', 35))
        self.select_button2.move(330, 250)

        self.select_button3 = QPushButton('50', self)
        self.select_button3.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button3.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button3.setFont(QFont('Arial', 35))
        self.select_button3.move(530, 250)


class NumberOfQuestionsWidget2(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.label1 = QLabel(self)
        self.label1.setText('Please select number of questions:')
        self.label1.setStyleSheet('color: white')
        self.label1.setFont(QFont('Arial', 25))
        self.label1.move(40, 120)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.select_button1 = QPushButton('10', self)
        self.select_button1.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button1.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button1.setFont(QFont('Arial', 35))
        self.select_button1.move(130, 250)

        self.select_button2 = QPushButton('25', self)
        self.select_button2.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button2.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button2.setFont(QFont('Arial', 35))
        self.select_button2.move(330, 250)

        self.select_button3 = QPushButton('50', self)
        self.select_button3.setStyleSheet("QPushButton { background-color: white } "
                                          "QPushButton { color: black }"
                                          "QPushButton { width: 120px }"
                                          "QPushButton { height: 120px }"
                                          "QPushButton { border-radius: 58px }")
        self.select_button3.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_button3.setFont(QFont('Arial', 35))
        self.select_button3.move(530, 250)


class ChartWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 45)

        self.text_output = QLabel(self)
        self.text_output.setFont(QFont('Arial', 25))
        self.text_output.setStyleSheet("QLabel { color: white }"
                                       "QLabel { background-color: #383838 }")
        self.text_output.setAlignment(Qt.AlignCenter)
        self.text_output.resize(350, 38)
        self.text_output.move(320, 1)

        self.label1 = QLabel(self)
        self.label1.setText('Tap a symbol to hear the sound.')
        self.label1.setFont(QFont('Arial', 25))
        self.label1.setStyleSheet("QLabel { color: white }")
        self.label1.resize(600, 40)
        self.label1.move(30, 720)

        self.label2 = QLabel(self)
        self.label2.setText('Tap and hold to hear the sound and an example word.')
        self.label2.setFont(QFont('Arial', 25))
        self.label2.setStyleSheet("QLabel { color: white }")
        self.label2.resize(800, 40)
        self.label2.move(30, 770)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 8)

        self.pixmap = QPixmap('images/phonemic-chart.png')
        self.phonemic_chart = QLabel(self)
        self.phonemic_chart.move(16, 70)
        self.phonemic_chart.resize(960, 626)
        self.phonemic_chart.setPixmap(self.pixmap)

        self.chart_knopki = ['iː', 'ɪ', 'ʊ', 'uː', 'ɪə', 'eɪ', 'e', 'ə', 'ɜː', 'ɔː', 'ʊə', 'ɔɪ', 'əʊ',
                             'æ', 'ʌ', 'ɑː', 'ɒ', 'eə', 'aɪ', 'aʊ', 'p', 'b', 't', 'd', 'ʧ', 'ʤ', 'k',
                             'g', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'm', 'n', 'ŋ', 'h', 'l', 'r',
                             'w', 'j']

        self.sounds = {'iː': ('audio/ii.mp3', 'audio/steel.mp3', 'steel'), 'ɪ': ('audio/i.mp3', 'audio/risk.mp3', 'risk'),
                       'ʊ': ('audio/u.mp3', 'audio/put.mp3', 'put'), 'uː': ('audio/uu.mp3', 'audio/room.mp3', 'room'),
                       'ɪə': ('audio/ie.mp3', 'audio/near.mp3', 'near'), 'eɪ': ('audio/ei.mp3', 'audio/pay.mp3', 'pay'),
                       'e': ('audio/e.mp3', 'audio/spell.mp3', 'spell'), 'ə': ('audio/ee.mp3', 'audio/again.mp3', 'again'),
                       'ɜː': ('audio/ear.mp3', 'audio/first.mp3', 'first'), 'ɔː': ('audio/oo.mp3', 'audio/stall.mp3', 'stall'),
                       'ʊə': ('audio/ue.mp3', 'audio/pure.mp3', 'pure'), 'ɔɪ': ('audio/oi.mp3', 'audio/noise.mp3', 'noise'),
                       'əʊ': ('audio/ou.mp3', 'audio/snow.mp3', 'snow'), 'æ': ('audio/ae.mp3', 'audio/sand.mp3', 'sand'),
                       'ʌ': ('audio/a.mp3', 'audio/study.mp3', 'study'), 'ɑː': ('audio/aa.mp3', 'audio/spark.mp3', 'spark'),
                       'ɒ': ('audio/o.mp3', 'audio/soft.mp3', 'soft'), 'eə': ('audio/are.mp3', 'audio/where.mp3', 'where'),
                       'aɪ': ('audio/ai.mp3', 'audio/write.mp3', 'write'), 'aʊ': ('audio/au.mp3', 'audio/noun.mp3', 'noun'),
                       'p': ('audio/p.mp3', 'audio/pen.mp3', 'pen'), 'b': ('audio/b.mp3', 'audio/box.mp3', 'box'),
                       't': ('audio/t.mp3', 'audio/time.mp3', 'time'), 'd': ('audio/d.mp3', 'audio/dull.mp3', 'dull'),
                       'ʧ': ('audio/tch.mp3', 'audio/chair.mp3', 'chair'), 'ʤ': ('audio/dz.mp3', 'audio/gym.mp3', 'gym'),
                       'k': ('audio/k.mp3', 'audio/cat.mp3', 'cat'), 'g': ('audio/g.mp3', 'audio/good.mp3', 'good'),
                       'f': ('audio/f.mp3', 'audio/photo.mp3', 'photo'), 'v': ('audio/v.mp3', 'audio/vest.mp3', 'vest'),
                       'θ': ('audio/ff.mp3', 'audio/through.mp3', 'through'), 'ð': ('audio/th.mp3', 'audio/them.mp3', 'them'),
                       's': ('audio/s.mp3', 'audio/start.mp3', 'start'), 'z': ('audio/z.mp3', 'audio/zeal.mp3', 'zeal'),
                       'ʃ': ('audio/sh.mp3', 'audio/shy.mp3', 'shy'), 'ʒ': ('audio/zh.mp3', 'audio/pleasure.mp3', 'pleasure'),
                       'm': ('audio/m.mp3', 'audio/miss.mp3', 'miss'), 'n': ('audio/n.mp3', 'audio/next.mp3', 'next'),
                       'ŋ': ('audio/ng.mp3', 'audio/song.mp3', 'song'), 'h': ('audio/h.mp3', 'audio/his.mp3', 'his'),
                       'l': ('audio/l.mp3', 'audio/less.mp3', 'less'), 'r': ('audio/r.mp3', 'audio/rain.mp3', 'rain'),
                       'w': ('audio/w.mp3', 'audio/wet.mp3', 'wet'), 'j': ('audio/j.mp3', 'audio/yard.mp3', 'yard')}
        self.x = 50
        self.x2 = 515
        for i in range(6):
            if self.chart_knopki[i] != 'ɪə' and self.chart_knopki[i] != 'eɪ':
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #32cacb }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x, 123)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x += 115
            else:
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #333367 }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x2, 123)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x2 += 115
        self.x = 50
        self.x2 = 515
        for i in range(6, 13):
            if self.chart_knopki[i] != 'ʊə' and self.chart_knopki[i] != 'ɔɪ' \
                    and self.chart_knopki[i] != 'əʊ':
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #32cacb }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x, 218)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x += 115
            else:
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #333367 }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x2, 218)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x2 += 115
        self.x = 50
        self.x2 = 515
        for i in range(13, 20):
            if self.chart_knopki[i] != 'eə' and self.chart_knopki[i] != 'aɪ' \
                    and self.chart_knopki[i] != 'aʊ':
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #32cacb }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x, 314)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x += 115
            else:
                self.chart_button = QPushButton(self.chart_knopki[i], self)
                self.chart_button.setStyleSheet("QPushButton { background-color: #333367 }"
                                                "QPushButton { color: white }"
                                                "QPushButton { border-radius: 8px }"
                                                "QPushButton:pressed { background-color: white }"
                                                "QPushButton:pressed { color: black }")
                self.chart_button.setFont(QFont('Arial', 45))
                self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.chart_button.resize(110, 90)
                self.chart_button.move(self.x2, 314)
                self.chart_button.pressed.connect(self.set_voice)
                self.chart_button.clicked.connect(self.delete_text)
                self.x2 += 115
        self.x = 50
        for i in range(20, 28):
            self.chart_button = QPushButton(self.chart_knopki[i], self)
            self.chart_button.setStyleSheet("QPushButton { background-color: #ff6766 }"
                                            "QPushButton { color: white }"
                                            "QPushButton { border-radius: 8px }"
                                            "QPushButton:pressed { background-color: white }"
                                            "QPushButton:pressed { color: black }")
            self.chart_button.setFont(QFont('Arial', 45))
            self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.chart_button.resize(110, 90)
            self.chart_button.move(self.x, 415)
            self.chart_button.pressed.connect(self.set_voice)
            self.chart_button.clicked.connect(self.delete_text)
            self.x += 115
        self.x = 50
        for i in range(28, 36):
            self.chart_button = QPushButton(self.chart_knopki[i], self)
            self.chart_button.setStyleSheet("QPushButton { background-color: #ff6766 }"
                                            "QPushButton { color: white }"
                                            "QPushButton { border-radius: 8px }"
                                            "QPushButton:pressed { background-color: white }"
                                            "QPushButton:pressed { color: black }")
            self.chart_button.setFont(QFont('Arial', 45))
            self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.chart_button.resize(110, 90)
            self.chart_button.move(self.x, 511)
            self.chart_button.pressed.connect(self.set_voice)
            self.chart_button.clicked.connect(self.delete_text)
            self.x += 115
        self.x = 50
        for i in range(36, 44):
            self.chart_button = QPushButton(self.chart_knopki[i], self)
            self.chart_button.setStyleSheet("QPushButton { background-color: #ff6766 }"
                                            "QPushButton { color: white }"
                                            "QPushButton { border-radius: 8px }"
                                            "QPushButton:pressed { background-color: white }"
                                            "QPushButton:pressed { color: black }")
            self.chart_button.setFont(QFont('Arial', 45))
            self.chart_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.chart_button.resize(110, 90)
            self.chart_button.move(self.x, 607)
            self.chart_button.pressed.connect(self.set_voice)
            self.chart_button.clicked.connect(self.delete_text)
            self.x += 115

    def set_voice(self):
        text = self.sender().text()
        self.media_player = QMediaPlayer(self)
        self.url = QUrl.fromLocalFile(self.sounds[text][0])
        self.content = QMediaContent(self.url)
        self.media_player.setMedia(self.content)
        self.media_player.play()
        now = time.time()
        future = now + 1
        while mouse.is_pressed("left"):
            if time.time() > future:
                self.media_player = QMediaPlayer(self)
                self.url = QUrl.fromLocalFile(self.sounds[text][1])
                self.content = QMediaContent(self.url)
                self.media_player.setMedia(self.content)
                self.media_player.play()
                self.text_output.setText(self.sounds[text][2])
                break

    def delete_text(self):
        now = time.time()
        future = now + 1
        while time.time() < future:
            pass
        else:
            self.text_output.clear()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 45, 10000, 45)


class StatisticsWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 }"
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.clean_button = QPushButton('Clear statistics', self)
        self.clean_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                        "QPushButton { background-color: white }")
        self.clean_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clean_button.setFont(QFont('Arial', 12))
        self.clean_button.resize(140, 30)
        self.clean_button.move(840, 500)

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Surname", "Age", "Task", "Result", "Date"])
        self.table.horizontalHeader().setFont(QFont('Arial', 15))
        self.table.setColumnWidth(0, 190)
        self.table.setColumnWidth(1, 210)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 160)
        self.table.setColumnWidth(4, 90)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("QTableWidget { border: none }"
                                 "QTableWidget { background-color: white }")
        self.table.verticalHeader().setStyleSheet('background-color: white')
        self.table.setFont(QFont('Arial', 14))
        self.table.verticalScrollBar().setStyleSheet("QScrollBar { background-color: yellow }"
                                                     "QScrollBar:handle { background-color: #07b9d9 }"
                                                     "QScrollBar:handle { border-radius: 7px }")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.resize(980, 400)
        self.table.move(0, 70)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)


class ReadWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange }"
                                       "QPushButton:hover { color: black }")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.check_button = QPushButton('Check', self)
        self.check_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                        "QPushButton { background-color: white }")
        self.check_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.check_button.setFont(QFont('Arial', 22))
        self.check_button.resize(150, 70)
        self.check_button.move(550, 130)

        self.show_button = QPushButton('Show', self)
        self.show_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                       "QPushButton { background-color: white }")
        self.show_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.show_button.setFont(QFont('Arial', 22))
        self.show_button.resize(290, 70)
        self.show_button.move(30, 285)

        self.next_button = QPushButton('Next', self)
        self.next_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                       "QPushButton { background-color: white }")
        self.next_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.next_button.setFont(QFont('Arial', 22))
        self.next_button.resize(290, 70)
        self.next_button.move(410, 285)

        self.text_input = QLineEdit(self)
        self.text_input.resize(380, 70)
        self.text_input.move(30, 130)
        self.text_input.setFont(QFont('Arial', 30))
        self.text_input.setStyleSheet("QLineEdit { color: white }"
                                      "QLineEdit { background-color: #121212 }"
                                      "QLineEdit { border-radius: 10px }"
                                      "QLineEdit { border:2px solid #757575 }")

        self.label1 = QLabel(self)
        self.label1.setFont(QFont('Arial', 25))
        self.label1.setStyleSheet('color: white')
        self.label1.resize(400, 40)
        self.label1.move(35, 75)

        self.label2 = QLabel(self)
        self.label2.setFont(QFont('Arial', 25))
        self.label2.setStyleSheet('color: #fc6214')
        self.label2.resize(400, 40)
        self.label2.move(35, 215)

        self.label3 = QLabel('QUESTION:', self)
        self.label3.setFont(QFont('Arial', 12))
        self.label3.setStyleSheet("QLabel { color: white }"
                                  "QLabel { background-color: #383838 }")
        self.label3.resize(160, 20)
        self.label3.move(355, 11)

        self.label4 = QLabel('SCORE: 0', self)
        self.label4.setFont(QFont('Arial', 12))
        self.label4.setStyleSheet("QLabel { color: white }"
                                  "QLabel { background-color: #383838 }")
        self.label4.resize(100, 20)
        self.label4.move(585, 11)

        self.pixmap1 = QPixmap('images/green-galka.png')
        self.pixmap2 = QPixmap('images/red-krestik.png')
        self.znak = QLabel(self)
        self.znak.move(490, 147)
        self.znak.resize(40, 37)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)


class WriteWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange }"
                                       "QPushButton:hover { color: black }")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.check_button = QPushButton('Check', self)
        self.check_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                        "QPushButton { background-color: white }")
        self.check_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.check_button.setFont(QFont('Arial', 22))
        self.check_button.resize(150, 70)
        self.check_button.move(550, 130)

        self.show_button = QPushButton('Show', self)
        self.show_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                       "QPushButton { background-color: white }")
        self.show_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.show_button.setFont(QFont('Arial', 22))
        self.show_button.resize(290, 70)
        self.show_button.move(30, 285)

        self.next_button = QPushButton('Next', self)
        self.next_button.setStyleSheet("QPushButton { border-radius: 5px }"
                                       "QPushButton { background-color: white }")
        self.next_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.next_button.setFont(QFont('Arial', 22))
        self.next_button.resize(290, 70)
        self.next_button.move(410, 285)

        self.delete_button = QPushButton(self)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_button.setStyleSheet("QPushButton { border: none }")
        self.delete_button.setIcon(QIcon('images/delete-button.png'))
        self.delete_button.setIconSize(QSize(120, 60))
        self.delete_button.resize(100, 60)
        self.delete_button.move(530, 430)
        self.delete_button.clicked.connect(self.delete_text)

        self.text_input = QLineEdit(self)
        self.text_input.resize(380, 70)
        self.text_input.move(30, 130)
        self.text_input.setFont(QFont('Arial', 30))
        self.text_input.setStyleSheet("QLineEdit { color: white }"
                                      "QLineEdit { background-color: #121212 }"
                                      "QLineEdit { border-radius: 10px }"
                                      "QLineEdit { border:2px solid #757575 }")

        self.label1 = QLabel(self)
        self.label1.setFont(QFont('Arial', 25))
        self.label1.setStyleSheet('color: white')
        self.label1.resize(400, 40)
        self.label1.move(35, 75)

        self.label2 = QLabel(self)
        self.label2.setFont(QFont('Arial', 25))
        self.label2.setStyleSheet('color: #fc6214')
        self.label2.resize(400, 40)
        self.label2.move(35, 215)

        self.label3 = QLabel('QUESTION:', self)
        self.label3.setFont(QFont('Arial', 12))
        self.label3.setStyleSheet("QLabel { color: white }"
                                  "QLabel { background-color: #383838 }")
        self.label3.resize(160, 20)
        self.label3.move(355, 11)

        self.label4 = QLabel('SCORE:', self)
        self.label4.setFont(QFont('Arial', 12))
        self.label4.setStyleSheet("QLabel { color: white }"
                                  "QLabel { background-color: #383838 }")
        self.label4.resize(100, 20)
        self.label4.move(585, 11)

        self.pixmap1 = QPixmap('images/green-galka.png')
        self.pixmap2 = QPixmap('images/red-krestik.png')
        self.znak = QLabel(self)
        self.znak.move(490, 147)
        self.znak.resize(40, 37)

        self.keyboard_knopki = ['iː', 'ɪ', 'ʊ', 'uː', 'ɪə', 'eɪ', 'e', 'ə', 'ɜː', 'ɔː', 'ʊə', 'ɔɪ', 'əʊ',
                                'æ', 'ʌ', 'ɑː', 'ɒ', 'eə', 'aɪ', 'aʊ', 'p', 'b', 't', 'd', 'ʧ', 'ʤ', 'k',
                                'g', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'm', 'n', 'ŋ', 'h', 'l', 'r',
                                'w', 'j']

        self.sounds = {'iː': 'audio/ii.mp3', 'ɪ': 'audio/i.mp3', 'ʊ': 'audio/u.mp3', 'uː': 'audio/uu.mp3',
                       'ɪə': 'audio/ie.mp3', 'eɪ': 'audio/ei.mp3', 'e': 'audio/e.mp3', 'ə': 'audio/ee.mp3',
                       'ɜː': 'audio/ear.mp3', 'ɔː': 'audio/oo.mp3', 'ʊə': 'audio/ue.mp3', 'ɔɪ': 'audio/oi.mp3',
                       'əʊ': 'audio/ou.mp3', 'æ': 'audio/ae.mp3', 'ʌ': 'audio/a.mp3', 'ɑː': 'audio/aa.mp3',
                       'ɒ': 'audio/o.mp3', 'eə': 'audio/are.mp3', 'aɪ': 'audio/ai.mp3', 'aʊ': 'audio/au.mp3',
                       'p': 'audio/p.mp3', 'b': 'audio/b.mp3', 't': 'audio/t.mp3', 'd': 'audio/d.mp3',
                       'ʧ': 'audio/tch.mp3', 'ʤ': 'audio/dz.mp3', 'k': 'audio/k.mp3', 'g': 'audio/g.mp3',
                       'f': 'audio/f.mp3', 'v': 'audio/v.mp3', 'θ': 'audio/ff.mp3', 'ð': 'audio/th.mp3',
                       's': 'audio/s.mp3', 'z': 'audio/z.mp3', 'ʃ': 'audio/sh.mp3', 'ʒ': 'audio/zh.mp3',
                       'm': 'audio/m.mp3', 'n': 'audio/n.mp3', 'ŋ': 'audio/ng.mp3', 'h': 'audio/h.mp3',
                       'l': 'audio/l.mp3', 'r': 'audio/r.mp3', 'w': 'audio/w.mp3', 'j': 'audio/j.mp3'}
        self.x = 140
        for i in range(6):
            if self.keyboard_knopki[i] != 'ɪə' and self.keyboard_knopki[i] != 'eɪ':
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #eeff00 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 430)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
            else:
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #ff8800 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 430)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
        self.x = 140
        for i in range(6, 13):
            if self.keyboard_knopki[i] != 'ʊə' and self.keyboard_knopki[i] != 'ɔɪ' \
                    and self.keyboard_knopki[i] != 'əʊ':
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #eeff00 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 493)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
            else:
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #ff8800 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 493)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
        self.x = 140
        for i in range(13, 20):
            if self.keyboard_knopki[i] != 'eə' and self.keyboard_knopki[i] != 'aɪ' \
                    and self.keyboard_knopki[i] != 'aʊ':
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #eeff00 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 556)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
            else:
                self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
                self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                                   "QPushButton { color: black }"
                                                   "QPushButton { border-radius: 8px }"
                                                   "QPushButton { border:3px solid #ff8800 }")
                self.keyboard_button.setFont(QFont('Arial', 25))
                self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
                self.keyboard_button.resize(60, 60)
                self.keyboard_button.move(self.x, 556)
                self.keyboard_button.clicked.connect(self.set_text)
                self.x += 63
        self.x = 140
        for i in range(20, 28):
            self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
            self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                               "QPushButton { color: black }"
                                               "QPushButton { border-radius: 8px }"
                                               "QPushButton { border:3px solid #f007f0 }")
            self.keyboard_button.setFont(QFont('Arial', 25))
            self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.keyboard_button.resize(60, 60)
            self.keyboard_button.move(self.x, 619)
            self.keyboard_button.clicked.connect(self.set_text)
            self.x += 63
        self.x = 140
        for i in range(28, 36):
            self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
            self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                               "QPushButton { color: black }"
                                               "QPushButton { border-radius: 8px }"
                                               "QPushButton { border:3px solid #f007f0 }")
            self.keyboard_button.setFont(QFont('Arial', 25))
            self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.keyboard_button.resize(60, 60)
            self.keyboard_button.move(self.x, 682)
            self.keyboard_button.clicked.connect(self.set_text)
            self.x += 63
        self.x = 140
        for i in range(36, 44):
            self.keyboard_button = QPushButton(self.keyboard_knopki[i], self)
            self.keyboard_button.setStyleSheet("QPushButton { background-color: white }"
                                               "QPushButton { color: black }"
                                               "QPushButton { border-radius: 8px }"
                                               "QPushButton { border:3px solid #f007f0 }")
            self.keyboard_button.setFont(QFont('Arial', 25))
            self.keyboard_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.keyboard_button.resize(60, 60)
            self.keyboard_button.move(self.x, 745)
            self.keyboard_button.clicked.connect(self.set_text)
            self.x += 63

    def set_text(self):
        text = self.sender().text()
        text1 = self.text_input.text()
        self.text_input.setText(f'{text1}{text}')
        self.media_player = QMediaPlayer(self)
        self.url = QUrl.fromLocalFile(self.sounds[text])
        self.content = QMediaContent(self.url)
        self.media_player.setMedia(self.content)
        self.media_player.play()

    def delete_text(self):
        text = self.text_input.text()
        symbols = 'iː uː ɜː ɔː ɑː ɪə eɪ ʊə ɔɪ əʊ eə aɪ aʊ ʧ ʤ'
        if len(text) > 1:
            new_text = text[-2:]
            if new_text in symbols:
                self.text_input.setText(text[:-2])
            else:
                self.text_input.setText(text[:-1])
        else:
            self.text_input.clear()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)


class GameOverWindowWidget1(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.label1 = QLabel(self)
        self.label1.setStyleSheet('color: white')
        self.label1.setFont(QFont('Arial', 20))
        self.label1.move(40, 60)

        self.label2 = QLabel('You can record your personal data for further statistics:', self)
        self.label2.setStyleSheet('color: white')
        self.label2.setFont(QFont('Arial', 20))
        self.label2.move(40, 110)

        self.label3 = QLabel('Name', self)
        self.label3.setStyleSheet('color: white')
        self.label3.setFont(QFont('Arial', 18))
        self.label3.move(90, 175)

        self.label4 = QLabel('Surname', self)
        self.label4.setStyleSheet('color: white')
        self.label4.setFont(QFont('Arial', 18))
        self.label4.move(55, 225)

        self.label5 = QLabel('Age', self)
        self.label5.setStyleSheet('color: white')
        self.label5.setFont(QFont('Arial', 18))
        self.label5.move(110, 275)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                     "QPushButton { background-color: white }")
        self.ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ok_button.setFont(QFont('Arial', 12))
        self.ok_button.resize(35, 35)
        self.ok_button.move(455, 274)

        self.name = QLineEdit(self)
        self.name.setStyleSheet("QLineEdit { color: white }"
                                "QLineEdit { background-color: #121212 }"
                                "QLineEdit { border-radius: 10px }"
                                "QLineEdit { border:2px solid #757575 }")
        self.name.setFont(QFont('Arial', 16))
        self.name.resize(240, 40)
        self.name.move(170, 170)

        self.surname = QLineEdit(self)
        self.surname.setStyleSheet("QLineEdit { color: white }"
                                   "QLineEdit { background-color: #121212 }"
                                   "QLineEdit { border-radius: 10px }"
                                   "QLineEdit { border:2px solid #757575 }")
        self.surname.setFont(QFont('Arial', 16))
        self.surname.resize(240, 40)
        self.surname.move(170, 220)

        self.age = QLineEdit(self)
        self.age.setStyleSheet("QLineEdit { color: white }"
                               "QLineEdit { background-color: #121212 }"
                               "QLineEdit { border-radius: 10px }"
                               "QLineEdit { border:2px solid #757575 }")
        self.age.setFont(QFont('Arial', 16))
        self.age.resize(240, 40)
        self.age.move(170, 270)

        self.pixmap = QPixmap('images/game-over.png')
        self.game_over = QLabel(self)
        self.game_over.move(50, 330)
        self.game_over.resize(930, 380)
        self.game_over.setPixmap(self.pixmap)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)


class GameOverWindowWidget2(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QFrame(self)
        self.line.setStyleSheet("background-color: #383838")
        self.line.resize(10000, 40)

        self.label1 = QLabel(self)
        self.label1.setStyleSheet('color: white')
        self.label1.setFont(QFont('Arial', 20))
        self.label1.move(40, 60)

        self.label2 = QLabel('You can record your personal data for further statistics:', self)
        self.label2.setStyleSheet('color: white')
        self.label2.setFont(QFont('Arial', 20))
        self.label2.move(40, 110)

        self.label3 = QLabel('Name', self)
        self.label3.setStyleSheet('color: white')
        self.label3.setFont(QFont('Arial', 18))
        self.label3.move(90, 175)

        self.label4 = QLabel('Surname', self)
        self.label4.setStyleSheet('color: white')
        self.label4.setFont(QFont('Arial', 18))
        self.label4.move(55, 225)

        self.label5 = QLabel('Age', self)
        self.label5.setStyleSheet('color: white')
        self.label5.setFont(QFont('Arial', 18))
        self.label5.move(110, 275)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                       "QPushButton { background-color: #505153 } "
                                       "QPushButton { color: white }"
                                       "QPushButton { border: 1px solid #000000 }"
                                       "QPushButton:hover { background-color: orange } "
                                       "QPushButton:hover { color: black } ")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setFont(QFont('Arial', 12))
        self.back_button.resize(70, 30)
        self.back_button.move(30, 5)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.setStyleSheet("QPushButton { border-radius: 4px }"
                                     "QPushButton { background-color: white }")
        self.ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ok_button.setFont(QFont('Arial', 12))
        self.ok_button.resize(35, 35)
        self.ok_button.move(455, 274)

        self.name = QLineEdit(self)
        self.name.setStyleSheet("QLineEdit { color: white }"
                                "QLineEdit { background-color: #121212 }"
                                "QLineEdit { border-radius: 10px }"
                                "QLineEdit { border:2px solid #757575 }")
        self.name.setFont(QFont('Arial', 16))
        self.name.resize(240, 40)
        self.name.move(170, 170)

        self.surname = QLineEdit(self)
        self.surname.setStyleSheet("QLineEdit { color: white }"
                                   "QLineEdit { background-color: #121212 }"
                                   "QLineEdit { border-radius: 10px }"
                                   "QLineEdit { border:2px solid #757575 }")
        self.surname.setFont(QFont('Arial', 16))
        self.surname.resize(240, 40)
        self.surname.move(170, 220)

        self.age = QLineEdit(self)
        self.age.setStyleSheet("QLineEdit { color: white }"
                               "QLineEdit { background-color: #121212 }"
                               "QLineEdit { border-radius: 10px }"
                               "QLineEdit { border:2px solid #757575 }")
        self.age.setFont(QFont('Arial', 16))
        self.age.resize(240, 40)
        self.age.move(170, 270)

        self.pixmap = QPixmap('images/game-over.png')
        self.game_over = QLabel(self)
        self.game_over.move(50, 330)
        self.game_over.resize(930, 380)
        self.game_over.setPixmap(self.pixmap)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        pen1 = QPen(QColor(186, 186, 186), 2)
        qp.setPen(pen1)
        qp.drawLine(0, 40, 10000, 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.exit(app.exec())
