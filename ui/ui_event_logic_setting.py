# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'event_logic_settingOnUfEB.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 300)
        Dialog.setMinimumSize(QSize(480, 300))
        Dialog.setMaximumSize(QSize(480, 300))
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(15, 70, 450, 190))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_algorithn = QLabel(self.frame_2)
        self.label_algorithn.setObjectName(u"label_algorithn")
        self.label_algorithn.setGeometry(QRect(30, 70, 101, 16))
        font = QFont()
        font.setPointSize(11)
        self.label_algorithn.setFont(font)
        self.combo_algorithm = QComboBox(self.frame_2)
        self.combo_algorithm.setObjectName(u"combo_algorithm")
        self.combo_algorithm.setGeometry(QRect(30, 100, 381, 31))
        self.radio_ai = QRadioButton(Dialog)
        self.radio_ai.setObjectName(u"radio_ai")
        self.radio_ai.setGeometry(QRect(90, 30, 92, 20))
        self.radio_algorithm = QRadioButton(Dialog)
        self.radio_algorithm.setObjectName(u"radio_algorithm")
        self.radio_algorithm.setGeometry(QRect(310, 30, 121, 20))
        self.button_accept = QPushButton(Dialog)
        self.button_accept.setObjectName(u"button_accept")
        self.button_accept.setGeometry(QRect(390, 270, 75, 24))
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(15, 70, 450, 190))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_ai = QLabel(self.frame)
        self.label_ai.setObjectName(u"label_ai")
        self.label_ai.setGeometry(QRect(30, 20, 48, 16))
        self.combo_ai = QComboBox(self.frame)
        self.combo_ai.setObjectName(u"combo_ai")
        self.combo_ai.setGeometry(QRect(30, 50, 401, 31))
        self.combo_object = QComboBox(self.frame)
        self.combo_object.setObjectName(u"combo_object")
        self.combo_object.setGeometry(QRect(30, 130, 401, 31))
        self.label_object = QLabel(self.frame)
        self.label_object.setObjectName(u"label_object")
        self.label_object.setGeometry(QRect(30, 100, 48, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_algorithn.setText(QCoreApplication.translate("Dialog", u"\ud310\ub2e8 \uc54c\uace0\ub9ac\uc998", None))
        self.radio_ai.setText(QCoreApplication.translate("Dialog", u"AI \ubaa8\ub378", None))
        self.radio_algorithm.setText(QCoreApplication.translate("Dialog", u"\ud310\ub2e8 \uc54c\uace0\ub9ac\uc998", None))
        self.button_accept.setText(QCoreApplication.translate("Dialog", u"\ucd94\uac00", None))
        self.label_ai.setText(QCoreApplication.translate("Dialog", u"AI \ubaa8\ub378", None))
        self.label_object.setText(QCoreApplication.translate("Dialog", u"\uac1d\uccb4", None))
    # retranslateUi

