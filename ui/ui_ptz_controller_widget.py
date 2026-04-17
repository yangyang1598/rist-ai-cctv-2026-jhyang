# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ptz_controller_widgetvFxqMa.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(254, 272)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 3, 0, 5)
        self.label_pan_tilt_control = QLabel(Widget)
        self.label_pan_tilt_control.setObjectName(u"label_pan_tilt_control")
        self.label_pan_tilt_control.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.label_pan_tilt_control.setToolTipDuration(-1)

        self.verticalLayout.addWidget(self.label_pan_tilt_control)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, -1, 10, -1)
        self.button_up_left = QPushButton(Widget)
        self.button_up_left.setObjectName(u"button_up_left")
        self.button_up_left.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_up_left, 0, 0, 1, 1)

        self.button_up = QPushButton(Widget)
        self.button_up.setObjectName(u"button_up")
        self.button_up.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_up, 0, 1, 1, 1)

        self.button_up_right = QPushButton(Widget)
        self.button_up_right.setObjectName(u"button_up_right")
        self.button_up_right.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_up_right, 0, 2, 1, 1)

        self.button_left = QPushButton(Widget)
        self.button_left.setObjectName(u"button_left")
        self.button_left.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_left, 1, 0, 1, 1)

        self.button_center = QPushButton(Widget)
        self.button_center.setObjectName(u"button_center")
        self.button_center.setEnabled(False)
        self.button_center.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_center, 1, 1, 1, 1)

        self.button_right = QPushButton(Widget)
        self.button_right.setObjectName(u"button_right")
        self.button_right.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_right, 1, 2, 1, 1)

        self.button_down_left = QPushButton(Widget)
        self.button_down_left.setObjectName(u"button_down_left")
        self.button_down_left.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_down_left, 2, 0, 1, 1)

        self.button_down = QPushButton(Widget)
        self.button_down.setObjectName(u"button_down")
        self.button_down.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_down, 2, 1, 1, 1)

        self.button_down_right = QPushButton(Widget)
        self.button_down_right.setObjectName(u"button_down_right")
        self.button_down_right.setMinimumSize(QSize(40, 40))

        self.gridLayout.addWidget(self.button_down_right, 2, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.label_zoom_control = QLabel(Widget)
        self.label_zoom_control.setObjectName(u"label_zoom_control")

        self.verticalLayout.addWidget(self.label_zoom_control)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.button_zoom_in = QPushButton(Widget)
        self.button_zoom_in.setObjectName(u"button_zoom_in")
        self.button_zoom_in.setMinimumSize(QSize(40, 40))

        self.horizontalLayout_2.addWidget(self.button_zoom_in)

        self.button_zoom_out = QPushButton(Widget)
        self.button_zoom_out.setObjectName(u"button_zoom_out")
        self.button_zoom_out.setMinimumSize(QSize(40, 40))

        self.horizontalLayout_2.addWidget(self.button_zoom_out)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.button_ptz_reset = QPushButton(Widget)
        self.button_ptz_reset.setObjectName(u"button_ptz_reset")
        self.button_ptz_reset.setMinimumSize(QSize(0, 30))

        self.verticalLayout.addWidget(self.button_ptz_reset)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_pan_tilt_control.setText(QCoreApplication.translate("Widget", u"- \uc774\ub3d9", None))
        self.button_up_left.setText(QCoreApplication.translate("Widget", u"\u2196", None))
        self.button_up.setText(QCoreApplication.translate("Widget", u"\u2191", None))
        self.button_up_right.setText(QCoreApplication.translate("Widget", u"\u2197", None))
        self.button_left.setText(QCoreApplication.translate("Widget", u"\u2190", None))
        self.button_center.setText(QCoreApplication.translate("Widget", u"\u25aa", None))
        self.button_right.setText(QCoreApplication.translate("Widget", u"\u2192", None))
        self.button_down_left.setText(QCoreApplication.translate("Widget", u"\u2199", None))
        self.button_down.setText(QCoreApplication.translate("Widget", u"\u2193", None))
        self.button_down_right.setText(QCoreApplication.translate("Widget", u"\u2198", None))
        self.label_zoom_control.setText(QCoreApplication.translate("Widget", u"- zoom", None))
        self.button_zoom_in.setText(QCoreApplication.translate("Widget", u"+", None))
        self.button_zoom_out.setText(QCoreApplication.translate("Widget", u"-", None))
#if QT_CONFIG(tooltip)
        self.button_ptz_reset.setToolTip(QCoreApplication.translate("Widget", u"\uc774\ub3d9 \ucd08\uae30\ud654", None))
#endif // QT_CONFIG(tooltip)
        self.button_ptz_reset.setText(QCoreApplication.translate("Widget", u"\u21bb", None))
    # retranslateUi

