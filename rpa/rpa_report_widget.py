import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import *  # QFileDialog 추가
from PySide6.QtCore import *
from PySide6.QtGui import QCloseEvent, QPixmap, QIcon

from rpa.ui.ui_RpaReportWidget import Ui_RpaReportWidget
from rpa.rpa_report_detail_dialog import RpaReportDetailDialog
from rpa.db.db_rpa_report import RpaReport

import rpa.rpa_helper as rpa_helper

class RpaReportWidget(QWidget, Ui_RpaReportWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # RpaReport().init()  # DB 테이블 생성

        self.tableWidget_report.setRowCount(0)      # Table 초기화
        self.tableWidget_report.cellDoubleClicked.connect(self.tableWidget_report_cell_double_clicked)  # 셀 더블 클릭 이벤트 연결

        # 버튼 클릭 이벤트 연결
        self.pushButton_report_new_manual.clicked.connect(self.pushButton_report_new_manual_clicked)
        self.pushButton_report_new_dummy.clicked.connect(self.pushButton_report_new_dummy_clicked)  # 더미 버튼 클릭 이벤트 연결 (추가)
        self.pushButton_search.clicked.connect(self.pushButton_search_clicked)
        self.pushButton_period_today.clicked.connect(self.pushButton_period_today_clicked)

        # 검색기간 필터 초기화
        self.dateTimeEdit_from.setDateTime(QDateTime.currentDateTime().addMonths(-1))
        self.dateTimeEdit_to.setDateTime(QDateTime.currentDateTime()) 


        # 위험유형 필터 초기화
        event_types = RpaReport().get_distinct_event_types()
        event_type_list = set()
        for event in event_types:
            if event:  # row[0] = event_type
                types = [t.strip() for t in event.split(",") if t.strip()]
                event_type_list.update(types)

        event_type_list = sorted(event_type_list)  # 정렬
        self.event_type_checkboxes = [ QCheckBox(f"{text}") for text in event_type_list ]
        rpa_helper.populate_grid(self.gridLayout_event_type, self.event_type_checkboxes, columns=4)  # 그리드 레이아웃에 위젯 추가

        # 숨김처리
        self.pushButton_report_new_dummy.setVisible(False)

    def tableWidget_report_cell_double_clicked(self, row: int, column: int):  # 테이블 셀 더블 클릭 이벤트 연결
        print("RPA Report Widget : tableWidget_report_cell_double_clicked")

        row_data = []
        for col in range(self.tableWidget_report.columnCount()):
            item = self.tableWidget_report.item(row, col)
            row_data.append(item.text() if item else "")

        # print(f"클릭된 행: {row}")
        # print(f"데이터: {row_data}")
    
        dialog = RpaReportDetailDialog(self)  
        dialog.label_dialog_title.setText("보고서 확인")  # 대화상자 제목 설정
        rr = RpaReport().select(id=row_data[0])  # 클릭된 행의 ID로 DB에서 데이터 조회
        if( len(rr) > 0):
            print(rr[0].title)
            dialog.set(id=rr[0].id,
                       event_time=rr[0].event_time, 
                       report_time=rr[0].report_time, 
                       title=rr[0].title, 
                       location=rr[0].location, 
                       event_type=rr[0].event_type, 
                       severity=rr[0].severity, 
                       action=rr[0].action, 
                       image_path=rr[0].image_path)
        dialog.show() 



    def pushButton_report_new_manual_clicked(self):  # 수동 보고서 작성 클릭 이벤트 연결 (추가)
        print("RPA Report Widget : btn_report_new_manual_clicked")

        dialog = RpaReportDetailDialog(self)  # 부모 위젯을 전달하여 모달 대화상자 생성
        dialog.show()  # 모달 대화상자를 사용하지 않는 경우



    def pushButton_report_new_dummy_clicked(self):  # 더미 버튼 클릭 이벤트 연결 (추가)
        print("RPA Report Widget : btn_report_new_dummy_clicked")

        dialog = RpaReportDetailDialog(self)  # 부모 위젯을 전달하여 모달 대화상자 생성
        dialog.show()  # 모달 대화상자를 사용하지 않는 경우


    def pushButton_search_clicked(self):  # 검색 버튼 클릭 이벤트 연결 (추가)
        # 검색 기간 조건 추출
        event_date_from = self.dateTimeEdit_from.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        event_date_to = self.dateTimeEdit_to.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        # 심각도 조건 추출
        severities = []
        if self.checkBox_severity_danger_highhigh.isChecked():
            severities.append( "danger_highhigh" )  # "매우 심각"
        if self.checkBox_severity_danger_high.isChecked():
            severities.append( "danger_high" )  # "심각"
        if self.checkBox_severity_danger_mid.isChecked():
            severities.append( "danger_mid" )
        if self.checkBox_severity_danger_low.isChecked():
            severities.append( "danger_low" )
        if self.checkBox_severity_danger_lowlow.isChecked():
            severities.append( "danger_lowlow" )
        if self.checkBox_severity_good_highhigh.isChecked():
            severities.append( "good_highhigh" )
        if self.checkBox_severity_good_high.isChecked():
            severities.append( "godd_high" )
        if self.checkBox_severity_good_mid.isChecked():
            severities.append( "goood_mid" )
        
        # 이벤트 유형 조건 추출
        selected_event_types = [cb.text() for cb in self.event_type_checkboxes if cb.isChecked()]

        # DB 쿼리 실행
        reports = RpaReport().select(event_date_from=event_date_from, 
                                     event_date_to=event_date_to, 
                                     severity=severities, 
                                     event_type=selected_event_types)

        # 실행결과 시각화
        self.tableWidget_report.setIconSize(QSize(120, 120))  # 아이콘 크기 설정        
        self.tableWidget_report.setRowCount(len(reports))

        for row_idx, report in enumerate(reports):
            # 각 열에 맞게 값 설정
            self.tableWidget_report.setItem(row_idx, 0, QTableWidgetItem(str(report.id)))
            self.tableWidget_report.setItem(row_idx, 1, QTableWidgetItem(report.event_time.strftime("%Y-%m-%d %H:%M:%S") if report.event_time else ""))
            self.tableWidget_report.setItem(row_idx, 2, QTableWidgetItem(report.report_time.strftime("%Y-%m-%d %H:%M:%S") if report.report_time else ""))
            self.tableWidget_report.setItem(row_idx, 3, QTableWidgetItem(report.title))
            self.tableWidget_report.setItem(row_idx, 4, QTableWidgetItem(report.location))
            self.tableWidget_report.setItem(row_idx, 5, QTableWidgetItem(report.event_type))
            self.tableWidget_report.setItem(row_idx, 6, QTableWidgetItem( rpa_helper.severity_to_label( report.severity) ))
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

    def pushButton_period_today_clicked(self):
        print("pushButton_period_today_clicked")
        self.dateTimeEdit_to.setDateTime( QDateTime().currentDateTime() )


    def closeEvent(self, event: QCloseEvent) -> None:
        print("RPA Report Widget : closeEvent")
        # self.parent().show()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpaReportWidget()
    window.show()
    sys.exit(app.exec())