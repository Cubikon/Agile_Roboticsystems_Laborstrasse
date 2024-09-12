from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QComboBox, QSpinBox, \
    QDoubleSpinBox, QDateEdit


class ExperimentPreparationWidget(QWidget):
    def __init__(self, vorbereitungStackedTab, parent=None):
        super().__init__(parent)
        self.vorbereitungStackedTab = vorbereitungStackedTab

        # Make sure the QStackedWidget has an expanding size policy
        self.vorbereitungStackedTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add the QStackedWidget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.vorbereitungStackedTab)

        self.setLayout(layout)

        for index in range(vorbereitungStackedTab.count()):
            widget = vorbereitungStackedTab.widget(index)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            if isinstance(widget, QWidget):
                widget.update()
        vorbereitungStackedTab.update()

    def addToMainWindow(self, main_window):
        if main_window and main_window.tab_widget_home_dashboard:
            main_window.tab_widget_home_dashboard.addTab(self, "Vorbereitung")
            vorbereitung_index = main_window.tab_widget_home_dashboard.indexOf(self)
            main_window.tab_widget_home_dashboard.setCurrentIndex(vorbereitung_index)

    def reset_input_of_past_experiments(self):
        for index in range(self.vorbereitungStackedTab.count()):
            widget = self.vorbereitungStackedTab.widget(index)

            # Reset all QLineEdit widgets to an empty string
            for line_edit in widget.findChildren(QLineEdit):
                line_edit.clear()

            # Reset all QTextEdit widgets to an empty string
            for text_edit in widget.findChildren(QTextEdit):
                text_edit.clear()

            # Reset all QComboBox widgets to the first index
            for combo_box in widget.findChildren(QComboBox):
                combo_box.setCurrentIndex(0)

            # Reset all QSpinBox and QDoubleSpinBox widgets to their minimum value
            for spin_box in widget.findChildren(QSpinBox):
                spin_box.setValue(spin_box.minimum())
            for double_spin_box in widget.findChildren(QDoubleSpinBox):
                double_spin_box.setValue(double_spin_box.minimum())

            # Reset all QDateEdit widgets to their default date, if one is specified
            for date_edit in widget.findChildren(QDateEdit):
                date_edit.setDate(date_edit.minimumDate())

        self.vorbereitungStackedTab.setCurrentIndex(0)
