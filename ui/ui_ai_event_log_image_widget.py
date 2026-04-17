# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_image_widgetfdNaEf.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(322, 751)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 5, 5)
        self.label_event_log_image = QLabel(Widget)
        self.label_event_log_image.setObjectName(u"label_event_log_image")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_event_log_image.setFont(font)

        self.verticalLayout.addWidget(self.label_event_log_image)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 3, 0, -1)
        self.scroll_area_event_log_image = QScrollArea(Widget)
        self.scroll_area_event_log_image.setObjectName(u"scroll_area_event_log_image")
        self.scroll_area_event_log_image.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 309, 716))
        self.scroll_area_event_log_image.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scroll_area_event_log_image)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_event_log_image.setText(QCoreApplication.translate("Widget", u"\u25bc \uc774\ubca4\ud2b8 \ub85c\uadf8 \uc774\ubbf8\uc9c0 \ubaa9\ub85d", None))
    # retranslateUi

