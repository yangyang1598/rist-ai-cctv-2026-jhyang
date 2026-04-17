from PySide6.QtWidgets import QDialog, QMessageBox, QListWidgetItem, QButtonGroup
from PySide6.QtCore import Qt, Signal
from ui.ui_event_logic_add_dialog import Ui_Dialog
from db.db_logic_list import DbLogicList
from dialog.event_logic_setting_dialog import EventLogicSettingDialog


class EventLogicAddDialog(QDialog, Ui_Dialog):
    """
    이벤트 추가 다이얼로그 클래스
    ui_EventAdd.py를 기반으로 한 이벤트 추가 기능을 제공합니다.
    """
    event_added = Signal()  # Signal to notify when an event is added

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("이벤트 추가")
        
        self.logic_list_data_arr = []  # 이벤트 절차 목록 데이터 저장용 리스트
        
        self.line_edit_input_img_size.setText("640,640") # 입력 이미지 사이즈 기본값 설정
        self.button_add_event_data.setEnabled(False) # 검증 전 추가버튼 비활성화
        
        # 라디오 버튼 그룹 설정 - 위험도 설정과 지적확인 방향 설정을 별도 그룹으로 분리
        self.risk_level_group = QButtonGroup(self)
        self.risk_level_group.addButton(self.radio_danger_lowlow)
        self.risk_level_group.addButton(self.radio_danger_low)
        self.risk_level_group.addButton(self.radio_danger_mid)
        self.risk_level_group.addButton(self.radio_danger_high)
        self.risk_level_group.addButton(self.radio_danger_highhigh)
        
        self.direction_group = QButtonGroup(self)
        self.direction_group.addButton(self.radio_left)
        self.direction_group.addButton(self.radio_right)
        self.direction_group.addButton(self.radio_top_side)
        self.direction_group.addButton(self.radio_under_side)

        # 이벤트 추가 /삭제 /검증 버튼 시그널
        self.button_add_event_process.clicked.connect(self.open_logic_setting_dialog)# 이벤트 로직 추가 버튼
        self.button_del_event_process.clicked.connect(self.remove_selected_logic) 
        
        self.button_add_event_data.clicked.connect(self.add_event_data) 
        
        self.button_val.clicked.connect(self.validate_event_data)  
        # Up/Down 버튼 시그널 연결
        self.button_event_up.clicked.connect(self.move_item_up)
        self.button_event_down.clicked.connect(self.move_item_down)

    def open_logic_setting_dialog(self):
        """
        이벤트 로직 설정 다이얼로그를 엽니다.
        """
        # 모달 대화상자로 열기
        dialog = EventLogicSettingDialog(self)
        dialog.signal_error_Qmessagebox.connect(self.show_model_combo_error)  # 오류 발생 시그널 연결
        # 로직 선택 시그널 연결
        dialog.signal_logic_selected.connect(self.add_logic_to_list)
        dialog.exec()
        
    def show_model_combo_error(self,title, error_message):
        # 트라이톤 모델 로드 오류 경고창
        QMessageBox.warning(self, title, error_message)
        
    def add_logic_to_list(self, logic_info):
        # 선택한 AI 또는 로직을 이벤트 절차 목록에 추가
        self.logic_list_data_arr.append(logic_info)
        print("logic_info:", logic_info)
        if logic_info["type"] == "AI":
            display_text = f"AI 모델-{logic_info['name']} ({logic_info['object']})"
        else:
            display_text = f"로직-{logic_info['name']}"
        # QListWidget에 항목 추가
        item = QListWidgetItem(display_text)
        # item.setFlags(item.flags() | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
        self.listwidget_logic_list.addItem(item)
        
        # 로직이 변경되었으므로 추가 버튼 비활성화
        self.button_add_event_data.setEnabled(False)

    """이벤트 로직 추가/삭제/검증 버튼 시그널 연결"""
    def add_event_data(self):
        #이벤트 절차 목록 내 데이터 추가
        event_name = self.line_edit_event_name.text().strip()
        skip_frame = self.spinbox_skip_frame.value()
        input_img_size = self.line_edit_input_img_size.text().strip()
        risk_level_status = 0 if self.radio_danger_lowlow.isChecked() else 1 if self.radio_danger_low.isChecked() else 2 if self.radio_danger_mid.isChecked() else 3 if self.radio_danger_high.isChecked() else 4 if self.radio_danger_highhigh.isChecked else 8
        jiguk_direction = 1 if self.radio_left.isChecked() else 2 if self.radio_right.isChecked() else 3 if self.radio_top_side.isChecked() else 4 if self.radio_under_side.isChecked() else 0

        # if self.radio_warning.isChecked():
        #     risk_level_status = "warning"
        # else:
        #     risk_level_status = "caution"
        
        try:
            if not skip_frame:
                skip_frame = 0 # 최소값 0로 설정
            else:
                skip_frame = int(skip_frame)
        except ValueError:
            QMessageBox.warning(self, "검증 오류", "Skip Frame은 정수여야 합니다.")
            return False
            
        # 이미지 크기 형식 검증 (예: "640,640")
        try:
            width, height = input_img_size.split(",")
            width = int(width.strip())
            height = int(height.strip())
            if width <= 0 or height <= 0:
                QMessageBox.warning(self, "검증 오류", "이미지 크기는 양수여야 합니다.")
                return False
        except (ValueError, TypeError):
            QMessageBox.warning(self, "검증 오류", "이미지 크기는 'width,height' 형식이어야 합니다.")
            return False
        
        # 입력값 검증
        if not event_name:
            QMessageBox.warning(self, "입력 오류", "이벤트 이름을 입력해주세요.")
            return
            
        # 로직이 선택되었는지 확인
        if not self.logic_list_data_arr:
            QMessageBox.warning(self, "입력 오류", "최소한 하나의 이벤트 로직을 추가해주세요.")
            return
            
        # 여기에 데이터베이스 저장 로직 추가
        self.logic_DB = DbLogicList()
        self.logic_DB.logic_name = event_name
        self.logic_DB.skip_frame = skip_frame
        self.logic_DB.input_img_size = input_img_size
        self.logic_DB.logicListData = self.logic_list_data_arr
        self.logic_DB.risk_level = risk_level_status # 위험 수준 기본값 설정, 필요시 수정 가능
        self.logic_DB.jiguk_direction = jiguk_direction
        self.logic_DB.insert()
        # Emit the signal after successfully adding the event
        self.event_added.emit()
        # 데이터베이스에 저장
        QMessageBox.information(self, "이벤트 추가", "이벤트가 추가되었습니다.")
        self.close()

    def remove_selected_logic(self):
        # 이벤트 절차 목록 내 데이터 삭제
        selected_items = self.listwidget_logic_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "삭제 오류", "삭제할 로직을 선택해주세요.")
            return
        
        # 선택된 항목 삭제
        for item in selected_items:
            row = self.listwidget_logic_list.row(item)
            self.listwidget_logic_list.takeItem(row)
            if 0 <= row < len(self.logic_list_data_arr):
                self.logic_list_data_arr.pop(row)
        
        # 로직이 변경되었으므로 추가 버튼 비활성화
        self.button_add_event_data.setEnabled(False)
        
    def validate_event_data(self):
        # 이벤트 절차 목록 순서 적합성 검증

        # 첫 번째는 반드시 AI 모델이어야 함
        if not self.logic_list_data_arr or self.logic_list_data_arr[0]["model"] is None:
            QMessageBox.warning(self, "검증 오류", "로직 실행 전에 입력 AI 모델이 필요합니다.")
            return False
        result=self.val_event(self.logic_list_data_arr)

        if result:
            QMessageBox.warning(self, "검증 결과", " 로직이 성공적으로 처리되었습니다.")
            self.button_add_event_data.setEnabled(True)
        else:
            # 검증이 실패하면 버튼 비활성화 유지
            self.button_add_event_data.setEnabled(False)
 
        return True
    
    def val_event(self, logic_list_data_arr):
        """알고리즘 추가 시 해당 else문 내 내용 추가"""
        detections_arr = []  # 감지된 객체 정보 저장
        try:
            # 1. AI 모델만 있는지 확인
            ai_only = True
            for logic in logic_list_data_arr:
                if "model" not in logic:
                    ai_only = False
                    break
            # 2. AI 모델만 있는 경우 - 모두 성공적으로 탐지되면 True 반환
            if ai_only:
                # 모든 객체 탐지 성공
                return True
            
            # 3. AI와 로직이 혼합된 경우
            else:
                for idx, logic_info in enumerate(logic_list_data_arr):
                    # AI 모델 처리
                    if "model" in logic_info:

                        detections_arr.append(True)  # AI 모델 탐지 성공
                    # 로직 처리
                    else:
                        # 거리 알고리즘 처리 - 입력 AI가 2개여야 함
                        if logic_info.get("name") == "거리":
                            if len(detections_arr) != 2:
                                QMessageBox.warning(self, "검증 오류", f"거리 알고리즘은 입력 AI가 2개 필요합니다. (현재: {len(detections_arr)}개)")
                                return False
                            else:
                                detections_arr.clear()  
                                pass
                        if logic_info.get("name") == "크기":
                            if len(detections_arr) != 1:
                                QMessageBox.warning(self, "검증 오류", f"크기 알고리즘은 입력 AI가 1개 필요합니다. (현재: {len(detections_arr)}개)")
                                return False
                            else:
                                detections_arr.clear()  
                                pass
                        if logic_info.get("name") == "화재 감지":
                            if len(detections_arr) != 1:
                                QMessageBox.warning(self, "검증 오류", f"화재 감지 알고리즘은 입력 AI가 1개 필요합니다. (현재: {len(detections_arr)}개)")
                                return False
                            else:
                                detections_arr.clear()  
                                pass
                
                # 모든 처리가 성공적으로 완료됨
                return True
        
        except Exception as e:
            print(f"로직 처리 중 오류 발생: {str(e)}")
            QMessageBox.warning(self, "오류 발생", f"로직 처리 중 오류가 발생했습니다: {str(e)}")
            return False
        
    """로직 목록에서 선택된 항목을 위/아래로 이동"""
    def move_item_up(self):
        
        current_row = self.listwidget_logic_list.currentRow()
        if current_row > 0:  # 첫 번째 아이템이 아닌 경우
            current_item = self.listwidget_logic_list.takeItem(current_row)
            self.listwidget_logic_list.insertItem(current_row - 1, current_item)
            self.listwidget_logic_list.setCurrentRow(current_row - 1)
            self.sync_listwidget_logic_list_data_widget()

    def move_item_down(self):
        
        current_row = self.listwidget_logic_list.currentRow()
        if current_row < self.listwidget_logic_list.count() - 1:  # 마지막 아이템이 아닌 경우
            current_item = self.listwidget_logic_list.takeItem(current_row)
            self.listwidget_logic_list.insertItem(current_row + 1, current_item)
            self.listwidget_logic_list.setCurrentRow(current_row + 1)
            self.sync_listwidget_logic_list_data_widget()

    def sync_listwidget_logic_list_data_widget(self):
        #QListWidget의 순서에 맞게 logic_list_data_arr를 동기화
        new_data = []
        for i in range(self.listwidget_logic_list.count()):
            text = self.listwidget_logic_list.item(i).text()
            # display_text가 일치하는 logic_info를 찾아서 추가
            for logic in self.logic_list_data_arr:
                if logic.get("type") == "AI":
                    if logic["name"] in text and logic["object"] in text:
                        print("logic:", logic)
                        new_data.append(logic)
                        break
                else:
                    if logic["name"] in text:
                        print("logic:", logic)
                        new_data.append(logic)
                        break
        self.logic_list_data_arr = new_data
        
        # 로직 순서가 변경되었으므로 추가 버튼 비활성화
        self.button_add_event_data.setEnabled(False)

    """기존에 저장된 이벤트 절차 목록 수정"""
    def edit_to_list(self, logic_list_data_arr):
        for logic_info in logic_list_data_arr:
            if logic_info["type"] == "AI":
                display_text = f"AI 모델-{logic_info['name']} ({logic_info['object']})"
            else:
                display_text = f"로직-{logic_info['name']}"
            item = QListWidgetItem(display_text)
            item.setFlags(item.flags() | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
            self.listwidget_logic_list.addItem(item)
        self.logic_list_data_arr = logic_list_data_arr
        self.button_add_event_data.setEnabled(False)

    