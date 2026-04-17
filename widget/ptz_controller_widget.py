import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QThread, Signal
from onvif import ONVIFCamera
from zeep.transports import Transport

from ui.ui_ptz_controller_widget import Ui_Widget

class CameraConnectThread(QThread):
    connected = Signal(object)  
    error = Signal(str)         

    def __init__(self, ip, port, user, password):
        super().__init__()
        self.setObjectName("CameraConnectQThread")
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
    def run(self):
        try:
            transport = Transport(operation_timeout=10)
            camera = ONVIFCamera(self.ip, 2020, self.user, self.password, adjust_time=True, no_cache=True, transport=transport)

            # 추가 초기화 작업
            self.connected.emit(camera)
        except Exception as e:
            self.error.emit(str(e))

class PtzControllerWidget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_ptz_buttons_enabled(False)
        
    def setup_ptz_controls(self, ip, port, user, password):
        self.camera_connect_thread = CameraConnectThread(ip, port, user, password)
        self.camera_connect_thread.connected.connect(self.on_camera_connected)
        self.camera_connect_thread.error.connect(self.on_connection_error)
        self.camera_connect_thread.start()


    def on_camera_connected(self, camera):
        try:
            media = camera.create_media_service()
            self.ptz = camera.create_ptz_service()
            self.media_profile = media.GetProfiles()[0]

            ptz_supported = self.is_ptz_supported()
            self.set_ptz_buttons_enabled(ptz_supported)

            if ptz_supported:
                print("PTZ 지원 카메라입니다. 버튼을 활성화합니다.")
                self.connect_ptz_signals()
            else:
                print("PTZ 미지원 카메라입니다. 버튼을 비활성화합니다.")

        except Exception as e:
            print(f"PTZ 초기화 중 오류 발생: {e}")
            self.set_ptz_buttons_enabled(False)

    def on_connection_error(self, error):
        print(f"PTZ 초기화 중 오류 발생: {error}")
        self.set_ptz_buttons_enabled(False)

    def is_ptz_supported(self):
        try:
            ptz_nodes = self.ptz.GetNodes()
            if not ptz_nodes:
                return False

            node = ptz_nodes[0]
            has_ptz_spaces = hasattr(node, 'SupportedPTZSpaces') and node.SupportedPTZSpaces is not None
            return bool(has_ptz_spaces)
        except Exception as e:
            print(f"PTZ 지원 여부 확인 실패: {e}")
            return False

    def set_ptz_buttons_enabled(self, enabled: bool):
        buttons = [
            self.button_up_left, self.button_up, self.button_up_right,
            self.button_left, self.button_right,
            self.button_down_left, self.button_down, self.button_down_right,
            self.button_zoom_in, self.button_zoom_out
        ]

        for btn in buttons:
            btn.setEnabled(enabled)

    def connect_ptz_signals(self):
        ptz_button = {
            self.button_up_left: 'up_left',
            self.button_up: 'up',
            self.button_up_right: 'up_right',
            self.button_left: 'left',
            self.button_right: 'right',
            self.button_down_left: 'down_left',
            self.button_down: 'down',
            self.button_down_right: 'down_right',
            self.button_zoom_in: 'zoom_in',
            self.button_zoom_out: 'zoom_out'
        }

        for button, command in ptz_button.items():
            button.pressed.connect(lambda cmd=command: self.ptz_control(cmd))
            button.released.connect(lambda cmd=command: self.ptz_control('stop'))

        self.button_ptz_reset.clicked.connect(lambda: self.ptz_control('home'))

    def ptz_control(self, command):
        commands = {
        "up_left": {'x': -0.05, 'y': 0.1},
        "up": {'x': 0, 'y': 0.1},
        "up_right": {'x': 0.05, 'y': 0.1},
        "left": {'x': -0.05, 'y': 0},
        "right": {'x': 0.05, 'y': 0},
        "down_left": {'x': -0.05, 'y': -0.1},
        "down": {'x': 0, 'y': -0.1},
        "down_right": {'x': 0.05, 'y': -0.1},
        "zoom_in": {'x': 1},
        "zoom_out": {'x': -1}
        }

        if command == "stop":
            print("Stopping PTZ movement")
            self.ptz.Stop({'ProfileToken': self.media_profile.token})
        elif command in commands:
            print("Moving PTZ", command)
            if "zoom" in command:
                velocity = {'Zoom': commands[command]}
            else:
                velocity = {'PanTilt': commands[command]}

            self.ptz.RelativeMove({
                'ProfileToken': self.media_profile.token,
                'Translation': velocity,
                'Speed': velocity
            })
        elif command == "home":
            self._move_to_home()

    def _move_to_home(self):
        presets = self.ptz.GetPresets({'ProfileToken': self.media_profile.token})
        try:
            if presets:
                preset_token = presets[0].token
                self.ptz.GotoPreset({
                    'ProfileToken': self.media_profile.token,
                    'PresetToken': preset_token
                })
                print(f"Moving to first preset with token: {preset_token}")
            else:
                raise ValueError("No presets found")
        except Exception as e:
            print(f"Preset error: {e} — falling back to default home position")
            self.ptz.GotoHomePosition({'ProfileToken': self.media_profile.token})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PtzControllerWidget()
    widget.setup_ptz_controls("192.168.88.100", "2020", "admin", "tmzkdltltm")
    widget.show()  
    sys.exit(app.exec()) 
