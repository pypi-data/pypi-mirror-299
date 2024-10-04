import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QSystemTrayIcon,
    QMenu,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtCore import Qt, Signal, QUrl, QObject
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWebEngineCore import QWebEnginePage
from .utils import get_resource_path, is_production
from .api import PylonAPI, Bridge
import uuid


class WindowAPI(PylonAPI):
    def __init__(self, window_id, app):
        super().__init__()
        self.window_id = window_id
        self.app = app

    @Bridge(result=str)
    def getWindowId(self):
        return self.window_id

    @Bridge()
    def closeWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.close()

    @Bridge()
    def hideWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.hide()

    @Bridge()
    def showWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.show()

    @Bridge()
    def toggleFullscreen(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.toggle_fullscreen()

    @Bridge()
    def minimizeWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.minimize_window()

    @Bridge()
    def maximizeWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.maximize_window()

    @Bridge()
    def restoreWindow(self):
        window = self.app.get_window_by_id(self.window_id)
        if window:
            window.restore_window()


class _BrowserWindow:
    def __init__(
        self,
        app,
        title,
        url,
        frame,
        context_menu,
        js_apis=[],
        enable_dev_tools=False,
        width=1200,
        height=800,
        x=100,
        y=100,
    ):
        self.id = str(uuid.uuid4())  # 고유 ID 생성
        self.app = app  # PylonApp 인스턴스 저장
        self.js_apis = [WindowAPI(self.id, self.app)]

        self._window = QMainWindow()
        self._window.closeEvent = self.closeEvent  # closeEvent 메서드 오버라이드
        self._window.setWindowTitle(title)
        self._window.setGeometry(x, y, width, height)

        self.web_view = QWebEngineView()
        self.title = title
        self.url = url
        self.frame = frame
        self.context_menu = context_menu
        self.enable_dev_tools = enable_dev_tools
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        # 아이콘 설정
        self._window.setWindowIcon(self.app.icon)

        # Windows 작업 표시줄 아이콘 설정
        if sys.platform == "win32":
            import ctypes

            myappid = "mycompany.myproduct.subproduct.version"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # 타이틀바와 테두리를 제거 (필요하다면 사용)
        if not frame:
            self._window.setWindowFlags(Qt.FramelessWindowHint)

        # 기본 컨텍스트 메뉴 비활성화
        if not context_menu:
            self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        # QWebChannel 설정
        self.channel = QWebChannel()
        for js_api in js_apis:
            self.js_apis.append(js_api)

        # 추가 JS API 등록
        if self.js_apis:
            for js_api in self.js_apis:
                self.channel.registerObject(js_api.__class__.__name__, js_api)

        self.web_view.page().setWebChannel(self.channel)

        # 웹 페이지 로드
        # URL이 로컬 HTML 파일인지 확인
        if url.startswith("file://") or os.path.isfile(url):
            self.load_html_file(url)
        else:
            self.web_view.setUrl(url)

        # pylonjs 브릿지 연결
        self.web_view.loadFinished.connect(self._on_load_finished)

        # QWebEngineView를 메인 윈도우에 추가
        self._window.setCentralWidget(self.web_view)

        # F12 단축키 설정
        if enable_dev_tools:
            self.dev_tools_shortcut = QShortcut(QKeySequence("F12"), self._window)
            self.dev_tools_shortcut.activated.connect(self.open_dev_window)

    def load_html_file(self, file_path):
        if file_path.startswith("file://"):
            file_path = file_path[7:]  # 'file://' 제거

        url = QUrl.fromLocalFile(file_path)

        self.web_view.setUrl(url)

    def _on_load_finished(self, ok):
        if ok and self.js_apis:
            js_code = """
            if (typeof QWebChannel !== 'undefined') {
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.pylon = {};
                    %s
                });
            } else {
                console.error('QWebChannel이 정의되지 않았습니다.');
            }
            """
            js_api_init = "\n".join(
                [
                    f"window.pylon['{js_api.__class__.__name__}'] = channel.objects['{js_api.__class__.__name__}'];\n"
                    f"console.log('pylon.{js_api.__class__.__name__} 객체가 초기화되었습니다:', window.pylon['{js_api.__class__.__name__}']);"
                    for js_api in self.js_apis
                ]
            )
            self.web_view.page().runJavaScript(js_code % js_api_init)
        else:
            pass

    def open_dev_window(self):
        self.web_view.page().setDevToolsPage(QWebEnginePage(self.web_view.page()))
        self.dev_tools_window = QMainWindow(self._window)
        dev_tools_view = QWebEngineView(self.dev_tools_window)
        dev_tools_view.setPage(self.web_view.page().devToolsPage())
        self.dev_tools_window.setCentralWidget(dev_tools_view)
        self.dev_tools_window.resize(800, 600)
        self.dev_tools_window.show()

    def get_window_properties(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "frame": self.frame,
            "context_menu": self.context_menu,
            "enable_dev_tools": self.enable_dev_tools,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
        }

    def closeEvent(self, event):
        # 여기에 창이 닫힐 때 수행할 작업을 추가하세요
        self._remove_from_app_windows()
        event.accept()  # 이벤트 수락 (창 닫기 허용)

    def _remove_from_app_windows(self):
        if self in self.app.windows:
            self.app.windows.remove(self)
        if not self.app.windows:
            self.app.quit()  # 모든 창이 닫히면 앱을 종료합니다.

    ###########################################################################################
    # 윈도우 에서의 관리 (id 필요 없음)
    ###########################################################################################
    def hide_window(self):
        self._window.hide()

    def show_window(self):
        self._window.show()

    def close_window(self):
        self._window.close()

    def toggle_fullscreen(self):
        if self._window.isFullScreen():
            self._window.showNormal()
        else:
            self._window.showFullScreen()

    def minimize_window(self):
        self._window.showMinimized()

    def maximize_window(self):
        self._window.showMaximized()

    def restore_window(self):
        self._window.showNormal()


class _WindowController(QObject):
    hide_window_signal = Signal(str)
    show_window_signal = Signal(str)
    close_window_signal = Signal(str)
    stop_app_signal = Signal()
    create_window_signal = Signal(
        QApplication, str, str, bool, bool, list, bool, int, int, int, int
    )


class PylonApp(QApplication):
    def __init__(self, single_instance=True, icon_path=""):
        super().__init__(sys.argv)
        self.windows = []
        self.server = None

        self.single_instance = single_instance
        if self.single_instance:
            self._init_single_instance()

        self.controller = _WindowController()
        self.controller.create_window_signal.connect(self._create_window_function)
        # self.controller.hide_window_signal.connect(self._hide_window)
        # self.controller.show_window_signal.connect(self._show_window)
        # self.controller.close_window_signal.connect(self._close_window_by_id)
        # self.controller.stop_app_signal.connect(self.quit)

        self.tray_icon_path = None
        self.tray_icon = None
        self.tray_menu_items = []
        self.icon_path = icon_path
        self.icon = self.load_icon(icon_path)
        self.tray_icon_actions = {}  # 트레이 아이콘 활성화 동작을 저장할 딕셔너리

    def load_icon(self, icon_path: str):
        if is_production():
            icon_path = get_resource_path(icon_path)
        return QIcon(icon_path)

    def set_tray_icon_path(self, tray_icon_path: str):
        self.tray_icon_path = tray_icon_path
        self.tray_icon = self.load_icon(tray_icon_path)

    def set_tray_menu_items(self, tray_menu_items):
        self.tray_menu_items = tray_menu_items

    def create_window(
        self,
        url: str,
        title: str = "pylon",
        frame: bool = True,
        context_menu: bool = False,
        js_apis=[],
        enable_dev_tools=False,
        width=1200,
        height=800,
        x=300,
        y=300,
    ) -> _BrowserWindow:
        # URL이 로컬 파일 경로이고 .html로 끝나는 경우 'file://' 접두사 추가
        if os.path.isfile(url) and url.lower().endswith(".html"):
            url = f"file://{os.path.abspath(url)}"

        if is_production():
            url = f"file://{get_resource_path(url)}"

        self.controller.create_window_signal.emit(
            self,
            title,
            url,
            frame,
            context_menu,
            js_apis,
            enable_dev_tools,
            width,
            height,
            x,
            y,
        )
        return self.windows[-1]

    def _create_window_function(
        self,
        app,
        title: str,
        url: str,
        frame: bool,
        context_menu: bool,
        js_apis=[],
        enable_dev_tools=True,
        width=1200,
        height=800,
        x=100,
        y=100,
    ) -> _BrowserWindow:
        window = _BrowserWindow(
            app,
            title,
            url,
            frame,
            context_menu,
            js_apis,
            enable_dev_tools,
            width,
            height,
            x,
            y,
        )
        self.windows.append(window)
        window._window.show()
        if not self.windows:  # 첫 번째 창인 경우
            self.tray_icon.activated.connect(self.tray_icon_activated)
        return window

    def run(self):
        sys.exit(self.exec())

    def _init_single_instance(self):
        socket = QLocalSocket()
        socket.connectToServer("PylonBrowserApp")
        if socket.waitForConnected(500):
            # 이미 실행 중인 인스턴스가 있음
            sys.exit(1)

        # 새로운 서버 생성
        self.server = QLocalServer()
        self.server.listen("PylonBrowserApp")
        self.server.newConnection.connect(self._handle_new_connection)

    def _handle_new_connection(self):
        pass

    ###########################################################################################
    # 앱에서의 윈도우 관리 (id 필요)
    ###########################################################################################
    def get_windows(self) -> list[_BrowserWindow]:
        return self.windows

    def get_window_by_id(self, window_id: str) -> _BrowserWindow:
        for window in self.windows:
            if window.id == window_id:
                return window
        return None

    def hide_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.hide()

    def show_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.show()

    def close_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.close()

    def toggle_fullscreen(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            if window._window.isFullScreen():
                window._window.showNormal()
            else:
                window._window.showFullScreen()

    def minimize_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.showMinimized()

    def maximize_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.showMaximized()

    def restore_window(self, window_id: str):
        window = self.get_window_by_id(window_id)
        if window:
            window._window.showNormal()

    ###########################################################################################
    # 트레이
    ###########################################################################################
    def setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        if (
            self.tray_icon_path is None
        ):  # 트레이 아이콘이 아직 설정되지 않은 경우에 기본 아이콘으로 설정
            self.tray.setIcon(self.icon)
        else:
            self.tray.setIcon(self.tray_icon)

        tray_menu = QMenu()

        # 외부에서 전달받은 메뉴 항목 추가
        if self.tray_menu_items:
            for item in self.tray_menu_items:
                action = tray_menu.addAction(item["label"])
                action.triggered.connect(item["callback"])

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self.tray_activated)
        self.tray.show()

    def tray_activated(self, reason):
        reason_enum = QSystemTrayIcon.ActivationReason(reason)

        if self.tray_actions:
            self.tray_actions.get(reason_enum)()

    def set_tray_actions(self, actions):
        """
        트레이 아이콘 활성화 동작을 설정합니다.

        actions: 딕셔너리 형태로, 키는 QSystemTrayIcon.ActivationReason 열거형 값이고,
                 값은 해당 활성화 이유에 대한 콜백 함수입니다.
        """
        self.tray_actions = actions


# class PylonApp:
#     def __init__(self, single_instance=True, icon_path=""):
#         self._app = _PylonApp(single_instance, icon_path)

#     def create_window(self, *args, **kwargs):
#         return self._app.create_window(*args, **kwargs)

#     def run(self):
#         self._app.run()

#     def get_windows(self):
#         return self._app.get_windows()

#     def get_window_by_id(self, window_id):
#         return self._app.get_window_by_id(window_id)

#     def show_main_window(self):
#         self._app.show_main_window()

#     def toggle_main_window(self):
#         self._app.toggle_main_window()


# 애플리케이션 실행
if __name__ == "__main__":
    app = PylonApp(icon_path="assets/icon.ico")

    window = app.create_window(
        title="Pylon Browser",
        url="https://www.example.com",
        frame=True,
        context_menu=True,
        enable_dev_tools=True,
        width=1200,
        height=800,
        x=100,
        y=100,
    )

    window.show()
    # 이벤트 루프 시작
    app.run()

    print("애플리케이션이 종료되었습니다.")
