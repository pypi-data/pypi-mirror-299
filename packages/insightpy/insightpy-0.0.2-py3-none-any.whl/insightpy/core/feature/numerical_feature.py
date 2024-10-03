from insightpy.core.feature.base_feature import Feature


class NumericalFeature(Feature):
    def summary(self):
        return {
            "mean": self.data.mean(),
            "std": self.data.std(),
            "min": self.data.min(),
            "max": self.data.max()
        }

    def detect_outliers(self, method='IQR'):
        """Stateless function that detects outliers in the feature data."""
        if method == 'IQR':
            q1 = self.data.quantile(0.25)
            q3 = self.data.quantile(0.75)
            iqr = q3 - q1
            return self.data[(self.data < (q1 - 1.5 * iqr)) | (self.data > (q3 + 1.5 * iqr))]