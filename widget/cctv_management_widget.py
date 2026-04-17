import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.db_cctv_list as db_cctv_list
from db.db_cctv_setting import DbCctvSetting
from db.db_cctv_list import DbCctvList

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from collections import defaultdict
from natsort import natsorted

from ui.ui_cctv_management_widget import Ui_Widget
from dialog.cctv_register_management_dialog import CctvRegisterManagementDialog
class CctvManagementWidget(QDialog, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setup_ui()
    
    def setup_ui(self):
        self.table_widget_cctv_management.cellClicked.connect(self.on_table_cell_clicked)
        self.button_add_cctv.clicked.connect(self.on_button_add_cctv_clicked)
        self.button_delete_cctv.clicked.connect(self.on_button_delete_cctv_clicked)
        
        self.db_cctv_list = DbCctvList()
        self.load_cctv_list_to_table()


    @Slot()
    def load_cctv_list_to_table(self):
        """CCTV 목록을 테이블에 로드"""
        self.load_cctv_list_to_table()
    
    @Slot(str)
    def filtered_cctv_list(self, filter_text):
        """선택된 위치에 해당하는 CCTV만 필터링하여 표시"""
        if not filter_text:
            # 필터링 텍스트가 비어있는 경우 전체 CCTV 목록을 표시
            self.load_cctv_list_to_table()
            return
        cctv_list = db_cctv_list.get_cctv_list()
        
        # filter_text 리스트에 포함된 camera_location의 CCTV만 필터링
        filtered_cctvs = [cctv for cctv in cctv_list if cctv['camera_location'] in filter_text]
        
        if not filtered_cctvs:
            # 해당 위치들에 CCTV가 없는 경우
            self.table_widget_cctv_management.clearContents()
            print(f"선택된 위치 {filter_text}에 해당하는 CCTV 없음")
            return
        
        # 위치별로 CCTV 그룹화
        location_dict = defaultdict(list)
        for cctv in filtered_cctvs:
            location_dict[cctv['camera_location']].append(cctv)
        
        # 위치를 자연 정렬
        sorted_locations = natsorted(location_dict.keys())
        # 위치와 CCTV 리스트 쌍을 준비
        location_cctv_pairs = [(location, location_dict[location]) for location in sorted_locations]
        
        # 필터링된 CCTV 목록을 테이블에 표시
        count = self.setup_table_widget(location_cctv_pairs)
        print(f"'{filter_text}' 위치의 CCTV {count}개 표시 완료")
        
    def setup_table_widget(self, location_cctv_pairs):
        """공통 테이블 설정 및 데이터 추가 함수"""
        # 테이블 설정
        self.table_widget_cctv_management.setColumnCount(4)
        self.table_widget_cctv_management.setHorizontalHeaderLabels(["이름", "IP", "비디오 포트", "스트림 경로"])
        self.table_widget_cctv_management.verticalHeader().setVisible(False)

        # 전체 행 수 계산 (위치 헤더 + CCTV 데이터)
        total_rows = sum(len(cctvs) + 1 for _, cctvs in location_cctv_pairs)
        self.table_widget_cctv_management.setRowCount(total_rows)

        row = 0
        for location, cctvs in location_cctv_pairs:
            # 위치 헤더 행 추가
            location_item = QTableWidgetItem(location)
            location_item.setTextAlignment(Qt.AlignCenter)
            location_item.setBackground(QColor(255, 240, 190))
            location_item.setFont(QFont("Arial", 10, QFont.Bold))

            for col in range(4):
                if col == 0:
                    self.table_widget_cctv_management.setItem(row, col, location_item)
                else:
                    dummy_item = QTableWidgetItem("")
                    dummy_item.setBackground(QColor(255, 240, 190))
                    self.table_widget_cctv_management.setItem(row, col, dummy_item)
            row += 1

            # CCTV 데이터 행들 추가
            sorted_cctvs = natsorted(cctvs, key=lambda x: x['camera_name'])
            for cctv in sorted_cctvs:
                name_item = QTableWidgetItem(cctv['camera_name'])
                name_item.setTextAlignment(Qt.AlignCenter)

                ip_item = QTableWidgetItem(cctv["camera_ip"])
                ip_item.setTextAlignment(Qt.AlignCenter)

                port_item = QTableWidgetItem(str(cctv["port"]) if cctv["port"] else "")
                port_item.setTextAlignment(Qt.AlignCenter)

                stream_path_item = QTableWidgetItem(cctv["stream_path"] if cctv["stream_path"] else "")
                stream_path_item.setTextAlignment(Qt.AlignCenter)

                self.table_widget_cctv_management.setItem(row, 0, name_item)
                self.table_widget_cctv_management.setItem(row, 1, ip_item)
                self.table_widget_cctv_management.setItem(row, 2, port_item)
                self.table_widget_cctv_management.setItem(row, 3, stream_path_item)
                row += 1

        # 테이블 헤더 크기 조정
        header = self.table_widget_cctv_management.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        return sum(len(cctvs) for _, cctvs in location_cctv_pairs)
 
            
    def on_table_cell_clicked(self, row, column):
        item_name = self.table_widget_cctv_management.item(row, 0)
        item_ip = self.table_widget_cctv_management.item(row, 1)

        name = item_name.text() if item_name else ""
        ip = item_ip.text() if item_ip else ""

        if name and ip:
            print(f"CCTV 클릭됨 - 이름: {name}, IP: {ip}")
        elif name:
            print(f"[위치 행] {name} 클릭됨")
        camera=self.db_cctv_list.select(camera_name=name)
        if camera:
            self.open_cctv_setting_dialog(camera[0])
            
    def open_cctv_setting_dialog(self, camera_data):
        print(f"카메라 rtsp_id: {camera_data.rtsp_id}, rtsp_pw: {camera_data.rtsp_pw}")
        self.camera_setting_dialog = CctvRegisterManagementDialog(
            self,
            edit_mode=True,
            camera_location=camera_data.camera_location,
            camera_name=camera_data.camera_name,
            camera_ip=camera_data.camera_ip,
            port=str(camera_data.port) if camera_data.port else "",
            ptz_port=str(camera_data.ptz_port) if camera_data.ptz_port else "",
            protocol=camera_data.protocol,
            rtsp_id=camera_data.rtsp_id if camera_data.rtsp_id else "",
            rtsp_pw=camera_data.rtsp_pw if camera_data.rtsp_pw else "",
            stream_path=camera_data.stream_path if camera_data.stream_path else "",
        )
        self.camera_setting_dialog.exec()
        
    def on_button_add_cctv_clicked(self):
        self.cctv_register_dialog = CctvRegisterManagementDialog(self)
        self.cctv_register_dialog.show()
        
    def on_button_delete_cctv_clicked(self):
        row = self.table_widget_cctv_management.currentRow()
        if row < 0:
            QMessageBox.warning(self, "삭제 실패", "삭제할 행을 선택해주세요.")
            return

        name_item = self.table_widget_cctv_management.item(row, 0)
        ip_item = self.table_widget_cctv_management.item(row, 1)

        if not name_item or not ip_item:
            QMessageBox.warning(self, "삭제 실패", "유효한 CCTV 정보가 아닙니다.")
            return

        name = name_item.text()
        ip = ip_item.text()

        result = QMessageBox.question(self,"CCTV 삭제",f"'{name}' (IP: {ip})를 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            db_cctv_list.delete_cctv_by_name(name)
            
            db_cctv_setting=DbCctvSetting() 
            db_cctv_setting.delete(camera_name=name)  # CCTV 설정 삭제
            
            self.table_widget_cctv_management.removeRow(row)
            # self.refresh()
            QMessageBox.information(self, "카메라 데이터 변경", "변경된 설정 값은 프로그램 재실행 시 적용됩니다.")


    def load_cctv_list_to_table(self):
        cctv_list = db_cctv_list.get_cctv_list()

        # 위치별 CCTV 리스트 구성
        location_dict = defaultdict(list)
        for cctv in cctv_list:
            location_dict[cctv['camera_location']].append(cctv)

        # 위치를 자연 정렬
        sorted_locations = natsorted(location_dict.keys())
        # 위치와 CCTV 리스트 쌍을 준비
        location_cctv_pairs = [(location, location_dict[location]) for location in sorted_locations]

        # 테이블 설정 및 데이터 추가
        self.setup_table_widget(location_cctv_pairs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = CctvManagementWidget()
    dlg.exec()

