# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'management_dialogWKdDqJ.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1200, 800)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.layout_management = QHBoxLayout()
        self.layout_management.setObjectName(u"layout_management")
        self.tree_widget_management_side_bar = QTreeWidget(Dialog)
        self.tree_widget_management_side_bar.headerItem().setText(0, "")
        __qtreewidgetitem = QTreeWidgetItem(self.tree_widget_management_side_bar)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        self.tree_widget_management_side_bar.setObjectName(u"tree_widget_management_side_bar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_widget_management_side_bar.sizePolicy().hasHeightForWidth())
        self.tree_widget_management_side_bar.setSizePolicy(sizePolicy)

        self.layout_management.addWidget(self.tree_widget_management_side_bar)

        self.label_management_widget = QLabel(Dialog)
        self.label_management_widget.setObjectName(u"label_management_widget")
        font = QFont()
        font.setPointSize(12)
        self.label_management_widget.setFont(font)
        self.label_management_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_management_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_management.addWidget(self.label_management_widget)

        self.layout_management.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.layout_management)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))

        __sortingEnabled = self.tree_widget_management_side_bar.isSortingEnabled()
        self.tree_widget_management_side_bar.setSortingEnabled(False)
        ___qtreewidgetitem = self.tree_widget_management_side_bar.topLevelItem(0)
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\uad00\ub9ac", None));
        ___qtreewidgetitem1 = ___qtreewidgetitem.child(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"CCTV", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem.child(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"\ubd88\uc548\uc804 \uc0c1\ud669 \uac10\uc9c0", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Dialog", u"\uc774\ubca4\ud2b8", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem2.child(1)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("Dialog", u"\ubaa8\ub378 \ub4f1\ub85d \ubc0f \ud559\uc2b5", None));
        self.tree_widget_management_side_bar.setSortingEnabled(__sortingEnabled)

        self.label_management_widget.setText(QCoreApplication.translate("Dialog", u"\uad00\ub9ac \uc704\uc82f", None))
    # retranslateUi

