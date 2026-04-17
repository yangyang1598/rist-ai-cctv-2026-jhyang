import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QApplication

from ui.ui_ai_event_log_page_button_frame_widget import Ui_Widget

class AiEventLogPageButtonFrameWidget(QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AiEventLogPageButtonFrameWidget()
    widget.show()  
    sys.exit(app.exec()) 