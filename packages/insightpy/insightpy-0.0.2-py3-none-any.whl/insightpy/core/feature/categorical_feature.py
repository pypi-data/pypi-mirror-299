from insightpy.core.feature.base_feature import Feature


class CategoricalFeature(Feature):
    def summary(self):
        return {
            "categories": self.data.unique(),
            "missing_values": self.data.isnull().sum(),
            "frequency": self.data.value_counts()
        }
