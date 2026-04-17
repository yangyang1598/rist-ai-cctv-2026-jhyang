# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'event_logic_add_dialogqGOMrD.ui'
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
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1020, 684)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_input_img_size = QLabel(Dialog)
        self.label_input_img_size.setObjectName(u"label_input_img_size")
        font1 = QFont()
        font1.setPointSize(11)
        self.label_input_img_size.setFont(font1)

        self.gridLayout_3.addWidget(self.label_input_img_size, 2, 0, 1, 1)

        self.line_edit_input_img_size = QLineEdit(Dialog)
        self.line_edit_input_img_size.setObjectName(u"line_edit_input_img_size")

        self.gridLayout_3.addWidget(self.line_edit_input_img_size, 2, 1, 1, 1)

        self.label_skip_frame = QLabel(Dialog)
        self.label_skip_frame.setObjectName(u"label_skip_frame")
        self.label_skip_frame.setFont(font1)

        self.gridLayout_3.addWidget(self.label_skip_frame, 1, 0, 1, 1)

        self.label_rist_level = QLabel(Dialog)
        self.label_rist_level.setObjectName(u"label_rist_level")
        self.label_rist_level.setFont(font1)

        self.gridLayout_3.addWidget(self.label_rist_level, 5, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radio_left = QRadioButton(Dialog)
        self.radio_left.setObjectName(u"radio_left")

        self.horizontalLayout_5.addWidget(self.radio_left)

        self.radio_right = QRadioButton(Dialog)
        self.radio_right.setObjectName(u"radio_right")

        self.horizontalLayout_5.addWidget(self.radio_right)

        self.radio_top_side = QRadioButton(Dialog)
        self.radio_top_side.setObjectName(u"radio_top_side")

        self.horizontalLayout_5.addWidget(self.radio_top_side)

        self.radio_under_side = QRadioButton(Dialog)
        self.radio_under_side.setObjectName(u"radio_under_side")

        self.horizontalLayout_5.addWidget(self.radio_under_side)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 3, 1, 1, 1)

        self.label_event_name = QLabel(Dialog)
        self.label_event_name.setObjectName(u"label_event_name")
        self.label_event_name.setFont(font1)

        self.gridLayout_3.addWidget(self.label_event_name, 0, 0, 1, 1)

        self.spinbox_skip_frame = QSpinBox(Dialog)
        self.spinbox_skip_frame.setObjectName(u"spinbox_skip_frame")
        self.spinbox_skip_frame.setMinimum(1)
        self.spinbox_skip_frame.setMaximum(60)

        self.gridLayout_3.addWidget(self.spinbox_skip_frame, 1, 1, 1, 1)

        self.line_edit_event_name = QLineEdit(Dialog)
        self.line_edit_event_name.setObjectName(u"line_edit_event_name")

        self.gridLayout_3.addWidget(self.line_edit_event_name, 0, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radio_danger_lowlow = QRadioButton(Dialog)
        self.radio_danger_lowlow.setObjectName(u"radio_danger_lowlow")
        font2 = QFont()
        font2.setPointSize(8)
        self.radio_danger_lowlow.setFont(font2)
        self.radio_danger_lowlow.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radio_danger_lowlow)

        self.radio_danger_low = QRadioButton(Dialog)
        self.radio_danger_low.setObjectName(u"radio_danger_low")
        self.radio_danger_low.setFont(font2)

        self.horizontalLayout_4.addWidget(self.radio_danger_low)

        self.radio_danger_mid = QRadioButton(Dialog)
        self.radio_danger_mid.setObjectName(u"radio_danger_mid")
        self.radio_danger_mid.setFont(font2)

        self.horizontalLayout_4.addWidget(self.radio_danger_mid)

        self.radio_danger_high = QRadioButton(Dialog)
        self.radio_danger_high.setObjectName(u"radio_danger_high")
        self.radio_danger_high.setFont(font2)

        self.horizontalLayout_4.addWidget(self.radio_danger_high)

        self.radio_danger_highhigh = QRadioButton(Dialog)
        self.radio_danger_highhigh.setObjectName(u"radio_danger_highhigh")
        self.radio_danger_highhigh.setFont(font2)

        self.horizontalLayout_4.addWidget(self.radio_danger_highhigh)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 5, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_event_process_logic = QLabel(Dialog)
        self.label_event_process_logic.setObjectName(u"label_event_process_logic")
        self.label_event_process_logic.setFont(font1)

        self.horizontalLayout.addWidget(self.label_event_process_logic)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_add_event_process = QPushButton(Dialog)
        self.button_add_event_process.setObjectName(u"button_add_event_process")
        font3 = QFont()
        font3.setPointSize(13)
        font3.setBold(True)
        self.button_add_event_process.setFont(font3)

        self.horizontalLayout.addWidget(self.button_add_event_process)

        self.button_del_event_process = QPushButton(Dialog)
        self.button_del_event_process.setObjectName(u"button_del_event_process")
        font4 = QFont()
        font4.setPointSize(14)
        font4.setBold(True)
        self.button_del_event_process.setFont(font4)

        self.horizontalLayout.addWidget(self.button_del_event_process)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.button_event_up = QPushButton(Dialog)
        self.button_event_up.setObjectName(u"button_event_up")

        self.horizontalLayout_2.addWidget(self.button_event_up)

        self.button_event_down = QPushButton(Dialog)
        self.button_event_down.setObjectName(u"button_event_down")

        self.horizontalLayout_2.addWidget(self.button_event_down)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.listwidget_logic_list = QListWidget(Dialog)
        self.listwidget_logic_list.setObjectName(u"listwidget_logic_list")

        self.gridLayout.addWidget(self.listwidget_logic_list, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_val = QPushButton(Dialog)
        self.button_val.setObjectName(u"button_val")

        self.horizontalLayout_3.addWidget(self.button_val)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.button_add_event_data = QPushButton(Dialog)
        self.button_add_event_data.setObjectName(u"button_add_event_data")

        self.horizontalLayout_3.addWidget(self.button_add_event_data)


        self.gridLayout.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\ubd88\uc548\uc804 \uc0c1\ud669 \uac10\uc9c0 \uc774\ubca4\ud2b8 \ucd94\uac00", None))
        self.label_input_img_size.setText(QCoreApplication.translate("Dialog", u"Input Image Size", None))
        self.label_skip_frame.setText(QCoreApplication.translate("Dialog", u"Skip Frame", None))
        self.label_rist_level.setText(QCoreApplication.translate("Dialog", u"\uc704\ud5d8\ub3c4 \uc124\uc815", None))
        self.radio_left.setText(QCoreApplication.translate("Dialog", u"Left(\uc67c\ucabd)", None))
        self.radio_right.setText(QCoreApplication.translate("Dialog", u"Right(\uc624\ub978\ucabd)", None))
        self.radio_top_side.setText(QCoreApplication.translate("Dialog", u"Top-side(\uc704\ucabd)", None))
        self.radio_under_side.setText(QCoreApplication.translate("Dialog", u"Under-side(\uc544\ub798\ucabd)", None))
        self.label_event_name.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \uba85", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\uc9c0\uc801\ud655\uc778 \ubc29\ud5a5 \uc124\uc815", None))
        self.radio_danger_lowlow.setText(QCoreApplication.translate("Dialog", u"Danger_Lowlow(\ub9e4\uc6b0 \uacbd\ubbf8)", None))
        self.radio_danger_low.setText(QCoreApplication.translate("Dialog", u"Danger_Low(\uacbd\ubbf8)", None))
        self.radio_danger_mid.setText(QCoreApplication.translate("Dialog", u"Danger_Mid(\uc704\ud5d8)", None))
        self.radio_danger_high.setText(QCoreApplication.translate("Dialog", u"Danger_High(\uc2ec\uac01)", None))
        self.radio_danger_highhigh.setText(QCoreApplication.translate("Dialog", u"Danger_Highhigh(\ub9e4\uc6b0 \uc2ec\uac01)", None))
        self.label_event_process_logic.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ubc1c\uc0dd \ub85c\uc9c1", None))
        self.button_add_event_process.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.button_del_event_process.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.button_event_up.setText(QCoreApplication.translate("Dialog", u"\u25b2", None))
        self.button_event_down.setText(QCoreApplication.translate("Dialog", u"\u25bc", None))
        self.button_val.setText(QCoreApplication.translate("Dialog", u"\uac80\uc99d", None))
        self.button_add_event_data.setText(QCoreApplication.translate("Dialog", u"\ud655\uc778", None))
    # retranslateUi

