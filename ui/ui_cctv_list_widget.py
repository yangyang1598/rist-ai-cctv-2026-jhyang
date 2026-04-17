# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_list_widgetonQFBW.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QHeaderView, QLineEdit, QPushButton, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(254, 300)
        Widget.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        Widget.setFont(font)
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

        self.tree_widget_cctv_list = QTreeWidget(Widget)
        __qtreewidgetitem = QTreeWidgetItem(self.tree_widget_cctv_list)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.tree_widget_cctv_list)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.tree_widget_cctv_list)
        QTreeWidgetItem(__qtreewidgetitem2)
        self.tree_widget_cctv_list.setObjectName(u"tree_widget_cctv_list")
        self.tree_widget_cctv_list.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.tree_widget_cctv_list.setAutoScrollMargin(14)
        self.tree_widget_cctv_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree_widget_cctv_list.setHeaderHidden(True)
        self.tree_widget_cctv_list.setColumnCount(1)
        self.tree_widget_cctv_list.header().setVisible(False)

        self.verticalLayout.addWidget(self.tree_widget_cctv_list)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.button_cctv_search.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9", None))
        ___qtreewidgetitem = self.tree_widget_cctv_list.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Widget", u"1", None));

        __sortingEnabled = self.tree_widget_cctv_list.isSortingEnabled()
        self.tree_widget_cctv_list.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_widget_cctv_list.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Widget", u"1\uacf5\uc7a5", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Widget", u"CCTV 01", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Widget", u"CCTV 02", None));
        ___qtreewidgetitem4 = self.tree_widget_cctv_list.topLevelItem(1)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("Widget", u"2\uacf5\uc7a5", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem4.child(0)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("Widget", u"CCTV 11", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem4.child(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("Widget", u"CCTV 12", None));
        ___qtreewidgetitem7 = self.tree_widget_cctv_list.topLevelItem(2)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("Widget", u"3\uacf5\uc7a5", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem7.child(0)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("Widget", u"CCTV 21", None));
        self.tree_widget_cctv_list.setSortingEnabled(__sortingEnabled)

    # retranslateUi

