import sys, os
sys.path.append(os.path.abspath(os.curdir))

# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
# from rpa.db.db_manager_rpa import RpaDBManager
from db.db_manager import DBManager

from rpa import rpa_helper as helper

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QApplication, QMessageBox
)
from PySide6.QtCore import Qt
class RpaTask:
    TABLE_NAME = 'rpa_task'

    def __init__(self):
        self.id = 0
        self.task_name = ''
        self.repeat_day_of_week = ''         # 예: "Mon,Wed,Fri"
        self.repeat_time = ''         # 예: "08:00"
        self.report_duration_hours = 0
        self.report_duration_days = 0
        self.report_severity = ''     # 예: "danger_highhigh,danger_high"
        self.report_event_type = ''   # 예: "화재,추락"
        self.email_receiver = ''      # 콤마로 구분된 이메일 리스트
        self.email_subject = ''
        self.email_body = ''

    def get_dbmanager(self)-> DBManager:
        return DBManager()

    def init(self):
        db = self.get_dbmanager()
        return db.query(self.sql_create_table(), fetch_type='none')
    def insert(self):
        db = self.get_dbmanager()
        return db.query(self.sql_insert(),fetch_type='none', return_rowcount=True)

    def update(self, id):
        db = self.get_dbmanager()
        return db.query(self.sql_update(id),fetch_type='none', return_rowcount=True)

    def delete(self, id):
        db = self.get_dbmanager()
        return db.query(self.sql_delete(id),fetch_type='none', return_rowcount=True)

    def select(self, id=None):
        db = self.get_dbmanager()
        sql = self.sql_select(id)
        rows= db.query(sql,fetch_type='all')
        task_list = []

        for r in rows:
            t = RpaTask()
            t.id = r.get('id')
            t.task_name = r.get('task_name')
            t.repeat_day_of_week = r.get('repeat_day_of_week')
            t.repeat_time = r.get('repeat_time')
            t.report_duration_hours = r.get('report_duration_hours')
            t.report_duration_days = r.get('report_duration_days')
            t.report_severity = r.get('report_severity')
            t.report_event_type = r.get('report_event_type')
            t.email_receiver = r.get('email_receiver')
            t.email_subject = r.get('email_subject')
            t.email_body = r.get('email_body')
            task_list.append(t)

        return task_list

    def sql_create_table(self):
        return f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_name VARCHAR(255),
                repeat_day_of_week VARCHAR(255),
                repeat_time VARCHAR(10),
                report_duration_hours INT,
                report_duration_days INT,
                report_severity TEXT,
                report_event_type TEXT,
                email_receiver TEXT,
                email_subject TEXT,
                email_body TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

    def sql_insert(self):
        return f"""
            INSERT INTO {self.TABLE_NAME}
            (task_name, repeat_day_of_week, repeat_time, report_duration_hours, report_duration_days,
             report_severity, report_event_type, email_receiver, email_subject, email_body)
            VALUES (
                '{self.task_name}', '{self.repeat_day_of_week}', '{self.repeat_time}', {self.report_duration_hours},
                {self.report_duration_days}, '{self.report_severity}', '{self.report_event_type}',
                '{self.email_receiver}', '{self.email_subject}', '{self.email_body}'
            );
        """

    def sql_update(self, id):
        return f"""
            UPDATE {self.TABLE_NAME}
            SET 
                task_name = '{self.task_name}',
                repeat_day_of_week = '{self.repeat_day_of_week}',
                repeat_time = '{self.repeat_time}',
                report_duration_hours = {self.report_duration_hours},
                report_duration_days = {self.report_duration_days},
                report_severity = '{self.report_severity}',
                report_event_type = '{self.report_event_type}',
                email_receiver = '{self.email_receiver}',
                email_subject = '{self.email_subject}',
                email_body = '{self.email_body}'
            WHERE id = {id};
        """

    def sql_delete(self, id):
        return f"DELETE FROM {self.TABLE_NAME} WHERE id = {id};"

    def sql_select(self, id=None):
        sql = f"SELECT * FROM {self.TABLE_NAME}"
        if id is not None:
            sql += f" WHERE id = {id}"
        sql += " ORDER BY id DESC"
        return sql


class RpaTaskTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA Task Test")
        self.setGeometry(200, 200, 600, 600)

        self.task = RpaTask()
        self.task.init()

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        self.inputs = {}
        fields = [
            ('task_name', 'Task Name'),
            ('repeat_day_of_week', 'Repeat Day of week (e.g. Mon,Tue,Wed,Fri)'),
            ('repeat_time', 'Repeat Time (e.g. 08:00)'),
            ('report_duration_hours', 'Report Duration (hours)'),
            ('report_duration_days', 'Report Duration (days)'),
            ('report_severity', 'Report Severity (e.g. danger_highhigh,danger_high)'),
            ('report_event_type', 'Report Event Type (e.g. 화재,추락)'),
            ('email_receiver', 'Email Receivers (comma-separated)'),
            ('email_subject', 'Email Subject'),
        ]

        for field, label in fields:
            layout.addWidget(QLabel(label))
            line_edit = QLineEdit()
            self.inputs[field] = line_edit
            layout.addWidget(line_edit)

        layout.addWidget(QLabel("Email Body"))
        self.email_body_input = QTextEdit()
        layout.addWidget(self.email_body_input)

        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.on_save)
        button_layout.addWidget(save_button)

        load_button = QPushButton("Load Latest")
        load_button.clicked.connect(self.on_load)
        button_layout.addWidget(load_button)

        sample_button = QPushButton("샘플 입력")  # 샘플 입력 버튼 추가
        sample_button.clicked.connect(self.fill_sample_data)
        button_layout.addWidget(sample_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_save(self):
        for field in self.inputs:
            value = self.inputs[field].text()
            if field in ['report_duration_hours', 'report_duration_days']:
                try:
                    value = int(value)
                except ValueError:
                    QMessageBox.warning(self, "Warning", f"{field} must be an integer.")
                    return
            setattr(self.task, field, value)
        self.task.email_body = self.email_body_input.toPlainText()

        self.task.insert()
        QMessageBox.information(self, "Info", "Task saved successfully!")

    def on_load(self):
        tasks = self.task.select()
        if not tasks:
            QMessageBox.information(self, "Info", "No tasks found.")
            return

        self.task = tasks[0]
        for field in self.inputs:
            self.inputs[field].setText(str(getattr(self.task, field)))
        self.email_body_input.setPlainText(self.task.email_body)

    def fill_sample_data(self):  # 샘플 데이터 채우기 함수 추가
        import random
        import datetime

        sample_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        sample_severities = ['danger_highhigh', 'danger_high', 'danger_mid', 'danger_low', 'danger_lowlow']
        sample_event_types = ['화재', '추락', '침입', '가스누출']
        sample_receivers = []

        self.inputs['task_name'].setText(f"주간보고서 송신업무 - {random.randint(1, 100)}")
        self.inputs['repeat_day_of_week'].setText(','.join(  helper.sort_weekdays( random.sample(sample_days, random.randint(1, 3)))))
        self.inputs['repeat_time'].setText(f"{random.randint(0,23):02}:{random.choice([0,30]):02}")
        self.inputs['report_duration_hours'].setText(str(random.choice([6, 12, 24])))
        self.inputs['report_duration_days'].setText(str(random.choice([1, 2, 3])))
        self.inputs['report_severity'].setText(','.join(random.sample(sample_severities, 1)))
        self.inputs['report_event_type'].setText(','.join(random.sample(sample_event_types, random.randint(1, 3))))
        self.inputs['email_receiver'].setText(','.join(random.sample(sample_receivers, random.randint(1, 3))))
        self.inputs['email_subject'].setText(f"테스트 이메일 제목 {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        self.email_body_input.setPlainText("이것은 샘플 이메일 본문입니다.\n테스트용 문구입니다.")



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RpaTaskTestWindow()
    window.show()
    sys.exit(app.exec())