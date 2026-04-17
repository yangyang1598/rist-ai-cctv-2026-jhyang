# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RpaTaskWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_RpaTaskWidget(object):
    def setupUi(self, RpaTaskWidget):
        if not RpaTaskWidget.objectName():
            RpaTaskWidget.setObjectName(u"RpaTaskWidget")
        RpaTaskWidget.resize(1063, 633)
        self.gridLayout = QGridLayout(RpaTaskWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(RpaTaskWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 20pt \"Arial\";")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(RpaTaskWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.pushButton_task_scheduler_restart = QPushButton(RpaTaskWidget)
        self.pushButton_task_scheduler_restart.setObjectName(u"pushButton_task_scheduler_restart")

        self.horizontalLayout.addWidget(self.pushButton_task_scheduler_restart)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(RpaTaskWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_task_new = QWidget()
        self.tab_task_new.setObjectName(u"tab_task_new")
        self.gridLayout_5 = QGridLayout(self.tab_task_new)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_task_new = QPushButton(self.tab_task_new)
        self.pushButton_task_new.setObjectName(u"pushButton_task_new")
        self.pushButton_task_new.setMinimumSize(QSize(0, 80))

        self.gridLayout_4.addWidget(self.pushButton_task_new, 0, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_task_new, "")
        self.tab_task_list = QWidget()
        self.tab_task_list.setObjectName(u"tab_task_list")
        self.gridLayout_3 = QGridLayout(self.tab_task_list)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tableWidget_task = QTableWidget(self.tab_task_list)
        if (self.tableWidget_task.columnCount() < 9):
            self.tableWidget_task.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_task.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.tableWidget_task.rowCount() < 3):
            self.tableWidget_task.setRowCount(3)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_task.setVerticalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_task.setVerticalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_task.setVerticalHeaderItem(2, __qtablewidgetitem11)
        self.tableWidget_task.setObjectName(u"tableWidget_task")
        self.tableWidget_task.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_task.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_task.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_task.verticalHeader().setVisible(True)
        self.tableWidget_task.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_2.addWidget(self.tableWidget_task, 1, 0, 1, 1)

        self.pushButton_search = QPushButton(self.tab_task_list)
        self.pushButton_search.setObjectName(u"pushButton_search")

        self.gridLayout_2.addWidget(self.pushButton_search, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_task_list, "")

        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)


        self.retranslateUi(RpaTaskWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RpaTaskWidget)
    # setupUi

    def retranslateUi(self, RpaTaskWidget):
        RpaTaskWidget.setWindowTitle(QCoreApplication.translate("RpaTaskWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("RpaTaskWidget", u"RPA \uc5c5\ubb34 \uad00\ub9ac", None))
        self.label_2.setText(QCoreApplication.translate("RpaTaskWidget", u"RPA \uc5c5\ubb34 \ubcc0\uacbd \ud6c4 Scheduler \uc7ac\uc2dc\uc791", None))
        self.pushButton_task_scheduler_restart.setText(QCoreApplication.translate("RpaTaskWidget", u"RPA Scheduler \uc7ac\uc2dc\uc791", None))
        self.pushButton_task_new.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc0c8 \uc5c5\ubb34 \ub9cc\ub4e4\uae30", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_task_new), QCoreApplication.translate("RpaTaskWidget", u"\uc0c8 \uc5c5\ubb34", None))
        ___qtablewidgetitem = self.tableWidget_task.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RpaTaskWidget", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget_task.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc5c5\ubb34\uba85\uce6d", None));
        ___qtablewidgetitem2 = self.tableWidget_task.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc2e4\ud589 \uc694\uc77c", None));
        ___qtablewidgetitem3 = self.tableWidget_task.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc2e4\ud589 \uc2dc\uac04", None));
        ___qtablewidgetitem4 = self.tableWidget_task.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RpaTaskWidget", u"\ubcf4\uace0\uc11c-\uc774\ubca4\ud2b8 \ubc1c\uc0dd\uae30\uac04(day)", None));
        ___qtablewidgetitem5 = self.tableWidget_task.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RpaTaskWidget", u"\ubcf4\uace0\uc11c-\uc2ec\uac01\ub3c4", None));
        ___qtablewidgetitem6 = self.tableWidget_task.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RpaTaskWidget", u"\ubcf4\uace0\uc11c-\uc704\ud5d8\uc720\ud615", None));
        ___qtablewidgetitem7 = self.tableWidget_task.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc774\uba54\uc77c \uc218\uc2e0\uc790", None));
        ___qtablewidgetitem8 = self.tableWidget_task.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc774\uba54\uc77c \uc81c\ubaa9", None));
        ___qtablewidgetitem9 = self.tableWidget_task.verticalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem10 = self.tableWidget_task.verticalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc0c8 \uc5f4", None));
        ___qtablewidgetitem11 = self.tableWidget_task.verticalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("RpaTaskWidget", u"\uc0c8 \uc5f4", None));
        self.pushButton_search.setText(QCoreApplication.translate("RpaTaskWidget", u"RPA \uc5c5\ubb34 \uac80\uc0c9", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_task_list), QCoreApplication.translate("RpaTaskWidget", u"\uc5c5\ubb34 \ubaa9\ub85d", None))
    # retranslateUi

