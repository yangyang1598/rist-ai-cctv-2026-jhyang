import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import db.db_ai_event_log as db_ai_event_log

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QMessageBox
from PySide6.QtCore import QDateTime, QDate, QTime, QThread, Signal, Slot


class LoadEventLogsQThread(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, start_dt: str, end_dt: str, selected_cctvs: dict, selected_events: list):
        super().__init__()
        self.setObjectName("LoadEventLogsQThread")
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.selected_cctvs = selected_cctvs
        self.selected_events = selected_events
    def run(self):
        fields = "DATE(date) AS event_date, content, COUNT(*) AS count"
        event_logs = db_ai_event_log.get_ai_event_logs(fields=fields, start_dt=self.start_dt, end_dt=self.end_dt, selected_cctvs=self.selected_cctvs, selected_events=self.selected_events, order_by="event_date, content", group_by=['event_date', 'content'])
        self.finished.emit(event_logs)

class AiEventLogGraphWidget(QWidget):
    ai_event_logs_loading_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"이벤트 로그 통계")
        self.setup_ui()
        self.init_ui()
        
    def setup_ui(self):
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'  # 대체 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def init_ui(self):
        self.canvas = None
        self.last_pivot = None
        # 검색 필터 값
        self.start_dt = QDateTime(QDate(2024,5,13), QTime(0, 0, 0)).toString("yyyy-MM-dd HH:mm:ss")
        # self.start_dt = QDateTime(QDate.currentDate(), QTime(0, 0, 0)).toString("yyyy-MM-dd HH:mm:ss")
        self.end_dt = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.selected_cctvs = {}
        self.selected_events = []
        self.load_event_logs()

    def load_event_logs(self):
        self.load_thread = LoadEventLogsQThread(self.start_dt, self.end_dt, self.selected_cctvs, self.selected_events)
        self.load_thread.finished.connect(self.update_heatmap)
        self.load_thread.start()

    def update_heatmap(self, event_logs: list[dict]):
        # 이전 캔버스 제거
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None

        # 새 캔버스 생성 및 추가
        self.canvas = self.create_heatmap_canvas(event_logs)
        self.layout.addWidget(self.canvas)

        self.ai_event_logs_loading_finished.emit()

    def custom_label(self, start: pd.Timestamp, end: pd.Timestamp) -> str:
        return f"{start.date()}" if start.date() == end.date() else f"{start.date()} ~ {end.date()}"

    def group_data_by_unit(self, df: pd.DataFrame):
        if df.empty:
            return pd.DataFrame()

        df = df.copy()
        df['event_date'] = pd.to_datetime(df['event_date'])

        # 기간 계산
        start_date = pd.to_datetime(self.start_dt)
        end_date = pd.to_datetime(self.end_dt)
        total_days = (end_date - start_date).days

        # 단위 선택
        max_columns = 20
        total_days = (end_date - start_date).days + 1

        if total_days / 1 <= max_columns:
            unit = 'D'
        elif total_days / 7 <= max_columns:
            unit = 'W'
        elif total_days / 30 <= max_columns:
            unit = 'M'
        else:
            unit = 'Y'

        # 그룹 기준 컬럼 만들기
        if unit == 'D':
            df['group_label'] = df['event_date'].dt.strftime('%Y-%m-%d')
            group_labels = pd.date_range(start_date, end_date, freq='D').strftime('%Y-%m-%d').tolist()

        elif unit == 'W':
            df['event_date'] = pd.to_datetime(df['event_date'])

            group_labels = []
            label_map = {}

            current = start_date

            # 첫 주: 시작일 ~ 그 주 일요일까지
            first_sunday = start_date + pd.Timedelta(days=(6 - start_date.weekday()))
            first_end = min(first_sunday, end_date)
            label = self.custom_label(current, first_end)
            group_labels.append(label)
            for d in pd.date_range(current, first_end, freq='D'):
                label_map[d.date()] = label

            current = first_end + pd.Timedelta(days=1)

            # 중간 주들: 월~일
            while current + pd.Timedelta(days=6) <= end_date:
                week_start = current
                week_end = current + pd.Timedelta(days=6)
                label = self.custom_label(week_start, week_end)
                group_labels.append(label)
                for d in pd.date_range(week_start, week_end, freq='D'):
                    label_map[d.date()] = label
                current = week_end + pd.Timedelta(days=1)

            # 마지막 주 처리
            if current <= end_date:
                label = self.custom_label(current, end_date)
                group_labels.append(label)
                for d in pd.date_range(current, end_date, freq='D'):
                    label_map[d.date()] = label

            # 라벨 지정
            df['group_label'] = df['event_date'].dt.date.map(label_map)

        elif unit == 'M':
            df['group_label'] = df['event_date'].dt.to_period('M').astype(str)

            aligned_start = pd.to_datetime(f"{start_date.year}-{start_date.month:02d}-01")
            month_range = pd.date_range(start=aligned_start, end=end_date, freq='MS')
            group_labels = month_range.strftime('%Y-%m').tolist()

        else:
            df['group_label'] = df['event_date'].dt.to_period('Y').astype(str)
            year_range = pd.date_range(start=start_date, end=end_date, freq='YS')
            group_labels = year_range.strftime('%Y').tolist()

        # 집계
        grouped = df.groupby(['content', 'group_label'])['count'].sum().reset_index()
        pivot = grouped.pivot(index='content', columns='group_label', values='count')

        # 누락된 열 보완
        pivot = pivot.reindex(columns=group_labels, fill_value=0)
        pivot = pivot.fillna(0)

        return pivot
        
    def create_heatmap_canvas(self, event_logs):
        fig, ax = plt.subplots(
            figsize=(14, 6),
            constrained_layout=True
        )

        if not event_logs:
            # 메시지 출력
            ax.text(0.5, 0.5, '해당 기간 내 데이터가 없습니다.', ha='center', va='center', fontsize=14)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)
        else:
            df = pd.DataFrame(event_logs)
            # 피벗 생성
            pivot = self.group_data_by_unit(df)

            sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)

            ax.set_title("이벤트별 발생 건수")
            ax.set_xlabel("기간")
            ax.set_ylabel("이벤트 종류")
            ax.tick_params(axis='x', labelrotation=45)
            for label in ax.get_xticklabels():
                label.set_horizontalalignment('right')
                label.set_fontsize(9)

            self.heatmap_ax = ax
            self.last_pivot = pivot

        # 캔버스 생성
        canvas = FigureCanvas(fig)
        # canvas.mpl_connect("button_press_event", self.on_heatmap_click)

        return canvas

    def display_search_results(self, start_dt: str, end_dt: str, selected_cctvs: dict, selected_events: list):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.selected_cctvs = selected_cctvs
        self.selected_events = selected_events

        self.load_event_logs()

    # def on_heatmap_click(self, event):
    #     if self.last_pivot is None:
    #         return

    #     ax = self.heatmap_ax

    #     # 셀 클릭 처리
    #     if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
    #         x = int(event.xdata)
    #         y = int(event.ydata)
    #         try:
    #             if value:= self.last_pivot.iloc[y, x]:
    #                 print(value)
    #                 col_label = self.last_pivot.columns[x].split('~')
    #                 if len(col_label) > 1:
    #                     self.start_dt = col_label[0]
    #                     self.end_dt = col_label[1]
    #                 else:
    #                     # 행이 다수이면 처리해야함
    #                     return

    #                 self.selected_events = [self.last_pivot.index[y]]

    #                 print(f"[셀 클릭]")
    #                 print("→ 시작 날짜:", self.start_dt)
    #                 print("→ 종료 날짜:", self.end_dt)
    #                 print(f"이벤트: {self.selected_events}")
    #                 self.load_event_logs()
    #             else:
    #                 QMessageBox.information(self, "이벤트 통계", "해당 기간 내 데이터가 없습니다.")
    #         except (IndexError, KeyError):
    #             pass
    #         return

    #     # 축 라벨 클릭은 픽셀 좌표 기준 처리
    #     # → Axes 내부가 아니므로 event.inaxes는 None
    #     fig = event.canvas.figure
    #     xticks = ax.get_xticklabels()
    #     yticks = ax.get_yticklabels()

    #     for label in xticks:
    #         bbox = label.get_window_extent(renderer=fig.canvas.get_renderer())
    #         if bbox.contains(event.x, event.y):
    #             col_label = label.get_text()
    #             values = self.last_pivot[col_label]
    #             col_label = label.get_text().split('~')
    #             if len(col_label) > 1:
    #                 self.start_dt = col_label[0]
    #                 self.end_dt = col_label[1]
    #             else:
    #                 return

    #             self.selected_events = list(values[values.notna()].index)   # content 이름만 리스트로 추출 (값이 NaN이 아닌 항목만 포함)

    #             self.load_event_logs()
    #             print(f"[날짜 클릭]")
    #             print("→ 시작 날짜:", self.start_dt)
    #             print("→ 종료 날짜:", self.end_dt)
    #             print("content 리스트:", self.selected_events)
    #             return

    #     for label in yticks:
    #         bbox = label.get_window_extent(renderer=fig.canvas.get_renderer())
    #         if bbox.contains(event.x, event.y):
    #             row_label = label.get_text()  # 예: '지게차 접근'

    #             # 해당 이벤트 행에서 NaN이 아닌 열만 추출 (이벤트 발생한 날짜들)
    #             values = self.last_pivot.loc[row_label]
    #             valid_dates = values[values.notna()].index.tolist()

    #             if valid_dates:
    #                 start_date = valid_dates[0]
    #                 end_date = valid_dates[-1]
    #                 print(f"[이벤트 클릭] {row_label}")
    #                 print("→ 시작 날짜:", start_date)
    #                 print("→ 종료 날짜:", end_date)
    #             else:
    #                 print(f"[이벤트 클릭] {row_label} (발생한 날짜 없음)")
    #             return
                    
    def on_search_clicked(self):
        event_logs = fetch_event_logs_from_db(...)
        self.heatmap_widget.update_heatmap(event_logs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogChartWidget()
    widget.show()  
    sys.exit(app.exec()) 
