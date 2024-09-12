from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class ArrowOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.table_widget = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        for row in range(self.table_widget.rowCount()):
            start_button = self.table_widget.cellWidget(row, 1)
            middle_button = self.table_widget.cellWidget(row, 2)
            end_button = self.table_widget.cellWidget(row, 3)

            if start_button and middle_button:
                self.draw_arrow(painter, start_button, middle_button)

            if middle_button and end_button:
                self.draw_arrow(painter, middle_button, end_button)

    def draw_arrow(self, painter, start_button, end_button):
        start_rect = start_button.geometry()
        end_rect = end_button.geometry()

        start_pos = start_rect.topRight()
        end_pos = end_rect.topLeft()

        # Convert widget positions to the overlay's coordinate system
        start_pos = self.table_widget.mapToParent(start_pos)
        end_pos = self.table_widget.mapToParent(end_pos)

        start_pos = self.mapFromParent(start_pos)
        end_pos = self.mapFromParent(end_pos)

        painter.drawLine(start_pos, end_pos)
