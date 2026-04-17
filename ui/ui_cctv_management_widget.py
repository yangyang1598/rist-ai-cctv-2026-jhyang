# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_management_widgetvOxufk.ui'
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
        Widget.resize(862, 464)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_cctv_management = QLabel(Widget)
        self.label_cctv_management.setObjectName(u"label_cctv_management")
        self.label_cctv_management.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(16)
        self.label_cctv_management.setFont(font)
        self.label_cctv_management.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_cctv_management)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.button_add_cctv = QPushButton(Widget)
        self.button_add_cctv.setObjectName(u"button_add_cctv")

        self.horizontalLayout.addWidget(self.button_add_cctv)

        self.button_delete_cctv = QPushButton(Widget)
        self.button_delete_cctv.setObjectName(u"button_delete_cctv")

        self.horizontalLayout.addWidget(self.button_delete_cctv)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.table_widget_cctv_management = QTableWidget(Widget)
        if (self.table_widget_cctv_management.columnCount() < 2):
            self.table_widget_cctv_management.setColumnCount(2)
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font1);
        self.table_widget_cctv_management.setHorizontalHeaderItem(0, __qtablewidgetitem)
        font2 = QFont()
        font2.setBold(True)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font2);
        self.table_widget_cctv_management.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.table_widget_cctv_management.rowCount() < 2):
            self.table_widget_cctv_management.setRowCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_management.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_cctv_management.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_management.setItem(0, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_management.setItem(0, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_management.setItem(1, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_management.setItem(1, 1, __qtablewidgetitem7)
        self.table_widget_cctv_management.setObjectName(u"table_widget_cctv_management")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_widget_cctv_management.sizePolicy().hasHeightForWidth())
        self.table_widget_cctv_management.setSizePolicy(sizePolicy)
        self.table_widget_cctv_management.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_widget_cctv_management.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_widget_cctv_management.horizontalHeader().setDefaultSectionSize(400)
        self.table_widget_cctv_management.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.table_widget_cctv_management)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_cctv_management.setText(QCoreApplication.translate("Widget", u"CCTV \uad00\ub9ac", None))
        self.button_add_cctv.setText(QCoreApplication.translate("Widget", u"CCTV \ucd94\uac00", None))
        self.button_delete_cctv.setText(QCoreApplication.translate("Widget", u"CCTV \uc0ad\uc81c", None))
        ___qtablewidgetitem = self.table_widget_cctv_management.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Widget", u"\uc774\ub984", None));
        ___qtablewidgetitem1 = self.table_widget_cctv_management.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Widget", u"IP", None));

        __sortingEnabled = self.table_widget_cctv_management.isSortingEnabled()
        self.table_widget_cctv_management.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.table_widget_cctv_management.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Widget", u"CCTV 01", None));
        ___qtablewidgetitem3 = self.table_widget_cctv_management.item(0, 1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Widget", u"192.168.0.1", None));
        ___qtablewidgetitem4 = self.table_widget_cctv_management.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Widget", u"CCTV 02", None));
        ___qtablewidgetitem5 = self.table_widget_cctv_management.item(1, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Widget", u"192.168.8.2", None));
        self.table_widget_cctv_management.setSortingEnabled(__sortingEnabled)

    # retranslateUi

