class LeftNavigation:
    """
    Left Navigation Buttons
    """
    def __init__(self, ui):
        self.ui = ui

    def map_buttons_to_pages(self):
        # Connect all the buttons to its respective button
        # self.ui.homeBtn.clicked.connect(
        #     lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.home_btn_dashboard.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.test_page_home)))
        self.ui.statistik.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.importPage)))
        self.ui.qrGenBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))
        self.ui.cliBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.cliPage)))
        self.ui.experimentPreparationBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(
            self.ui.stackedWidget.indexOf(self.ui.experimentPreparationPage)))
        self.ui.experiment_info_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.experiment_info_view)))

