# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.curdir))
import random

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextBrowser,
    QTableWidget, QTableWidgetItem, QWidget
)
from PySide6.QtCore import QDateTime, QTimer
from datetime import datetime, timedelta
# from rpa.db.db_manager_rpa import RpaDBManager
from db.db_manager import DBManager

from rpa import rpa_helper as helper

class RpaReport():
    TABLE_NAME = 'rpa_report'

    def __init__(self):
        self.id = 0
        self.event_time = None
        self.report_time = None
        self.title = ''
        self.location = ''
        self.event_type = ''
        self.severity = ''
        self.action = ''
        self.image_path = ''

    def get_dbmanager(self)-> DBManager:
        return DBManager()
        
    def init(self):
        db = self.get_dbmanager()
        return db.query(self.sql_create_table(), fetch_type='none')

    def insert(self):
        db = self.get_dbmanager()
        return db.query(self.sql_insert(), fetch_type='none',return_rowcount=True)

    def update(self, id):
        db = self.get_dbmanager()
        return db.query(self.sql_update(id),fetch_type='none', return_rowcount=True)

    def delete(self, id):
        db = self.get_dbmanager()
        return db.query(self.sql_delete(id),fetch_type='none', return_rowcount=True)

    def select(self, id=None, event_date_from=None, event_date_to=None, severity=None, event_type=None, limit=None):
        db = self.get_dbmanager()
        sql = self.sql_select(id, event_date_from, event_date_to, severity, event_type, limit)
        rows = db.query(sql,fetch_type='all')
        report_list = []

        for r in rows:
            report = RpaReport()
            report.id = r.get('id')
            report.event_time = r.get('event_time')
            report.report_time = r.get('report_time')
            report.title = r.get('title')
            report.location = r.get('location')
            report.event_type = r.get('event_type')
            report.severity = r.get('severity')
            report.action = r.get('action')
            report.image_path = r.get('image_path')
            report_list.append(report)

        return report_list


    # 이벤트 유형을 가져오는 메서드 ('추락', '화재', '가스누출', '지적감시', '훈소', '충돌', '협착', ...)
    def get_distinct_event_types(self):
        db = self.get_dbmanager()
        sql = f"SELECT DISTINCT event_type FROM {self.TABLE_NAME} WHERE event_type IS NOT NULL;"
        rows = db.query(sql,fetch_type='all')
        return [r.get("event_type") for r in rows]

    def sql_insert(self):
        return f"""
            INSERT INTO {self.TABLE_NAME}
            (event_time, report_time, title, location, event_type, severity, action, image_path)
            VALUES (
                '{self.event_time}', '{self.report_time}', '{self.title}', '{self.location}', 
                '{self.event_type}', '{self.severity}', '{self.action}', '{self.image_path}'
            );
        """

    def sql_update(self, id):
        return f"""
            UPDATE {self.TABLE_NAME}
            SET 
                event_time = '{self.event_time}',
                report_time = '{self.report_time}',
                title = '{self.title}',
                location = '{self.location}',
                event_type = '{self.event_type}',
                severity = '{self.severity}',
                action = '{self.action}',
                image_path = '{self.image_path}'
            WHERE id = {id};
        """

    def sql_delete(self, id):
        return f"DELETE FROM {self.TABLE_NAME} WHERE id = {id};"

    def sql_select(self, id=None, event_date_from=None, event_date_to=None, severity=None, event_type=None, limit=None):
        conditions = []

        if id is not None:
            conditions.append(f"id = {id}")
        if event_date_from and event_date_to:
            conditions.append(f"event_time BETWEEN '{event_date_from}' AND '{event_date_to}'")
        elif event_date_from:
            conditions.append(f"event_time >= '{event_date_from}'")
        elif event_date_to:
            conditions.append(f"event_time <= '{event_date_to}'")
        if severity:  # 리스트가 비어있지 않다면
            severity_list = ', '.join([f"'{s}'" for s in severity])
            conditions.append(f"severity IN ({severity_list})") 
        if event_type:
            for etype in event_type:
                # % 기호가 포매팅 기호로 해석되지 않도록 %%로 이스케이프 처리
                escaped_etype = etype.replace('%', '%%')
                conditions.append(f"event_type LIKE '%%{escaped_etype}%%'")

            

        sql = f"""
            SELECT id, event_time, report_time, title, location, event_type, severity, action, image_path
            FROM {self.TABLE_NAME}
        """

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY report_time DESC"

        if limit is not None:
            sql += f" LIMIT {limit}"

        print(f"SQL Query: {sql}")

        return sql

    def sql_create_table(self):
        return f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_time DATETIME,
                report_time DATETIME,
                title VARCHAR(255),
                location VARCHAR(255),
                event_type VARCHAR(255),
                severity VARCHAR(255),
                action TEXT,
                image_path VARCHAR(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

    def time_utc_to_kst(self, datetime_utc) -> datetime:
        if datetime_utc:
            return datetime_utc + timedelta(hours=9)
        return None


class RpaReportTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA Report 테스트 UI")
        self.setGeometry(100, 100, 1000, 700)

        self.init_ui()
        RpaReport().init()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("상태: 대기중")
        self.log_view = QTextBrowser()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "발생일시", "보고일시", "제목", "장소", "위험유형", "심각도", "사진경로"
        ])

        self.insert_btn = QPushButton("이벤트 등록")
        self.insert_btn.clicked.connect(self.insert_event)

        self.update_btn = QPushButton("ID=1 이벤트 수정")
        self.update_btn.clicked.connect(self.update_event)

        self.delete_btn = QPushButton("ID=1 이벤트 삭제")
        self.delete_btn.clicked.connect(self.delete_event)

        self.query_btn = QPushButton("이벤트 전체 조회")
        self.query_btn.clicked.connect(self.query_events)

        layout.addWidget(self.status_label)
        layout.addWidget(self.insert_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.query_btn)
        layout.addWidget(self.table)
        layout.addWidget(self.log_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log(self, msg):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.log_view.append(f"[{timestamp}] {msg}")

    def insert_event(self):
        report = RpaReport()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.event_time = now
        report.report_time = now
        report.title = "이벤트 발생" + str(random.randint(1, 1000))
        report.location = random.choice(["제1공장 CCTV1",   "제1공장 CCTV2", "제2공장 CCTV1", "제2공장 CCTV2"])
        report.event_type = ",".join( random.sample( sorted(set(["화재","훈소", "충돌","협착","충돌", "지적감시" , "가_위험유형", "나_위험유형", "다_위험유형", "라_위험유형"])), random.randint(1,3)) )
        report.severity = random.choice(["danger_highhigh","danger_high","danger_mid","danger_low","danger_lowlow", "good_highhigh","good_high","good_mid"])
        report.action = random.choice(["자동알림","수동알림"]) +  " 및 " + random.choice(["소방출동" , "소방서에 자동 신고 완료", "현장 대피 및 출입 통제", "소방서에 수동 신고 완료"])
        report.image_path = "images/fire_detected.jpg"

        report.insert()
        self.log("이벤트 등록 완료")

    def update_event(self):
        report = RpaReport()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.event_time = now
        report.report_time = now
        report.title = "이벤트 수정됨" + str(random.randint(1, 1000))
        report.location = random.choice(["제1공장 CCTV1",   "제1공장 CCTV2", "제2공장 CCTV1", "제2공장 CCTV2"])
        report.event_type = ",".join( random.sample( sorted(set(["화재","훈소", "충돌","협착","충돌", "지적감시" , "가_위험유형", "나_위험유형", "다_위험유형", "라_위험유형"])), random.randint(1,3)) )
        report.severity = random.choice(["danger_highhigh","danger_high","danger_mid","danger_low","danger_lowlow", "good_highhigh","good_high","good_mid"])
        report.action = random.choice(["자동알림","수동알림"]) +  " 및 " + random.choice(["소방출동" , "소방서에 자동 신고 완료", "현장 대피 및 출입 통제", "소방서에 수동 신고 완료"])
        report.image_path = "images/gas_leak.jpg"

        _id_to_update = 75  # 예시로 ID 1을 수정
        result = report.update( _id_to_update)
        self.log(f"ID={_id_to_update} 이벤트 수정 완료" if result else "이벤트 수정 실패")

    def delete_event(self):
        report = RpaReport()
        _id_to_delete = 76  # 예시로 ID 77을 삭제

        result = report.delete( _id_to_delete)
        self.log(f"ID={_id_to_delete} 이벤트 삭제 완료" if result else "이벤트 삭제 실패")

    def query_events(self):
        report = RpaReport()
        reports = report.select(limit=10)

        self.table.setRowCount(len(reports))
        for row_idx, r in enumerate(reports):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(r.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(r.event_time)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(r.report_time)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(r.title))
            self.table.setItem(row_idx, 4, QTableWidgetItem(r.location))
            self.table.setItem(row_idx, 5, QTableWidgetItem(r.event_type))
            self.table.setItem(row_idx, 6, QTableWidgetItem(r.severity))
            self.table.setItem(row_idx, 7, QTableWidgetItem(r.image_path))

        self.log("이벤트 조회 완료")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = RpaReportTestWindow()
    window.show()
    sys.exit(app.exec())


    # # 1. 테이블 생성
    # rr = RpaReport()
    # rr.init()
    # print("테이블 생성 완료.")

    # # 2. 데이터 삽입
    # rr.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # rr.report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # rr.title = "화재 발생"
    # rr.location = "울산 산악지"
    # rr.event_type = "산불"
    # rr.severity = random.choice(["매우 심각","심각","위험","경미","매우경미","매우우수","우수","정상"])
    # rr.action = "소방서에 자동 신고 완료"
    # rr.image_path = "/images/fire_event.jpg"

    # rr.insert()
    # print("데이터 삽입 완료.")

    # # 3. 데이터 조회
    # reports = rr.select(limit=5)
    # print(f"{len(reports)}건의 데이터 조회됨.")
    # for r in reports:
    #     print(f"[{r.id}] {r.event_time} | {r.title} | {r.severity}")

    # if reports:
    #     # 4. 데이터 수정
    #     first = reports[0]
    #     first.title = "화재 경보 (수정됨)"
    #     first.severity = "Critical"
    #     first.action = "드론 자동 출동"
    #     first.update(first.id)
    #     print(f"ID {first.id} 수정 완료.")

    #     # 5. 데이터 삭제 테스트
    #     rr.delete(first.id)
    #     print(f"ID {first.id} 삭제 완료.")