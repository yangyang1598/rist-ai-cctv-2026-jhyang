# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_layout_widgetEXqnjR.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(493, 300)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_video_layout = QLabel(Widget)
        self.label_video_layout.setObjectName(u"label_video_layout")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_video_layout.setFont(font)

        self.horizontalLayout.addWidget(self.label_video_layout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_add_video_layout = QPushButton(Widget)
        self.button_add_video_layout.setObjectName(u"button_add_video_layout")
        self.button_add_video_layout.setMinimumSize(QSize(0, 0))
        self.button_add_video_layout.setMaximumSize(QSize(30, 30))
        self.button_add_video_layout.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.button_add_video_layout.setToolTipDuration(-1)

        self.horizontalLayout.addWidget(self.button_add_video_layout)

        self.button_delete_video_layout = QPushButton(Widget)
        self.button_delete_video_layout.setObjectName(u"button_delete_video_layout")
        self.button_delete_video_layout.setMinimumSize(QSize(0, 0))
        self.button_delete_video_layout.setMaximumSize(QSize(30, 30))
        self.button_delete_video_layout.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.button_delete_video_layout.setToolTipDuration(-1)

        self.horizontalLayout.addWidget(self.button_delete_video_layout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 3, -1, -1)
        self.list_widget_video_layout = QListWidget(Widget)
        QListWidgetItem(self.list_widget_video_layout)
        QListWidgetItem(self.list_widget_video_layout)
        self.list_widget_video_layout.setObjectName(u"list_widget_video_layout")
        self.list_widget_video_layout.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_widget_video_layout.setSpacing(0)

        self.verticalLayout_2.addWidget(self.list_widget_video_layout)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Widget)

        self.list_widget_video_layout.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_video_layout.setText(QCoreApplication.translate("Widget", u"\u25bc \uc601\uc0c1 \ub808\uc774\uc544\uc6c3 \uad6c\uc131 \ubaa9\ub85d", None))
        self.button_add_video_layout.setText(QCoreApplication.translate("Widget", u"+", None))
        self.button_delete_video_layout.setText(QCoreApplication.translate("Widget", u"-", None))

        __sortingEnabled = self.list_widget_video_layout.isSortingEnabled()
        self.list_widget_video_layout.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_widget_video_layout.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Widget", u"1*1 \uc0ac\ub78c\uac10\uc9c0", None));
        ___qlistwidgetitem1 = self.list_widget_video_layout.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Widget", u"2*2 \uc0ac\ub78c\uac10\uc9c0", None));
        self.list_widget_video_layout.setSortingEnabled(__sortingEnabled)

    # retranslateUi

