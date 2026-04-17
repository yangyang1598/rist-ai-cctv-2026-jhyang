# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_connection_status_widgetEZSJTC.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(311, 67)
        Widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 3, 0, 5)
        self.table_widget_cctv_connection_status = QTableWidget(Widget)
        if (self.table_widget_cctv_connection_status.columnCount() < 3):
            self.table_widget_cctv_connection_status.setColumnCount(3)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.table_widget_cctv_connection_status.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.table_widget_cctv_connection_status.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.table_widget_cctv_connection_status.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.table_widget_cctv_connection_status.rowCount() < 1):
            self.table_widget_cctv_connection_status.setRowCount(1)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_connection_status.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_connection_status.setItem(0, 1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.table_widget_cctv_connection_status.setItem(0, 2, __qtablewidgetitem5)
        self.table_widget_cctv_connection_status.setObjectName(u"table_widget_cctv_connection_status")
        self.table_widget_cctv_connection_status.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.table_widget_cctv_connection_status.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_widget_cctv_connection_status.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_widget_cctv_connection_status.setAutoScrollMargin(16)
        self.table_widget_cctv_connection_status.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_cctv_connection_status.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_widget_cctv_connection_status.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_widget_cctv_connection_status.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)
        self.table_widget_cctv_connection_status.setRowCount(1)
        self.table_widget_cctv_connection_status.horizontalHeader().setCascadingSectionResizes(False)
        self.table_widget_cctv_connection_status.horizontalHeader().setMinimumSectionSize(20)
        self.table_widget_cctv_connection_status.horizontalHeader().setDefaultSectionSize(95)
        self.table_widget_cctv_connection_status.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget_cctv_connection_status.horizontalHeader().setStretchLastSection(True)
        self.table_widget_cctv_connection_status.verticalHeader().setVisible(False)
        self.table_widget_cctv_connection_status.verticalHeader().setDefaultSectionSize(28)

        self.verticalLayout.addWidget(self.table_widget_cctv_connection_status)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        ___qtablewidgetitem = self.table_widget_cctv_connection_status.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Widget", u"\uc804\uccb4", None));
        ___qtablewidgetitem1 = self.table_widget_cctv_connection_status.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Widget", u"\uc628\ub77c\uc778", None));
        ___qtablewidgetitem2 = self.table_widget_cctv_connection_status.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Widget", u"\uc624\ud504\ub77c\uc778", None));

        __sortingEnabled = self.table_widget_cctv_connection_status.isSortingEnabled()
        self.table_widget_cctv_connection_status.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.table_widget_cctv_connection_status.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Widget", u"72", None));
        ___qtablewidgetitem4 = self.table_widget_cctv_connection_status.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Widget", u"50", None));
        ___qtablewidgetitem5 = self.table_widget_cctv_connection_status.item(0, 2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Widget", u"22", None));
        self.table_widget_cctv_connection_status.setSortingEnabled(__sortingEnabled)

    # retranslateUi

