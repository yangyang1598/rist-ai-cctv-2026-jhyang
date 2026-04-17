# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_event_settingozNOmp.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(841, 678)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_cctvname = QLabel(Dialog)
        self.label_cctvname.setObjectName(u"label_cctvname")
        font = QFont()
        font.setPointSize(20)
        self.label_cctvname.setFont(font)

        self.verticalLayout.addWidget(self.label_cctvname)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.listwidget_set_event_list = QListWidget(Dialog)
        self.listwidget_set_event_list.setObjectName(u"listwidget_set_event_list")

        self.gridLayout_2.addWidget(self.listwidget_set_event_list, 1, 2, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.button_add_event = QPushButton(Dialog)
        self.button_add_event.setObjectName(u"button_add_event")

        self.verticalLayout_6.addWidget(self.button_add_event)

        self.button_cancel_event = QPushButton(Dialog)
        self.button_cancel_event.setObjectName(u"button_cancel_event")

        self.verticalLayout_6.addWidget(self.button_cancel_event)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout_6, 1, 1, 1, 1)

        self.label_event = QLabel(Dialog)
        self.label_event.setObjectName(u"label_event")
        font1 = QFont()
        font1.setUnderline(False)
        self.label_event.setFont(font1)

        self.gridLayout_2.addWidget(self.label_event, 0, 0, 1, 1)

        self.label_US = QLabel(Dialog)
        self.label_US.setObjectName(u"label_US")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_US.setFont(font2)

        self.gridLayout_2.addWidget(self.label_US, 0, 2, 1, 1)

        self.button_ok = QPushButton(Dialog)
        self.button_ok.setObjectName(u"button_ok")
        font3 = QFont()
        font3.setFamilies([u"\ud55c\ucef4\uc0b0\ub73b\ub3cb\uc6c0"])
        font3.setPointSize(12)
        self.button_ok.setFont(font3)

        self.gridLayout_2.addWidget(self.button_ok, 2, 2, 1, 1)

        self.event_list_widget = QWidget(Dialog)
        self.event_list_widget.setObjectName(u"event_list_widget")

        self.gridLayout_2.addWidget(self.event_list_widget, 1, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_cctvname.setText(QCoreApplication.translate("Dialog", u"cctv name", None))
        self.button_add_event.setText(QCoreApplication.translate("Dialog", u"\u25b6", None))
        self.button_cancel_event.setText(QCoreApplication.translate("Dialog", u"\u25c0", None))
        self.label_event.setText(QCoreApplication.translate("Dialog", u"\u25bc Event List", None))
        self.label_US.setText(QCoreApplication.translate("Dialog", u"\ubd88\uc548\uc815 \uc0c1\ud669 \uac10\uc9c0 \uc774\ubca4\ud2b8", None))
        self.button_ok.setText(QCoreApplication.translate("Dialog", u"\uc124\uc815", None))
    # retranslateUi

