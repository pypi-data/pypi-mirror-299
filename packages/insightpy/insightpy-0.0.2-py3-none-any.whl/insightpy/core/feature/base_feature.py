# Base Feature class
class Feature:
    def __init__(self, name: str, data):
        self.name = name
        self.data = data

    def summary(self):
        """Abstract method for generating a summary of the feature."""
        raise NotImplementedError