# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_new_model_dialogqDkWIS.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(605, 255)
        Dialog.setMinimumSize(QSize(500, 250))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_add_new_model = QLabel(Dialog)
        self.label_add_new_model.setObjectName(u"label_add_new_model")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_add_new_model.sizePolicy().hasHeightForWidth())
        self.label_add_new_model.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_add_new_model.setFont(font)
        self.label_add_new_model.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.label_add_new_model.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_add_new_model)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_edit_model_description = QLineEdit(Dialog)
        self.line_edit_model_description.setObjectName(u"line_edit_model_description")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_model_description.sizePolicy().hasHeightForWidth())
        self.line_edit_model_description.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(10)
        self.line_edit_model_description.setFont(font1)
        self.line_edit_model_description.setToolTipDuration(30000)

        self.gridLayout.addWidget(self.line_edit_model_description, 0, 1, 1, 1)

        self.line_edit_model_file_path = QLineEdit(Dialog)
        self.line_edit_model_file_path.setObjectName(u"line_edit_model_file_path")
        self.line_edit_model_file_path.setFont(font1)
        self.line_edit_model_file_path.setToolTipDuration(30000)

        self.gridLayout.addWidget(self.line_edit_model_file_path, 2, 1, 1, 1)

        self.line_edit_model_name = QLineEdit(Dialog)
        self.line_edit_model_name.setObjectName(u"line_edit_model_name")
        self.line_edit_model_name.setFont(font1)
        self.line_edit_model_name.setToolTipDuration(30000)

        self.gridLayout.addWidget(self.line_edit_model_name, 1, 1, 1, 1)

        self.label_dataset_config_file_path = QLabel(Dialog)
        self.label_dataset_config_file_path.setObjectName(u"label_dataset_config_file_path")
        self.label_dataset_config_file_path.setEnabled(True)
        font2 = QFont()
        font2.setPointSize(11)
        self.label_dataset_config_file_path.setFont(font2)
        self.label_dataset_config_file_path.setToolTipDuration(30000)
        self.label_dataset_config_file_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dataset_config_file_path, 3, 0, 1, 1)

        self.button_model_file_path = QPushButton(Dialog)
        self.button_model_file_path.setObjectName(u"button_model_file_path")
        self.button_model_file_path.setEnabled(True)

        self.gridLayout.addWidget(self.button_model_file_path, 2, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_model_name = QLabel(Dialog)
        self.label_model_name.setObjectName(u"label_model_name")
        self.label_model_name.setFont(font2)
        self.label_model_name.setToolTipDuration(30000)
        self.label_model_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_model_name)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.line_edit_dataset_config_file_path = QLineEdit(Dialog)
        self.line_edit_dataset_config_file_path.setObjectName(u"line_edit_dataset_config_file_path")
        self.line_edit_dataset_config_file_path.setEnabled(True)
        self.line_edit_dataset_config_file_path.setFont(font1)
        self.line_edit_dataset_config_file_path.setToolTipDuration(30000)

        self.gridLayout.addWidget(self.line_edit_dataset_config_file_path, 3, 1, 1, 1)

        self.label_model_file_path = QLabel(Dialog)
        self.label_model_file_path.setObjectName(u"label_model_file_path")
        self.label_model_file_path.setFont(font2)
        self.label_model_file_path.setToolTipDuration(30000)
        self.label_model_file_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_model_file_path, 2, 0, 1, 1)

        self.button_dataset_config_file_path = QPushButton(Dialog)
        self.button_dataset_config_file_path.setObjectName(u"button_dataset_config_file_path")
        self.button_dataset_config_file_path.setEnabled(True)

        self.gridLayout.addWidget(self.button_dataset_config_file_path, 3, 2, 1, 1)

        self.label_model_description = QLabel(Dialog)
        self.label_model_description.setObjectName(u"label_model_description")
        self.label_model_description.setFont(font2)
        self.label_model_description.setToolTipDuration(30000)
        self.label_model_description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_model_description, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.verticalLayout_2.setStretch(2, 5)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_add_new_model.setText(QCoreApplication.translate("Dialog", u"\uc2e0\uaddc AI \ubaa8\ub378 \ub4f1\ub85d", None))
