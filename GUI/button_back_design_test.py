from PyQt6.QtWidgets import QApplication, QPushButton, QWidget
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QColor, QFontMetrics
from PyQt6.QtCore import Qt, QSize, QRect


class CustomBackButton(QPushButton):
    """
    Creates a Custom Button for Back Button, which would be shown in Title Bar
    """
    def __init__(self, text, icon_pixmap, parent=None):
        super().__init__(text, parent)
        self.hover = False
        self.icon_pixmap = icon_pixmap
        self.setMouseTracking(True)  # Enable mouse hover events

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define the fill color based on hover state
        fill_color = QColor('lightgrey') if self.hover else QColor('#eee')

        # Calculate the triangle size based on the button height
        triangle_height = self.height() // 2
        triangle_base = triangle_height * 2

        # Draw the triangle
        painter.setBrush(fill_color)
        painter.setPen(Qt.PenStyle.NoPen)  # No border for the triangle fill
        triangle_path = QPainterPath()
        triangle_path.moveTo(0, triangle_height)
        triangle_path.lineTo(triangle_height, 0)
        triangle_path.lineTo(triangle_height, triangle_base)
        triangle_path.lineTo(0, triangle_height)
        painter.drawPath(triangle_path)

        # Draw the rectangle
        painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle fill
        painter.drawRect(triangle_height, 0, self.width() - triangle_height, self.height())

        # Draw the border around the button
        border_color = QColor('black')
        painter.setPen(QPen(border_color, 2))  # Set the pen for the border
        border_path = QPainterPath()
        border_path.moveTo(0, triangle_height)
        border_path.lineTo(triangle_height, 0)
        border_path.lineTo(triangle_height, 0)
        border_path.lineTo(self.width(), 0)
        border_path.lineTo(self.width(), self.height())
        border_path.lineTo(triangle_height, self.height())
        border_path.lineTo(0, triangle_height)
        painter.drawPath(border_path)

        # Set the pen for the text color
        text_color = QColor('black') if self.hover else QColor('black')
        painter.setPen(text_color)

        # Calculate the text rectangle
        text_rect = QRect(triangle_height, 0, self.width() - triangle_height, self.height())

        # Draw the text aligned to the center of the text rectangle
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.text())

    def sizeHint(self):
        # Provide a default size hint for the button
        return QSize(80, 50)

    def enterEvent(self, event):
        # Change the hover state and repaint the button when the mouse enters
        self.hover = True
        self.update()

    def leaveEvent(self, event):
        # Change the hover state and repaint the button when the mouse leaves
        self.hover = False
        self.update()
