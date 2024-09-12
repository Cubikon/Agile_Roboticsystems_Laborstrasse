from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView, QHeaderView, QScrollArea, QFileDialog, \
    QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect, QPoint

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton, TubesSingleton


class CustomLiveWidget(QWidget):
    """
    Custom view for the Live View Table. Still on Work.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.experiment_data = ExperimentSingleton()

        scroll = QScrollArea(self)
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)

        self.layout = QVBoxLayout(frame)
        self.design_layout(self.layout, 1)

    def display_tubes_data(self):
        print('-------\n' + str(self.experiment_data))
        self.clear_layout(self.layout)
        if self.experiment_data.plasmid_tubes:
            for tube in self.experiment_data.get_all_tubes():
                print(f"Tube ID: {tube}")
                self.design_layout(self.layout, tube)

    def design_layout(self, layout, tube):
        widget = QWidget()
        widget.setObjectName("itemRowLiveData")
        layout.addWidget(widget)
        h_layout = QHBoxLayout(widget)
        label = QLabel(str(tube))
        h_layout.addWidget(label)
        buttons = [QPushButton(f'{j + 1}') for j in range(3)]
        for button in buttons:
            h_layout.addWidget(button)
            arrow_right_label = QLabel()
            pixmap = QPixmap(":/icons/img/arrow-right.svg")
            scaled_pixmap = pixmap.scaled(150, 20, Qt.AspectRatioMode.KeepAspectRatio)
            arrow_right_label.setPixmap(scaled_pixmap)
            h_layout.addWidget(arrow_right_label)

            arrow_left_label = QLabel()
            pixmap = QPixmap(":/icons/img/arrow-left.svg")
            scaled_pixmap = pixmap.scaled(150, 20, Qt.AspectRatioMode.KeepAspectRatio)
            arrow_left_label.setPixmap(scaled_pixmap)
            h_layout.addWidget(arrow_left_label)

        more_btn = QPushButton(" > ")
        more_btn.setObjectName("more_btn")
        more_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        h_layout.insertStretch(h_layout.indexOf(more_btn), 1)
        h_layout.addWidget(more_btn)

    def clear_layout(self, layout):
        """
        Remove all widgets from the given layout.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class ArrowWidget(QWidget):
    def __init__(self, start_widget, end_widget):
        super().__init__()
        self.start_widget = start_widget
        self.end_widget = end_widget

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.GlobalColor.black, 2)
        qp.setPen(pen)

        start_pos = self.start_widget.pos()
        end_pos = self.end_widget.pos()

        qp.drawLine(
            QPoint(start_pos.x() + self.start_widget.width(), int(start_pos.y() + self.start_widget.height() / 2)),
            QPoint(end_pos.x(), int(end_pos.y() + self.end_widget.height() / 2)))

        qp.end()
