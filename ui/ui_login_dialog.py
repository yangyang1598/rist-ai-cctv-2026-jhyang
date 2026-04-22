# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_dialogroJqbC.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 300))
        Dialog.setMaximumSize(QSize(500, 300))
        self.lineEdit_id = QLineEdit(Dialog)
        self.lineEdit_id.setObjectName(u"lineEdit_id")
        self.lineEdit_id.setGeometry(QRect(60, 120, 251, 41))
        self.button_login = QPushButton(Dialog)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setGeometry(QRect(360, 120, 101, 91))
        font = QFont()
        font.setPointSize(13)
        self.button_login.setFont(font)
        self.button_login.setStyleSheet(u"background-color: rgb(0, 0, 107);\n"
"color:rgb(255,255,255);")
        self.lineEdit_pw = QLineEdit(Dialog)
        self.lineEdit_pw.setObjectName(u"lineEdit_pw")
        self.lineEdit_pw.setGeometry(QRect(60, 180, 251, 41))
        self.checkBox_save_id_info = QCheckBox(Dialog)
        self.checkBox_save_id_info.setObjectName(u"checkBox_save_id_info")
        self.checkBox_save_id_info.setGeometry(QRect(60, 250, 82, 23))
        self.checkBox_auto_login = QCheckBox(Dialog)
        self.checkBox_auto_login.setObjectName(u"checkBox_auto_login")
        self.checkBox_auto_login.setGeometry(QRect(140, 250, 82, 23))
        self.label_title_login = QLabel(Dialog)
        self.label_title_login.setObjectName(u"label_title_login")
        self.label_title_login.setGeometry(QRect(50, 30, 421, 51))
        font1 = QFont()
        font1.setPointSize(16)
        self.label_title_login.setFont(font1)
        self.label_title_login.setStyleSheet(u"background-color: rgb(0, 0, 171);\n"
"color:rgb(255, 255, 255);\n"
"")
        self.label_title_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lineEdit_id.setPlaceholderText(QCoreApplication.translate("Dialog", u"ID", None))
        self.button_login.setText(QCoreApplication.translate("Dialog", u"\ub85c\uadf8\uc778", None))
        self.lineEdit_pw.setPlaceholderText(QCoreApplication.translate("Dialog", u"password", None))
        self.checkBox_save_id_info.setText(QCoreApplication.translate("Dialog", u"ID \uc800\uc7a5", None))
        self.checkBox_auto_login.setText(QCoreApplication.translate("Dialog", u"\uc790\ub3d9 \ub85c\uadf8\uc778", None))
        self.label_title_login.setText(QCoreApplication.translate("Dialog", u"  \uc9c0\ub2a5\ud615 CCTV \ud50c\ub7ab\ud3fc  ", None))
    # retranslateUi

