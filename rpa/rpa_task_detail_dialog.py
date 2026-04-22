import sys, os
sys.path.append(os.path.abspath(os.curdir))

from rpa.db.db_rpa_report import RpaReport

from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, QIODevice, QDateTime, QTimeZone, QSize, QTime, Signal
from PySide6.QtGui import *
from datetime import datetime

from rpa.ui.ui_RpaTaskDetailDialog import Ui_RpaTaskDetailDialog
from rpa import rpa_helper as helper
from rpa.db.db_rpa_task import RpaTask

class RpaTaskDetailDialog (QDialog, Ui_RpaTaskDetailDialog):

    task_delete_signal = Signal(int, str)  # RPA 업무 삭제 시그널
    task_update_signal = Signal(int, str)  # RPA 업무 업데이트 시그널
    task_insert_signal = Signal(str)  # RPA 업무 추가 시그널

    def __init__(self, parent=None):
        super(RpaTaskDetailDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_report_search.clicked.connect(self.pushButton_report_search_clicked)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)  # 삭제 버튼은 닫기와 동일하게 설정
        self.pushButton_insert.clicked.connect(self.pushButton_insert_task_clicked)
        self.pushButton_close.clicked.connect(self.pushButton_close_clicked)
        self.pushButton_accept.clicked.connect(self.pushButton_accept_clicked)

        self.radioButton_report_duration_days_30.toggled.connect(self.radioButton_report_duration_days_toggled)
        self.radioButton_report_duration_days_7.toggled.connect(self.radioButton_report_duration_days_toggled)
        self.radioButton_report_duration_days.toggled.connect(self.radioButton_report_duration_days_toggled)
        self.lineEdit_report_duration_days.textChanged.connect(self.radioButton_report_duration_days_toggled)

        # QLineEdit Validator 설정
        self.lineEdit_report_duration_days
        validator = QIntValidator(1, 500, self)
        self.lineEdit_report_duration_days.setValidator(validator)

        self.week_days_chb = [
            ("monday", self.checkBox_mon),
            ("tuesday", self.checkBox_tue),
            ("wednesday", self.checkBox_wed),
            ("thursday", self.checkBox_thu),
            ("friday", self.checkBox_fri),
            ("saturday", self.checkBox_sat),
            ("sunday", self.checkBox_sun)
        ]

        self.report_severity_chb = [
                ("danger_highhigh", self.checkBox_report_severity_danger_highhigh),
                ("danger_high",     self.checkBox_report_severity_danger_high),
                ("danger_mid",      self.checkBox_report_severity_danger_mid),
                ("danger_low",      self.checkBox_report_severity_danger_low),
                ("danger_lowlow",   self.checkBox_report_severity_danger_lowlow),
                ("good_highhigh",   self.checkBox_report_severity_good_highhigh),
                ("good_high",       self.checkBox_report_severity_good_high),
                ("good_mid",        self.checkBox_report_severity_good_mid),
        ]

        # 검색기간 필터 초기화
        self.dateTimeEdit_from.setDateTime(QDateTime.currentDateTime().addDays(-30))
        self.dateTimeEdit_to.setDateTime(QDateTime.currentDateTime()) 

        # 위험유형 필터 초기화
        # 한개의 이벤트에 복수개의 위험유형이 있을 수 있기에 복수개의 이벤트를 개별이벤트 체크박스로 할당
        # ex> "화재", "화재,추락" -> ["화재", "추락"]
        event_types = RpaReport().get_distinct_event_types()
        event_type_list = set()
        for event in event_types:
            if event:  # row[0] = event_type
                types = [t.strip() for t in event.split(",") if t.strip()]
                event_type_list.update(types)

        event_type_list = sorted(event_type_list)  # 정렬
        self.report_eventtype_checkboxes = [ QCheckBox(f"{text}") for text in event_type_list ]
        helper.populate_grid(self.gridLayout_event_type, self.report_eventtype_checkboxes, columns=4)  # 그리드 레이아웃에 위젯 추가      

        # 보고서 리스트 초기화
        self.tableWidget_report.setRowCount(0)      # Table 초기화

        # 이메일 주소록 항목 숨김
        self.pushButton_email_addressbook.setVisible(False)

        # 이메일 제목 항목 숨김
        # self.label_email_title.setVisible(False)
        # self.lineEdit_email_title.setVisible(False)
        self.pushButton_email_title_default.setVisible(False)

        # 이메일 내용 항목 숨김
        self.label_email_body.setVisible(False)
        self.plainTextEdit_email_body.setVisible(False)
        self.pushButton_email_body_default.setVisible(False)

        # 이메일 첨부파일 항목 숨김
        self.label_9.setVisible(False) 
        self.listWidget_email_attach.setVisible(False)
        self.pushButton_email_attach.setVisible(False)


    def get_selected_days(self):
        selected = []
        for eng_day, checkbox in self.week_days_chb:
            if checkbox.isChecked():
                selected.append(eng_day)

        result = ",".join(selected)
        print(f"get_selected_days() : {result}")  # 결과 출력 (예: Mon,Wed,Fri)
        return result  # 결과 출력 (예: Mon,Wed,Fri)
    
    def get_severity(self):
        
        selected = []
        for severity, checkBox in self.report_severity_chb:
            if checkBox.isChecked():
                selected.append(severity)
                
        result = ",".join(selected)
        print(f"get_severity() : {result}")
        
        return result
                

    def get_report_duration_days(self):
        
        if self.radioButton_report_duration_days_30.isChecked():
            return 30
        elif self.radioButton_report_duration_days_7.isChecked():
            return 7
        elif self.radioButton_report_duration_days.isChecked():
            return int(self.lineEdit_report_duration_days.text()) if self.lineEdit_report_duration_days.text() else 0

    def pushButton_insert_task_clicked(self):
        # 데이터베이스에 저장하는 로직 추가
        task = RpaTask()
        task.task_name = self.lineEdit_task_name.text()
        task.repeat_day_of_week = self.get_selected_days()
        task.repeat_time = self.timeEdit_sendtime.time().toString("HH:mm")
        task.report_duration_days = self.get_report_duration_days()
        task.report_severity = self.get_severity()
        task.report_severity = ",".join([severity for severity, cb in self.report_severity_chb if cb.isChecked()])
        task.report_event_type = ",".join([cb.text() for cb in self.report_eventtype_checkboxes if cb.isChecked()])

        task.email_subject = self.lineEdit_email_title.text()
        task.email_receiver = self.lineEdit_email_to.text()
        task.email_body = self.plainTextEdit_email_body.toPlainText()

        task.insert()

        self.task_insert_signal.emit(task.task_name)  # 시그널 발생

    def pushButton_close_clicked(self):
        print("RPA Task Detail Dialog : pushButton_close_clicked")
        self.close()

    def pushButton_accept_clicked(self):
        print("RPA Task Detail Dialog : pushButton_accept_clicked")
        if self.id is None or self.id < 0:
            print("RPA Task Detail Dialog : id is None")
            return
        
        task = RpaTask()
        task.id = self.id
        task.task_name = self.lineEdit_task_name.text()
        task.repeat_day_of_week = self.get_selected_days()
        task.repeat_time = self.timeEdit_sendtime.time().toString("HH:mm")
        task.report_duration_days = self.get_report_duration_days()
        task.report_severity = self.get_severity()
        task.report_event_type = ",".join([cb.text() for cb in self.report_eventtype_checkboxes if cb.isChecked()])
        task.email_subject = self.lineEdit_email_title.text()
        task.email_receiver = self.lineEdit_email_to.text()
        task.email_body = self.plainTextEdit_email_body.toPlainText()
        task.update(id = task.id)

        self.task_update_signal.emit(task.id, task.task_name)  # 시그널 발생


    def radioButton_report_duration_days_toggled(self):
        self.dateTimeEdit_from.setDateTime( self.dateTimeEdit_to.dateTime().addDays(-self.get_report_duration_days()) )
            

    def pushButton_report_search_clicked(self):
        print("RPA Task Detail Dialog : pushButton_report_search_clicked")
    
        # DB 쿼리 실행
        reports = RpaReport().select(event_date_from    = self.dateTimeEdit_from.dateTime().toString("yyyy-MM-dd HH:mm:ss"), 
                                     event_date_to      = self.dateTimeEdit_to.dateTime().toString("yyyy-MM-dd HH:mm:ss"), 
                                     severity           = [severity for severity, cb in self.report_severity_chb if cb.isChecked()], 
                                     event_type         = [cb.text() for cb in self.report_eventtype_checkboxes if cb.isChecked()])

        # 실행결과 시각화
        self.tableWidget_report.setIconSize(QSize(120, 120))  # 아이콘 크기 설정        
        self.tableWidget_report.setRowCount(len(reports))

        for row_idx, report in enumerate(reports):
            # 각 열에 맞게 값 설정
            report_event_time = datetime.fromisoformat(str(report.event_time))
            report_report_time = datetime.fromisoformat(str(report.report_time))
            self.tableWidget_report.setItem(row_idx, 0, QTableWidgetItem(str(report.id)))
            self.tableWidget_report.setItem(row_idx, 1, QTableWidgetItem(report_event_time.strftime("%Y-%m-%d %H:%M:%S") if report_event_time else ""))
            self.tableWidget_report.setItem(row_idx, 2, QTableWidgetItem(report_report_time.strftime("%Y-%m-%d %H:%M:%S") if report_report_time else ""))
            self.tableWidget_report.setItem(row_idx, 3, QTableWidgetItem(report.title))
            self.tableWidget_report.setItem(row_idx, 4, QTableWidgetItem(report.location))
            self.tableWidget_report.setItem(row_idx, 5, QTableWidgetItem(report.event_type))
            self.tableWidget_report.setItem(row_idx, 6, QTableWidgetItem( helper.severity_to_label( report.severity) ))
            self.tableWidget_report.setItem(row_idx, 7, QTableWidgetItem(report.action))

            # 이미지 경로 설정 및 썸네일 아이콘 설정
            if report.image_path and os.path.exists(report.image_path):
                thumbnail = QPixmap(report.image_path)
                if not thumbnail.isNull():
                    self.tableWidget_report.setRowHeight(row_idx, 120)
                    icon = QIcon(thumbnail.scaled(120, 120, Qt.KeepAspectRatio))
                    item = QTableWidgetItem()
                    item.setIcon(icon)
                    item.setText(report.image_path)
                    self.tableWidget_report.setItem(row_idx, 8, item)
                else:
                    self.tableWidget_report.setItem(row_idx, 8, QTableWidgetItem("이미지 없음"))
            else:
                self.tableWidget_report.setItem(row_idx, 8, QTableWidgetItem("이미지 없음"))

        # self.log("[DB] 최근 이벤트 테이블 갱신 완료")

    def pushButton_delete_clicked(self):
        print("RPA Task Detail Dialog : pushButton_delete_task_clicked")
        
        if self.id is None or self.id < 0:
            print("RPA Task Detail Dialog : id is None")
            return
        
        # RpaTask 객체 생성 후 삭제
        task = RpaTask()
        task.delete(id=self.id)

        self.task_delete_signal.emit(self.id, self.lineEdit_task_name.text())  # 시그널 발생
        
        self.close()

    def set(self, id=None, task_name="", repeat_day_of_week="", repeat_time="",
            report_duration_days=0, report_severity="", report_event_type="",
            email_subject="", email_receiver="", email_body=""):
        
        self.id = id  # RPA 업무 ID
        self.task_name = task_name
        self.repeat_day_of_week = repeat_day_of_week
        self.repeat_time = repeat_time
        self.report_duration_days = report_duration_days
        self.report_severity_str = report_severity
        self.report_event_type = report_event_type
        self.email_subject = email_subject
        self.email_receiver = email_receiver
        self.email_body = email_body

        self.update_all_status()
        
    def update_all_status(self):
        """
        RPA 업무 상세 정보를 업데이트합니다.
        """
        self.lineEdit_id.setText(str(self.id) if self.id else "")
        self.lineEdit_task_name.setText(self.task_name if self.task_name else "")
        self.timeEdit_sendtime.setTime(QTime.fromString(self.repeat_time, "HH:mm"))
        self.lineEdit_report_duration_days.setText(str(self.report_duration_days))
        self.radioButton_report_duration_days.setChecked(True)
        
        # 반복 요일 설정
        for eng_day, checkbox in self.week_days_chb:
            checkbox.setChecked(eng_day in self.repeat_day_of_week.split(","))
        
        # 보고서 심각도 설정
        for severity, checkBox in self.report_severity_chb:
            checkBox.setChecked(severity in self.report_severity_str.split(","))
        
        # 보고서 이벤트 유형 설정
        for cb in self.report_eventtype_checkboxes:
            cb.setChecked(cb.text() in self.report_event_type.split(","))
        
        self.lineEdit_email_title.setText(self.email_subject)
        self.lineEdit_email_to.setText(self.email_receiver)
        self.plainTextEdit_email_body.setPlainText(self.email_body)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaTaskDetailDialog()
    window.label_dialog_title.setText("RPA 업무 기능 테스트")
    window.set(id=-1,
               task_name="Test Task",
               repeat_day_of_week="monday,tuesday,friday",
               repeat_time="12:00",
               report_duration_days=30,
               report_severity="danger_high,danger_mid",
               report_event_type="나_위험유형",
               email_subject="Test Email Subject",
               email_receiver="srlee@skysys.co.kr",
               email_body="This is a test email body.")
    
    window.show()
    sys.exit(app.exec())