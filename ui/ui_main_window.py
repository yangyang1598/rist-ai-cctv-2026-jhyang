# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowsIrZIq.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 1018)
        MainWindow.setMinimumSize(QSize(1600, 1000))
        self.action_cctv_settings = QAction(MainWindow)
        self.action_cctv_settings.setObjectName(u"action_cctv_settings")
        self.action_system_status = QAction(MainWindow)
        self.action_system_status.setObjectName(u"action_system_status")
        self.action_event_logs = QAction(MainWindow)
        self.action_event_logs.setObjectName(u"action_event_logs")
        self.action_rpa_settings = QAction(MainWindow)
        self.action_rpa_settings.setObjectName(u"action_rpa_settings")
        self.action_event_logic_management = QAction(MainWindow)
        self.action_event_logic_management.setObjectName(u"action_event_logic_management")
        self.action_ai_train_management = QAction(MainWindow)
        self.action_ai_train_management.setObjectName(u"action_ai_train_management")
        self.action_cctv_management = QAction(MainWindow)
        self.action_cctv_management.setObjectName(u"action_cctv_management")
        self.action_auto_delete_settings = QAction(MainWindow)
        self.action_auto_delete_settings.setObjectName(u"action_auto_delete_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.layout_right = QHBoxLayout()
        self.layout_right.setObjectName(u"layout_right")
        self.layout_left = QVBoxLayout()
        self.layout_left.setObjectName(u"layout_left")
        self.layout_left.setContentsMargins(5, 10, 10, 0)
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setMinimumSize(QSize(0, 0))
        self.label_logo.setMaximumSize(QSize(290, 90))
        font = QFont()
        font.setPointSize(9)
        self.label_logo.setFont(font)
        self.label_logo.setStyleSheet(u"")
        self.label_logo.setLineWidth(1)
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo.setMargin(0)

        self.layout_left.addWidget(self.label_logo)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_user_name = QLabel(self.centralwidget)
        self.label_user_name.setObjectName(u"label_user_name")
        font1 = QFont()
        font1.setPointSize(18)
        self.label_user_name.setFont(font1)

        self.horizontalLayout.addWidget(self.label_user_name)

        self.label_title_id = QLabel(self.centralwidget)
        self.label_title_id.setObjectName(u"label_title_id")
        self.label_title_id.setFont(font1)

        self.horizontalLayout.addWidget(self.label_title_id)


        self.layout_left.addLayout(self.horizontalLayout)

        self.label_clock_widget = QLabel(self.centralwidget)
        self.label_clock_widget.setObjectName(u"label_clock_widget")
        self.label_clock_widget.setMinimumSize(QSize(300, 0))
        font2 = QFont()
        font2.setPointSize(12)
        self.label_clock_widget.setFont(font2)
        self.label_clock_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_clock_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_left.addWidget(self.label_clock_widget)

        self.label_cctv_connection_status = QLabel(self.centralwidget)
        self.label_cctv_connection_status.setObjectName(u"label_cctv_connection_status")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.label_cctv_connection_status.setFont(font3)

        self.layout_left.addWidget(self.label_cctv_connection_status)

        self.label_cctv_connection_status_widget = QLabel(self.centralwidget)
        self.label_cctv_connection_status_widget.setObjectName(u"label_cctv_connection_status_widget")
        self.label_cctv_connection_status_widget.setMinimumSize(QSize(300, 0))
        self.label_cctv_connection_status_widget.setMaximumSize(QSize(16777215, 16777215))
        self.label_cctv_connection_status_widget.setFont(font2)
        self.label_cctv_connection_status_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_cctv_connection_status_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_left.addWidget(self.label_cctv_connection_status_widget)

        self.label_cctv_list = QLabel(self.centralwidget)
        self.label_cctv_list.setObjectName(u"label_cctv_list")
        self.label_cctv_list.setFont(font3)

        self.layout_left.addWidget(self.label_cctv_list)

        self.label_cctv_list_widget = QLabel(self.centralwidget)
        self.label_cctv_list_widget.setObjectName(u"label_cctv_list_widget")
        self.label_cctv_list_widget.setMinimumSize(QSize(300, 110))
        self.label_cctv_list_widget.setFont(font2)
        self.label_cctv_list_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_cctv_list_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_left.addWidget(self.label_cctv_list_widget)

        self.label_video_layout_widget = QLabel(self.centralwidget)
        self.label_video_layout_widget.setObjectName(u"label_video_layout_widget")
        self.label_video_layout_widget.setMinimumSize(QSize(300, 110))
        self.label_video_layout_widget.setFont(font2)
        self.label_video_layout_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_video_layout_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_left.addWidget(self.label_video_layout_widget)

        self.label_ptz_controller = QLabel(self.centralwidget)
        self.label_ptz_controller.setObjectName(u"label_ptz_controller")
        self.label_ptz_controller.setFont(font3)

        self.layout_left.addWidget(self.label_ptz_controller)

        self.label_ptz_controller_widget = QLabel(self.centralwidget)
        self.label_ptz_controller_widget.setObjectName(u"label_ptz_controller_widget")
        self.label_ptz_controller_widget.setMinimumSize(QSize(300, 270))
        self.label_ptz_controller_widget.setFont(font2)
        self.label_ptz_controller_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ptz_controller_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_left.addWidget(self.label_ptz_controller_widget)

        self.layout_left.setStretch(6, 1)
        self.layout_left.setStretch(7, 1)

        self.layout_right.addLayout(self.layout_left)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.button_show_sidebar = QPushButton(self.centralwidget)
        self.button_show_sidebar.setObjectName(u"button_show_sidebar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.button_show_sidebar.sizePolicy().hasHeightForWidth())
        self.button_show_sidebar.setSizePolicy(sizePolicy1)
        self.button_show_sidebar.setMaximumSize(QSize(20, 80))
        self.button_show_sidebar.setStyleSheet(u"background-color:rgb(25, 53, 83);\n"
"color: rgb(255, 255, 255);")
        self.button_show_sidebar.setCheckable(True)

        self.verticalLayout_2.addWidget(self.button_show_sidebar)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.layout_right.addLayout(self.verticalLayout_2)

        self.layout_center = QVBoxLayout()
        self.layout_center.setObjectName(u"layout_center")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, -1, -1, -1)
        self.button_video_player_layout_1x1 = QPushButton(self.centralwidget)
        self.button_video_player_layout_1x1.setObjectName(u"button_video_player_layout_1x1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_video_player_layout_1x1.sizePolicy().hasHeightForWidth())
        self.button_video_player_layout_1x1.setSizePolicy(sizePolicy2)
        self.button_video_player_layout_1x1.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_8.addWidget(self.button_video_player_layout_1x1)

        self.button_video_player_layout_2x2 = QPushButton(self.centralwidget)
        self.button_video_player_layout_2x2.setObjectName(u"button_video_player_layout_2x2")
        sizePolicy2.setHeightForWidth(self.button_video_player_layout_2x2.sizePolicy().hasHeightForWidth())
        self.button_video_player_layout_2x2.setSizePolicy(sizePolicy2)
        self.button_video_player_layout_2x2.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_8.addWidget(self.button_video_player_layout_2x2)

        self.button_video_player_layout_3x3 = QPushButton(self.centralwidget)
        self.button_video_player_layout_3x3.setObjectName(u"button_video_player_layout_3x3")
        sizePolicy2.setHeightForWidth(self.button_video_player_layout_3x3.sizePolicy().hasHeightForWidth())
        self.button_video_player_layout_3x3.setSizePolicy(sizePolicy2)
        self.button_video_player_layout_3x3.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_8.addWidget(self.button_video_player_layout_3x3)

        self.button_video_player_layout_4x4 = QPushButton(self.centralwidget)
        self.button_video_player_layout_4x4.setObjectName(u"button_video_player_layout_4x4")
        sizePolicy2.setHeightForWidth(self.button_video_player_layout_4x4.sizePolicy().hasHeightForWidth())
        self.button_video_player_layout_4x4.setSizePolicy(sizePolicy2)
        self.button_video_player_layout_4x4.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_8.addWidget(self.button_video_player_layout_4x4)

        self.button_video_player_layout_5x5 = QPushButton(self.centralwidget)
        self.button_video_player_layout_5x5.setObjectName(u"button_video_player_layout_5x5")
        sizePolicy2.setHeightForWidth(self.button_video_player_layout_5x5.sizePolicy().hasHeightForWidth())
        self.button_video_player_layout_5x5.setSizePolicy(sizePolicy2)
        self.button_video_player_layout_5x5.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_8.addWidget(self.button_video_player_layout_5x5)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, -1, -1, -1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout_7)


        self.layout_center.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.checkBox_activate_grid = QCheckBox(self.centralwidget)
        self.checkBox_activate_grid.setObjectName(u"checkBox_activate_grid")

        self.horizontalLayout_9.addWidget(self.checkBox_activate_grid)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)

        self.button_modify_layout = QPushButton(self.centralwidget)
        self.button_modify_layout.setObjectName(u"button_modify_layout")
        self.button_modify_layout.setCheckable(True)

        self.horizontalLayout_9.addWidget(self.button_modify_layout)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)

        self.button_delete_selected_layout = QPushButton(self.centralwidget)
        self.button_delete_selected_layout.setObjectName(u"button_delete_selected_layout")

        self.horizontalLayout_9.addWidget(self.button_delete_selected_layout)


        self.layout_center.addLayout(self.horizontalLayout_9)

        self.tab_widget_video_player = QTabWidget(self.centralwidget)
        self.tab_widget_video_player.setObjectName(u"tab_widget_video_player")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_snapshot_image_widget = QLabel(self.tab)
        self.label_snapshot_image_widget.setObjectName(u"label_snapshot_image_widget")
        self.label_snapshot_image_widget.setFont(font1)
        self.label_snapshot_image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_snapshot_image_widget, 0, 0, 1, 1)

        self.tab_widget_video_player.addTab(self.tab, "")

        self.layout_center.addWidget(self.tab_widget_video_player)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_ai_event_log = QLabel(self.centralwidget)
        self.label_ai_event_log.setObjectName(u"label_ai_event_log")

        self.horizontalLayout_3.addWidget(self.label_ai_event_log)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.button_show_event_log = QPushButton(self.centralwidget)
        self.button_show_event_log.setObjectName(u"button_show_event_log")
        self.button_show_event_log.setStyleSheet(u"background-color: rgb(25, 53, 83);\n"
"\n"
"color: rgb(255, 255, 255);")
        self.button_show_event_log.setCheckable(True)
        self.button_show_event_log.setChecked(False)

        self.horizontalLayout_3.addWidget(self.button_show_event_log)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.layout_center.addLayout(self.horizontalLayout_3)

        self.label_ai_event_log_widget = QLabel(self.centralwidget)
        self.label_ai_event_log_widget.setObjectName(u"label_ai_event_log_widget")
        self.label_ai_event_log_widget.setMinimumSize(QSize(250, 150))
        self.label_ai_event_log_widget.setFont(font2)
        self.label_ai_event_log_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_ai_event_log_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_center.addWidget(self.label_ai_event_log_widget)

        self.layout_center.setStretch(2, 4)

        self.layout_right.addLayout(self.layout_center)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.button_show_ai_event_image_log = QPushButton(self.centralwidget)
        self.button_show_ai_event_image_log.setObjectName(u"button_show_ai_event_image_log")
        sizePolicy1.setHeightForWidth(self.button_show_ai_event_image_log.sizePolicy().hasHeightForWidth())
        self.button_show_ai_event_image_log.setSizePolicy(sizePolicy1)
        self.button_show_ai_event_image_log.setMaximumSize(QSize(20, 80))
        self.button_show_ai_event_image_log.setStyleSheet(u"background-color:rgb(25, 53, 83);\n"
"color: rgb(255, 255, 255);")
        self.button_show_ai_event_image_log.setCheckable(True)

        self.verticalLayout.addWidget(self.button_show_ai_event_image_log)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.layout_right.addLayout(self.verticalLayout)

        self.label_event_log_image_widget = QLabel(self.centralwidget)
        self.label_event_log_image_widget.setObjectName(u"label_event_log_image_widget")
        self.label_event_log_image_widget.setFont(font2)
        self.label_event_log_image_widget.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.label_event_log_image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_right.addWidget(self.label_event_log_image_widget)

        self.layout_right.setStretch(2, 4)
        self.layout_right.setStretch(4, 1)

        self.horizontalLayout_5.addLayout(self.layout_right)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 23))
        self.menu_program = QMenu(self.menubar)
        self.menu_program.setObjectName(u"menu_program")
        self.menu_setting = QMenu(self.menubar)
        self.menu_setting.setObjectName(u"menu_setting")
        self.menu_management = QMenu(self.menubar)
        self.menu_management.setObjectName(u"menu_management")
        self.menu_restart_stream = QMenu(self.menubar)
        self.menu_restart_stream.setObjectName(u"menu_restart_stream")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_program.menuAction())
        self.menubar.addAction(self.menu_setting.menuAction())
        self.menubar.addAction(self.menu_management.menuAction())
        self.menubar.addAction(self.menu_restart_stream.menuAction())
        self.menu_program.addSeparator()
        self.menu_program.addAction(self.action_system_status)
        self.menu_program.addAction(self.action_event_logs)
        self.menu_setting.addAction(self.action_cctv_settings)
        self.menu_setting.addAction(self.action_rpa_settings)
        self.menu_setting.addAction(self.action_auto_delete_settings)
        self.menu_management.addAction(self.action_cctv_management)
        self.menu_management.addAction(self.action_event_logic_management)
        self.menu_management.addAction(self.action_ai_train_management)

        self.retranslateUi(MainWindow)

        self.tab_widget_video_player.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_cctv_settings.setText(QCoreApplication.translate("MainWindow", u"CCTV \uc124\uc815", None))
        self.action_system_status.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c \uc0c1\ud0dc \ud655\uc778", None))
        self.action_event_logs.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \ud655\uc778", None))
        self.action_rpa_settings.setText(QCoreApplication.translate("MainWindow", u"RPA \uc124\uc815", None))
        self.action_event_logic_management.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ub85c\uc9c1 \uad00\ub9ac", None))
        self.action_ai_train_management.setText(QCoreApplication.translate("MainWindow", u"AI \ud559\uc2b5 \uad00\ub9ac", None))
        self.action_cctv_management.setText(QCoreApplication.translate("MainWindow", u"CCTV \uad00\ub9ac", None))
        self.action_auto_delete_settings.setText(QCoreApplication.translate("MainWindow", u"\uc790\ub3d9 \uc815\ub9ac \uc124\uc815", None))
        self.label_logo.setText("")
        self.label_user_name.setText(QCoreApplication.translate("MainWindow", u"\u25b2  ID: ", None))
        self.label_title_id.setText(QCoreApplication.translate("MainWindow", u"root", None))
        self.label_clock_widget.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \uc2dc\uac04 \uc704\uc82f", None))
        self.label_cctv_connection_status.setText(QCoreApplication.translate("MainWindow", u"\u25b2 CCTV \uc5f0\uacb0 \uc0c1\ud0dc", None))
        self.label_cctv_connection_status_widget.setText(QCoreApplication.translate("MainWindow", u"CCTV \uc5f0\uacb0 \uc0c1\ud0dc \uc704\uc82f", None))
        self.label_cctv_list.setText(QCoreApplication.translate("MainWindow", u"\u25b2 CCTV \ubaa9\ub85d", None))
        self.label_cctv_list_widget.setText(QCoreApplication.translate("MainWindow", u"CCTV \ubaa9\ub85d \uc704\uc82f", None))
        self.label_video_layout_widget.setText(QCoreApplication.translate("MainWindow", u"\ub808\uc774\uc544\uc6c3 \uad6c\uc131 \ubaa9\ub85d \uc704\uc82f", None))
        self.label_ptz_controller.setText(QCoreApplication.translate("MainWindow", u"\u25b2 PTZ \uc81c\uc5b4", None))
        self.label_ptz_controller_widget.setText(QCoreApplication.translate("MainWindow", u"PTZ \uc81c\uc5b4 \uc704\uc82f", None))
        self.button_show_sidebar.setText(QCoreApplication.translate("MainWindow", u"\u25c0", None))
        self.button_video_player_layout_1x1.setText(QCoreApplication.translate("MainWindow", u"1x1", None))
        self.button_video_player_layout_2x2.setText(QCoreApplication.translate("MainWindow", u"2x2", None))
        self.button_video_player_layout_3x3.setText(QCoreApplication.translate("MainWindow", u"3x3", None))
        self.button_video_player_layout_4x4.setText(QCoreApplication.translate("MainWindow", u"4x4", None))
        self.button_video_player_layout_5x5.setText(QCoreApplication.translate("MainWindow", u"5x5", None))
        self.checkBox_activate_grid.setText(QCoreApplication.translate("MainWindow", u"\uaca9\uc790 \ud45c\uc2dc", None))
        self.button_modify_layout.setText(QCoreApplication.translate("MainWindow", u"\ud654\uba74 \ubc30\uce58 \ubcc0\uacbd", None))
        self.button_delete_selected_layout.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd \uadf8\ub9ac\ub4dc \uc0ad\uc81c", None))
        self.label_snapshot_image_widget.setText(QCoreApplication.translate("MainWindow", u"snapshot \uc774\ubbf8\uc9c0 \uadf8\ub9ac\ub4dc", None))
        self.tab_widget_video_player.setTabText(self.tab_widget_video_player.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Snapshot", None))
        self.label_ai_event_log.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 (\ucd5c\uadfc 100\uac74)", None))
        self.button_show_event_log.setText(QCoreApplication.translate("MainWindow", u"\u25bc", None))
        self.label_ai_event_log_widget.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ub85c\uadf8 \ubaa9\ub85d \uc704\uc82f", None))
        self.button_show_ai_event_image_log.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.label_event_log_image_widget.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ub85c\uc9c1 \uc774\ubbf8\uc9c0 \uadf8\ub9ac\ub4dc \uc704\uc82f", None))
        self.menu_program.setTitle(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uadf8\ub7a8", None))
        self.menu_setting.setTitle(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.menu_management.setTitle(QCoreApplication.translate("MainWindow", u"\uad00\ub9ac\uc790 \uba54\ub274", None))
        self.menu_restart_stream.setTitle(QCoreApplication.translate("MainWindow", u"\uc2a4\ud2b8\ub9bc \uc7ac\uc2dc\uc791", None))
    # retranslateUi

