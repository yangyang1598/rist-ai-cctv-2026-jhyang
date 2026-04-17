# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'model_management_widgetDSwuiC.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(893, 651)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_ai_list = QLabel(Widget)
        self.label_ai_list.setObjectName(u"label_ai_list")
        font = QFont()
        font.setPointSize(16)
        self.label_ai_list.setFont(font)
        self.label_ai_list.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_ai_list)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_delete_model = QPushButton(Widget)
        self.button_delete_model.setObjectName(u"button_delete_model")

        self.horizontalLayout.addWidget(self.button_delete_model)

        self.button_add_new_model = QPushButton(Widget)
        self.button_add_new_model.setObjectName(u"button_add_new_model")

        self.horizontalLayout.addWidget(self.button_add_new_model)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableview_model_list = QTableView(Widget)
        self.tableview_model_list.setObjectName(u"tableview_model_list")

        self.verticalLayout.addWidget(self.tableview_model_list)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_ai_list.setText(QCoreApplication.translate("Widget", u"AI \ubaa8\ub378 \ubaa9\ub85d", None))
        self.button_delete_model.setText(QCoreApplication.translate("Widget", u"\ubaa8\ub378 \uc0ad\uc81c", None))
        self.button_add_new_model.setText(QCoreApplication.translate("Widget", u"\ubaa8\ub378 \ub4f1\ub85d", None))
    # retranslateUi

