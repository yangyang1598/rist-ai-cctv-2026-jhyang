# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_setting_dialoggtjOyD.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(781, 575)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tablewidget_cctv_setting = QTableWidget(Dialog)
        if (self.tablewidget_cctv_setting.columnCount() < 2):
            self.tablewidget_cctv_setting.setColumnCount(2)
        font = QFont()
        font.setPointSize(9)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tablewidget_cctv_setting.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablewidget_cctv_setting.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tablewidget_cctv_setting.rowCount() < 1):
            self.tablewidget_cctv_setting.setRowCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablewidget_cctv_setting.setVerticalHeaderItem(0, __qtablewidgetitem2)
        self.tablewidget_cctv_setting.setObjectName(u"tablewidget_cctv_setting")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablewidget_cctv_setting.sizePolicy().hasHeightForWidth())
        self.tablewidget_cctv_setting.setSizePolicy(sizePolicy)
        self.tablewidget_cctv_setting.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tablewidget_cctv_setting.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tablewidget_cctv_setting.horizontalHeader().setDefaultSectionSize(150)
        self.tablewidget_cctv_setting.horizontalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.tablewidget_cctv_setting, 1, 1, 1, 1)

        self.SideBar = QVBoxLayout()
        self.SideBar.setSpacing(3)
        self.SideBar.setObjectName(u"SideBar")
        self.SideBar.setContentsMargins(-1, 10, -1, -1)
        self.label_cctv_list_widget = QLabel(Dialog)
        self.label_cctv_list_widget.setObjectName(u"label_cctv_list_widget")

        self.SideBar.addWidget(self.label_cctv_list_widget)


        self.gridLayout.addLayout(self.SideBar, 1, 0, 1, 1)

        self.label_cctvSetting = QLabel(Dialog)
        self.label_cctvSetting.setObjectName(u"label_cctvSetting")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(17)
        font1.setBold(False)
        font1.setUnderline(True)
        self.label_cctvSetting.setFont(font1)
        self.label_cctvSetting.setAutoFillBackground(False)
        self.label_cctvSetting.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_cctvSetting, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_line = QLabel(Dialog)
        self.label_line.setObjectName(u"label_line")

        self.horizontalLayout.addWidget(self.label_line)

        self.label_use_rps_text = QLabel(Dialog)
        self.label_use_rps_text.setObjectName(u"label_use_rps_text")
        font2 = QFont()
        font2.setBold(True)
        self.label_use_rps_text.setFont(font2)

        self.horizontalLayout.addWidget(self.label_use_rps_text)

        self.label_use_rps_value = QLabel(Dialog)
        self.label_use_rps_value.setObjectName(u"label_use_rps_value")

        self.horizontalLayout.addWidget(self.label_use_rps_value)

        self.label_line_2 = QLabel(Dialog)
        self.label_line_2.setObjectName(u"label_line_2")

        self.horizontalLayout.addWidget(self.label_line_2)

        self.label_free_rps_text = QLabel(Dialog)
        self.label_free_rps_text.setObjectName(u"label_free_rps_text")
        self.label_free_rps_text.setFont(font2)

        self.horizontalLayout.addWidget(self.label_free_rps_text)

        self.label_free_rps_value = QLabel(Dialog)
        self.label_free_rps_value.setObjectName(u"label_free_rps_value")

        self.horizontalLayout.addWidget(self.label_free_rps_value)

        self.label_line_3 = QLabel(Dialog)
        self.label_line_3.setObjectName(u"label_line_3")

        self.horizontalLayout.addWidget(self.label_line_3)

        self.label_limit_rps_text = QLabel(Dialog)
        self.label_limit_rps_text.setObjectName(u"label_limit_rps_text")
        self.label_limit_rps_text.setFont(font2)

        self.horizontalLayout.addWidget(self.label_limit_rps_text)

        self.label_limit_rps_value = QLabel(Dialog)
        self.label_limit_rps_value.setObjectName(u"label_limit_rps_value")

        self.horizontalLayout.addWidget(self.label_limit_rps_value)

        self.label_line_1 = QLabel(Dialog)
        self.label_line_1.setObjectName(u"label_line_1")

        self.horizontalLayout.addWidget(self.label_line_1)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 5)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        ___qtablewidgetitem = self.tablewidget_cctv_setting.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\uc774\ub984", None));
        ___qtablewidgetitem1 = self.tablewidget_cctv_setting.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\ubd88\uc548\uc804 \uc0c1\ud669 \uac10\uc9c0 \uc774\ubca4\ud2b8", None));
        self.label_cctv_list_widget.setText(QCoreApplication.translate("Dialog", u"CCTV \ubaa9\ub85d \uc704\uc82f", None))
        self.label_cctvSetting.setText(QCoreApplication.translate("Dialog", u" CCTV \uc124\uc815", None))
        self.label_line.setText(QCoreApplication.translate("Dialog", u"|", None))
        self.label_use_rps_text.setText(QCoreApplication.translate("Dialog", u" \uc0ac\uc6a9 RPS", None))
        self.label_use_rps_value.setText(QCoreApplication.translate("Dialog", u"500", None))
        self.label_line_2.setText(QCoreApplication.translate("Dialog", u"|", None))
        self.label_free_rps_text.setText(QCoreApplication.translate("Dialog", u"\uc5ec\uc720 RPS", None))
        self.label_free_rps_value.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_line_3.setText(QCoreApplication.translate("Dialog", u"|", None))
        self.label_limit_rps_text.setText(QCoreApplication.translate("Dialog", u"\ud55c\uacc4 RPS", None))
        self.label_limit_rps_value.setText(QCoreApplication.translate("Dialog", u"600", None))
        self.label_line_1.setText(QCoreApplication.translate("Dialog", u"|", None))
    # retranslateUi

