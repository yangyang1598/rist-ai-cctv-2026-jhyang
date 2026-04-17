from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QTextCursor

class LogTextWidget(QPlainTextEdit):
    def __init__(self, max_lines=1000, parent=None):
        super().__init__(parent)
        self.max_lines = max_lines
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    def append_log(self, text: str):
        """로그를 추가하고 최대 줄 수를 초과하면 가장 오래된 줄 제거"""
        self.appendPlainText(text)
        self.ensureCursorVisible()
        self._trim_lines()

    def _trim_lines(self):
        """최대 줄 수를 초과하면 앞에서부터 줄을 삭제"""
        doc = self.document()
        block_count = doc.blockCount()

        if block_count <= self.max_lines:
            return

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        lines_to_remove = block_count - self.max_lines
        for _ in range(lines_to_remove):
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()  # 줄바꿈 제거

        # 커서 초기화 및 스크롤 유지
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
