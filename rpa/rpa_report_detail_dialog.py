import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, QIODevice, QDateTime, QTimeZone, QSize
from PySide6.QtGui import *

from rpa.ui.ui_RpaReportDetailDialog import Ui_RpaReportDetailDialog
import rpa.rpa_helper as rpa_helper
from rpa.db.db_rpa_report import RpaReport

class RpaReportDetailDialog(QDialog, Ui_RpaReportDetailDialog):
    def __init__(self, parent=None):
        super(RpaReportDetailDialog, self).__init__(parent)
        self.setupUi(self)

        # 버튼 클릭 이벤트 연결
        # self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.btn_ok_clicked)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.btn_close_clicked)
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.btn_apply_clicked)

        
        self.pushButton_event_time_today.clicked.connect(self.pushButton_event_time_today_clicked)
        self.pushButton_report_time_today.clicked.connect(self.pushButton_report_time_today_clicked)
        self.pushButton_image_path_open.clicked.connect(self.pushButton_image_path_open_clicked)

        # 위험유형 필터 초기화
        rows = RpaReport().get_distinct_event_types()

        event_types = set()
        for row in rows:
            if row:  # row[0] = event_type
                types = [t.strip() for t in row.split(",") if t.strip()]
                event_types.update(types)

        event_types = sorted(event_types)  # 정렬
        self.event_type_checkboxes = [ QCheckBox(f"{text}") for text in event_types ]
        rpa_helper.populate_grid(self.gridLayout_event_type, self.event_type_checkboxes, columns=4)  # 그리드 레이아웃에 위젯 추가

        # 위험유형 커스텀 기능 숨김
        self.checkBox_event_type_custom.setVisible(False)  # 커스텀 체크박스 숨김
        self.lineEdit_event_type_custom.setVisible(False)  # 커스텀 입력 필드 숨김

        # 초기값 설정
        self.set(
            id=None, 
            event_time=QDateTime.currentDateTime(), 
            report_time=QDateTime.currentDateTime(), 
            title="새 보고서", 
            location="발생장소", 
            event_type="", 
            severity="danger_mid", 
            action="위험발생상황 조치내용", 
            image_path=""
        )

    def set(self, id=None, event_time=None, report_time=None, title=None, location=None, event_type=None, severity=None, action=None, image_path=None):
        self.id = id
        self.event_time = event_time
        self.report_time = report_time
        self.title = title
        self.location = location
        self.event_type = event_type
        self.severity = severity
        self.action = action
        self.image_path = image_path

        self.update_all_status()
        
    def update_all_status(self):
        self.lineEdit_id.setText(str(self.id))
        
        # event_time 문자열을 QDateTime으로 변환 (기존 QDateTime 객체인 경우 그대로 사용)
        if isinstance(self.event_time, str):
            dt_event = QDateTime.fromString(self.event_time, "yyyy-MM-dd HH:mm:ss")
            if not dt_event.isValid():
                dt_event = QDateTime.fromString(self.event_time, "yyyy-MM-ddTHH:mm:ss") # ISO format fallback
            self.dateTimeEdit_event_time.setDateTime(dt_event)
        elif self.event_time is not None:
            self.dateTimeEdit_event_time.setDateTime(self.event_time)

        # report_time 문자열을 QDateTime으로 변환
        if isinstance(self.report_time, str):
            dt_report = QDateTime.fromString(self.report_time, "yyyy-MM-dd HH:mm:ss")
            if not dt_report.isValid():
                dt_report = QDateTime.fromString(self.report_time, "yyyy-MM-ddTHH:mm:ss")
            self.dateTimeEdit_report_time.setDateTime(dt_report)
        elif self.report_time is not None:
            self.dateTimeEdit_report_time.setDateTime(self.report_time)

        self.lineEdit_title.setText(self.title if self.title else "")
        self.lineEdit_location.setText(self.location if self.location else "")
        self.plainTextEdit_action.setPlainText(self.action if self.action else "")
        self.lineEdit_image_path.setText(self.image_path if self.image_path else "")

        # 위험유형 체크박스 상태 설정 
        # 문자열을 리스트로 변환 (공백 제거) (예: "화재,지게차 접근,작업자 낙상")
        selected_types = [t.strip() for t in self.event_type.split(",")]
        # 체크박스를 순회하며 해당 텍스트가 리스트에 있으면 체크
        for checkbox in self.event_type_checkboxes:
            if checkbox.text() in selected_types:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)


        # 심각도 상태 설정
        if self.severity == "danger_highhigh":
            self.radioButton_severity_danger_highhigh.setChecked(True)
        elif self.severity == "danger_high":
            self.radioButton_severity_danger_high.setChecked(True)
        elif self.severity == "danger_mid":
            self.radioButton_severity_danger_mid.setChecked(True)
        elif self.severity == "danger_low":
            self.radioButton_severity_danger_low.setChecked(True)
        elif self.severity == "danger_lowlow":
            self.radioButton_severity_danger_lowlow.setChecked(True)
        elif self.severity == "good_highhigh":
            self.radioButton_severity_good_highhigh.setChecked(True)
        elif self.severity == "good_high":
            self.radioButton_severity_good_high.setChecked(True)
        elif self.severity == "good_mid":
            self.radioButton_severity_good_mid.setChecked(True)

        # 이미지 표시
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            print(self.label_image.size())
            self.label_image.setPixmap(pixmap.scaled(QSize(500, 400), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def btn_ok_clicked(self):
        print("RPA Report New Manual Dialog : btn_ok_clicked")
        self.close()

    def btn_close_clicked(self):
        print("RPA Report New Manual Dialog : btn_close_clicked")
        self.close()    

    def btn_apply_clicked(self):
        print("RPA Report New Manual Dialog : btn_apply_clicked")
        
        rr = RpaReport()
        rr.event_time = self.dateTimeEdit_event_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        rr.report_time = self.dateTimeEdit_report_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        rr.title = self.lineEdit_title.text()
        rr.location = self.lineEdit_location.text()
        rr.event_type = ",".join([cb.text() for cb in self.event_type_checkboxes if cb.isChecked()])
        rr.severity = self.radioButton_severity_danger_highhigh.isChecked() and "danger_highhigh" or \
                      self.radioButton_severity_danger_high.isChecked() and "danger_high" or \
                      self.radioButton_severity_danger_mid.isChecked() and "danger_mid" or \
                      self.radioButton_severity_danger_low.isChecked() and "danger_low" or \
                      self.radioButton_severity_danger_lowlow.isChecked() and "danger_lowlow" or \
                      self.radioButton_severity_good_highhigh.isChecked() and "good_highhigh" or \
                      self.radioButton_severity_good_high.isChecked() and "good_high" or \
                      self.radioButton_severity_good_mid.isChecked() and "good_mid" or None
        rr.action = self.plainTextEdit_action.toPlainText()
        rr.image_path = self.lineEdit_image_path.text()
        

        if getattr(self, 'id', None) is None or self.id <= 0:
            rr.insert()
            print("RPA Report INSERT")
        else:
            rr.update(id=self.id)
            print("RPA Report UPDATE")


    def pushButton_event_time_today_clicked(self):
        print("RPA Report New Manual Dialog : pushButton_event_time_today_clicked")
        current_time = QDateTime.currentDateTime()
        self.dateTimeEdit_event_time.setDateTime(current_time)

    def pushButton_report_time_today_clicked(self):
        print("RPA Report New Manual Dialog : pushButton_report_time_today_clicked")
        current_time = QDateTime.currentDateTime()
        self.dateTimeEdit_report_time.setDateTime(current_time)

    def pushButton_image_path_open_clicked(self):
        print("RPA Report New Manual Dialog : pushButton_image_path_open_clicked")
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.lineEdit_image_path.setText(selected_files[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaReportDetailDialog()
    window.label_dialog_title.setText("RPA Report 보고서 기능 테스트")
    window.set(id=-1, 
               event_time=QDateTime.currentDateTime(), 
               report_time=QDateTime.currentDateTime(), 
               title="Test Title", 
               location="Test Location", 
               event_type="Test Type", 
               severity="danger_high", 
               action="Test Action", 
               image_path="D:\\1_SKYSYS\\9999_workspace\\VSCode\\rist-cctv-master\\rpa\\image_sample\\welding001.jpg")
    window.show()
    sys.exit(app.exec())