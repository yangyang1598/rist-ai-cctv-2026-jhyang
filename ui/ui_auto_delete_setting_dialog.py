# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auto_delete_setting_dialogCMgipm.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(391, 235)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_capacity_setting = QLabel(Dialog)
        self.label_capacity_setting.setObjectName(u"label_capacity_setting")
        font = QFont()
        font.setPointSize(16)
        self.label_capacity_setting.setFont(font)
        self.label_capacity_setting.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_capacity_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.button_apply_setting = QPushButton(Dialog)
        self.button_apply_setting.setObjectName(u"button_apply_setting")

        self.horizontalLayout_4.addWidget(self.button_apply_setting)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_display_required_capacity_text = QLabel(Dialog)
        self.label_display_required_capacity_text.setObjectName(u"label_display_required_capacity_text")

        self.horizontalLayout_2.addWidget(self.label_display_required_capacity_text)

        self.spinbox_required_capacity = QSpinBox(Dialog)
        self.spinbox_required_capacity.setObjectName(u"spinbox_required_capacity")

        self.horizontalLayout_2.addWidget(self.spinbox_required_capacity)

        self.label_mb_text = QLabel(Dialog)
        self.label_mb_text.setObjectName(u"label_mb_text")

        self.horizontalLayout_2.addWidget(self.label_mb_text)

        self.horizontalLayout_2.setStretch(1, 7)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_max_use_capacity = QLabel(Dialog)
        self.label_max_use_capacity.setObjectName(u"label_max_use_capacity")

        self.horizontalLayout_5.addWidget(self.label_max_use_capacity)

        self.label_blank = QLabel(Dialog)
        self.label_blank.setObjectName(u"label_blank")

        self.horizontalLayout_5.addWidget(self.label_blank)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_display_delete_capacity_text = QLabel(Dialog)
        self.label_display_delete_capacity_text.setObjectName(u"label_display_delete_capacity_text")

        self.horizontalLayout_3.addWidget(self.label_display_delete_capacity_text)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.spinbox_delete_capacity = QSpinBox(Dialog)
        self.spinbox_delete_capacity.setObjectName(u"spinbox_delete_capacity")

        self.horizontalLayout_3.addWidget(self.spinbox_delete_capacity)

        self.label_mb_text2 = QLabel(Dialog)
        self.label_mb_text2.setObjectName(u"label_mb_text2")

        self.horizontalLayout_3.addWidget(self.label_mb_text2)

        self.horizontalLayout_3.setStretch(2, 7)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_max_use_capacity_2 = QLabel(Dialog)
        self.label_max_use_capacity_2.setObjectName(u"label_max_use_capacity_2")

        self.horizontalLayout_6.addWidget(self.label_max_use_capacity_2)

        self.label_blank_2 = QLabel(Dialog)
        self.label_blank_2.setObjectName(u"label_blank_2")

        self.horizontalLayout_6.addWidget(self.label_blank_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.gridLayout.addLayout(self.verticalLayout_2, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_capacity_setting.setText(QCoreApplication.translate("Dialog", u"\uc800\uc7a5\uc6a9\ub7c9 \uc124\uc815", None))
        self.button_apply_setting.setText(QCoreApplication.translate("Dialog", u"\uc801\uc6a9", None))
        self.label_display_required_capacity_text.setText(QCoreApplication.translate("Dialog", u"\uc0ad\uc81c \uae30\uc900 \uc794\uc5ec\uacf5\uac04(MB)", None))
        self.label_mb_text.setText(QCoreApplication.translate("Dialog", u"MB", None))
        self.label_max_use_capacity.setText("")
        self.label_blank.setText(QCoreApplication.translate("Dialog", u"(max :10,000 MB)", None))
        self.label_display_delete_capacity_text.setText(QCoreApplication.translate("Dialog", u"\uc0ad\uc81c\ud560 \uc6a9\ub7c9(MB)", None))
        self.label_mb_text2.setText(QCoreApplication.translate("Dialog", u"MB", None))
        self.label_max_use_capacity_2.setText("")
        self.label_blank_2.setText(QCoreApplication.translate("Dialog", u"(max :200 MB)", None))
    # retranslateUi

