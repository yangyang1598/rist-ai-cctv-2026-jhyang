# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaHomeWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QSizePolicy, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_RpaHomeWidget(object):
    def setupUi(self, RpaHomeWidget):
        if not RpaHomeWidget.objectName():
            RpaHomeWidget.setObjectName(u"RpaHomeWidget")
        RpaHomeWidget.resize(957, 669)
        self.gridLayout = QGridLayout(RpaHomeWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(RpaHomeWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 20pt \"Arial\";")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(RpaHomeWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tableWidget = QTableWidget(self.tab_5)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget.rowCount() < 9):
            self.tableWidget.setRowCount(9)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem11)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(40, 180, 631, 181))
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tabWidget.addTab(self.tab_6, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(RpaHomeWidget)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(RpaHomeWidget)
    # setupUi

    def retranslateUi(self, RpaHomeWidget):
        RpaHomeWidget.setWindowTitle(QCoreApplication.translate("RpaHomeWidget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("RpaHomeWidget", u"Home", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RpaHomeWidget", u"121111", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RpaHomeWidget", u"11111", None));
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem9 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("RpaHomeWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("RpaHomeWidget", u"b", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("RpaHomeWidget", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("RpaHomeWidget", u"Tab 2", None))
    # retranslateUi

