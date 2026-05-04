import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import Slot
from ui.ui_ai_event_log_search_dialog import Ui_Dialog

from widget.ai_event_log_search_cctv_list_widget import AiEventLogSearchCctvListWidget
from widget.ai_event_log_filter_search_widget import AiEventLogFilterSearchWidget
from widget.ai_event_log_search_event_list_widget import AiEventLogSearchEventListWidget
from widget.ai_event_log_paging_widget import AiEventLogPagingWidget
from widget.ai_event_log_graph_widget import AiEventLogGraphWidget
from widget.ai_event_log_selected_image_widget import AiEventLogSelectedImageWidget

class AiEventLogSearchDialog(QDialog, Ui_Dialog):
    def __init__(self, rap_dialog, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # UI 설정
        
        self.rap_dialog = rap_dialog

        self.setup_ui()
        self.init_ui()


    def setup_ui(self):
        self.setWindowTitle(f"이벤트 로그 검색")
        
        self.layout_event_log_filter_search.insertSpacing(1, 5)
        self.layout_event_log_filter_search.insertSpacing(0, 5)

        # CCTV 목록
        self.ai_event_log_search_cctv_list_widget = AiEventLogSearchCctvListWidget()
        self.layout_cctv_list.replaceWidget(self.label_ai_event_log_search_cctv_list_widget, self.ai_event_log_search_cctv_list_widget)
        self.label_ai_event_log_search_cctv_list_widget.deleteLater()
        
        # 이벤트 검색
        self.ai_event_log_filter_search_widget = AiEventLogFilterSearchWidget()
        self.layout_event_log_filter_search.replaceWidget(self.label_ai_event_log_filter_search_widget, self.ai_event_log_filter_search_widget)
        self.label_ai_event_log_filter_search_widget.deleteLater()

        # 이벤트 목록
        self.ai_event_log_search_event_list_widget = AiEventLogSearchEventListWidget()
        self.layout_event_list.replaceWidget(self.label_ai_event_log_search_event_list_widget, self.ai_event_log_search_event_list_widget)
        self.label_ai_event_log_search_event_list_widget.deleteLater()

        # 이벤트 로그 목록
        self.ai_event_log_paging_widget = AiEventLogPagingWidget(self.rap_dialog)
        self.layout_event_log_list.replaceWidget(self.label_ai_event_log_paging_widget, self.ai_event_log_paging_widget)
        self.label_ai_event_log_paging_widget.deleteLater()

        # 이벤트 통계 그래프
        self.ai_event_log_graph_widget = AiEventLogGraphWidget()
        self.layout_event_log_graph.replaceWidget(self.label_ai_event_log_graph_widget, self.ai_event_log_graph_widget)
        self.label_ai_event_log_graph_widget.deleteLater()

        # 이벤트 로그 선택 이미지
        self.ai_event_log_selected_image_widget = AiEventLogSelectedImageWidget()
        self.ai_event_log_selected_image_widget.setMaximumSize(713, 150) # 위젯의 최대 크기 제한
        self.layout_event_log_list.replaceWidget(self.label_ai_event_log_selected_image_widget, self.ai_event_log_selected_image_widget)
        self.label_ai_event_log_selected_image_widget.deleteLater()
        self.ai_event_log_selected_image_widget.hide()

    def init_ui(self):
        self.tab_widget_event_log.setCurrentIndex(0)

        # 보고서 작성
        self.button_report.clicked.connect(self.on_button_report_clicked)

        # 새로고침
        self.button_refresh.clicked.connect(self.on_button_refresh_clicked)

        # 이벤트 로그 목록
        self.ai_event_log_paging_widget.table_cell_clicked.connect(self.toggle_event_log_selected_image_widget)
        self.ai_event_log_paging_widget.ai_event_logs_loading_finished.connect(self.load_ai_event_logs_finished)

        # 이벤트 통계 그래프
        self.ai_event_log_graph_widget.ai_event_logs_loading_finished.connect(self.load_ai_event_logs_finished)

        # 이벤트 검색
        self.ai_event_log_filter_search_widget.search_requested.connect(self.search_ai_event_logs)

    def on_button_report_clicked(self):
        self.ai_event_log_paging_widget.create_report()

    @Slot(dict)
    def toggle_event_log_selected_image_widget(self, event_log_info):
        widget = self.ai_event_log_selected_image_widget

        widget.set_event_log_info(event_log_info)
        if event_log_info['checked']:
            widget.show()
        else:
            widget.hide()

    @Slot()
    def load_ai_event_logs_finished(self):
        self.ai_event_log_filter_search_widget.set_search_buttons_enabled(True)

    @Slot(str, str)
    def search_ai_event_logs(self, start_dt: str, end_dt: str):
        selected_cctvs = self.ai_event_log_search_cctv_list_widget.get_selected_items_dict()
        selected_events = self.ai_event_log_search_event_list_widget.get_selected_items_dict()
        self.ai_event_log_paging_widget.display_search_results(start_dt, end_dt, selected_cctvs, selected_events)
        self.ai_event_log_graph_widget.display_search_results(start_dt, end_dt, selected_cctvs, selected_events)

    def on_button_refresh_clicked(self):
        """새로고침 버튼 클릭 시 호출되는 함수 """
        # 1. CCTV 목록 새로고침 
        self.ai_event_log_search_cctv_list_widget.load_cctv_list_to_tree(
            self.ai_event_log_search_cctv_list_widget.tree_view_cctv_list
        )
        
        # 2. 이벤트 목록 새로고침 
        import db.db_logic_list as db_logic_list
        self.ai_event_log_search_event_list_widget.event_list = db_logic_list.get_event_logic_name()
        self.ai_event_log_search_event_list_widget.load_event_list_to_list(
            self.ai_event_log_search_event_list_widget.event_list
        )
        
        # 3. 이벤트 로그 페이징 위젯 새로고침 
        self.ai_event_log_paging_widget.init_ui()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AiEventLogSearchDialog(rap_dialog=None)
    window.show()
    sys.exit(app.exec())


    