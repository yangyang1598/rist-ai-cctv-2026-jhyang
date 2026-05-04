# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_register_management_dialogHWUEHd.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(615, 506)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_camera_protocol_2 = QLabel(self.groupBox_2)
        self.label_camera_protocol_2.setObjectName(u"label_camera_protocol_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_camera_protocol_2.sizePolicy().hasHeightForWidth())
        self.label_camera_protocol_2.setSizePolicy(sizePolicy)
        self.label_camera_protocol_2.setMaximumSize(QSize(120, 120))
        self.label_camera_protocol_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_camera_protocol_2, 2, 0, 1, 1)

        self.line_edit_stream_path_2 = QLineEdit(self.groupBox_2)
        self.line_edit_stream_path_2.setObjectName(u"line_edit_stream_path_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_stream_path_2.sizePolicy().hasHeightForWidth())
        self.line_edit_stream_path_2.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.line_edit_stream_path_2, 1, 1, 1, 1)

        self.protocol_horizon_2 = QHBoxLayout()
        self.protocol_horizon_2.setObjectName(u"protocol_horizon_2")
        self.radio_tcp_2 = QRadioButton(self.groupBox_2)
        self.radio_tcp_2.setObjectName(u"radio_tcp_2")
        self.radio_tcp_2.setChecked(True)

        self.protocol_horizon_2.addWidget(self.radio_tcp_2)

        self.radio_udp_2 = QRadioButton(self.groupBox_2)
        self.radio_udp_2.setObjectName(u"radio_udp_2")

        self.protocol_horizon_2.addWidget(self.radio_udp_2)


        self.gridLayout_5.addLayout(self.protocol_horizon_2, 2, 1, 1, 1)

        self.label_ip_2 = QLabel(self.groupBox_2)
        self.label_ip_2.setObjectName(u"label_ip_2")
        sizePolicy.setHeightForWidth(self.label_ip_2.sizePolicy().hasHeightForWidth())
        self.label_ip_2.setSizePolicy(sizePolicy)
        self.label_ip_2.setMaximumSize(QSize(120, 120))
        self.label_ip_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_ip_2, 0, 0, 1, 1)

        self.line_edit_ip_2 = QLineEdit(self.groupBox_2)
        self.line_edit_ip_2.setObjectName(u"line_edit_ip_2")
        sizePolicy1.setHeightForWidth(self.line_edit_ip_2.sizePolicy().hasHeightForWidth())
        self.line_edit_ip_2.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.line_edit_ip_2, 0, 1, 1, 1)

        self.label_rtsp_id_2 = QLabel(self.groupBox_2)
        self.label_rtsp_id_2.setObjectName(u"label_rtsp_id_2")
        sizePolicy.setHeightForWidth(self.label_rtsp_id_2.sizePolicy().hasHeightForWidth())
        self.label_rtsp_id_2.setSizePolicy(sizePolicy)
        self.label_rtsp_id_2.setMaximumSize(QSize(120, 120))
        self.label_rtsp_id_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_rtsp_id_2, 3, 0, 1, 1)

        self.label_stream_path_2 = QLabel(self.groupBox_2)
        self.label_stream_path_2.setObjectName(u"label_stream_path_2")
        sizePolicy.setHeightForWidth(self.label_stream_path_2.sizePolicy().hasHeightForWidth())
        self.label_stream_path_2.setSizePolicy(sizePolicy)
        self.label_stream_path_2.setMaximumSize(QSize(120, 120))
        self.label_stream_path_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_stream_path_2, 1, 0, 1, 1)

        self.line_edit_rtsp_id_2 = QLineEdit(self.groupBox_2)
        self.line_edit_rtsp_id_2.setObjectName(u"line_edit_rtsp_id_2")
        sizePolicy1.setHeightForWidth(self.line_edit_rtsp_id_2.sizePolicy().hasHeightForWidth())
        self.line_edit_rtsp_id_2.setSizePolicy(sizePolicy1)
        self.line_edit_rtsp_id_2.setMaximumSize(QSize(10000, 40))

        self.gridLayout_5.addWidget(self.line_edit_rtsp_id_2, 3, 1, 1, 1)

        self.label_rtsp_password_2 = QLabel(self.groupBox_2)
        self.label_rtsp_password_2.setObjectName(u"label_rtsp_password_2")
        sizePolicy.setHeightForWidth(self.label_rtsp_password_2.sizePolicy().hasHeightForWidth())
        self.label_rtsp_password_2.setSizePolicy(sizePolicy)
        self.label_rtsp_password_2.setMaximumSize(QSize(120, 120))
        self.label_rtsp_password_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_rtsp_password_2, 4, 0, 1, 1)

        self.line_edit_rtsp_password_2 = QLineEdit(self.groupBox_2)
        self.line_edit_rtsp_password_2.setObjectName(u"line_edit_rtsp_password_2")
        sizePolicy1.setHeightForWidth(self.line_edit_rtsp_password_2.sizePolicy().hasHeightForWidth())
        self.line_edit_rtsp_password_2.setSizePolicy(sizePolicy1)
        self.line_edit_rtsp_password_2.setMaximumSize(QSize(10000, 40))

        self.gridLayout_5.addWidget(self.line_edit_rtsp_password_2, 4, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.gridLayout_7 = QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.line_edit_video_port_2 = QLineEdit(self.groupBox_3)
        self.line_edit_video_port_2.setObjectName(u"line_edit_video_port_2")
        sizePolicy1.setHeightForWidth(self.line_edit_video_port_2.sizePolicy().hasHeightForWidth())
        self.line_edit_video_port_2.setSizePolicy(sizePolicy1)

        self.gridLayout_7.addWidget(self.line_edit_video_port_2, 1, 1, 1, 1)

        self.line_edit_ptz_port_2 = QLineEdit(self.groupBox_3)
        self.line_edit_ptz_port_2.setObjectName(u"line_edit_ptz_port_2")
        sizePolicy1.setHeightForWidth(self.line_edit_ptz_port_2.sizePolicy().hasHeightForWidth())
        self.line_edit_ptz_port_2.setSizePolicy(sizePolicy1)

        self.gridLayout_7.addWidget(self.line_edit_ptz_port_2, 2, 1, 1, 1)

        self.label_ptz_port_2 = QLabel(self.groupBox_3)
        self.label_ptz_port_2.setObjectName(u"label_ptz_port_2")
        sizePolicy.setHeightForWidth(self.label_ptz_port_2.sizePolicy().hasHeightForWidth())
        self.label_ptz_port_2.setSizePolicy(sizePolicy)
        self.label_ptz_port_2.setMaximumSize(QSize(120, 120))
        self.label_ptz_port_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_ptz_port_2, 2, 0, 1, 1)

        self.label_video_port_2 = QLabel(self.groupBox_3)
        self.label_video_port_2.setObjectName(u"label_video_port_2")
        sizePolicy.setHeightForWidth(self.label_video_port_2.sizePolicy().hasHeightForWidth())
        self.label_video_port_2.setSizePolicy(sizePolicy)
        self.label_video_port_2.setMaximumSize(QSize(120, 120))
        self.label_video_port_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_video_port_2, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 4, 0, 1, 1)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setPointSize(12)
        self.groupBox.setFont(font1)
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_cctv_name_2 = QLabel(self.groupBox)
        self.label_cctv_name_2.setObjectName(u"label_cctv_name_2")
        sizePolicy.setHeightForWidth(self.label_cctv_name_2.sizePolicy().hasHeightForWidth())
        self.label_cctv_name_2.setSizePolicy(sizePolicy)
        self.label_cctv_name_2.setMaximumSize(QSize(120, 120))
        self.label_cctv_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_cctv_name_2, 1, 0, 1, 1)

        self.combo_camera_location_2 = QComboBox(self.groupBox)
        self.combo_camera_location_2.setObjectName(u"combo_camera_location_2")
        sizePolicy1.setHeightForWidth(self.combo_camera_location_2.sizePolicy().hasHeightForWidth())
        self.combo_camera_location_2.setSizePolicy(sizePolicy1)
        self.combo_camera_location_2.setMaximumSize(QSize(10000, 40))
        font2 = QFont()
        font2.setPointSize(9)
        self.combo_camera_location_2.setFont(font2)

        self.gridLayout_6.addWidget(self.combo_camera_location_2, 0, 1, 1, 1)

        self.line_edit_cctv_name_2 = QLineEdit(self.groupBox)
        self.line_edit_cctv_name_2.setObjectName(u"line_edit_cctv_name_2")
        sizePolicy1.setHeightForWidth(self.line_edit_cctv_name_2.sizePolicy().hasHeightForWidth())
        self.line_edit_cctv_name_2.setSizePolicy(sizePolicy1)
        self.line_edit_cctv_name_2.setFont(font2)

        self.gridLayout_6.addWidget(self.line_edit_cctv_name_2, 1, 1, 1, 1)

        self.label_camera_location_2 = QLabel(self.groupBox)
        self.label_camera_location_2.setObjectName(u"label_camera_location_2")
        sizePolicy.setHeightForWidth(self.label_camera_location_2.sizePolicy().hasHeightForWidth())
        self.label_camera_location_2.setSizePolicy(sizePolicy)
        self.label_camera_location_2.setMaximumSize(QSize(120, 120))
        self.label_camera_location_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_camera_location_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.button_accept_2 = QPushButton(Dialog)
        self.button_accept_2.setObjectName(u"button_accept_2")

        self.horizontalLayout_2.addWidget(self.button_accept_2)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 7, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"RTSP \uc815\ubcf4", None))
        self.label_camera_protocol_2.setText(QCoreApplication.translate("Dialog", u"\ud504\ub85c\ud1a0\ucf5c", None))
        self.radio_tcp_2.setText(QCoreApplication.translate("Dialog", u"RTP/TCP", None))
        self.radio_udp_2.setText(QCoreApplication.translate("Dialog", u"RTP/UDP", None))
        self.label_ip_2.setText(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c IP", None))
        self.label_rtsp_id_2.setText(QCoreApplication.translate("Dialog", u"RTSP \uc544\uc774\ub514", None))
        self.label_stream_path_2.setText(QCoreApplication.translate("Dialog", u"Stream Path", None))
        self.label_rtsp_password_2.setText(QCoreApplication.translate("Dialog", u"RTSP \ube44\ubc00\ubc88\ud638", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u" \ud3ec\ud2b8      ", None))
        self.label_ptz_port_2.setText(QCoreApplication.translate("Dialog", u"\uc81c\uc5b4\uc6a9", None))
        self.label_video_port_2.setText(QCoreApplication.translate("Dialog", u"\uc601\uc0c1\uc6a9", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c \uc815\ubcf4", None))
        self.label_cctv_name_2.setText(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c \uc774\ub984", None))
        self.label_camera_location_2.setText(QCoreApplication.translate("Dialog", u"\uae30\uae30 \uc704\uce58", None))
        self.button_accept_2.setText(QCoreApplication.translate("Dialog", u"\ub4f1\ub85d", None))
    # retranslateUi

