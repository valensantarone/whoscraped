class CantGetMatchData(Exception):
    def __init__(self):
        self.message = f"WhoScored doesn't have enough data for the requested match.\nWhoScored no tiene suficiente inforamción para el partido solicitado."
        super().__init__(self.message)