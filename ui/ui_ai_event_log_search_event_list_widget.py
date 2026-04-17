# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_search_event_list_widgetVuSgfC.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLineEdit,
    QListView, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(254, 300)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 3, 0, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_edit_event_search = QLineEdit(Widget)
        self.line_edit_event_search.setObjectName(u"line_edit_event_search")

        self.horizontalLayout.addWidget(self.line_edit_event_search)

        self.button_event_search = QPushButton(Widget)
        self.button_event_search.setObjectName(u"button_event_search")

        self.horizontalLayout.addWidget(self.button_event_search)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.list_view_event_list = QListView(Widget)
        self.list_view_event_list.setObjectName(u"list_view_event_list")
        self.list_view_event_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list_view_event_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout.addWidget(self.list_view_event_list)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.button_event_search.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9", None))
    # retranslateUi

