from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class CustomTitleBar(QWidget):
    """
    Custom Frameless Titlebar
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_logo = None
        self.parent = parent
        self.draggable = True
        self.startPos = None
        self.initUI()
        # Makes the window frameless
        self.parent.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def initUI(self):
        layout = QHBoxLayout(self)
        self.layout_logo = QHBoxLayout(self)


        # App logo
        app_logo = QLabel(self)
        pixmap = QPixmap(":/icons/img/laboratory.svg")
        scaled_pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        app_logo.setPixmap(scaled_pixmap)
        self.layout_logo.addWidget(app_logo)
        self.layout_logo.addStretch(10)
        layout.addLayout(self.layout_logo)

        layout.addStretch(1)
        app_title = QLabel("Dashboard UI")
        layout.addWidget(app_title)
        layout.addStretch(1)

        # Minimize button
        minimize_btn = QPushButton("-")
        minimize_btn.clicked.connect(self.parent.showMinimized)
        minimize_btn.setObjectName("minimizeButton")
        layout.addWidget(minimize_btn)

        # Close button
        close_btn = QPushButton("X")
        close_btn.clicked.connect(self.parent.close)
        close_btn.setObjectName("closeButton")
        layout.addWidget(close_btn)

    def add_back_btn(self, button: QPushButton):
        self.layout_logo.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)
        button.setStyleSheet("margin-left: 10px;")
        button.setObjectName("back_btn")

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition()
            self.clickPos = event.position()
            self.isResizing = self.isInResizeArea(event.position())

    def mouseMoveEvent(self, event):
        if self.isResizing:
            self.resizeWindow(event)
        elif self.draggable and event.buttons() & Qt.MouseButton.LeftButton:
            if self.startPos:
                move = event.globalPosition() - self.startPos
                self.parent.move(self.parent.pos() + move.toPoint())  # Convert move to QPoint
                self.startPos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = None
            self.isResizing = False

    def isInResizeArea(self, pos):
        rect = self.rect()
        cornerSize = 10  # Size of the corner area for resizing
        if pos.x() >= rect.width() - cornerSize and pos.y() >= rect.height() - cornerSize:
            return True
        return False

    def resizeWindow(self, event):
        if self.isResizing:
            mousePos = event.globalPosition().toPoint()
            windowRect = self.parent.frameGeometry()
            newWidth = max(self.parent.minimumWidth(), mousePos.x() - windowRect.left())
            newHeight = max(self.parent.minimumHeight(), mousePos.y() - windowRect.top())
            self.parent.resize(newWidth, newHeight)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.parent.isMaximized():
                self.parent.showNormal()  # Restores the window if it's maximized
            else:
                self.parent.showMaximized()  # Maximizes the window

    def setDraggable(self, draggable):
        self.draggable = draggable
