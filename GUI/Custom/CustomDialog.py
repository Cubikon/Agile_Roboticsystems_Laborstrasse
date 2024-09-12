from enum import Enum
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea, QWidget, QHBoxLayout, \
    QLineEdit
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
import GUI.resource
from PyQt6 import sip

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class CustomTitleBarForDialogBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        # self.titleLabel = QLabel("")
        # self.layout.addWidget(self.titleLabel)
        self.layout.addStretch()
        self._dragging = False
        # Custom Styles
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #808080;  # Gray background
                color: white;  # White text
                font-size: 14px;  # Adjust font size as needed
                font-weight: bold;  # Bold font
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()


class ContentType(Enum):
    INPUT = 1,
    OUTPUT = 2


class CustomDialog(QDialog):
    """
    Main Dialog Box to show any Error or Message
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, parent=None, max_percentage=0.75):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.setMinimumWidth(600)
        self.scroll_area = None
        self.layout = None
        self.titleBar = None
        self.row_widgets = None
        self.max_percentage = max_percentage
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QDialog {
                border: 1px solid #5B5B5B;
                background-color: #FFFFFF;
            }
        """)
        self.row_widgets = []
        # Custom Title Bar
        self.titleBar = CustomTitleBarForDialogBox(self)
        self.layout.addWidget(self.titleBar)

        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Close Button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.hide)
        self.layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Update the size of the dialog dynamically
        self.update_size()

        self.lineEditTextChanged = ""

    def clear(self):
        for row_widget in self.row_widgets:
            for child in row_widget.children():
                if isinstance(child, QLineEdit) and child is self.input_line_edit:
                    continue

            self.scroll_area_layout.removeWidget(row_widget)
            row_widget.deleteLater()

    def removeItems(self, row_data):
        """
        Remove contents of the Dialog Box
        """
        for row_widget in row_data:
            # Check if the widget is valid and not deleted
            if row_widget is not None and not sip.isdeleted(row_widget):
                # Safely remove the widget from the layout
                self.scroll_area_layout.removeWidget(row_widget)
                # Delete the widget
                row_widget.deleteLater()

                # Remove the widget from the row_widgets list if it's there
                if row_widget in self.row_widgets:
                    self.row_widgets.remove(row_widget)

    def addContent(self, content, content_type=ContentType):
        row_widget = QWidget()
        row_box = QHBoxLayout()
        if content_type == ContentType.OUTPUT:
            label = QLabel(content)
            label.setWordWrap(True)
            row_box.addWidget(label)

            # Create and configure the copy button
            copy_button = QPushButton("")
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/img/contentcopy.svg"), QIcon.Mode.Normal, QIcon.State.Off)
            copy_button.setIcon(icon1)
            copy_button.clicked.connect(lambda: QApplication.clipboard().setText(content))
            copy_button.setFixedHeight(30)
            copy_button.setFixedWidth(30)
            # Add the copy button to the horizontal layout
            row_box.addWidget(copy_button)

        elif content_type == ContentType.INPUT:
            label = QLabel(content, self)
            row_box.addWidget(label)
            input_line_edit = QLineEdit(self)
            input_line_edit.textChanged.connect(self.emitTextChanged)
            row_box.addWidget(input_line_edit)
            send_button = QPushButton("Send")
            send_button.clicked.connect(lambda: self.sendButtonClicked.emit(input_line_edit.text()))
            row_box.addWidget(send_button)

        # Set the layout for the row widget
        row_widget.setLayout(row_box)

        # Add the row widget to the scroll area's layout
        self.scroll_area_layout.addWidget(row_widget)
        self.row_widgets.append(row_widget)
        return row_widget

    def emitTextChanged(self, text):
        self.lineEditTextChanged = text

    def update_size(self):
        self.setFixedWidth(int(self.parent().width() * 0.8))
        self.setMaximumHeight(int(self.parent().height() * 0.8))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = QDialog()
    main_window.resize(800, 600)

    dialog = CustomDialog(main_window)
    dialog.show()

    sys.exit(app.exec())
