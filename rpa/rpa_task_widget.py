import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import*  # QFileDialog 추가
from PySide6.QtCore import *
from PySide6.QtGui import QCloseEvent

from rpa.ui.ui_RpaTaskWidget import Ui_RpaTaskWidget
from rpa.rpa_task_detail_dialog import RpaTaskDetailDialog
from rpa.db.db_rpa_task import RpaTask
# from rpa.mail.email_scheduler import EmailScheduler
from rpa import rpa_helper as helper

class RpaTaskWidget(QWidget, Ui_RpaTaskWidget):
    
    scheduler_restart_signal = Signal()  # 스케줄러 재시작 시그널 정의
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("RPA 업무관리")
        
        self.pushButton_task_new.clicked.connect(self.pushButton_task_new_clicked)
        self.pushButton_search.clicked.connect(self.pushButton_search_clicked)
        self.pushButton_task_scheduler_restart.clicked.connect(self.pushButton_task_scheduler_restart_clicked)  # 스케줄러 재시작 버튼 클릭 이벤트 연결

        self.tableWidget_task.setRowCount(0)  # 테이블 초기화
        self.tableWidget_task.cellDoubleClicked.connect(self.tableWidget_task_cell_double_clicked)

        self.pushButton_search_clicked()


    def get_email_config(self):
        """이메일 발송 설정을 반환하는 콜백 함수"""
        config = {
            'task_name': self.lineEdit_task_name.text(),
            'repeat_day_of_week': self.get_selected_days(),
            'repeat_time': self.timeEdit_sendtime.time().toString("HH:mm"),
            'report_duration_days': self.get_report_duration_days(),
            'report_severity': ",".join([severity for severity, cb in self.report_severity if cb.isChecked()]),
            'report_event_type': ",".join([cb.text() for cb in self.report_eventtype_checkboxes if cb.isChecked()]),
            'email_subject': self.lineEdit_email_title.text(),
            'email_receiver': self.lineEdit_email_to.text(),
            'email_body': self.plainTextEdit_email_body.toPlainText()
        }
        return config

    def tableWidget_task_cell_double_clicked(self, row: int, column: int):  # 테이블 셀 더블 클릭 이벤트 연결
        print("RPA Task Widget : tableWidget_task_cell_double_clicked")
        row_data = []
        for col in range(self.tableWidget_task.columnCount()):
            item = self.tableWidget_task.item(row, col)
            row_data.append(item.text() if item else "")

        dialog = RpaTaskDetailDialog(self)
        dialog.label_dialog_title.setText("RPA 업무 확인")

        # RPA업무 변경 되었다면 화면갱신될 수 있게 검색 버튼 클릭
        dialog.task_delete_signal.connect(self.pushButton_search_clicked)
        dialog.task_update_signal.connect(self.pushButton_search_clicked)
        dialog.task_insert_signal.connect(self.pushButton_search_clicked)

        rt = RpaTask().select(id=row_data[0])  # 클릭된 행의 ID로 DB에서 데이터 조회
        if len(rt) > 0:
            print(rt[0].task_name)
            dialog.set(id=rt[0].id,
                       task_name=rt[0].task_name, 
                       repeat_day_of_week=rt[0].repeat_day_of_week, 
                       repeat_time=rt[0].repeat_time, 
                       report_duration_days=rt[0].report_duration_days, 
                       report_severity=rt[0].report_severity, 
                       report_event_type=rt[0].report_event_type, 
                       email_receiver=rt[0].email_receiver, 
                       email_subject=rt[0].email_subject, 
                       email_body=rt[0].email_body)
        
        dialog.show()

    def pushButton_search_clicked(self):  # 검색 버튼 클릭 이벤트 연결
        print("RPA Task Widget : pushButton_search_clicked")
        
        # DB 쿼리 실행
        tasks:list[RpaTask] = RpaTask().select()

        # 실행결과 시각화
        self.tableWidget_task.setIconSize(QSize(120, 120))  # 아이콘 크기 설정        
        self.tableWidget_task.setRowCount(len(tasks))

        for row_idx, task in enumerate(tasks):
            # print(task.id, task.task_name, task.repeat_day_of_week, task.repeat_time,
            #       task.report_duration_hours, task.report_duration_days,    
            #       task.report_severity, task.report_event_type, task.email_receiver,
            #       task.email_subject, task.email_body)


            # 각 열에 맞게 값 설정
            self.tableWidget_task.setItem(row_idx, 0, QTableWidgetItem( str(task.id)) )
            self.tableWidget_task.setItem(row_idx, 1, QTableWidgetItem(task.task_name))
            self.tableWidget_task.setItem(row_idx, 2, QTableWidgetItem( helper.convert_weekdays_to_korean(task.repeat_day_of_week) ))
            self.tableWidget_task.setItem(row_idx, 3, QTableWidgetItem(task.repeat_time))
            self.tableWidget_task.setItem(row_idx, 4, QTableWidgetItem( str(task.report_duration_days) ))
            self.tableWidget_task.setItem(row_idx, 5, QTableWidgetItem( helper.convert_severities_to_korean( task.report_severity) ))
            self.tableWidget_task.setItem(row_idx, 6, QTableWidgetItem(task.report_event_type))
            self.tableWidget_task.setItem(row_idx, 7, QTableWidgetItem(task.email_receiver))
            self.tableWidget_task.setItem(row_idx, 8, QTableWidgetItem(task.email_subject))
            # self.tableWidget_task.setItem(row_idx, 9, QTableWidgetItem(task.email_body))


    def pushButton_task_new_clicked(self):  # 수동 보고서 작성 클릭 이벤트 연결 (추가)
        print("RPA Task Widget : pushButton_task_new_clicked")

        dialog = RpaTaskDetailDialog(self)  # 부모 위젯을 전달하여 모달 대화상자 생성
        dialog.label_dialog_title.setText("새 RPA 업무 등록")

        #  RPA 새 업무 추가 창에서는 업무추가버튼만 사용하도록 설정
        dialog.pushButton_delete.setEnabled(False)
        dialog.pushButton_accept.setEnabled(False)
        dialog.show()


    def pushButton_task_scheduler_restart_clicked(self): 
        print("RPA Task Widget : pushButton_task_scheduler_clicked")

        # 스케줄러 재시작
        self.scheduler_restart_signal.emit()  
            

    def closeEvent(self, event: QCloseEvent) -> None:
        print("RPA Task Widget : closeEvent")
        # self.parent().show()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaTaskWidget()
    window.show()
    sys.exit(app.exec())