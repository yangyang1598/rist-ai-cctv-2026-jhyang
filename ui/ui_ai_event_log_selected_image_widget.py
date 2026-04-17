# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_selected_image_widgetkMztvg.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(965, 299)
        self.verticalLayout_2 = QVBoxLayout(Widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_event_log_images = QLabel(Widget)
        self.label_event_log_images.setObjectName(u"label_event_log_images")
        font = QFont()
        font.setPointSize(10)
        self.label_event_log_images.setFont(font)

        self.verticalLayout_2.addWidget(self.label_event_log_images)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, -1, 0, -1)
        self.label_image = QLabel(Widget)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_image)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_location = QLabel(Widget)
        self.label_location.setObjectName(u"label_location")
        font1 = QFont()
        font1.setBold(True)
        self.label_location.setFont(font1)

        self.verticalLayout.addWidget(self.label_location)

        self.label_date = QLabel(Widget)
        self.label_date.setObjectName(u"label_date")
        font2 = QFont()
        font2.setBold(False)
        self.label_date.setFont(font2)

        self.verticalLayout.addWidget(self.label_date)

        self.label_event = QLabel(Widget)
        self.label_event.setObjectName(u"label_event")

        self.verticalLayout.addWidget(self.label_event)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(1, 1)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_event_log_images.setText(QCoreApplication.translate("Widget", u"\u25bc \uc774\ubca4\ud2b8 \ub85c\uadf8 \uc774\ubbf8\uc9c0", None))
        self.label_image.setText(QCoreApplication.translate("Widget", u"\uc774\ubbf8\uc9c0", None))
        self.label_location.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc704\uce58 \ubc0f CCTV", None))
        self.label_date.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc77c\uc2dc", None))
        self.label_event.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc774\ubca4\ud2b8", None))
    # retranslateUi

