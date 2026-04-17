# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaSettingWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QTabWidget, QWidget)

class Ui_RpaSettingWidget(object):
    def setupUi(self, RpaSettingWidget):
        if not RpaSettingWidget.objectName():
            RpaSettingWidget.setObjectName(u"RpaSettingWidget")
        RpaSettingWidget.resize(984, 646)
        self.gridLayout = QGridLayout(RpaSettingWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(RpaSettingWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 20pt \"Arial\";")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(RpaSettingWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.tabWidget.addTab(self.tab_9, "")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.tabWidget.addTab(self.tab_17, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(RpaSettingWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RpaSettingWidget)
    # setupUi

    def retranslateUi(self, RpaSettingWidget):
        RpaSettingWidget.setWindowTitle(QCoreApplication.translate("RpaSettingWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("RpaSettingWidget", u"RPA Setting", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), QCoreApplication.translate("RpaSettingWidget", u"\uc774\uba54\uc77c  \uc124\uc815", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_17), QCoreApplication.translate("RpaSettingWidget", u"RPA \uc124\uc815", None))
    # retranslateUi

