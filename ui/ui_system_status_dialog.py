# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'system_status_dialogmsjBPM.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1037, 637)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tab_widget_system_status = QTabWidget(Dialog)
        self.tab_widget_system_status.setObjectName(u"tab_widget_system_status")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_2 = QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scroll_area_cctv_status = QScrollArea(self.tab)
        self.scroll_area_cctv_status.setObjectName(u"scroll_area_cctv_status")
        self.scroll_area_cctv_status.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 993, 570))
        self.horizontalLayout_5 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.layout_cctv_status = QVBoxLayout()
        self.layout_cctv_status.setSpacing(6)
        self.layout_cctv_status.setObjectName(u"layout_cctv_status")
        self.label_cctv_status_widget = QLabel(self.scrollAreaWidgetContents)
        self.label_cctv_status_widget.setObjectName(u"label_cctv_status_widget")
        font = QFont()
        font.setPointSize(12)
        self.label_cctv_status_widget.setFont(font)
        self.label_cctv_status_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_cctv_status_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_cctv_status.addWidget(self.label_cctv_status_widget)


        self.horizontalLayout_5.addLayout(self.layout_cctv_status)

        self.scroll_area_cctv_status.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scroll_area_cctv_status)

        self.tab_widget_system_status.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scrollArea = QScrollArea(self.tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 993, 570))
        self.horizontalLayout_6 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.layout_event_status = QVBoxLayout()
        self.layout_event_status.setObjectName(u"layout_event_status")
        self.label_event_status_widget = QLabel(self.scrollAreaWidgetContents_2)
        self.label_event_status_widget.setObjectName(u"label_event_status_widget")
        self.label_event_status_widget.setFont(font)
        self.label_event_status_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_event_status_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_status.addWidget(self.label_event_status_widget)


        self.horizontalLayout_6.addLayout(self.layout_event_status)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_3.addWidget(self.scrollArea)

        self.tab_widget_system_status.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.layout_server_status = QVBoxLayout()
        self.layout_server_status.setObjectName(u"layout_server_status")
        self.label_server_status_widget = QLabel(self.tab_3)
        self.label_server_status_widget.setObjectName(u"label_server_status_widget")
        self.label_server_status_widget.setFont(font)
        self.label_server_status_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_server_status_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_server_status.addWidget(self.label_server_status_widget)


        self.horizontalLayout_4.addLayout(self.layout_server_status)

        self.tab_widget_system_status.addTab(self.tab_3, "")

        self.horizontalLayout.addWidget(self.tab_widget_system_status)


        self.retranslateUi(Dialog)

        self.tab_widget_system_status.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_cctv_status_widget.setText(QCoreApplication.translate("Dialog", u"CCTV \uc0c1\ud0dc \uac10\uc9c0 \uc704\uc82f", None))
        self.tab_widget_system_status.setTabText(self.tab_widget_system_status.indexOf(self.tab), QCoreApplication.translate("Dialog", u"CCTV", None))
        self.label_event_status_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \uac10\uc9c0 \uc0c1\ud0dc \uc704\uc82f", None))
        self.tab_widget_system_status.setTabText(self.tab_widget_system_status.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\ubd88\uc548\uc804 \uc0c1\ud669 \uac10\uc9c0", None))
        self.label_server_status_widget.setText(QCoreApplication.translate("Dialog", u"\uc11c\ubc84 \uc0c1\ud0dc \uc704\uc82f", None))
        self.tab_widget_system_status.setTabText(self.tab_widget_system_status.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"\uc11c\ubc84", None))
    # retranslateUi

