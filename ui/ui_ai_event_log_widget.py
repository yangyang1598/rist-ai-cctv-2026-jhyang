# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_widgetnUmcKZ.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFormLayout, QHeaderView,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(874, 116)
        self.formLayout = QFormLayout(Widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.table_widget_ai_event_log = QTableWidget(Widget)
        if (self.table_widget_ai_event_log.columnCount() < 6):
            self.table_widget_ai_event_log.setColumnCount(6)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font);
        self.table_widget_ai_event_log.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.table_widget_ai_event_log.rowCount() < 3):
            self.table_widget_ai_event_log.setRowCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(0, 3, __qtablewidgetitem9)
        font1 = QFont()
        font1.setBold(False)
        font1.setUnderline(True)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font1);
        self.table_widget_ai_event_log.setItem(0, 5, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(1, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(1, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(1, 2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(1, 3, __qtablewidgetitem14)
        font2 = QFont()
        font2.setUnderline(True)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font2);
        self.table_widget_ai_event_log.setItem(1, 5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(2, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(2, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(2, 2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.table_widget_ai_event_log.setItem(2, 3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font2);
        self.table_widget_ai_event_log.setItem(2, 5, __qtablewidgetitem20)
        self.table_widget_ai_event_log.setObjectName(u"table_widget_ai_event_log")
        self.table_widget_ai_event_log.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.table_widget_ai_event_log.sizePolicy().hasHeightForWidth())
        self.table_widget_ai_event_log.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setPointSize(9)
        self.table_widget_ai_event_log.setFont(font3)
        self.table_widget_ai_event_log.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table_widget_ai_event_log.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_widget_ai_event_log.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_ai_event_log.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget_ai_event_log.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_widget_ai_event_log.horizontalHeader().setVisible(True)
        self.table_widget_ai_event_log.horizontalHeader().setCascadingSectionResizes(False)
        self.table_widget_ai_event_log.horizontalHeader().setDefaultSectionSize(140)
        self.table_widget_ai_event_log.horizontalHeader().setHighlightSections(True)
        self.table_widget_ai_event_log.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget_ai_event_log.horizontalHeader().setStretchLastSection(True)
        self.table_widget_ai_event_log.verticalHeader().setVisible(False)
        self.table_widget_ai_event_log.verticalHeader().setDefaultSectionSize(25)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.table_widget_ai_event_log)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        ___qtablewidgetitem = self.table_widget_ai_event_log.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Widget", u"\uc54c\ub78c\ubc1c\uc0dd\uc77c\uc2dc", None));
        ___qtablewidgetitem1 = self.table_widget_ai_event_log.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc704\uce58", None));
        ___qtablewidgetitem2 = self.table_widget_ai_event_log.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd CCTV", None));
        ___qtablewidgetitem3 = self.table_widget_ai_event_log.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc774\ubca4\ud2b8", None));
        ___qtablewidgetitem4 = self.table_widget_ai_event_log.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Widget", u"\ubc1c\uc0dd \uc704\ud5d8 \uc720\ud615", None));
        ___qtablewidgetitem5 = self.table_widget_ai_event_log.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Widget", u"\uc774\ubbf8\uc9c0", None));

        __sortingEnabled = self.table_widget_ai_event_log.isSortingEnabled()
        self.table_widget_ai_event_log.setSortingEnabled(False)
        ___qtablewidgetitem6 = self.table_widget_ai_event_log.item(0, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Widget", u"2025/05/01 23:59:59", None));
        ___qtablewidgetitem7 = self.table_widget_ai_event_log.item(0, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Widget", u"1\uacf5\uc7a5", None));
        ___qtablewidgetitem8 = self.table_widget_ai_event_log.item(0, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Widget", u"CCTV 01", None));
        ___qtablewidgetitem9 = self.table_widget_ai_event_log.item(0, 3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Widget", u"\uc0ac\ub78c \uac10\uc9c0", None));
        ___qtablewidgetitem10 = self.table_widget_ai_event_log.item(0, 5)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Widget", u"[ \uc774\ubbf8\uc9c0 \uacbd\ub85c ]", None));
        ___qtablewidgetitem11 = self.table_widget_ai_event_log.item(1, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Widget", u"2025/05/02 23:59:59", None));
        ___qtablewidgetitem12 = self.table_widget_ai_event_log.item(1, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Widget", u"5\uacf5\uc7a5", None));
        ___qtablewidgetitem13 = self.table_widget_ai_event_log.item(1, 2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Widget", u"CCTV 48", None));
        ___qtablewidgetitem14 = self.table_widget_ai_event_log.item(1, 3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Widget", u"\uc9c0\uac8c\ucc28 \uac10\uc9c0", None));
        ___qtablewidgetitem15 = self.table_widget_ai_event_log.item(1, 5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Widget", u"[ \uc774\ubbf8\uc9c0 \uacbd\ub85c ]", None));
        ___qtablewidgetitem16 = self.table_widget_ai_event_log.item(2, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Widget", u"2025/05/03 23:59:59", None));
        ___qtablewidgetitem17 = self.table_widget_ai_event_log.item(2, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Widget", u"2\uacf5\uc7a5", None));
        ___qtablewidgetitem18 = self.table_widget_ai_event_log.item(2, 2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Widget", u"CCTV 13", None));
        ___qtablewidgetitem19 = self.table_widget_ai_event_log.item(2, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Widget", u"\uc911\ub7c9\ubb3c \uac10\uc9c0", None));
        ___qtablewidgetitem20 = self.table_widget_ai_event_log.item(2, 5)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Widget", u"[ \uc774\ubbf8\uc9c0 \uacbd\ub85c ]", None));
        self.table_widget_ai_event_log.setSortingEnabled(__sortingEnabled)

    # retranslateUi

