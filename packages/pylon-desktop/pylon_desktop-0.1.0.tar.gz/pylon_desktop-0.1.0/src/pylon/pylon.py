import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QDir

def resource_path(relative_path):
    """ 리소스의 절대 경로를 가져오는 함수 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySide6 WebView Demo')
        self.setGeometry(100, 100, 1200, 800)

        # 아이콘 설정
        icon_path = 'assets/icon.ico'
        self.setWindowIcon(QIcon(icon_path))



        # Windows 작업 표시줄 아이콘 설정
        if sys.platform == 'win32':
            import ctypes
            myappid = 'mycompany.myproduct.subproduct.version'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # 타이틀바와 테두리를 제거 (필요하다면 사용)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # QWebEngineView 인스턴스 생성
        self.web_view = QWebEngineView()

        # 웹 페이지 로드
        self.web_view.setUrl('https://www.example.com')

        # 기본 컨텍스트 메뉴 비활성화
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        # QWebEngineView를 메인 윈도우에 추가
        self.setCentralWidget(self.web_view)

# 애플리케이션 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 현재 작업 디렉토리 출력
    print(f"현재 작업 디렉토리: {QDir.currentPath()}")

    
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
