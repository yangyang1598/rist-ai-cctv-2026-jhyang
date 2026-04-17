# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset_config_file_path_dialoggDdSHt.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(543, 103)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_dataset_config_file_path = QLabel(Dialog)
        self.label_dataset_config_file_path.setObjectName(u"label_dataset_config_file_path")

        self.horizontalLayout.addWidget(self.label_dataset_config_file_path)

        self.line_edit_dataset_config_file_path = QLineEdit(Dialog)
        self.line_edit_dataset_config_file_path.setObjectName(u"line_edit_dataset_config_file_path")
        self.line_edit_dataset_config_file_path.setReadOnly(False)

        self.horizontalLayout.addWidget(self.line_edit_dataset_config_file_path)

        self.button_dataset_config_file_path_search = QPushButton(Dialog)
        self.button_dataset_config_file_path_search.setObjectName(u"button_dataset_config_file_path_search")

        self.horizontalLayout.addWidget(self.button_dataset_config_file_path_search)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_dataset_config_file_path.setText(QCoreApplication.translate("Dialog", u"\ub370\uc774\ud130\uc14b \uad6c\uc131 \ud30c\uc77c", None))
        self.button_dataset_config_file_path_search.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

