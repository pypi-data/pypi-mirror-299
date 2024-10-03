# Correlation analysis
class Correlation:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        corr = self.data.corr()
        return corr
