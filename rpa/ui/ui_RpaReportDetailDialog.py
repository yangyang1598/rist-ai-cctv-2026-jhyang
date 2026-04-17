# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaReportDetailDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_RpaReportDetailDialog(object):
    def setupUi(self, RpaReportDetailDialog):
        if not RpaReportDetailDialog.objectName():
            RpaReportDetailDialog.setObjectName(u"RpaReportDetailDialog")
        RpaReportDetailDialog.resize(828, 893)
        self.gridLayout_2 = QGridLayout(RpaReportDetailDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(RpaReportDetailDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Close)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(RpaReportDetailDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -230, 791, 1051))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_image = QLabel(self.scrollAreaWidgetContents)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setMinimumSize(QSize(0, 400))
        self.label_image.setStyleSheet(u"background-color: rgb(150, 150, 150);")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_image, 1, 1, 1, 2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(120, 16777215))

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.dateTimeEdit_event_time = QDateTimeEdit(self.scrollAreaWidgetContents)
        self.dateTimeEdit_event_time.setObjectName(u"dateTimeEdit_event_time")
        self.dateTimeEdit_event_time.setMinimumSize(QSize(200, 0))
        self.dateTimeEdit_event_time.setCalendarPopup(True)

        self.gridLayout.addWidget(self.dateTimeEdit_event_time, 4, 1, 1, 1)

        self.plainTextEdit_action = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit_action.setObjectName(u"plainTextEdit_action")

        self.gridLayout.addWidget(self.plainTextEdit_action, 12, 1, 1, 2)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 5, 0, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 17, 0, 1, 1)

        self.checkBox_event_type_custom = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_event_type_custom.setObjectName(u"checkBox_event_type_custom")

        self.gridLayout.addWidget(self.checkBox_event_type_custom, 10, 1, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 12, 0, 1, 1)

        self.pushButton_event_time_today = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_event_time_today.setObjectName(u"pushButton_event_time_today")
        self.pushButton_event_time_today.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.pushButton_event_time_today, 4, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 17, 2, 1, 1)

        self.lineEdit_location = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_location.setObjectName(u"lineEdit_location")

        self.gridLayout.addWidget(self.lineEdit_location, 8, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 17, 1, 1, 1)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_8 = QGridLayout(self.groupBox)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.radioButton_severity_danger_high = QRadioButton(self.groupBox)
        self.radioButton_severity_danger_high.setObjectName(u"radioButton_severity_danger_high")

        self.gridLayout_7.addWidget(self.radioButton_severity_danger_high, 1, 0, 1, 1)

        self.radioButton_severity_danger_mid = QRadioButton(self.groupBox)
        self.radioButton_severity_danger_mid.setObjectName(u"radioButton_severity_danger_mid")
        self.radioButton_severity_danger_mid.setChecked(True)

        self.gridLayout_7.addWidget(self.radioButton_severity_danger_mid, 2, 0, 1, 1)

        self.radioButton_severity_danger_highhigh = QRadioButton(self.groupBox)
        self.radioButton_severity_danger_highhigh.setObjectName(u"radioButton_severity_danger_highhigh")

        self.gridLayout_7.addWidget(self.radioButton_severity_danger_highhigh, 0, 0, 1, 1)

        self.radioButton_severity_good_highhigh = QRadioButton(self.groupBox)
        self.radioButton_severity_good_highhigh.setObjectName(u"radioButton_severity_good_highhigh")

        self.gridLayout_7.addWidget(self.radioButton_severity_good_highhigh, 0, 1, 1, 1)

        self.radioButton_severity_danger_low = QRadioButton(self.groupBox)
        self.radioButton_severity_danger_low.setObjectName(u"radioButton_severity_danger_low")

        self.gridLayout_7.addWidget(self.radioButton_severity_danger_low, 3, 0, 1, 1)

        self.radioButton_severity_good_high = QRadioButton(self.groupBox)
        self.radioButton_severity_good_high.setObjectName(u"radioButton_severity_good_high")

        self.gridLayout_7.addWidget(self.radioButton_severity_good_high, 1, 1, 1, 1)

        self.radioButton_severity_danger_lowlow = QRadioButton(self.groupBox)
        self.radioButton_severity_danger_lowlow.setObjectName(u"radioButton_severity_danger_lowlow")

        self.gridLayout_7.addWidget(self.radioButton_severity_danger_lowlow, 4, 0, 1, 1)

        self.radioButton_severity_good_mid = QRadioButton(self.groupBox)
        self.radioButton_severity_good_mid.setObjectName(u"radioButton_severity_good_mid")

        self.gridLayout_7.addWidget(self.radioButton_severity_good_mid, 2, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 11, 1, 1, 2)

        self.lineEdit_id = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_id.setObjectName(u"lineEdit_id")
        self.lineEdit_id.setEnabled(False)
        self.lineEdit_id.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_id, 3, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.lineEdit_event_type_custom = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_event_type_custom.setObjectName(u"lineEdit_event_type_custom")

        self.gridLayout.addWidget(self.lineEdit_event_type_custom, 10, 2, 1, 1)

        self.lineEdit_title = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_title.setObjectName(u"lineEdit_title")

        self.gridLayout.addWidget(self.lineEdit_title, 7, 1, 1, 2)

        self.dateTimeEdit_report_time = QDateTimeEdit(self.scrollAreaWidgetContents)
        self.dateTimeEdit_report_time.setObjectName(u"dateTimeEdit_report_time")
        self.dateTimeEdit_report_time.setCalendarPopup(True)

        self.gridLayout.addWidget(self.dateTimeEdit_report_time, 5, 1, 1, 1)

        self.scrollArea_2 = QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setMinimumSize(QSize(0, 120))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 683, 118))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_event_type = QGridLayout()
        self.gridLayout_event_type.setObjectName(u"gridLayout_event_type")
        self.checkBox = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_event_type.addWidget(self.checkBox, 0, 0, 1, 1)

        self.checkBox_4 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_event_type.addWidget(self.checkBox_4, 0, 3, 1, 1)

        self.checkBox_3 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_event_type.addWidget(self.checkBox_3, 0, 2, 1, 1)

        self.checkBox_2 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_event_type.addWidget(self.checkBox_2, 0, 1, 1, 1)

        self.checkBox_5 = QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout_event_type.addWidget(self.checkBox_5, 1, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_event_type, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout.addWidget(self.scrollArea_2, 9, 1, 1, 2)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 11, 0, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)

        self.pushButton_report_time_today = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_report_time_today.setObjectName(u"pushButton_report_time_today")
        self.pushButton_report_time_today.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.pushButton_report_time_today, 5, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 16, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_image_path = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_image_path.setObjectName(u"lineEdit_image_path")

        self.horizontalLayout_4.addWidget(self.lineEdit_image_path)

        self.pushButton_image_path_open = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_image_path_open.setObjectName(u"pushButton_image_path_open")

        self.horizontalLayout_4.addWidget(self.pushButton_image_path_open)


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 1, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 2)

        self.label_dialog_title = QLabel(RpaReportDetailDialog)
        self.label_dialog_title.setObjectName(u"label_dialog_title")

        self.gridLayout_2.addWidget(self.label_dialog_title, 0, 0, 1, 2)

        QWidget.setTabOrder(self.lineEdit_image_path, self.pushButton_image_path_open)
        QWidget.setTabOrder(self.pushButton_image_path_open, self.lineEdit_id)
        QWidget.setTabOrder(self.lineEdit_id, self.dateTimeEdit_event_time)
        QWidget.setTabOrder(self.dateTimeEdit_event_time, self.pushButton_event_time_today)
        QWidget.setTabOrder(self.pushButton_event_time_today, self.dateTimeEdit_report_time)
        QWidget.setTabOrder(self.dateTimeEdit_report_time, self.pushButton_report_time_today)
        QWidget.setTabOrder(self.pushButton_report_time_today, self.lineEdit_title)
        QWidget.setTabOrder(self.lineEdit_title, self.lineEdit_location)
        QWidget.setTabOrder(self.lineEdit_location, self.scrollArea_2)
        QWidget.setTabOrder(self.scrollArea_2, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.checkBox_2)
        QWidget.setTabOrder(self.checkBox_2, self.checkBox_3)
        QWidget.setTabOrder(self.checkBox_3, self.checkBox_4)
        QWidget.setTabOrder(self.checkBox_4, self.checkBox_5)
        QWidget.setTabOrder(self.checkBox_5, self.checkBox_event_type_custom)
        QWidget.setTabOrder(self.checkBox_event_type_custom, self.lineEdit_event_type_custom)
        QWidget.setTabOrder(self.lineEdit_event_type_custom, self.radioButton_severity_danger_highhigh)
        QWidget.setTabOrder(self.radioButton_severity_danger_highhigh, self.radioButton_severity_danger_high)
        QWidget.setTabOrder(self.radioButton_severity_danger_high, self.radioButton_severity_danger_mid)
        QWidget.setTabOrder(self.radioButton_severity_danger_mid, self.radioButton_severity_danger_low)
        QWidget.setTabOrder(self.radioButton_severity_danger_low, self.radioButton_severity_danger_lowlow)
        QWidget.setTabOrder(self.radioButton_severity_danger_lowlow, self.radioButton_severity_good_highhigh)
        QWidget.setTabOrder(self.radioButton_severity_good_highhigh, self.radioButton_severity_good_high)
        QWidget.setTabOrder(self.radioButton_severity_good_high, self.radioButton_severity_good_mid)
        QWidget.setTabOrder(self.radioButton_severity_good_mid, self.plainTextEdit_action)
        QWidget.setTabOrder(self.plainTextEdit_action, self.scrollArea)

        self.retranslateUi(RpaReportDetailDialog)
        self.buttonBox.accepted.connect(RpaReportDetailDialog.accept)
        self.buttonBox.rejected.connect(RpaReportDetailDialog.reject)

        QMetaObject.connectSlotsByName(RpaReportDetailDialog)
    # setupUi

    def retranslateUi(self, RpaReportDetailDialog):
        RpaReportDetailDialog.setWindowTitle(QCoreApplication.translate("RpaReportDetailDialog", u"\ubcf4\uace0\uc11c", None))
        self.label_4.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc0ac\uc9c4", None))
        self.label_image.setText(QCoreApplication.translate("RpaReportDetailDialog", u"[Image]", None))
        self.label_3.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ubc1c\uc0dd\uc77c\uc2dc", None))
        self.dateTimeEdit_event_time.setDisplayFormat(QCoreApplication.translate("RpaReportDetailDialog", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_11.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ubcf4\uace0\uc77c\uc2dc", None))
        self.label_8.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc7a5\uc18c", None))
        self.checkBox_event_type_custom.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc704\ud5d8\uc720\ud615 \uc9c1\uc811\uc785\ub825", None))
        self.label_9.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc704\ud5d8\uc720\ud615", None))
        self.label_5.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ub300\uc751\uc870\uce58", None))
        self.pushButton_event_time_today.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ud604\uc7ac\uc2dc\uac01", None))
        self.groupBox.setTitle(QCoreApplication.translate("RpaReportDetailDialog", u"\uc120\ud0dd", None))
        self.radioButton_severity_danger_high.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc2ec\uac01", None))
        self.radioButton_severity_danger_mid.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc704\ud5d8", None))
        self.radioButton_severity_danger_highhigh.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ub9e4\uc6b0 \uc2ec\uac01", None))
        self.radioButton_severity_good_highhigh.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ub9e4\uc6b0 \uc6b0\uc218", None))
        self.radioButton_severity_danger_low.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uacbd\ubbf8", None))
        self.radioButton_severity_good_high.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc6b0\uc218", None))
        self.radioButton_severity_danger_lowlow.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ub9e4\uc6b0 \uacbd\ubbf8", None))
        self.radioButton_severity_good_mid.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc815\uc0c1", None))
        self.label_6.setText(QCoreApplication.translate("RpaReportDetailDialog", u"ID", None))
        self.dateTimeEdit_report_time.setDisplayFormat(QCoreApplication.translate("RpaReportDetailDialog", u"yyyy-MM-dd HH:mm:ss", None))
        self.checkBox.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uac00_\uc704\ud5d8\uc720\ud615", None))
        self.checkBox_4.setText(QCoreApplication.translate("RpaReportDetailDialog", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("RpaReportDetailDialog", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ub098_\uc704\ud5d8\uc720\ud615", None))
        self.checkBox_5.setText(QCoreApplication.translate("RpaReportDetailDialog", u"CheckBox", None))
        self.label_10.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc2ec\uac01\ub3c4", None))
        self.label_2.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc81c\ubaa9", None))
        self.pushButton_report_time_today.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\ud604\uc7ac\uc2dc\uac01", None))
        self.pushButton_image_path_open.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc5f4\uae30", None))
        self.label_dialog_title.setText(QCoreApplication.translate("RpaReportDetailDialog", u"\uc0c8 \ubcf4\uace0\uc11c", None))
    # retranslateUi