#if QT_CONFIG(tooltip)
        self.line_edit_model_description.setToolTip(QCoreApplication.translate("Dialog", u"<nobr><b>\ud504\ub85c\uadf8\ub7a8 \ub0b4\uc5d0\uc11c \ud45c\uc2dc\ub418\ub294 \uc774\ub984</b>\uc73c\ub85c, \uc0ac\uc6a9\uc790\uac00 \ubaa8\ub378\uc744 \uad6c\ubd84\ud560 \ub54c \uc0ac\uc6a9\ud569\ub2c8\ub2e4.</nobr>", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_model_description.setPlaceholderText(QCoreApplication.translate("Dialog", u"ex) \ubd88\ud2f0 \uac80\ucd9c", None))
#if QT_CONFIG(tooltip)
        self.line_edit_model_file_path.setToolTip(QCoreApplication.translate("Dialog", u"<nobr>Triton \uc11c\ubc84\uc5d0 \uc5c5\ub85c\ub4dc\ud560<b> AI \ubaa8\ub378 \ud30c\uc77c\uc758 \uc808\ub300 \uacbd\ub85c</b>\ub97c \uc785\ub825\ud569\ub2c8\ub2e4.<br><font color=\"#888888\"><i><u><b>(\uc601\ubb38\ub9cc \uc785\ub825 \uac00\ub2a5, \ud30c\uc77c \ud615\uc2dd: *.pt)</nobr></b></u></i></font>", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_model_file_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"ex) /home/rist/bulti.pt", None))
#if QT_CONFIG(tooltip)
        self.line_edit_model_name.setToolTip(QCoreApplication.translate("Dialog", u"<nobr><b>Triton \uc11c\ubc84\uc5d0 \ub4f1\ub85d\ud560 \ubaa8\ub378\uba85</b>\uc73c\ub85c, \ud504\ub85c\uadf8\ub7a8\uc774 \ud574\ub2f9 \ubaa8\ub378\uc744 \ubd88\ub7ec\uc62c \ub54c \uc0ac\uc6a9\ub429\ub2c8\ub2e4.<br><font color=\"#888888\"><i><u><b>(\uc601\ubb38\ub9cc \uc785\ub825 \uac00\ub2a5)</nobr></b></u></i></font>", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_model_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"ex) bulti", None))
#if QT_CONFIG(tooltip)
        self.label_dataset_config_file_path.setToolTip(QCoreApplication.translate("Dialog", u"\ubaa8\ub378 \ud559\uc2b5\uc5d0 \uc0ac\uc6a9\ud560 \ub370\uc774\ud130 \uad6c\uc131\uc744 \uc815\uc758\ud55c \uc124\uc815 \ud30c\uc77c \uacbd\ub85c (\ud30c\uc77c \ud615\uc2dd : *.yaml)", None))
#endif // QT_CONFIG(tooltip)
        self.label_dataset_config_file_path.setText(QCoreApplication.translate("Dialog", u"\ub370\uc774\ud130 \uad6c\uc131 \ud30c\uc77c", None))
        self.button_model_file_path.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_model_name.setToolTip(QCoreApplication.translate("Dialog", u"<nobr><b>Triton \uc11c\ubc84\uc5d0 \ub4f1\ub85d\ud560 \ubaa8\ub378\uba85</b>\uc73c\ub85c, \ud504\ub85c\uadf8\ub7a8\uc774 \ud574\ub2f9 \ubaa8\ub378\uc744 \ubd88\ub7ec\uc62c \ub54c \uc0ac\uc6a9\ub429\ub2c8\ub2e4.<br><font color=\"#888888\"><i><u><b>(\uc601\ubb38\ub9cc \uc785\ub825 \uac00\ub2a5)</nobr></b></u></i></font>", None))
#endif // QT_CONFIG(tooltip)
        self.label_model_name.setText(QCoreApplication.translate("Dialog", u"\ubaa8\ub378 ID", None))
#if QT_CONFIG(tooltip)
        self.line_edit_dataset_config_file_path.setToolTip(QCoreApplication.translate("Dialog", u"\ubaa8\ub378 \ud559\uc2b5\uc5d0 \uc0ac\uc6a9\ud560 \ub370\uc774\ud130 \uad6c\uc131\uc744 \uc815\uc758\ud55c \uc124\uc815 \ud30c\uc77c \uacbd\ub85c (\ud30c\uc77c \ud615\uc2dd : *.yaml)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_model_file_path.setToolTip(QCoreApplication.translate("Dialog", u"<nobr>Triton \uc11c\ubc84\uc5d0 \uc5c5\ub85c\ub4dc\ud560<b> AI \ubaa8\ub378 \ud30c\uc77c\uc758 \uc808\ub300 \uacbd\ub85c</b>\ub97c \uc785\ub825\ud569\ub2c8\ub2e4.<br><font color=\"#888888\"><i><u><b>(\uc601\ubb38\ub9cc \uc785\ub825 \uac00\ub2a5, \ud30c\uc77c \ud615\uc2dd: *.pt)</nobr></b></u></i></font>", None))
#endif // QT_CONFIG(tooltip)
        self.label_model_file_path.setText(QCoreApplication.translate("Dialog", u"\ubaa8\ub378 \ud30c\uc77c", None))
        self.button_dataset_config_file_path.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_model_description.setToolTip(QCoreApplication.translate("Dialog", u"<nobr><b>\ud504\ub85c\uadf8\ub7a8 \ub0b4\uc5d0\uc11c \ud45c\uc2dc\ub418\ub294 \uc774\ub984</b>\uc73c\ub85c, \uc0ac\uc6a9\uc790\uac00 \ubaa8\ub378\uc744 \uad6c\ubd84\ud560 \ub54c \uc0ac\uc6a9\ud569\ub2c8\ub2e4.</nobr>", None))
#endif // QT_CONFIG(tooltip)
        self.label_model_description.setText(QCoreApplication.translate("Dialog", u"\ubaa8\ub378\uba85", None))
    # retranslateUi

