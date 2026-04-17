# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'event_logic_management_widgetUYFeuK.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(839, 682)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_unsafelist = QLabel(Widget)
        self.label_unsafelist.setObjectName(u"label_unsafelist")
        font = QFont()
        font.setPointSize(16)
        self.label_unsafelist.setFont(font)
        self.label_unsafelist.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_unsafelist)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.button_delete_event = QPushButton(Widget)
        self.button_delete_event.setObjectName(u"button_delete_event")

        self.horizontalLayout.addWidget(self.button_delete_event)

        self.button_add_event = QPushButton(Widget)
        self.button_add_event.setObjectName(u"button_add_event")

        self.horizontalLayout.addWidget(self.button_add_event)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tablewidget_event_list = QTableWidget(Widget)
        if (self.tablewidget_event_list.columnCount() < 1):
            self.tablewidget_event_list.setColumnCount(1)
        font1 = QFont()
        font1.setPointSize(9)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font1);
        self.tablewidget_event_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.tablewidget_event_list.rowCount() < 2):
            self.tablewidget_event_list.setRowCount(2)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tablewidget_event_list.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablewidget_event_list.setVerticalHeaderItem(1, __qtablewidgetitem2)
        self.tablewidget_event_list.setObjectName(u"tablewidget_event_list")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablewidget_event_list.sizePolicy().hasHeightForWidth())
        self.tablewidget_event_list.setSizePolicy(sizePolicy)
        self.tablewidget_event_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tablewidget_event_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.tablewidget_event_list)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_unsafelist.setText(QCoreApplication.translate("Widget", u"\ubd88\uc548\uc804 \uc0c1\ud669 \uac10\uc9c0 \uc774\ubca4\ud2b8", None))
        self.button_delete_event.setText(QCoreApplication.translate("Widget", u"\uc774\ubca4\ud2b8 \uc0ad\uc81c", None))
        self.button_add_event.setText(QCoreApplication.translate("Widget", u"\uc774\ubca4\ud2b8 \ucd94\uac00", None))
        ___qtablewidgetitem = self.tablewidget_event_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Widget", u"\uc774\ubca4\ud2b8\uba85", None));
    # retranslateUi

