# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_event_log_filter_search_widgetPHSnEI.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(773, 98)
        self.horizontalLayout_4 = QHBoxLayout(Widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 3, 0, 5)
        self.layout_event_log_filter_search = QHBoxLayout()
        self.layout_event_log_filter_search.setObjectName(u"layout_event_log_filter_search")
        self.layout_search = QVBoxLayout()
        self.layout_search.setObjectName(u"layout_search")
        self.layout_start_date_filter = QHBoxLayout()
        self.layout_start_date_filter.setObjectName(u"layout_start_date_filter")
        self.label_start_date_filter = QLabel(Widget)
        self.label_start_date_filter.setObjectName(u"label_start_date_filter")

        self.layout_start_date_filter.addWidget(self.label_start_date_filter)

        self.datetime_start_date_filter = QDateTimeEdit(Widget)
        self.datetime_start_date_filter.setObjectName(u"datetime_start_date_filter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datetime_start_date_filter.sizePolicy().hasHeightForWidth())
        self.datetime_start_date_filter.setSizePolicy(sizePolicy)
        self.datetime_start_date_filter.setMaximumDateTime(QDateTime(QDate(9999, 12, 31), QTime(23, 59, 59)))

        self.layout_start_date_filter.addWidget(self.datetime_start_date_filter)


        self.layout_search.addLayout(self.layout_start_date_filter)

        self.layout_end_date_filter = QHBoxLayout()
        self.layout_end_date_filter.setObjectName(u"layout_end_date_filter")
        self.label_end_date_filter = QLabel(Widget)
        self.label_end_date_filter.setObjectName(u"label_end_date_filter")

        self.layout_end_date_filter.addWidget(self.label_end_date_filter)

        self.datetime_end_date_filter = QDateTimeEdit(Widget)
        self.datetime_end_date_filter.setObjectName(u"datetime_end_date_filter")
        sizePolicy.setHeightForWidth(self.datetime_end_date_filter.sizePolicy().hasHeightForWidth())
        self.datetime_end_date_filter.setSizePolicy(sizePolicy)
        self.datetime_end_date_filter.setMaximumDateTime(QDateTime(QDate(9999, 12, 31), QTime(23, 59, 59)))

        self.layout_end_date_filter.addWidget(self.datetime_end_date_filter)


        self.layout_search.addLayout(self.layout_end_date_filter)

        self.button_search = QPushButton(Widget)
        self.button_search.setObjectName(u"button_search")

        self.layout_search.addWidget(self.button_search)


        self.layout_event_log_filter_search.addLayout(self.layout_search)

        self.layout_quick_filter = QVBoxLayout()
        self.layout_quick_filter.setObjectName(u"layout_quick_filter")
        self.button_search_by_week = QPushButton(Widget)
        self.button_search_by_week.setObjectName(u"button_search_by_week")

        self.layout_quick_filter.addWidget(self.button_search_by_week)

        self.button_search_by_month = QPushButton(Widget)
        self.button_search_by_month.setObjectName(u"button_search_by_month")

        self.layout_quick_filter.addWidget(self.button_search_by_month)

        self.button_search_by_year = QPushButton(Widget)
        self.button_search_by_year.setObjectName(u"button_search_by_year")

        self.layout_quick_filter.addWidget(self.button_search_by_year)


        self.layout_event_log_filter_search.addLayout(self.layout_quick_filter)

        self.layout_event_log_filter_search.setStretch(0, 2)
        self.layout_event_log_filter_search.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.layout_event_log_filter_search)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_start_date_filter.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9 \uc2dc\uc791\uc77c :", None))
        self.datetime_start_date_filter.setDisplayFormat(QCoreApplication.translate("Widget", u"yyyy-MM-dd hh:mm:ss", None))
        self.label_end_date_filter.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9 \uc885\ub8cc\uc77c :", None))
        self.datetime_end_date_filter.setDisplayFormat(QCoreApplication.translate("Widget", u"yyyy-MM-dd hh:mm:ss", None))
        self.button_search.setText(QCoreApplication.translate("Widget", u"\uac80\uc0c9", None))
        self.button_search_by_week.setText(QCoreApplication.translate("Widget", u"\uc8fc\uac04 \uac80\uc0c9", None))
        self.button_search_by_month.setText(QCoreApplication.translate("Widget", u"\uc6d4\uac04 \uac80\uc0c9", None))
        self.button_search_by_year.setText(QCoreApplication.translate("Widget", u"\ub144\uac04 \uac80\uc0c9", None))
    # retranslateUi

