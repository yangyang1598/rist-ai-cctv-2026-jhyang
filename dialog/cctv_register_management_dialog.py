import json
from PySide6.QtWidgets import QDialog, QMessageBox,QLineEdit, QHBoxLayout, QPushButton
from PySide6.QtCore import Slot
from PySide6.QtGui import QFont
from ui.ui_cctv_register_management_dialog import Ui_Dialog  # Qt Designer로 생성된 UI 파일 임포트

from db.db_cctv_location import DbCctvLocation
from db.db_cctv_list import DbCctvList
from db.db_cctv_setting import DbCctvSetting
####수정 중 (06.10)
class CctvRegisterManagementDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None, edit_mode=False, camera_location="", camera_name="", camera_ip="", port="", ptz_port="",protocol="", rtsp_id="", rtsp_pw="", stream_path=""):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("CCTV 등록 및 수정")
        self.camera_list = DbCctvList()
        self.camera_setting= DbCctvSetting()
        
        self.edit_mode = edit_mode
        self.camera_name_original = camera_name

        # 폰트 사이즈 설정
        font = QFont()
        font.setPointSize(14)
        self.line_edit_cctv_name.setFont(font)
        self.line_edit_ip.setFont(font)
        self.line_edit_video_port.setFont(font)
        self.line_edit_ptz_port.setFont(font)
        self.line_edit_rtsp_id.setFont(font)
        self.line_edit_rtsp_password.setFont(font)
        self.line_edit_stream_path.setFont(font)
        
        self.line_edit_rtsp_password.setEchoMode(QLineEdit.Password) # 비밀번호 입력 시 ***로 표시
        
        self.load_camera_locations() # 카메라 위치 로드
        self.defalut_Text() # 다이얼로그 입력창 내 기본 텍스트 지정
        
        # 수정 모드인 경우 기존 값으로 채우기
        if edit_mode:
            self.combo_camera_location.setCurrentText(camera_location)
            self.line_edit_cctv_name.setText(camera_name)
            self.line_edit_ip.setText(camera_ip)
            self.line_edit_video_port.setText(port)
            self.line_edit_ptz_port.setText(ptz_port)
            self.line_edit_rtsp_id.setText(rtsp_id)
            self.line_edit_rtsp_password.setText(rtsp_pw)
            self.line_edit_stream_path.setText(stream_path)
            
            # 프로토콜 설정
            if protocol == "TCP":
                self.radio_tcp.setChecked(True)
            elif protocol == "UDP":
                self.radio_udp.setChecked(True)

        
       
        self.button_accept.clicked.connect(self.clicked_btn_accept) # OK 버튼 클릭 시 처리

    
    def load_camera_locations(self):
        #CameraLocation DB에서 값을 가져와 콤보 박스에 채우기
        locations = DbCctvLocation().select()
        self.combo_camera_location.clear()  # 기존 아이템 삭제
        for location in locations:
            self.combo_camera_location.addItem(location.camera_location)

    def defalut_Text(self):
        self.line_edit_cctv_name.setPlaceholderText("CCTV 1")
        self.line_edit_ip.setPlaceholderText("0.0.0.0")
        self.line_edit_video_port.setPlaceholderText("8554")
        self.line_edit_ptz_port.setPlaceholderText("2020")

    @Slot()
    def clicked_btn_accept(self):
        print("OK 버튼 클릭")

        # 입력된 카메라 이름 가져오기
        new_camera_name = self.line_edit_cctv_name.text().upper()
        
        # camera_name 중복 검사
        if not self.edit_mode or (self.edit_mode and new_camera_name != self.camera_name_original):
            # 새로 추가하는 경우 또는 수정 시 이름이 변경된 경우에만 중복 검사
            existing_cameras = self.camera_list.select(camera_name=new_camera_name)
            if existing_cameras:
                QMessageBox.warning(self, "중복된 카메라 이름", f"이미 [{new_camera_name}]이 존재합니다.")
                return  # 중복된 경우 저장하지 않고 함수 종료

        # 입력 값 cctv_list 테이블 저장
        self.camera_list.camera_location = self.combo_camera_location.currentText()
        self.camera_list.camera_name = new_camera_name
        self.camera_list.camera_ip = self.line_edit_ip.text()
        self.camera_list.port = int(self.line_edit_video_port.text()) if self.line_edit_video_port.text() else 0
        self.camera_list.ptz_port = int(self.line_edit_ptz_port.text()) if self.line_edit_ptz_port.text() else 0
        self.camera_list.rtsp_id = self.line_edit_rtsp_id.text()
        self.camera_list.rtsp_pw = self.line_edit_rtsp_password.text()
        self.camera_list.stream_path = self.line_edit_stream_path.text()  # 스트림 경로 추가

        # 입력 값 cctv_setting 테이블 저장
        self.camera_setting.camera_name = new_camera_name
        self.camera_setting.camera_location = self.combo_camera_location.currentText()
        self.camera_setting.fps_limit=None
        self.camera_setting.unsafe_event = None
        
        # 프로토콜 값 설정
        if self.radio_tcp.isChecked():
            self.camera_list.protocol = str("TCP")
        elif self.radio_udp.isChecked():
            self.camera_list.protocol = str("UDP")
        else:
            self.camera_list.protocol = None

        if self.edit_mode:
            # 수정 모드일 경우 기존 DB의 skip_frame 값 유지
            self.update_camera()
        else:
            self.camera_list.insert()
            self.camera_setting.insert()  # 카메라 설정도 DB에 추가
            self.parent().load_cctv_list_to_table()
        QMessageBox.information(self, "카메라 데이터 변경", "변경된 설정 값은 프로그램 재실행 시 적용됩니다.")
        self.accept()

    def update_camera(self):        
        # DB 업데이트 (WHERE 조건)
        self.camera_list.update(camera_name=self.camera_name_original)
        
        # 내용 변경 시 카메라 설정 업데이트
        camera_setting=DbCctvSetting()
        camera_setting.camera_name = self.line_edit_cctv_name.text().upper()
        camera_setting.camera_location = self.combo_camera_location.currentText()
        print(f"카메라 설정 업데이트: {camera_setting.camera_name}, {camera_setting.camera_location}")
        camera_setting.update(camera_name=self.camera_name_original)
        
        self.parent().load_cctv_list_to_table()
        