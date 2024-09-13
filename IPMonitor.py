import sys
import psutil
import requests
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QAction, QPainter, QColor, QBrush, QFont
from PySide6.QtCore import QTimer, QSize, Qt, QRect


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About IP Monitor")

        # Create layout
        layout = QVBoxLayout()
        
        # Add network icon with a QLabel
        icon_label = QLabel()
        icon_pixmap = QIcon.fromTheme("network-wired").pixmap(QSize(64, 64))
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        # Add other text labels
        layout.addWidget(QLabel("IP Monitor v1.0"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("by Ryon Shane Hall"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("endorpheus@gmail.com"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Created: 202409131224"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Modified: 202409131509"), alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Set window icon
        self.setWindowIcon(QIcon.fromTheme("network-wired"))
        
        # Adjust the size of the dialog based on content
        self.adjustSize()

        # Center the dialog on the screen
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(int((screen.width() - self.width()) / 2), int((screen.height() - self.height()) / 2))


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QRect

class IPDisplayWindow(QWidget):
    def __init__(self, internal_ips, external_ip, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Frameless and always on top
        self.setAttribute(Qt.WA_TranslucentBackground)  # Opaque background
        
        # Set window size to auto-fit the content
        self.adjustSize()

        # Set up layout and add the IPs
        self.layout = QVBoxLayout(self)

        # Set text style (18pt bold)
        self.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: white;
            }
        """)

        # Add internal IPs
        self.layout.addWidget(QLabel("Internal IPs:"))
        for ip in internal_ips:
            self.layout.addWidget(QLabel(ip))
        
        # Add external IP
        self.layout.addWidget(QLabel(f"External IP:\n {external_ip}"))
        
        # Add a close button
        close_button = QPushButton("X", self)
        close_button.clicked.connect(self.handle_close)  # Connect to custom close method
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.layout.addWidget(close_button, alignment=Qt.AlignRight)
    
    def paintEvent(self, event):
        """ Paint the background with rounded corners and 85% opacity. """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rounded_rect = QRect(0, 0, self.width(), self.height())
        
        # 85% opacity background color (RGBA) Purple-ish
        painter.setBrush(QBrush(QColor(26, 9, 32, 216)))  # 85% opacity (216/255)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rounded_rect, 20, 20)  # Rounded corners (20px radius)
    
    def handle_close(self):
        self.hide()  # Hide the widget instead of closing



class IPMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.tray_icon = QSystemTrayIcon(QIcon.fromTheme("network-wired"), self)
        self.tray_icon.setToolTip("IP Monitor")

        # Handle left-click activation
        self.tray_icon.activated.connect(self.on_tray_icon_click)
        
        self.menu = QMenu()
        self.internal_ip_menu = QMenu("Internal IPs")
        self.menu.addMenu(self.internal_ip_menu)
        
        self.external_ip_action = QAction("External IP: Loading...", self)
        self.external_ip_action.triggered.connect(lambda: self.copy_to_clipboard(self.external_ip))
        self.menu.addAction(self.external_ip_action)
        
        self.menu.addSeparator()
        
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.about_action)
        
        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(self.quit_action)
        
        self.tray_icon.setContextMenu(self.menu)
        
        self.about_dialog = AboutDialog(self)
        
        self.internal_ips = []
        self.external_ip = ""
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ips)
        self.timer.start(300000)  # Update every 5 minutes
        
        self.update_ips()
        self.tray_icon.show()

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left-click (Trigger)
            self.show_ip_window()

    def show_ip_window(self):
        """ Show the frameless IP display window. """
        if not hasattr(self, 'ip_window') or not self.ip_window.isVisible():
            self.ip_window = IPDisplayWindow(self.internal_ips, self.external_ip)
        self.ip_window.show()

    def update_ips(self):
        # Get internal IPs
        self.internal_ips = [addr.address for iface, addrs in psutil.net_if_addrs().items()
                             for addr in addrs if addr.family == 2 and not addr.address.startswith("127.")]
        
        # Update internal IP menu items
        self.internal_ip_menu.clear()
        for ip in self.internal_ips:
            action = QAction(ip, self)
            action.triggered.connect(lambda checked, ip=ip: self.copy_to_clipboard(ip))
            self.internal_ip_menu.addAction(action)
        
        # Get external IP using ifconfig.me
        try:
            self.external_ip = requests.get('http://ifconfig.me/ip', timeout=5).text.strip()
        except:
            self.external_ip = "Unable to fetch"
        
        self.external_ip_action.setText(f"External IP: {self.external_ip}")
        
    def show_about(self):
        self.about_dialog.exec()
        
    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ip_monitor = IPMonitor()
    sys.exit(app.exec())
