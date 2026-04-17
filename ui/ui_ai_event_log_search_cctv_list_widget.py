# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_search_cctv_list_widgetDOTmAy.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLineEdit, QPushButton, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)

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
        self.line_edit_cctv_search = QLineEdit(Widget)
        self.line_edit_cctv_search.setObjectName(u"line_edit_cctv_search")

        self.horizontalLayout.addWidget(self.line_edit_cctv_search)

        self.button_cctv_search = QPushButton(Widget)
        self.button_cctv_search.setObjectName(u"button_cctv_search")

        self.horizontalLayout.addWidget(self.button_cctv_search)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree_view_cctv_list = QTreeView(Widget)
        self.tree_view_cctv_list.setObjectName(u"tree_view_cctv_list")
        self.tree_view_cctv_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.verticalLayout.addWidget(self.tree_view_cctv_list)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.button_cctv_search.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9", None))
    # retranslateUi

