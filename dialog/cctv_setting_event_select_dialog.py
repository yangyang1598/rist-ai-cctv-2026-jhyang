from PySide6.QtWidgets import QDialog, QCheckBox, QHBoxLayout

class CctvSettingEventSelectDialog(QDialog):
    """체크박스가 포함된 리스트 아이템 위젯"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.checkbox = QCheckBox(text)
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setStretch(0, 1)
        
        self.setLayout(layout)