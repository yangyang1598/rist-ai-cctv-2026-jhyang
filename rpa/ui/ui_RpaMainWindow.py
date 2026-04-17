# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_RpaMainWindow(object):
    def setupUi(self, RpaMainWindow):
        if not RpaMainWindow.objectName():
            RpaMainWindow.setObjectName(u"RpaMainWindow")
        RpaMainWindow.resize(1088, 813)
        self.actionSetting = QAction(RpaMainWindow)
        self.actionSetting.setObjectName(u"actionSetting")
        self.centralwidget = QWidget(RpaMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 50))
        self.label.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(19)
        font.setBold(True)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: rgb(2, 75, 128);\n"
"color: rgb(255, 255, 255);")
        self.label.setMargin(0)
        self.label.setIndent(15)

        self.horizontalLayout.addWidget(self.label)

        self.pushButton_report = QPushButton(self.centralwidget)
        self.pushButton_report.setObjectName(u"pushButton_report")
        self.pushButton_report.setMinimumSize(QSize(180, 50))

        self.horizontalLayout.addWidget(self.pushButton_report)

        self.pushButton_task = QPushButton(self.centralwidget)
        self.pushButton_task.setObjectName(u"pushButton_task")
        self.pushButton_task.setMinimumSize(QSize(180, 50))

        self.horizontalLayout.addWidget(self.pushButton_task)

        self.pushButton_setting = QPushButton(self.centralwidget)
        self.pushButton_setting.setObjectName(u"pushButton_setting")
        self.pushButton_setting.setMinimumSize(QSize(180, 50))

        self.horizontalLayout.addWidget(self.pushButton_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")
        self.label_time.setMinimumSize(QSize(180, 0))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.label_time.setFont(font1)
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_time)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_report = QWidget()
        self.page_report.setObjectName(u"page_report")
        self.gridLayout_4 = QGridLayout(self.page_report)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_report = QGridLayout()
        self.gridLayout_report.setObjectName(u"gridLayout_report")
        self.label_3 = QLabel(self.page_report)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"background-color: rgb(85, 255, 0);\n"
"font: 20pt \"Arial\";")

        self.gridLayout_report.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_report, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_report)
        self.page_task = QWidget()
        self.page_task.setObjectName(u"page_task")
        self.gridLayout_6 = QGridLayout(self.page_task)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_task = QGridLayout()
        self.gridLayout_task.setObjectName(u"gridLayout_task")
        self.label_4 = QLabel(self.page_task)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"background-color: rgb(85, 255, 0);\n"
"font: 20pt \"Arial\";")

        self.gridLayout_task.addWidget(self.label_4, 0, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_task, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_task)
        self.page_setting = QWidget()
        self.page_setting.setObjectName(u"page_setting")
        self.gridLayout_7 = QGridLayout(self.page_setting)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_setting = QGridLayout()
        self.gridLayout_setting.setObjectName(u"gridLayout_setting")
        self.label_5 = QLabel(self.page_setting)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"background-color: rgb(85, 255, 0);\n"
"font: 20pt \"Arial\";")

        self.gridLayout_setting.addWidget(self.label_5, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_setting, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_setting)

        self.gridLayout.addWidget(self.stackedWidget, 2, 1, 1, 1)

        self.verticalLayout_log = QVBoxLayout()
        self.verticalLayout_log.setObjectName(u"verticalLayout_log")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background-color: rgb(85, 255, 0);\n"
"font: 20pt \"Arial\";")

        self.verticalLayout_log.addWidget(self.label_6)


        self.gridLayout.addLayout(self.verticalLayout_log, 3, 1, 1, 1)

        RpaMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(RpaMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1088, 22))
        self.menuRPA_Setting = QMenu(self.menubar)
        self.menuRPA_Setting.setObjectName(u"menuRPA_Setting")
        RpaMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(RpaMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        RpaMainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuRPA_Setting.menuAction())
        self.menuRPA_Setting.addAction(self.actionSetting)

        self.retranslateUi(RpaMainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RpaMainWindow)
    # setupUi

    def retranslateUi(self, RpaMainWindow):
        RpaMainWindow.setWindowTitle(QCoreApplication.translate("RpaMainWindow", u"RPA", None))
        self.actionSetting.setText(QCoreApplication.translate("RpaMainWindow", u"Setting", None))
        self.label.setText(QCoreApplication.translate("RpaMainWindow", u"RPA", None))
        self.pushButton_report.setText(QCoreApplication.translate("RpaMainWindow", u"\ubcf4\uace0\uc11c(Report)", None))
        self.pushButton_task.setText(QCoreApplication.translate("RpaMainWindow", u"\uc5c5\ubb34\uc790\ub3d9\ud654 \uad00\ub9ac", None))
        self.pushButton_setting.setText(QCoreApplication.translate("RpaMainWindow", u"\uc124\uc815", None))
        self.label_time.setText(QCoreApplication.translate("RpaMainWindow", u"2025-01-01 01:00:00", None))
        self.label_3.setText(QCoreApplication.translate("RpaMainWindow", u"RpaReportWidget", None))
        self.label_4.setText(QCoreApplication.translate("RpaMainWindow", u"RpaTask widget", None))
        self.label_5.setText(QCoreApplication.translate("RpaMainWindow", u"RpaSettingWidget", None))
        self.label_6.setText(QCoreApplication.translate("RpaMainWindow", u"LogTextWidget", None))
        self.menuRPA_Setting.setTitle(QCoreApplication.translate("RpaMainWindow", u"RPA Setting", None))
    # retranslateUi

