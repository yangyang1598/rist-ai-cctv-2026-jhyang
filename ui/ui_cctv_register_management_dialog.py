# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv_register_management_dialogZhSiuh.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(684, 488)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.port_info = QGridLayout()
        self.port_info.setObjectName(u"port_info")
        self.label_port = QLabel(Dialog)
        self.label_port.setObjectName(u"label_port")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_port.sizePolicy().hasHeightForWidth())
        self.label_port.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(15)
        self.label_port.setFont(font)
        self.label_port.setFrameShape(QFrame.Shape.WinPanel)
        self.label_port.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_port.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.port_info.addWidget(self.label_port, 0, 0, 1, 1)

        self.label_ptz_port = QLabel(Dialog)
        self.label_ptz_port.setObjectName(u"label_ptz_port")
        self.label_ptz_port.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.port_info.addWidget(self.label_ptz_port, 2, 0, 1, 1)

        self.line_edit_ptz_port = QLineEdit(Dialog)
        self.line_edit_ptz_port.setObjectName(u"line_edit_ptz_port")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_ptz_port.sizePolicy().hasHeightForWidth())
        self.line_edit_ptz_port.setSizePolicy(sizePolicy1)

        self.port_info.addWidget(self.line_edit_ptz_port, 2, 1, 1, 1)

        self.label_video_port = QLabel(Dialog)
        self.label_video_port.setObjectName(u"label_video_port")
        self.label_video_port.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.port_info.addWidget(self.label_video_port, 1, 0, 1, 1)

        self.line_edit_video_port = QLineEdit(Dialog)
        self.line_edit_video_port.setObjectName(u"line_edit_video_port")
        sizePolicy1.setHeightForWidth(self.line_edit_video_port.sizePolicy().hasHeightForWidth())
        self.line_edit_video_port.setSizePolicy(sizePolicy1)

        self.port_info.addWidget(self.line_edit_video_port, 1, 1, 1, 1)


        self.gridLayout.addLayout(self.port_info, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.rtsp_info = QGridLayout()
        self.rtsp_info.setObjectName(u"rtsp_info")
        self.label_ip = QLabel(Dialog)
        self.label_ip.setObjectName(u"label_ip")
        self.label_ip.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_ip, 4, 0, 1, 1)

        self.label_rtsp_password = QLabel(Dialog)
        self.label_rtsp_password.setObjectName(u"label_rtsp_password")
        self.label_rtsp_password.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_rtsp_password, 8, 0, 1, 1)

        self.line_edit_rtsp_password = QLineEdit(Dialog)
        self.line_edit_rtsp_password.setObjectName(u"line_edit_rtsp_password")
        sizePolicy1.setHeightForWidth(self.line_edit_rtsp_password.sizePolicy().hasHeightForWidth())
        self.line_edit_rtsp_password.setSizePolicy(sizePolicy1)
        self.line_edit_rtsp_password.setMaximumSize(QSize(10000, 40))

        self.rtsp_info.addWidget(self.line_edit_rtsp_password, 8, 2, 1, 1)

        self.label_rtsp_id = QLabel(Dialog)
        self.label_rtsp_id.setObjectName(u"label_rtsp_id")
        self.label_rtsp_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_rtsp_id, 7, 0, 1, 1)

        self.label_camera_protocol = QLabel(Dialog)
        self.label_camera_protocol.setObjectName(u"label_camera_protocol")
        self.label_camera_protocol.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_camera_protocol, 6, 0, 1, 1)

        self.protocol_horizon = QHBoxLayout()
        self.protocol_horizon.setObjectName(u"protocol_horizon")
        self.radio_tcp = QRadioButton(Dialog)
        self.radio_tcp.setObjectName(u"radio_tcp")
        self.radio_tcp.setChecked(True)

        self.protocol_horizon.addWidget(self.radio_tcp)

        self.radio_udp = QRadioButton(Dialog)
        self.radio_udp.setObjectName(u"radio_udp")

        self.protocol_horizon.addWidget(self.radio_udp)


        self.rtsp_info.addLayout(self.protocol_horizon, 6, 2, 1, 1)

        self.line_edit_rtsp_id = QLineEdit(Dialog)
        self.line_edit_rtsp_id.setObjectName(u"line_edit_rtsp_id")
        sizePolicy1.setHeightForWidth(self.line_edit_rtsp_id.sizePolicy().hasHeightForWidth())
        self.line_edit_rtsp_id.setSizePolicy(sizePolicy1)
        self.line_edit_rtsp_id.setMaximumSize(QSize(10000, 40))

        self.rtsp_info.addWidget(self.line_edit_rtsp_id, 7, 2, 1, 1)

        self.line_edit_ip = QLineEdit(Dialog)
        self.line_edit_ip.setObjectName(u"line_edit_ip")
        sizePolicy1.setHeightForWidth(self.line_edit_ip.sizePolicy().hasHeightForWidth())
        self.line_edit_ip.setSizePolicy(sizePolicy1)

        self.rtsp_info.addWidget(self.line_edit_ip, 4, 2, 1, 1)

        self.label_rtsp_info = QLabel(Dialog)
        self.label_rtsp_info.setObjectName(u"label_rtsp_info")
        self.label_rtsp_info.setFont(font)
        self.label_rtsp_info.setFrameShape(QFrame.Shape.WinPanel)
        self.label_rtsp_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_rtsp_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_rtsp_info, 1, 0, 1, 1)

        self.label_stream_path = QLabel(Dialog)
        self.label_stream_path.setObjectName(u"label_stream_path")
        self.label_stream_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rtsp_info.addWidget(self.label_stream_path, 5, 0, 1, 1)

        self.line_edit_stream_path = QLineEdit(Dialog)
        self.line_edit_stream_path.setObjectName(u"line_edit_stream_path")

        self.rtsp_info.addWidget(self.line_edit_stream_path, 5, 2, 1, 1)


        self.gridLayout.addLayout(self.rtsp_info, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.camera_info = QGridLayout()
        self.camera_info.setObjectName(u"camera_info")
        self.camera_info.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.line_edit_cctv_name = QLineEdit(Dialog)
        self.line_edit_cctv_name.setObjectName(u"line_edit_cctv_name")
        sizePolicy1.setHeightForWidth(self.line_edit_cctv_name.sizePolicy().hasHeightForWidth())
        self.line_edit_cctv_name.setSizePolicy(sizePolicy1)

        self.camera_info.addWidget(self.line_edit_cctv_name, 2, 1, 1, 1)

        self.combo_camera_location = QComboBox(Dialog)
        self.combo_camera_location.setObjectName(u"combo_camera_location")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.combo_camera_location.sizePolicy().hasHeightForWidth())
        self.combo_camera_location.setSizePolicy(sizePolicy2)
        self.combo_camera_location.setMaximumSize(QSize(10000, 40))

        self.camera_info.addWidget(self.combo_camera_location, 1, 1, 1, 1)

        self.label_camera_info = QLabel(Dialog)
        self.label_camera_info.setObjectName(u"label_camera_info")
        sizePolicy.setHeightForWidth(self.label_camera_info.sizePolicy().hasHeightForWidth())
        self.label_camera_info.setSizePolicy(sizePolicy)
        self.label_camera_info.setFont(font)
        self.label_camera_info.setFrameShape(QFrame.Shape.WinPanel)
        self.label_camera_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_camera_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.camera_info.addWidget(self.label_camera_info, 0, 0, 1, 1)

        self.label_camera_location = QLabel(Dialog)
        self.label_camera_location.setObjectName(u"label_camera_location")
        self.label_camera_location.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.camera_info.addWidget(self.label_camera_location, 1, 0, 1, 1)

        self.label_cctv_name = QLabel(Dialog)
        self.label_cctv_name.setObjectName(u"label_cctv_name")
        self.label_cctv_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.camera_info.addWidget(self.label_cctv_name, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.camera_info, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_accept = QPushButton(Dialog)
        self.button_accept.setObjectName(u"button_accept")

        self.horizontalLayout.addWidget(self.button_accept)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_port.setText(QCoreApplication.translate("Dialog", u"      \ud3ec\ud2b8      ", None))
        self.label_ptz_port.setText(QCoreApplication.translate("Dialog", u"\uc81c\uc5b4\uc6a9", None))
        self.label_video_port.setText(QCoreApplication.translate("Dialog", u"\uc601\uc0c1\uc6a9", None))
        self.label_ip.setText(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c IP", None))
        self.label_rtsp_password.setText(QCoreApplication.translate("Dialog", u"RTSP \ube44\ubc00\ubc88\ud638", None))
        self.label_rtsp_id.setText(QCoreApplication.translate("Dialog", u"RTSP \uc544\uc774\ub514", None))
        self.label_camera_protocol.setText(QCoreApplication.translate("Dialog", u"\ud504\ub85c\ud1a0\ucf5c", None))
        self.radio_tcp.setText(QCoreApplication.translate("Dialog", u"RTP/TCP", None))
        self.radio_udp.setText(QCoreApplication.translate("Dialog", u"RTP/UDP", None))
        self.label_rtsp_info.setText(QCoreApplication.translate("Dialog", u"RTSP \uc815\ubcf4", None))
        self.label_stream_path.setText(QCoreApplication.translate("Dialog", u"Stream Path", None))
        self.label_camera_info.setText(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c \uc815\ubcf4", None))
        self.label_camera_location.setText(QCoreApplication.translate("Dialog", u"\uae30\uae30 \uc704\uce58", None))
        self.label_cctv_name.setText(QCoreApplication.translate("Dialog", u"\uce74\uba54\ub77c \uc774\ub984", None))
        self.button_accept.setText(QCoreApplication.translate("Dialog", u"\ub4f1\ub85d", None))
    # retranslateUi

