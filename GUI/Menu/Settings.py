from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtCore import QSize

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class Settings:
    """
    Settings for changing user interface. Still on Progress.
    """
    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window
        self.original_sizes = {}

        self.ui.windowResizeSlider.valueChanged.connect(self.resize_window)

    def store_original_sizes(self):
        child_widgets = self.ui.leftNavigation.findChildren(QWidget)
        for widget in child_widgets:
            self.original_sizes[widget] = widget.size()

    def resize_child_sizes(self, value):
        child_widgets = self.ui.leftNavigation.findChildren(QWidget)
        for widget in child_widgets:
            if not isinstance(widget, (QHBoxLayout, QVBoxLayout, QGridLayout)):
                original_size = self.original_sizes.get(widget, QSize(100, 100))
                scale_factor = 1 + value / 100
                new_width = original_size.width() * scale_factor
                new_height = original_size.height() * scale_factor

                widget.setMinimumSize(new_width, new_height)
                widget.setMaximumSize(new_width * 1.1, new_height * 1.1)

    def resize_window(self, value):
        self.store_original_sizes()
        new_width = 800 + value * 10
        new_height = 600 + value * 10
        self.main_window.resize(QSize(new_width, new_height))
        self.resize_child_sizes(value)
