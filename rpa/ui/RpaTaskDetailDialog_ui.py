# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaTaskDetailDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateTimeEdit,
    QDialog, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPlainTextEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QTimeEdit, QWidget)

class Ui_RpaTaskDetailDialog(object):
    def setupUi(self, RpaTaskDetailDialog):
        if not RpaTaskDetailDialog.objectName():
            RpaTaskDetailDialog.setObjectName(u"RpaTaskDetailDialog")
        RpaTaskDetailDialog.resize(1082, 856)
        self.gridLayout_2 = QGridLayout(RpaTaskDetailDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(RpaTaskDetailDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -326, 1045, 1284))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_email_title_default = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_email_title_default.setObjectName(u"pushButton_email_title_default")

        self.gridLayout.addWidget(self.pushButton_email_title_default, 9, 2, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 8, 1, 1, 1)

        self.label_email_body = QLabel(self.scrollAreaWidgetContents)
        self.label_email_body.setObjectName(u"label_email_body")

        self.gridLayout.addWidget(self.label_email_body, 23, 0, 1, 1)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_11 = QGridLayout(self.frame_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_14 = QLabel(self.frame_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_11.addWidget(self.label_14, 1, 0, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout_11.addWidget(self.label, 5, 1, 1, 3)

        self.scrollArea_2 = QScrollArea(self.frame_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setMinimumSize(QSize(0, 120))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 707, 118))
        self.gridLayout_12 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.gridLayout_event_type = QGridLayout()
        self.gridLayout_event_type.setObjectName(u"gridLayout_event_type")
        self.checkBox_4 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_event_type.addWidget(self.checkBox_4, 0, 2, 1, 1)

        self.checkBox_5 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout_event_type.addWidget(self.checkBox_5, 0, 0, 1, 1)

        self.checkBox_8 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.gridLayout_event_type.addWidget(self.checkBox_8, 1, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_event_type.addWidget(self.checkBox_3, 0, 3, 1, 1)

        self.checkBox_2 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_event_type.addWidget(self.checkBox_2, 0, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_event_type, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_11.addWidget(self.scrollArea_2, 15, 1, 2, 3)

        self.dateTimeEdit_from = QDateTimeEdit(self.frame_2)
        self.dateTimeEdit_from.setObjectName(u"dateTimeEdit_from")
        self.dateTimeEdit_from.setEnabled(False)
        self.dateTimeEdit_from.setCalendarPopup(True)

        self.gridLayout_11.addWidget(self.dateTimeEdit_from, 3, 2, 1, 1)

        self.label_end = QLabel(self.frame_2)
        self.label_end.setObjectName(u"label_end")

        self.gridLayout_11.addWidget(self.label_end, 4, 1, 1, 1)

        self.label_type = QLabel(self.frame_2)
        self.label_type.setObjectName(u"label_type")

        self.gridLayout_11.addWidget(self.label_type, 12, 0, 1, 1)

        self.label_start = QLabel(self.frame_2)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_11.addWidget(self.label_start, 3, 1, 1, 1)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_11.addWidget(self.label_15, 15, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_2, 16, 0, 1, 1)

        self.dateTimeEdit_to = QDateTimeEdit(self.frame_2)
        self.dateTimeEdit_to.setObjectName(u"dateTimeEdit_to")
        self.dateTimeEdit_to.setEnabled(False)
        self.dateTimeEdit_to.setCalendarPopup(True)

        self.gridLayout_11.addWidget(self.dateTimeEdit_to, 4, 2, 1, 1)

        self.line_5 = QFrame(self.frame_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_11.addWidget(self.line_5, 7, 0, 1, 4)

        self.line_6 = QFrame(self.frame_2)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_11.addWidget(self.line_6, 14, 0, 1, 4)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_9 = QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_7, 3, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.gridLayout_13.addLayout(self.horizontalLayout_5, 3, 2, 1, 2)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_8, 3, 0, 1, 1)

        self.radioButton_report_duration_days_30 = QRadioButton(self.groupBox_2)
        self.radioButton_report_duration_days_30.setObjectName(u"radioButton_report_duration_days_30")
        self.radioButton_report_duration_days_30.setChecked(True)

        self.gridLayout_13.addWidget(self.radioButton_report_duration_days_30, 0, 0, 1, 1)

        self.radioButton_report_duration_days_7 = QRadioButton(self.groupBox_2)
        self.radioButton_report_duration_days_7.setObjectName(u"radioButton_report_duration_days_7")
        self.radioButton_report_duration_days_7.setChecked(False)

        self.gridLayout_13.addWidget(self.radioButton_report_duration_days_7, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_report_duration_days = QRadioButton(self.groupBox_2)
        self.radioButton_report_duration_days.setObjectName(u"radioButton_report_duration_days")

        self.horizontalLayout_2.addWidget(self.radioButton_report_duration_days)

        self.lineEdit_report_duration_days = QLineEdit(self.groupBox_2)
        self.lineEdit_report_duration_days.setObjectName(u"lineEdit_report_duration_days")
        self.lineEdit_report_duration_days.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_2.addWidget(self.lineEdit_report_duration_days)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_2.addWidget(self.label_13)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_9)


        self.gridLayout_13.addLayout(self.horizontalLayout_2, 0, 2, 1, 2)


        self.gridLayout_9.addLayout(self.gridLayout_13, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_2, 1, 1, 2, 2)

        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_8 = QGridLayout(self.groupBox)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.checkBox_report_severity_danger_low = QCheckBox(self.groupBox)
        self.checkBox_report_severity_danger_low.setObjectName(u"checkBox_report_severity_danger_low")
        self.checkBox_report_severity_danger_low.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_danger_low, 3, 0, 1, 1)

        self.checkBox_report_severity_danger_lowlow = QCheckBox(self.groupBox)
        self.checkBox_report_severity_danger_lowlow.setObjectName(u"checkBox_report_severity_danger_lowlow")
        self.checkBox_report_severity_danger_lowlow.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_danger_lowlow, 4, 0, 1, 1)

        self.checkBox_report_severity_danger_high = QCheckBox(self.groupBox)
        self.checkBox_report_severity_danger_high.setObjectName(u"checkBox_report_severity_danger_high")
        self.checkBox_report_severity_danger_high.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_danger_high, 1, 0, 1, 1)

        self.checkBox_report_severity_danger_highhigh = QCheckBox(self.groupBox)
        self.checkBox_report_severity_danger_highhigh.setObjectName(u"checkBox_report_severity_danger_highhigh")
        self.checkBox_report_severity_danger_highhigh.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_danger_highhigh, 0, 0, 1, 1)

        self.checkBox_report_severity_danger_mid = QCheckBox(self.groupBox)
        self.checkBox_report_severity_danger_mid.setObjectName(u"checkBox_report_severity_danger_mid")
        self.checkBox_report_severity_danger_mid.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_danger_mid, 2, 0, 1, 1)

        self.checkBox_report_severity_good_mid = QCheckBox(self.groupBox)
        self.checkBox_report_severity_good_mid.setObjectName(u"checkBox_report_severity_good_mid")
        self.checkBox_report_severity_good_mid.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_good_mid, 2, 1, 1, 1)

        self.checkBox_report_severity_good_highhigh = QCheckBox(self.groupBox)
        self.checkBox_report_severity_good_highhigh.setObjectName(u"checkBox_report_severity_good_highhigh")
        self.checkBox_report_severity_good_highhigh.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_good_highhigh, 0, 1, 1, 1)

        self.checkBox_report_severity_good_high = QCheckBox(self.groupBox)
        self.checkBox_report_severity_good_high.setObjectName(u"checkBox_report_severity_good_high")
        self.checkBox_report_severity_good_high.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_report_severity_good_high, 1, 1, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox, 12, 1, 2, 2)

        self.horizontalSpacer_6 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_6, 3, 3, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 11, 1, 1, 1)

        self.pushButton_email_addressbook = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_email_addressbook.setObjectName(u"pushButton_email_addressbook")

        self.gridLayout.addWidget(self.pushButton_email_addressbook, 7, 2, 1, 1)

        self.pushButton_report_search = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_report_search.setObjectName(u"pushButton_report_search")
        self.pushButton_report_search.setMinimumSize(QSize(0, 80))

        self.gridLayout.addWidget(self.pushButton_report_search, 11, 2, 1, 1)

        self.plainTextEdit_email_body = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit_email_body.setObjectName(u"plainTextEdit_email_body")
        self.plainTextEdit_email_body.setMinimumSize(QSize(0, 150))

        self.gridLayout.addWidget(self.plainTextEdit_email_body, 23, 1, 1, 1)

        self.tableWidget_report = QTableWidget(self.scrollAreaWidgetContents)
        if (self.tableWidget_report.columnCount() < 9):
            self.tableWidget_report.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_report.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.tableWidget_report.rowCount() < 2):
            self.tableWidget_report.setRowCount(2)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 5, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 6, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 7, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_report.setItem(0, 8, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 4, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 5, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 6, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 7, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_report.setItem(1, 8, __qtablewidgetitem24)
        self.tableWidget_report.setObjectName(u"tableWidget_report")
        self.tableWidget_report.setMinimumSize(QSize(0, 200))
        self.tableWidget_report.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_report.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.gridLayout.addWidget(self.tableWidget_report, 12, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 13, 1, 1, 1)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 20))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 10, 0, 1, 3)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)

        self.lineEdit_email_title = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_email_title.setObjectName(u"lineEdit_email_title")

        self.gridLayout.addWidget(self.lineEdit_email_title, 9, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 27, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 27, 1, 1, 1)

        self.listWidget_email_attach = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_email_attach.setObjectName(u"listWidget_email_attach")
        self.listWidget_email_attach.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.listWidget_email_attach, 24, 1, 1, 1)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 0))
        self.label_10.setSizeIncrement(QSize(0, 0))

        self.gridLayout_6.addWidget(self.label_10, 1, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBox_tue = QCheckBox(self.frame_3)
        self.checkBox_tue.setObjectName(u"checkBox_tue")

        self.gridLayout_4.addWidget(self.checkBox_tue, 0, 2, 1, 1)

        self.checkBox_sat = QCheckBox(self.frame_3)
        self.checkBox_sat.setObjectName(u"checkBox_sat")

        self.gridLayout_4.addWidget(self.checkBox_sat, 0, 6, 1, 1)

        self.checkBox_mon = QCheckBox(self.frame_3)
        self.checkBox_mon.setObjectName(u"checkBox_mon")
        self.checkBox_mon.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_mon, 0, 1, 1, 1)

        self.checkBox_thu = QCheckBox(self.frame_3)
        self.checkBox_thu.setObjectName(u"checkBox_thu")

        self.gridLayout_4.addWidget(self.checkBox_thu, 0, 4, 1, 1)

        self.checkBox_sun = QCheckBox(self.frame_3)
        self.checkBox_sun.setObjectName(u"checkBox_sun")

        self.gridLayout_4.addWidget(self.checkBox_sun, 0, 7, 1, 1)

        self.checkBox_fri = QCheckBox(self.frame_3)
        self.checkBox_fri.setObjectName(u"checkBox_fri")

        self.gridLayout_4.addWidget(self.checkBox_fri, 0, 5, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 8, 1, 1)

        self.checkBox_wed = QCheckBox(self.frame_3)
        self.checkBox_wed.setObjectName(u"checkBox_wed")

        self.gridLayout_4.addWidget(self.checkBox_wed, 0, 3, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_4, 1, 2, 1, 1)

        self.timeEdit_sendtime = QTimeEdit(self.frame_3)
        self.timeEdit_sendtime.setObjectName(u"timeEdit_sendtime")
        self.timeEdit_sendtime.setMinimumSize(QSize(200, 0))
        self.timeEdit_sendtime.setMaximumSize(QSize(200, 16777215))
        self.timeEdit_sendtime.setMinimumTime(QTime(2, 0, 0))
        self.timeEdit_sendtime.setCurrentSection(QDateTimeEdit.Section.AmPmSection)
        self.timeEdit_sendtime.setTime(QTime(9, 0, 0))

        self.gridLayout_6.addWidget(self.timeEdit_sendtime, 2, 2, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 2, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 5, 1, 1, 1)

        self.lineEdit_email_to = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_email_to.setObjectName(u"lineEdit_email_to")

        self.gridLayout.addWidget(self.lineEdit_email_to, 7, 1, 1, 1)

        self.lineEdit_task_name = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_task_name.setObjectName(u"lineEdit_task_name")

        self.gridLayout.addWidget(self.lineEdit_task_name, 2, 1, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 11, 0, 1, 1)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(0, 20))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 16, 0, 1, 3)

        self.label_email_title = QLabel(self.scrollAreaWidgetContents)
        self.label_email_title.setObjectName(u"label_email_title")

        self.gridLayout.addWidget(self.label_email_title, 9, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 27, 0, 1, 1)

        self.label_email_to = QLabel(self.scrollAreaWidgetContents)
        self.label_email_to.setObjectName(u"label_email_to")

        self.gridLayout.addWidget(self.label_email_to, 7, 0, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)

        self.lineEdit_id = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_id.setObjectName(u"lineEdit_id")
        self.lineEdit_id.setEnabled(False)
        self.lineEdit_id.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_id, 1, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 24, 0, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.pushButton_email_attach = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_email_attach.setObjectName(u"pushButton_email_attach")

        self.gridLayout.addWidget(self.pushButton_email_attach, 24, 2, 1, 1)

        self.pushButton_email_body_default = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_email_body_default.setObjectName(u"pushButton_email_body_default")

        self.gridLayout.addWidget(self.pushButton_email_body_default, 23, 2, 1, 1)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 6, 0, 1, 3)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 2)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pushButton_accept = QPushButton(RpaTaskDetailDialog)
        self.pushButton_accept.setObjectName(u"pushButton_accept")

        self.gridLayout_5.addWidget(self.pushButton_accept, 0, 4, 1, 1)

        self.pushButton_insert = QPushButton(RpaTaskDetailDialog)
        self.pushButton_insert.setObjectName(u"pushButton_insert")

        self.gridLayout_5.addWidget(self.pushButton_insert, 0, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_10, 0, 2, 1, 1)

        self.pushButton_delete = QPushButton(RpaTaskDetailDialog)
        self.pushButton_delete.setObjectName(u"pushButton_delete")

        self.gridLayout_5.addWidget(self.pushButton_delete, 0, 1, 1, 1)

        self.pushButton_close = QPushButton(RpaTaskDetailDialog)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.gridLayout_5.addWidget(self.pushButton_close, 0, 3, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_5, 2, 1, 1, 1)

        self.label_dialog_title = QLabel(RpaTaskDetailDialog)
        self.label_dialog_title.setObjectName(u"label_dialog_title")

        self.gridLayout_2.addWidget(self.label_dialog_title, 0, 0, 1, 2)

        QWidget.setTabOrder(self.lineEdit_id, self.lineEdit_task_name)
        QWidget.setTabOrder(self.lineEdit_task_name, self.checkBox_mon)
        QWidget.setTabOrder(self.checkBox_mon, self.checkBox_tue)
        QWidget.setTabOrder(self.checkBox_tue, self.checkBox_wed)
        QWidget.setTabOrder(self.checkBox_wed, self.checkBox_thu)
        QWidget.setTabOrder(self.checkBox_thu, self.checkBox_fri)
        QWidget.setTabOrder(self.checkBox_fri, self.checkBox_sat)
        QWidget.setTabOrder(self.checkBox_sat, self.checkBox_sun)
        QWidget.setTabOrder(self.checkBox_sun, self.timeEdit_sendtime)
        QWidget.setTabOrder(self.timeEdit_sendtime, self.radioButton_report_duration_days_30)
        QWidget.setTabOrder(self.radioButton_report_duration_days_30, self.radioButton_report_duration_days_7)
        QWidget.setTabOrder(self.radioButton_report_duration_days_7, self.radioButton_report_duration_days)
        QWidget.setTabOrder(self.radioButton_report_duration_days, self.dateTimeEdit_from)
        QWidget.setTabOrder(self.dateTimeEdit_from, self.dateTimeEdit_to)
        QWidget.setTabOrder(self.dateTimeEdit_to, self.checkBox_5)
        QWidget.setTabOrder(self.checkBox_5, self.checkBox_2)
        QWidget.setTabOrder(self.checkBox_2, self.checkBox_4)
        QWidget.setTabOrder(self.checkBox_4, self.checkBox_3)
        QWidget.setTabOrder(self.checkBox_3, self.checkBox_8)
        QWidget.setTabOrder(self.checkBox_8, self.scrollArea_2)
        QWidget.setTabOrder(self.scrollArea_2, self.tableWidget_report)
        QWidget.setTabOrder(self.tableWidget_report, self.listWidget_email_attach)
        QWidget.setTabOrder(self.listWidget_email_attach, self.pushButton_report_search)
        QWidget.setTabOrder(self.pushButton_report_search, self.pushButton_email_attach)
        QWidget.setTabOrder(self.pushButton_email_attach, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.pushButton_insert)
        QWidget.setTabOrder(self.pushButton_insert, self.plainTextEdit_email_body)

        self.retranslateUi(RpaTaskDetailDialog)

        QMetaObject.connectSlotsByName(RpaTaskDetailDialog)
    # setupUi

    def retranslateUi(self, RpaTaskDetailDialog):
        RpaTaskDetailDialog.setWindowTitle(QCoreApplication.translate("RpaTaskDetailDialog", u"RPA \uc5c5\ubb34\uc0c1\uc138", None))
        self.pushButton_email_title_default.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uae30\ubcf8\uac12", None))
        self.label_2.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc5ec\ub7ec\uba85\uc758 \uc218\uc2e0\uc790\ub294 ; \uae30\ud638\ub85c \uad6c\ubd84\uc785\ub825 \ud569\ub2c8\ub2e4. (\uc608\uc2dc: example1@mail.com;example2@mail.com)", None))
        self.label_email_body.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc774\uba54\uc77c \ub0b4\uc6a9", None))
        self.label_14.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubc1c\uc0dd\uc77c\uc2dc(\uae30\uac04)", None))
        self.label.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"( \ub4f1\ub85d\ud55c RPA\uc5c5\ubb34\uac00 \uc2e4\ud589 \ub420 \ub54c\ub294 \uc2e4\uc81c \uc5c5\ubb34\uc2e4\ud589 \uc2dc\uac01\uc744 \uae30\uc900\uc73c\ub85c \ubcf4\uace0\uc11c \uac80\uc0c9\uc744 \uc218\ud589\ud569\ub2c8\ub2e4.)", None))
        self.checkBox_4.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"CheckBox", None))
        self.checkBox_5.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uac00_\uc704\ud5d8\uc720\ud615", None))
        self.checkBox_8.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub098_\uc704\ud5d8\uc720\ud615", None))
        self.dateTimeEdit_from.setDisplayFormat(QCoreApplication.translate("RpaTaskDetailDialog", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_end.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uac80\uc0c9 \uc885\ub8cc\uc77c\uc2dc (\uae4c\uc9c0)", None))
        self.label_type.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc2ec\uac01\ub3c4", None))
        self.label_start.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uac80\uc0c9 \uc2dc\uc791\uc77c\uc2dc (\ubd80\ud130)", None))
        self.label_15.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc704\ud5d8\uc720\ud615", None))
        self.dateTimeEdit_to.setDisplayFormat(QCoreApplication.translate("RpaTaskDetailDialog", u"yyyy-MM-dd HH:mm:ss", None))
        self.groupBox_2.setTitle("")
        self.radioButton_report_duration_days_30.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucd5c\uadfc 30\uc77c", None))
        self.radioButton_report_duration_days_7.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucd5c\uadfc 1\uc8fc\uc77c", None))
        self.radioButton_report_duration_days.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucd5c\uadfc", None))
        self.lineEdit_report_duration_days.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"5", None))
        self.label_13.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc77c", None))
        self.groupBox.setTitle("")
        self.checkBox_report_severity_danger_low.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uacbd\ubbf8", None))
        self.checkBox_report_severity_danger_lowlow.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub9e4\uc6b0\uacbd\ubbf8", None))
        self.checkBox_report_severity_danger_high.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc2ec\uac01", None))
        self.checkBox_report_severity_danger_highhigh.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub9e4\uc6b0\uc2ec\uac01", None))
        self.checkBox_report_severity_danger_mid.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc704\ud5d8", None))
        self.checkBox_report_severity_good_mid.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc815\uc0c1", None))
        self.checkBox_report_severity_good_highhigh.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub9e4\uc6b0\uc6b0\uc218", None))
        self.checkBox_report_severity_good_high.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc6b0\uc218", None))
        self.pushButton_email_addressbook.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc8fc\uc18c\ub85d", None))
        self.pushButton_report_search.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubcf4\uace0\uc11c \uac80\uc0c9", None))
        ___qtablewidgetitem = self.tableWidget_report.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget_report.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubc1c\uc0dd\uc77c\uc2dc", None));
        ___qtablewidgetitem2 = self.tableWidget_report.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubcf4\uace0\uc77c\uc2dc", None));
        ___qtablewidgetitem3 = self.tableWidget_report.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc81c\ubaa9", None));
        ___qtablewidgetitem4 = self.tableWidget_report.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc7a5\uc18c", None));
        ___qtablewidgetitem5 = self.tableWidget_report.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc704\ud5d8\uc720\ud615", None));
        ___qtablewidgetitem6 = self.tableWidget_report.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc2ec\uac01\ub3c4", None));
        ___qtablewidgetitem7 = self.tableWidget_report.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub300\uc751\uc870\uce58", None));
        ___qtablewidgetitem8 = self.tableWidget_report.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc0ac\uc9c4", None));

        __sortingEnabled = self.tableWidget_report.isSortingEnabled()
        self.tableWidget_report.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.tableWidget_report.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"2", None));
        ___qtablewidgetitem10 = self.tableWidget_report.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"2025/07/01 00:00:00", None));
        ___qtablewidgetitem11 = self.tableWidget_report.item(0, 3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubd88\uc548\uc804 \uc0c1\ud669\uac10\uc9c0-\uc911\uc7a5\ube44 \ucda9\ub3cc", None));
        ___qtablewidgetitem12 = self.tableWidget_report.item(0, 4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc81c1\uacf5\uc7a5-A01 \uad6c\uc5ed", None));
        ___qtablewidgetitem13 = self.tableWidget_report.item(0, 5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucda9\ub3cc", None));
        ___qtablewidgetitem14 = self.tableWidget_report.item(0, 6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub9e4\uc6b0 \uc2ec\uac01", None));
        ___qtablewidgetitem15 = self.tableWidget_report.item(0, 7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubc29\uc1a1", None));
        ___qtablewidgetitem16 = self.tableWidget_report.item(0, 8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"[\uc0ac\uc9c4]", None));
        ___qtablewidgetitem17 = self.tableWidget_report.item(1, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"1", None));
        ___qtablewidgetitem18 = self.tableWidget_report.item(1, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"2025/06/01 00:00:00", None));
        ___qtablewidgetitem19 = self.tableWidget_report.item(1, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubd88\uc548\uc804 \uc0c1\ud669\uac10\uc9c0-\uac1c\uad6c\ubd80 \uc811\uadfc", None));
        ___qtablewidgetitem20 = self.tableWidget_report.item(1, 4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc81c2\uacf5\uc7a5-B02 \uad6c\uc5ed", None));
        ___qtablewidgetitem21 = self.tableWidget_report.item(1, 5)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucd94\ub77d", None));
        ___qtablewidgetitem22 = self.tableWidget_report.item(1, 6)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc704\ud5d8", None));
        ___qtablewidgetitem23 = self.tableWidget_report.item(1, 7)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc54c\ub78c", None));
        ___qtablewidgetitem24 = self.tableWidget_report.item(1, 8)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"[\uc0ac\uc9c4]", None));
        self.tableWidget_report.setSortingEnabled(__sortingEnabled)

        self.label_3.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"( \ub4f1\ub85d\ud55c RPA\uc5c5\ubb34\uac00 \uc2e4\ud589\ub420 \ub54c\ub294 \uc2e4\uc81c \uc5c5\ubb34\uc2e4\ud589 \uc2dc\uac01\uc744 \uae30\uc900\uc73c\ub85c \ubcf4\uace0\uc11c \uac80\uc0c9\ud558\ubbc0\ub85c \ubcf4\uace0\uc11c \ubaa9\ub85d\uc740 \uc704\uc640 \ub2ec\ub77c\uc9c8 \uc218 \uc788\uc2b5\ub2c8\ub2e4.)", None))
        self.lineEdit_email_title.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc815\uae30\ubcf4\uace0", None))
        self.label_10.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc774\uba54\uc77c \ubc1c\uc1a1 \uc694\uc77c", None))
        self.checkBox_tue.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ud654", None))
        self.checkBox_sat.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ud1a0", None))
        self.checkBox_mon.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc6d4", None))
        self.checkBox_thu.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubaa9", None))
        self.checkBox_sun.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc77c", None))
        self.checkBox_fri.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uae08", None))
        self.checkBox_wed.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc218", None))
        self.label_4.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc774\uba54\uc77c \ubc1c\uc1a1 \uc2dc\uac04", None))
        self.lineEdit_task_name.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"RPA \ubc18\ubcf5\uc5c5\ubb34", None))
        self.lineEdit_task_name.setPlaceholderText("")
        self.label_11.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"<html><head/><body><p>\ucca8\ubd80<br/>\ubcf4\uace0\uc11c<br/>\uc124\uc815</p></body></html>", None))
        self.label_email_title.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc774\uba54\uc77c \uc81c\ubaa9", None))
        self.label_email_to.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc774\uba54\uc77c \uc218\uc2e0\uc790", None))
        self.label_12.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ubc18\ubcf5 \uc77c\uc815", None))
        self.label_6.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"ID", None))
        self.label_9.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucca8\ubd80\ud30c\uc77c", None))
        self.label_7.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc5c5\ubb34 \uba85\uce6d", None))
        self.pushButton_email_attach.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ucca8\ubd80\ud30c\uc77c \uc120\ud0dd", None))
        self.pushButton_email_body_default.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uae30\ubcf8\uac12", None))
        self.pushButton_accept.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc801\uc6a9", None))
        self.pushButton_insert.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ud604\uc7ac \uc5c5\ubb34\ub97c \uc0c8 RPA\uc5c5\ubb34\ub85c \ub4f1\ub85d", None))
        self.pushButton_delete.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ud604\uc7ac \uc5c5\ubb34 \uc0ad\uc81c", None))
        self.pushButton_close.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\ub2eb\uae30", None))
        self.label_dialog_title.setText(QCoreApplication.translate("RpaTaskDetailDialog", u"\uc0c8 \uc5c5\ubb34\ub4f1\ub85d", None))
    # retranslateUi

