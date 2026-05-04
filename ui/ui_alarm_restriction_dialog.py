# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'alarm_restriction_dialogRckPJN.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(630, 345)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_restriction_alarm_title = QLabel(Dialog)
        self.label_restriction_alarm_title.setObjectName(u"label_restriction_alarm_title")
        font = QFont()
        font.setPointSize(25)
        self.label_restriction_alarm_title.setFont(font)

        self.verticalLayout.addWidget(self.label_restriction_alarm_title)

        self.label_cctv_name = QLabel(Dialog)
        self.label_cctv_name.setObjectName(u"label_cctv_name")
        font1 = QFont()
        font1.setPointSize(15)
        self.label_cctv_name.setFont(font1)

        self.verticalLayout.addWidget(self.label_cctv_name)

        self.radio_restriction_alarm_mode = QRadioButton(Dialog)
        self.radio_restriction_alarm_mode.setObjectName(u"radio_restriction_alarm_mode")
        font2 = QFont()
        font2.setPointSize(11)
        self.radio_restriction_alarm_mode.setFont(font2)

        self.verticalLayout.addWidget(self.radio_restriction_alarm_mode)

        self.radio_stop_ai_mode = QRadioButton(Dialog)
        self.radio_stop_ai_mode.setObjectName(u"radio_stop_ai_mode")
        self.radio_stop_ai_mode.setFont(font2)

        self.verticalLayout.addWidget(self.radio_stop_ai_mode)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_set_time_title = QLabel(Dialog)
        self.label_set_time_title.setObjectName(u"label_set_time_title")
        self.label_set_time_title.setFont(font2)

        self.horizontalLayout.addWidget(self.label_set_time_title)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.lineEdit_set_time = QLineEdit(Dialog)
        self.lineEdit_set_time.setObjectName(u"lineEdit_set_time")

        self.horizontalLayout.addWidget(self.lineEdit_set_time)

        self.combo_time_format = QComboBox(Dialog)
        self.combo_time_format.addItem("")
        self.combo_time_format.addItem("")
        self.combo_time_format.addItem("")
        self.combo_time_format.setObjectName(u"combo_time_format")

        self.horizontalLayout.addWidget(self.combo_time_format)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.button_ok = QPushButton(Dialog)
        self.button_ok.setObjectName(u"button_ok")

        self.horizontalLayout_2.addWidget(self.button_ok)

        self.button_cancel = QPushButton(Dialog)
        self.button_cancel.setObjectName(u"button_cancel")

        self.horizontalLayout_2.addWidget(self.button_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_restriction_alarm_title.setText(QCoreApplication.translate("Dialog", u"\uc54c\ub78c \uc81c\ud55c \uc124\uc815", None))
        self.label_cctv_name.setText(QCoreApplication.translate("Dialog", u"CCTV 01", None))
        self.radio_restriction_alarm_mode.setText(QCoreApplication.translate("Dialog", u"\uc54c\ub78c \uc804\uc1a1 \uc81c\ud55c \ubaa8\ub4dc", None))
        self.radio_stop_ai_mode.setText(QCoreApplication.translate("Dialog", u"AI \uc5f0\uc0b0 \uc77c\uc2dc\uc815\uc9c0 \ubaa8\ub4dc", None))
        self.label_set_time_title.setText(QCoreApplication.translate("Dialog", u"\uc81c\ud55c/\uc77c\uc2dc\uc815\uc9c0 \uc2dc\uac04", None))
        self.combo_time_format.setItemText(0, QCoreApplication.translate("Dialog", u"\ubd84", None))
        self.combo_time_format.setItemText(1, QCoreApplication.translate("Dialog", u"\uc2dc\uac04", None))
        self.combo_time_format.setItemText(2, QCoreApplication.translate("Dialog", u"\ucd08", None))

        self.button_ok.setText(QCoreApplication.translate("Dialog", u"\uc124\uc815", None))
        self.button_cancel.setText(QCoreApplication.translate("Dialog", u"\ucde8\uc18c", None))
    # retranslateUi

