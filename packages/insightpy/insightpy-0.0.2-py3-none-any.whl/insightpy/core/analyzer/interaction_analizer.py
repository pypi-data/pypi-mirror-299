
# Interaction Analyzer class
class InteractionAnalyzer:
    @staticmethod
    def correlation(feature1, feature2):
        """Stateless function to calculate correlation between two numerical features."""
        return feature1.data.corr(feature2.data)