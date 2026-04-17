from itertools import count
import sys, os
sys.path.append(os.path.abspath(os.curdir))

from PySide6.QtWidgets import QApplication, QMainWindow, QDialogButtonBox, QDialog, QMessageBox, QWidget, QLabel
from PySide6.QtCore import QFile, QIODevice, QDateTime, QTimeZone, QTimer
from PySide6.QtGui import QCloseEvent

import schedule
import time
import threading
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from rpa.ui.ui_RpaMainWindow import Ui_RpaMainWindow
from rpa.rpa_report_widget import RpaReportWidget
from rpa.rpa_home_widget import RpaHomeWidget
from rpa.rpa_task_widget import RpaTaskWidget
from rpa.rpa_setting_widget import RpaSettingWidget
from rpa.log_text_widget import LogTextWidget
# from rpa.mail.email_scheduler import EmailScheduler
from rpa.db.db_rpa_report import RpaReport
from rpa.db.db_rpa_task import RpaTask
# 이메일 설정 불러오기
from rpa.config import config
from rpa import rpa_helper as helper

__DEBUG__ = False

class RpaMainWindow(QMainWindow, Ui_RpaMainWindow):

    # 스택 위젯 인덱스 정의
    _report = 0
    _task = 1
    _setting = 2

    def __init__(self, parent=None):
        super(RpaMainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowTitle("RPA Main Dialog")
        # self.setGeometry(100, 100, 800, 600)

        self.rpaReportWidget = RpaReportWidget(self)
        self.rpaTaskWidget = RpaTaskWidget(self)
        self.rpaSettingWidget = RpaSettingWidget(self)

        self.logTextWidget = LogTextWidget()    # RAP 업무의 동작상태 표시하기위한 로그창

        self.rpaTaskWidget.scheduler_restart_signal.connect(self.pushButton_task_scheduler_restart_clicked)  # 스케줄러 재시작 시그널 연결

        for i in range(self.gridLayout_report.count()):
            self.gridLayout_report.itemAt(i).widget().deleteLater()

        for i in range(self.gridLayout_task.count()):
            self.gridLayout_task.itemAt(i).widget().deleteLater()

        for i in range(self.gridLayout_setting.count()):
            self.gridLayout_setting.itemAt(i).widget().deleteLater()

        for i in range(self.verticalLayout_log.count()):
            self.verticalLayout_log.itemAt(i).widget().deleteLater()

        self.gridLayout_report.addWidget( self.rpaReportWidget )
        self.gridLayout_task.addWidget( self.rpaTaskWidget )
        self.gridLayout_setting.addWidget( self.rpaSettingWidget )
        self.verticalLayout_log.addWidget( self.logTextWidget )

        # Main 메뉴 버튼 클릭 이벤트 연결
        self.pushButton_report.clicked.connect(self.pushButton_report_clicked)
        self.pushButton_task.clicked.connect(self.pushButton_task_clicked)
        self.pushButton_setting.clicked.connect(self.pushButton_setting_clicked)

        self.logTextWidget.append_log("[ 지능형 CCTV 플랫폼 - RPA(Robotic Process Automation) 업무 관리 ]")
        self.logTextWidget.append_log("RPA 업무를 스케줄링합니다.")
        self.refresh_schedule() # RPA 업무 등록
        
        self.run_scheduler()  # RPA 스케줄러 실행
        self.update_current_time()  # 현재 시간 갱신 함수 호출

        # 기능숨김
        self.pushButton_setting.setVisible(False)  # 설정 버튼 숨김

    def refresh_schedule(self):
        rpa_task_list = RpaTask().select()
        rpa_task_count = len(rpa_task_list)  # DB에서 RPA 업무 개수 조회
    
        schedule.clear()  # 기존 스케줄 초기화
        for i, rpa_task in enumerate(rpa_task_list):           
            self.schedule_emails(rpa_task=rpa_task)  # 이메일 스케줄러 설정

            print(f"RPA Main Dialog : run_scheduler - {i+1}/{rpa_task_count} - {rpa_task.task_name} ({rpa_task.repeat_day_of_week}, {rpa_task.repeat_time})")
            self.logTextWidget.append_log(f"📆 {i+1}/{rpa_task_count}. {rpa_task.task_name} : "\
                                          f"매주 {helper.convert_weekdays_to_korean(rpa_task.repeat_day_of_week)}요일 {rpa_task.repeat_time} 예약 완료")    
            
        self.logTextWidget.append_log(f"✅ RPA 업무 {rpa_task_count}개 등록이 완료되었습니다.") # 서브 메뉴 숨기기
    
    def run_scheduler(self):
        def loop():
            while True:
                if __DEBUG__:
                    # print("RPA Main Dialog : run_scheduler - running")
                    pass
                schedule.run_pending()
                time.sleep(config.RPA_SCHEDULE_INTERVAL_SEC)
        threading.Thread(target=loop, daemon=True).start()

    # 현재 시간을 1초마다 갱신하는 함수
    def update_current_time(self):
        def refresh():
            self.label_time.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        timer = QTimer(self)
        timer.timeout.connect(refresh)
        timer.start(1000)  # 1초마다 갱신
        refresh()

    def schedule_emails(self, rpa_task:RpaTask=None):
        # if __DEBUG__:
        #     print("RPA Main Dialog : schedule_emails")

        _repeat_day_of_week =  rpa_task.repeat_day_of_week if rpa_task.repeat_day_of_week is not None else ""
        _repeat_day_of_week = _repeat_day_of_week.split(",")  # 쉼표로 분리하여 리스트로 변환

        for i, week_day in enumerate(_repeat_day_of_week):
            # print(f"RPA Main Dialog : schedule_emails - {week_day} {rpa_task.repeat_time}")

            if( week_day == "monday" ):
                schedule.every().monday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )            
            elif( week_day == "tuesday" ):
                schedule.every().tuesday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            elif( week_day == "wednesday" ):
                schedule.every().wednesday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            elif( week_day == "thursday" ):
                schedule.every().thursday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            elif( week_day == "friday" ):
                schedule.every().friday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            elif( week_day == "saturday" ):
                schedule.every().saturday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            elif( week_day == "sunday" ):
                schedule.every().sunday.at(rpa_task.repeat_time).do(self.send_email, rpa_task )
            else:
                self.logTextWidget.append_log(f"❌ 잘못된 요일: {week_day}")
                continue

    def send_email(self, rpa_task:RpaTask):

        if not rpa_task.email_receiver or not rpa_task.email_receiver.strip():
            self.logTextWidget.append_log("❌ 이메일 수신자가 지정되지 않았습니다.")
            return

        try:
            if __DEBUG__:
                print("RPA Main Dialog : send_email")
                
            to_list = [email.strip() for email in rpa_task.email_receiver.split(';') if email.strip()]

            msg = MIMEMultipart('related')  # 이미지 삽입 위해 related로 설정
            msg['From'] = config.RPA_EMAIL_ADDRESS
            msg['To'] = ", ".join(to_list)
            msg['Subject'] = f"[지능형CCTV플랫폼] {rpa_task.email_subject}"

            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)

            # HTML 본문 추가
            msg_alternative.attach(MIMEText(self.email_body_html(rpa_task), 'html'))

            with smtplib.SMTP(config.RPA_EMAIL_SMTP_SERVER, config.RPA_EMAIL_SMTP_PORT) as smtp:
                if config.RPA_TLS_ENABLED:
                    smtp.starttls()
                smtp.login(config.RPA_EMAIL_ADDRESS, config.RPA_EMAIL_APP_PASSWORD)
                smtp.send_message(msg)

            self.logTextWidget.append_log(f"✅ 이메일 전송 성공 → {msg['To']}")
            if __DEBUG__:
                print("RPA Main Dialog : send_email - Competed")
        except Exception as e:
            self.logTextWidget.append_log(f"❌ 이메일 전송 실패: {str(e)}")
            if __DEBUG__:
                print("RPA Main Dialog : send_email - failed : ", e)


    def email_body_html(self, rpa_task:RpaTask):
        if __DEBUG__:
            print("RPA Main Dialog : email_body_html")
        
        report_period_from = datetime.now() - timedelta(days=rpa_task.report_duration_days)
        report_period_to = datetime.now()

        _html = f"""
            <html>
            <body>
                <p>안녕하세요,<br>
                지능형 CCTV 플랫폼 RPA 리포트입니다.</p>
                <br>
                <p><b>업무명칭: {rpa_task.task_name}</b><br>
                업무 실행주기: {helper.convert_weekdays_to_korean(rpa_task.repeat_day_of_week)}<br>
                업무 실행시간: {rpa_task.repeat_time}<br>
                이메일 수신자: {rpa_task.email_receiver}<br></p>
            """

        if rpa_task.report_duration_days > 0:
            _html += f"""<p><b>보고서 검색기간: {report_period_from.strftime('%Y-%m-%d %H:%M:%S') }~
                       { report_period_to.strftime('%Y-%m-%d %H:%M:%S') }까지 </b>
                       (최근 {rpa_task.report_duration_days}일간)<br>
                       """                       
        
        _html += f"보고대상 이벤트 유형 : {rpa_task.report_event_type}<br>"
        _html += f"보고대상 이벤트 위험도: {  helper.convert_severities_to_korean( rpa_task.report_severity) }<br></p>"

        # DB 쿼리 실행
        report_list = RpaReport().select(event_date_from    = report_period_from.strftime("%Y-%m-%d %H:%M:%S"), 
                                        event_date_to      = report_period_to.strftime("%Y-%m-%d %H:%M:%S"), 
                                        severity           = rpa_task.report_severity.split(",") if rpa_task.report_severity else [], 
                                        event_type         = rpa_task.report_event_type.split(",") if rpa_task.report_event_type else [] )

        _html += """
            <h3>이벤트 리포트</h3>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px;">
                <thead>
                    <tr>
                    <th>순번</th>
                    <th>ID</th>
                    <th>이벤트 시간</th>
                    <th>보고 시간</th>
                    <th>제목</th>
                    <th>위치</th>
                    <th>이벤트 유형</th>
                    <th>이벤트 위험도</th>
                    <th>이벤트 조치</th>
                    <!-- <th>이벤트 이미지</th> -->
                    </tr>
                </thead>
                <tbody>
        """

        for row_idx, report in enumerate(report_list):
            event_time = report.event_time.strftime('%Y-%m-%d %H:%M:%S') if report.event_time else 'N/A'
            report_time = report.report_time.strftime('%Y-%m-%d %H:%M:%S') if report.report_time else 'N/A'
            severity = helper.severity_to_label(report.severity)
            image_cell = report.image_path if report.image_path else '이미지 없음'

            # 이미지 경로가 URL이면 링크로
            if report.image_path and report.image_path.startswith("http"):
                image_cell = f'<a href="{report.image_path}" target="_blank">이미지 보기</a>'

            _html += f"""
                    <tr>
                    <td>{row_idx + 1}</td>
                    <td>{report.id}</td>
                    <td>{event_time}</td>
                    <td>{report_time}</td>
                    <td>{report.title}</td>
                    <td>{report.location}</td>
                    <td>{report.event_type}</td>
                    <td>{severity}</td>
                    <td>{report.action}</td>
                    <!-- <td>{image_cell}</td> -->
                    </tr>
            """

        _html += """
                </tbody>
            </table>
        </body>
        </html>"""

        return _html

    # Main 메뉴 버튼 클릭 이벤트
    def pushButton_report_clicked(self):
        print("RPA Main Dialog : pushButton_report_clicked")
        self.stackedWidget.setCurrentIndex(self._report)

    def pushButton_task_clicked(self):
        print("RPA Main Dialog : pushButton_task_clicked")
        self.stackedWidget.setCurrentIndex( self._task)
        
    def pushButton_setting_clicked(self):
        print("RPA Main Dialog : pushButton_setting_clicked")
        self.stackedWidget.setCurrentIndex( self._setting)

    def pushButton_task_scheduler_restart_clicked(self):
        print("RPA Main Dialog : pushButton_task_scheduler_restart_clicked")
        self.logTextWidget.append_log("🔄 RPA 스케줄러를 재시작합니다.")
        self.refresh_schedule()

    def closeEvent(self, event):
        if __DEBUG__:
            print("RPA Main Dialog : closeEvent")
        else:
            event.ignore()
            self.hide()
    

if __name__ == "__main__":
    __DEBUG__ = True

    app = QApplication(sys.argv)
    window = RpaMainWindow()
    window.show()
    sys.exit(app.exec())


    # rpatask = RpaTask()
    # rpatask.task_name = "테스트 업무"
    # rpatask.repeat_day_of_week = "monday,tuesday,wednesday,thursday,friday"
    # rpatask.repeat_time = "09:00"
    # rpatask.report_duration_days = 10
    # rpatask.report_severity = "danger_highhigh,danger_high,danger_mid,danger_low,danger_lowlow"
    # rpatask.report_event_type = ""
    # rpatask.email_receiver = "srlee@skysys.co.kr;"
        
    # app = QApplication(sys.argv)
    # window = RpaMainWindow()

    # print( window.email_body_html(rpatask) )
    # sys.exit(app.exec())
