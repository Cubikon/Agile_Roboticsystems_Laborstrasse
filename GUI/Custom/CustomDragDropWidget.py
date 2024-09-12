from PyQt6.QtWidgets import QWidget
from DBService.DBUIAdapter import DBUIAdapter

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class DragDropWidget(QWidget):
    """
    Drag and Drop Feature, still in Progress.
    """

    def __init__(self, parent=None, db_ui=DBUIAdapter):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.db_ui = db_ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.endswith('.xls') or path.endswith('.xlsx'):
                # TODO provide data to importer
                self.db_ui.insert_metadaten(path)
                print(f'Dropped Excel file: {path}')
            else:
                print(f'Ignored non-Excel file: {path}')
