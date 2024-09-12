from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, \
    QAbstractScrollArea

from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Navigation import Ui_MainWindow


class TableInformationFetchByParameter(QWidget):

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.current_table = QTableWidget()
        self.ui = ui
        self.main_window = main_window
        self.current_table.cellDoubleClicked.connect(self.open_image)
        # combo_option_class_type

    def load_and_display_tube_info(self):
        tubeid_input_text = self.ui.tube_info_tubeid_input.text()
        if tubeid_input_text:
            print(tubeid_input_text)
            self.append_info_to_view(tubeid_input_text, self.ui.combo_option_class_type.currentText())
        else:
            self.main_window.show_message_in_dialog("Please Enter Tube Id to proceed!")

    def open_image(self, row, column):
        # TODO Open image in an image viewer
        item = self.table.item(row, column)
        if item:
            key = item.text()
            if key == 'image_location':
                image_path = self.data_for_table.get('image_location')
                if image_path:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(image_path))

    def append_info_to_view(self, input_id, current_option):
        global text_label_for_option
        data_for_table = None
        is_tube_selected = False
        try:
            if current_option == 'Experiment':
                # Create the left-aligned label
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.get_experiment_by_id(input_id)
                # Convert the Experimente instance to a dictionary
                data_for_table = vars(data_for_table)
            elif current_option == 'Plasmid':
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.metadata_adapter.get_plasmid_data_by_nr(input_id)
            elif current_option == 'Tube':
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.tube_adapter.get_tube_data_by_probe_nr(input_id)

                qr_code_widget = QRCodesWidget(self.main_window)
                pixmap, image_location = qr_code_widget.generate_qr_code(data_for_table['qr_code'])
                data_for_table['pixmap'] = pixmap
                data_for_table['image_location'] = image_location

        except Exception as ex:
            self.main_window.removeDialogBoxContents()
            self.main_window.show_message_in_dialog(ex)

        print(data_for_table)
        text_qlabel_option = QLabel(text_label_for_option)
        text_qlabel_option.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create the right-aligned label
        right_label = QLabel("Details")
        right_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add the labels to the grid layout
        self.ui.tube_info_grid_layout.addWidget(text_qlabel_option, 0, 0)  # Add to row 0, column 0
        self.ui.tube_info_grid_layout.addWidget(right_label, 0, 1)  # Add to row 0, column 1

        if not data_for_table:
            text_qlabel_option.setText(f"Could not load data for {current_option} with id {input_id}")
            pass

        try:
            # Remove the old table from the layout, if it exists
            if hasattr(self, 'current_table') and self.current_table:
                self.ui.tube_info_grid_layout.removeWidget(self.current_table)
                self.current_table.deleteLater()

            # Create the table
            table = QTableWidget()
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            table.setMinimumSize(400, 500)

            # QSS for table
            table.setStyleSheet("""
                QTableWidget {
                    gridline-color: #E0E0E0;
                    background-color: transparent;
                }
                QTableWidget::item {
                    padding: 10px;
                }
                QHeaderView::section {
                    background-color: #F5F5F5;
                    padding: 10px;
                    border: 1px solid #E0E0E0;
                }
            """)
            self.current_table = table

            # Set the number of rows and columns based on the data
            table.setRowCount(len(data_for_table))
            table.setColumnCount(2)

            table.setHorizontalHeaderLabels(['Key Name', 'Value'])
            # Hide the row and column headers
            table.verticalHeader().hide()

            # Populate the table with data
            for i, (key, value) in enumerate(data_for_table.items()):
                key_item = QTableWidgetItem(key)
                key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                self.current_table.setItem(i, 0, key_item)

                if key == 'pixmap':
                    label = QLabel()
                    label.setPixmap(value)
                    self.current_table.setCellWidget(i, 1, label)
                elif key == 'image_location':
                    value_item = QTableWidgetItem(value)
                    value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                    self.current_table.setItem(i, 1, value_item)
                else:
                    value_item = QTableWidgetItem(str(value))
                    value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                    self.current_table.setItem(i, 1, value_item)

            # Remove the background
            table.setObjectName('tube_info_table')

            # Set the size policy to expand to the available space
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Add the table to the grid layout
            self.ui.tube_info_grid_layout.addWidget(table, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        except Exception as ex:
            print(ex)
