# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_search_dialoggZrYcj.ui'
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
    QPushButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1150, 700)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_event_log_search = QLabel(Dialog)
        self.label_event_log_search.setObjectName(u"label_event_log_search")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        self.label_event_log_search.setFont(font)

        self.verticalLayout.addWidget(self.label_event_log_search)

        self.layout_event_log_search = QHBoxLayout()
        self.layout_event_log_search.setObjectName(u"layout_event_log_search")
        self.layout_event_log_search.setContentsMargins(5, -1, -1, -1)
        self.layout_event_log_filter_search = QVBoxLayout()
        self.layout_event_log_filter_search.setObjectName(u"layout_event_log_filter_search")
        self.layout_event_log_filter_search.setContentsMargins(-1, -1, 5, -1)
        self.label_ai_event_log_filter_search_widget = QLabel(Dialog)
        self.label_ai_event_log_filter_search_widget.setObjectName(u"label_ai_event_log_filter_search_widget")
        self.label_ai_event_log_filter_search_widget.setMinimumSize(QSize(0, 200))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_ai_event_log_filter_search_widget.setFont(font1)
        self.label_ai_event_log_filter_search_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_filter_search_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_log_filter_search.addWidget(self.label_ai_event_log_filter_search_widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.layout_cctv_list = QVBoxLayout()
        self.layout_cctv_list.setObjectName(u"layout_cctv_list")
        self.label_cctv_list = QLabel(Dialog)
        self.label_cctv_list.setObjectName(u"label_cctv_list")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_cctv_list.setFont(font2)
        self.label_cctv_list.setMargin(0)
        self.label_cctv_list.setIndent(0)

        self.layout_cctv_list.addWidget(self.label_cctv_list)

        self.label_ai_event_log_search_cctv_list_widget = QLabel(Dialog)
        self.label_ai_event_log_search_cctv_list_widget.setObjectName(u"label_ai_event_log_search_cctv_list_widget")
        self.label_ai_event_log_search_cctv_list_widget.setFont(font1)
        self.label_ai_event_log_search_cctv_list_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_search_cctv_list_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_cctv_list.addWidget(self.label_ai_event_log_search_cctv_list_widget)

        self.layout_cctv_list.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.layout_cctv_list)

        self.layout_event_list = QVBoxLayout()
        self.layout_event_list.setObjectName(u"layout_event_list")
        self.label_event_list = QLabel(Dialog)
        self.label_event_list.setObjectName(u"label_event_list")
        self.label_event_list.setFont(font2)

        self.layout_event_list.addWidget(self.label_event_list)

        self.label_ai_event_log_search_event_list_widget = QLabel(Dialog)
        self.label_ai_event_log_search_event_list_widget.setObjectName(u"label_ai_event_log_search_event_list_widget")
        self.label_ai_event_log_search_event_list_widget.setFont(font1)
        self.label_ai_event_log_search_event_list_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_search_event_list_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_list.addWidget(self.label_ai_event_log_search_event_list_widget)

        self.layout_event_list.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.layout_event_list)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.layout_event_log_filter_search.addLayout(self.horizontalLayout)

        self.layout_event_log_filter_search.setStretch(1, 1)

        self.layout_event_log_search.addLayout(self.layout_event_log_filter_search)

        self.layout_event_log = QVBoxLayout()
        self.layout_event_log.setObjectName(u"layout_event_log")
        self.layout_event_log.setContentsMargins(5, 0, 5, -1)
        self.layout_button = QHBoxLayout()
        self.layout_button.setObjectName(u"layout_button")
        self.button_refresh = QPushButton(Dialog)
        self.button_refresh.setObjectName(u"button_refresh")

        self.layout_button.addWidget(self.button_refresh)

        self.button_report = QPushButton(Dialog)
        self.button_report.setObjectName(u"button_report")

        self.layout_button.addWidget(self.button_report)


        self.layout_event_log.addLayout(self.layout_button)

        self.tab_widget_event_log = QTabWidget(Dialog)
        self.tab_widget_event_log.setObjectName(u"tab_widget_event_log")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_4 = QHBoxLayout(self.tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.layout_event_log_list = QVBoxLayout()
        self.layout_event_log_list.setSpacing(6)
        self.layout_event_log_list.setObjectName(u"layout_event_log_list")
        self.label_ai_event_log_paging_widget = QLabel(self.tab)
        self.label_ai_event_log_paging_widget.setObjectName(u"label_ai_event_log_paging_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ai_event_log_paging_widget.sizePolicy().hasHeightForWidth())
        self.label_ai_event_log_paging_widget.setSizePolicy(sizePolicy)
        self.label_ai_event_log_paging_widget.setFont(font1)
        self.label_ai_event_log_paging_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_paging_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_log_list.addWidget(self.label_ai_event_log_paging_widget)


        self.horizontalLayout_4.addLayout(self.layout_event_log_list)

        self.tab_widget_event_log.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.layout_event_log_graph = QVBoxLayout()
        self.layout_event_log_graph.setObjectName(u"layout_event_log_graph")
        self.label_ai_event_log_graph_widget = QLabel(self.tab_2)
        self.label_ai_event_log_graph_widget.setObjectName(u"label_ai_event_log_graph_widget")
        self.label_ai_event_log_graph_widget.setFont(font1)
        self.label_ai_event_log_graph_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_graph_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_log_graph.addWidget(self.label_ai_event_log_graph_widget)


        self.horizontalLayout_2.addLayout(self.layout_event_log_graph)

        self.tab_widget_event_log.addTab(self.tab_2, "")

        self.layout_event_log.addWidget(self.tab_widget_event_log)

        self.label_ai_event_log_selected_image_widget = QLabel(Dialog)
        self.label_ai_event_log_selected_image_widget.setObjectName(u"label_ai_event_log_selected_image_widget")
        self.label_ai_event_log_selected_image_widget.setFont(font1)
        self.label_ai_event_log_selected_image_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_selected_image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_event_log.addWidget(self.label_ai_event_log_selected_image_widget)

        self.layout_event_log.setStretch(1, 3)
        self.layout_event_log.setStretch(2, 1)

        self.layout_event_log_search.addLayout(self.layout_event_log)

        self.layout_event_log_search.setStretch(0, 1)
        self.layout_event_log_search.setStretch(1, 2)

        self.verticalLayout.addLayout(self.layout_event_log_search)


        self.retranslateUi(Dialog)

        self.tab_widget_event_log.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_event_log_search.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \uac80\uc0c9", None))
        self.label_ai_event_log_filter_search_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \ud544\ud130 \uac80\uc0c9 \uc704\uc82f", None))
        self.label_cctv_list.setText(QCoreApplication.translate("Dialog", u"\u25bc CCTV \ubaa9\ub85d", None))
        self.label_ai_event_log_search_cctv_list_widget.setText(QCoreApplication.translate("Dialog", u"CCTV \ubaa9\ub85d \uc704\uc82f", None))
        self.label_event_list.setText(QCoreApplication.translate("Dialog", u"\u25bc \uc774\ubca4\ud2b8 \ubaa9\ub85d", None))
        self.label_ai_event_log_search_event_list_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ubaa9\ub85d \uc704\uc82f", None))
        self.button_refresh.setText(QCoreApplication.translate("Dialog", u"\uc0c8\ub85c\uace0\uce68", None))
        self.button_report.setText(QCoreApplication.translate("Dialog", u"\ubcf4\uace0\uc11c \uc791\uc131", None))
        self.label_ai_event_log_paging_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \uc704\uc82f", None))
        self.tab_widget_event_log.setTabText(self.tab_widget_event_log.indexOf(self.tab), QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8", None))
        self.label_ai_event_log_graph_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \uadf8\ub798\ud504 \uc704\uc82f", None))
        self.tab_widget_event_log.setTabText(self.tab_widget_event_log.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ud1b5\uacc4", None))
        self.label_ai_event_log_selected_image_widget.setText(QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \uc120\ud0dd \uc774\ubbf8\uc9c0 \uc704\uc82f", None))
    # retranslateUi

