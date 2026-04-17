# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clock_widgetnugnNj.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_ClockWidget(object):
    def setupUi(self, ClockWidget):
        if not ClockWidget.objectName():
            ClockWidget.setObjectName(u"ClockWidget")
        ClockWidget.resize(187, 43)
        ClockWidget.setMaximumSize(QSize(16777215, 16777215))
        ClockWidget.setStyleSheet(u"")
        self.gridLayout = QGridLayout(ClockWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 10, 0, 10)
        self.label_clock = QLabel(ClockWidget)
        self.label_clock.setObjectName(u"label_clock")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_clock.sizePolicy().hasHeightForWidth())
        self.label_clock.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(15)
        self.label_clock.setFont(font)

        self.gridLayout.addWidget(self.label_clock, 0, 0, 1, 1)


        self.retranslateUi(ClockWidget)

        QMetaObject.connectSlotsByName(ClockWidget)
    # setupUi

    def retranslateUi(self, ClockWidget):
        ClockWidget.setWindowTitle(QCoreApplication.translate("ClockWidget", u"Form", None))
        self.label_clock.setText(QCoreApplication.translate("ClockWidget", u"2022-12-31 23:59:59", None))
    # retranslateUi

