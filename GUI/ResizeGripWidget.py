from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPolygon
from PyQt6.QtWidgets import QWidget

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class ResizeGripWidget(QWidget):
    """
    Resize the Main Window by draging the Traingle on Buttom Right Corner.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.draggable = None
        self.clickPosition = None
        self.parent = parent
        self.setCursor(Qt.CursorShape.SizeFDiagCursor)  # Diagonal resize cursor
        self.setToolTip("Drag to resize")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        points = QPolygon([
            QPoint(self.width() - 16, self.height() - 16),
            QPoint(self.width() - 1, self.height() - 16),
            QPoint(self.width() - 16, self.height() - 1)
        ])

        # Draw the triangle
        painter.drawPolygon(points)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clickPosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.parent:
            # Calculate the new size
            currentPos = event.globalPosition().toPoint()
            diff = currentPos - self.clickPosition
            newWidth = self.parent.width() + diff.x()
            newHeight = self.parent.height() + diff.y()

            # Update the main window size
            self.parent.resize(newWidth, newHeight)

            # Update click position
            self.clickPosition = currentPos

            # Reposition the triangle
            if self.parent.isMaximized():
                self.setGeometry(self.parent.width() - 16, self.parent.height() - 16, 16, 16)
            else:
                self.setGeometry(newWidth - 16, newHeight - 16, 16, 16)

    def setDraggable(self, draggable):
        self.draggable = draggable
