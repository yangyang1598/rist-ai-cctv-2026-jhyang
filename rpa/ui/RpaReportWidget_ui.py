# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaReportWidget.ui'
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
    QFrame, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_RpaReportWidget(object):
    def setupUi(self, RpaReportWidget):
        if not RpaReportWidget.objectName():
            RpaReportWidget.setObjectName(u"RpaReportWidget")
        RpaReportWidget.resize(1044, 769)
        self.gridLayout = QGridLayout(RpaReportWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(RpaReportWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 20pt \"Arial\";")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(RpaReportWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_new = QWidget()
        self.tab_new.setObjectName(u"tab_new")
        self.gridLayout_3 = QGridLayout(self.tab_new)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_report_new_dummy = QPushButton(self.tab_new)
        self.pushButton_report_new_dummy.setObjectName(u"pushButton_report_new_dummy")
        self.pushButton_report_new_dummy.setMinimumSize(QSize(0, 80))

        self.gridLayout_2.addWidget(self.pushButton_report_new_dummy, 1, 0, 1, 1)

        self.pushButton_report_new_manual = QPushButton(self.tab_new)
        self.pushButton_report_new_manual.setObjectName(u"pushButton_report_new_manual")
        self.pushButton_report_new_manual.setMinimumSize(QSize(0, 80))

        self.gridLayout_2.addWidget(self.pushButton_report_new_manual, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_new, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_5 = QGridLayout(self.tab_list)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tableWidget_report = QTableWidget(self.tab_list)
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
        self.tableWidget_report.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_report.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.gridLayout_4.addWidget(self.tableWidget_report, 0, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.tab_list)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.pushButton_search = QPushButton(self.groupBox)
        self.pushButton_search.setObjectName(u"pushButton_search")

        self.gridLayout_6.addWidget(self.pushButton_search, 1, 0, 1, 1)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_9 = QGridLayout(self.frame_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.line_2 = QFrame(self.frame_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_9.addWidget(self.line_2, 4, 0, 1, 4)

        self.checkBox_severity_danger_low = QCheckBox(self.frame_2)
        self.checkBox_severity_danger_low.setObjectName(u"checkBox_severity_danger_low")

        self.gridLayout_9.addWidget(self.checkBox_severity_danger_low, 12, 1, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_9.addWidget(self.label_3, 0, 0, 1, 1)

        self.line = QFrame(self.frame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_9.addWidget(self.line, 15, 0, 1, 4)

        self.dateTimeEdit_to = QDateTimeEdit(self.frame_2)
        self.dateTimeEdit_to.setObjectName(u"dateTimeEdit_to")
        self.dateTimeEdit_to.setCalendarPopup(True)

        self.gridLayout_9.addWidget(self.dateTimeEdit_to, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 16, 0, 1, 1)

        self.label_end = QLabel(self.frame_2)
        self.label_end.setObjectName(u"label_end")

        self.gridLayout_9.addWidget(self.label_end, 1, 1, 1, 1)

        self.pushButton_period_today = QPushButton(self.frame_2)
        self.pushButton_period_today.setObjectName(u"pushButton_period_today")

        self.gridLayout_9.addWidget(self.pushButton_period_today, 1, 3, 1, 1)

        self.checkBox_severity_good_mid = QCheckBox(self.frame_2)
        self.checkBox_severity_good_mid.setObjectName(u"checkBox_severity_good_mid")

        self.gridLayout_9.addWidget(self.checkBox_severity_good_mid, 11, 2, 1, 1)

        self.checkBox_severity_danger_highhigh = QCheckBox(self.frame_2)
        self.checkBox_severity_danger_highhigh.setObjectName(u"checkBox_severity_danger_highhigh")

        self.gridLayout_9.addWidget(self.checkBox_severity_danger_highhigh, 9, 1, 1, 1)

        self.checkBox_severity_good_high = QCheckBox(self.frame_2)
        self.checkBox_severity_good_high.setObjectName(u"checkBox_severity_good_high")

        self.gridLayout_9.addWidget(self.checkBox_severity_good_high, 10, 2, 1, 1)

        self.checkBox_severity_danger_high = QCheckBox(self.frame_2)
        self.checkBox_severity_danger_high.setObjectName(u"checkBox_severity_danger_high")

        self.gridLayout_9.addWidget(self.checkBox_severity_danger_high, 10, 1, 1, 1)

        self.checkBox_severity_danger_mid = QCheckBox(self.frame_2)
        self.checkBox_severity_danger_mid.setObjectName(u"checkBox_severity_danger_mid")

        self.gridLayout_9.addWidget(self.checkBox_severity_danger_mid, 11, 1, 1, 1)

        self.checkBox_severity_good_highhigh = QCheckBox(self.frame_2)
        self.checkBox_severity_good_highhigh.setObjectName(u"checkBox_severity_good_highhigh")

        self.gridLayout_9.addWidget(self.checkBox_severity_good_highhigh, 9, 2, 1, 1)

        self.dateTimeEdit_from = QDateTimeEdit(self.frame_2)
        self.dateTimeEdit_from.setObjectName(u"dateTimeEdit_from")
        self.dateTimeEdit_from.setCalendarPopup(True)

        self.gridLayout_9.addWidget(self.dateTimeEdit_from, 0, 2, 1, 1)

        self.label_start = QLabel(self.frame_2)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_9.addWidget(self.label_start, 0, 1, 1, 1)

        self.checkBox_severity_danger_lowlow = QCheckBox(self.frame_2)
        self.checkBox_severity_danger_lowlow.setObjectName(u"checkBox_severity_danger_lowlow")

        self.gridLayout_9.addWidget(self.checkBox_severity_danger_lowlow, 13, 1, 1, 1)

        self.label_type = QLabel(self.frame_2)
        self.label_type.setObjectName(u"label_type")

        self.gridLayout_9.addWidget(self.label_type, 9, 0, 1, 1)

        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 120))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 703, 118))
        self.gridLayout_12 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.gridLayout_event_type = QGridLayout()
        self.gridLayout_event_type.setObjectName(u"gridLayout_event_type")
        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_event_type.addWidget(self.checkBox, 0, 1, 1, 1)

        self.checkBox_4 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_event_type.addWidget(self.checkBox_4, 0, 2, 1, 1)

        self.checkBox_3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_event_type.addWidget(self.checkBox_3, 0, 3, 1, 1)

        self.checkBox_2 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_event_type.addWidget(self.checkBox_2, 0, 0, 1, 1)

        self.checkBox_8 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.gridLayout_event_type.addWidget(self.checkBox_8, 1, 0, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_event_type, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_9.addWidget(self.scrollArea, 16, 1, 2, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 17, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_list, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(RpaReportWidget)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(RpaReportWidget)
    # setupUi

    def retranslateUi(self, RpaReportWidget):
        RpaReportWidget.setWindowTitle(QCoreApplication.translate("RpaReportWidget", u"RPA \ubcf4\uace0\uc11c", None))
        self.label.setText(QCoreApplication.translate("RpaReportWidget", u"RPA \ubcf4\uace0\uc11c", None))
        self.pushButton_report_new_dummy.setText(QCoreApplication.translate("RpaReportWidget", u"\ub354\ubbf8\ub370\uc774\ud130\ub85c \uc0c8 \ubcf4\uace0\uc11c \ub9cc\ub4e4\uae30", None))
        self.pushButton_report_new_manual.setText(QCoreApplication.translate("RpaReportWidget", u"\uc9c1\uc811\uc785\ub825 \uc0c8 \ubcf4\uace0\uc11c \ub9cc\ub4e4\uae30", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_new), QCoreApplication.translate("RpaReportWidget", u"\uc0c8 \ubcf4\uace0\uc11c", None))
        ___qtablewidgetitem = self.tableWidget_report.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RpaReportWidget", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget_report.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RpaReportWidget", u"\ubc1c\uc0dd\uc77c\uc2dc", None));
        ___qtablewidgetitem2 = self.tableWidget_report.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RpaReportWidget", u"\ubcf4\uace0\uc77c\uc2dc", None));
        ___qtablewidgetitem3 = self.tableWidget_report.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RpaReportWidget", u"\uc81c\ubaa9", None));
        ___qtablewidgetitem4 = self.tableWidget_report.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RpaReportWidget", u"\uc7a5\uc18c", None));
        ___qtablewidgetitem5 = self.tableWidget_report.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RpaReportWidget", u"\uc704\ud5d8\uc720\ud615", None));
        ___qtablewidgetitem6 = self.tableWidget_report.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RpaReportWidget", u"\uc2ec\uac01\ub3c4", None));
        ___qtablewidgetitem7 = self.tableWidget_report.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RpaReportWidget", u"\ub300\uc751\uc870\uce58", None));
        ___qtablewidgetitem8 = self.tableWidget_report.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RpaReportWidget", u"\uc0ac\uc9c4", None));

        __sortingEnabled = self.tableWidget_report.isSortingEnabled()
        self.tableWidget_report.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.tableWidget_report.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("RpaReportWidget", u"2", None));
        ___qtablewidgetitem10 = self.tableWidget_report.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("RpaReportWidget", u"2025/07/01 00:00:00", None));
        ___qtablewidgetitem11 = self.tableWidget_report.item(0, 3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("RpaReportWidget", u"\ubd88\uc548\uc804 \uc0c1\ud669\uac10\uc9c0-\uc911\uc7a5\ube44 \ucda9\ub3cc", None));
        ___qtablewidgetitem12 = self.tableWidget_report.item(0, 4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("RpaReportWidget", u"\uc81c1\uacf5\uc7a5-A01 \uad6c\uc5ed", None));
        ___qtablewidgetitem13 = self.tableWidget_report.item(0, 5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("RpaReportWidget", u"\ucda9\ub3cc", None));
        ___qtablewidgetitem14 = self.tableWidget_report.item(0, 6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("RpaReportWidget", u"\ub9e4\uc6b0 \uc2ec\uac01", None));
        ___qtablewidgetitem15 = self.tableWidget_report.item(0, 7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("RpaReportWidget", u"\ubc29\uc1a1", None));
        ___qtablewidgetitem16 = self.tableWidget_report.item(0, 8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("RpaReportWidget", u"[\uc0ac\uc9c4]", None));
        ___qtablewidgetitem17 = self.tableWidget_report.item(1, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("RpaReportWidget", u"1", None));
        ___qtablewidgetitem18 = self.tableWidget_report.item(1, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("RpaReportWidget", u"2025/06/01 00:00:00", None));
        ___qtablewidgetitem19 = self.tableWidget_report.item(1, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("RpaReportWidget", u"\ubd88\uc548\uc804 \uc0c1\ud669\uac10\uc9c0-\uac1c\uad6c\ubd80 \uc811\uadfc", None));
        ___qtablewidgetitem20 = self.tableWidget_report.item(1, 4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("RpaReportWidget", u"\uc81c2\uacf5\uc7a5-B02 \uad6c\uc5ed", None));
        ___qtablewidgetitem21 = self.tableWidget_report.item(1, 5)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("RpaReportWidget", u"\ucd94\ub77d", None));
        ___qtablewidgetitem22 = self.tableWidget_report.item(1, 6)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("RpaReportWidget", u"\uc704\ud5d8", None));
        ___qtablewidgetitem23 = self.tableWidget_report.item(1, 7)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("RpaReportWidget", u"\uc54c\ub78c", None));
        ___qtablewidgetitem24 = self.tableWidget_report.item(1, 8)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("RpaReportWidget", u"[\uc0ac\uc9c4]", None));
        self.tableWidget_report.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("RpaReportWidget", u"\ubcf4\uace0\uc11c \uac80\uc0c9", None))
        self.pushButton_search.setText(QCoreApplication.translate("RpaReportWidget", u"\ubcf4\uace0\uc11c \uac80\uc0c9", None))
        self.checkBox_severity_danger_low.setText(QCoreApplication.translate("RpaReportWidget", u"\uacbd\ubbf8", None))
        self.label_3.setText(QCoreApplication.translate("RpaReportWidget", u"\ubc1c\uc0dd\uc77c\uc2dc", None))
        self.dateTimeEdit_to.setDisplayFormat(QCoreApplication.translate("RpaReportWidget", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_2.setText(QCoreApplication.translate("RpaReportWidget", u"\uc704\ud5d8\uc720\ud615", None))
        self.label_end.setText(QCoreApplication.translate("RpaReportWidget", u"\uac80\uc0c9 \uc885\ub8cc\uc77c\uc2dc (\uae4c\uc9c0)", None))
        self.pushButton_period_today.setText(QCoreApplication.translate("RpaReportWidget", u"\uc624\ub298", None))
        self.checkBox_severity_good_mid.setText(QCoreApplication.translate("RpaReportWidget", u"\uc815\uc0c1", None))
        self.checkBox_severity_danger_highhigh.setText(QCoreApplication.translate("RpaReportWidget", u"\ub9e4\uc6b0 \uc2ec\uac01", None))
        self.checkBox_severity_good_high.setText(QCoreApplication.translate("RpaReportWidget", u"\uc6b0\uc218", None))
        self.checkBox_severity_danger_high.setText(QCoreApplication.translate("RpaReportWidget", u"\uc2ec\uac01", None))
        self.checkBox_severity_danger_mid.setText(QCoreApplication.translate("RpaReportWidget", u"\uc704\ud5d8", None))
        self.checkBox_severity_good_highhigh.setText(QCoreApplication.translate("RpaReportWidget", u"\ub9e4\uc6b0 \uc6b0\uc218", None))
        self.dateTimeEdit_from.setDisplayFormat(QCoreApplication.translate("RpaReportWidget", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_start.setText(QCoreApplication.translate("RpaReportWidget", u"\uac80\uc0c9 \uc2dc\uc791\uc77c\uc2dc (\ubd80\ud130)", None))
        self.checkBox_severity_danger_lowlow.setText(QCoreApplication.translate("RpaReportWidget", u"\ub9e4\uc6b0 \uacbd\ubbf8", None))
        self.label_type.setText(QCoreApplication.translate("RpaReportWidget", u"\uc2ec\uac01\ub3c4", None))
        self.checkBox.setText(QCoreApplication.translate("RpaReportWidget", u"\ub098_\uc704\ud5d8\uc720\ud615", None))
        self.checkBox_4.setText(QCoreApplication.translate("RpaReportWidget", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("RpaReportWidget", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("RpaReportWidget", u"\uac00_\uc704\ud5d8\uc720\ud615", None))
        self.checkBox_8.setText(QCoreApplication.translate("RpaReportWidget", u"CheckBox", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_list), QCoreApplication.translate("RpaReportWidget", u"\ubcf4\uace0\uc11c \ubaa9\ub85d", None))
    # retranslateUi

