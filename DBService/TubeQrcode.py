class TubeQrcode:
    def __init__(self, qr_code, datum ):
        self.qr_code = qr_code  # QR-Code
        self.datum = datum      # Datum der Erstellung
     

    def __str__(self):
        return f"QR-Code: {self.qr_code}, Datum: {self.datum}"