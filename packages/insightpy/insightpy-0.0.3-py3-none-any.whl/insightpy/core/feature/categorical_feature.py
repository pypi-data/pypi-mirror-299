from insightpy.core.feature.base_feature import Feature
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import chi2_contingency, f_oneway
import pandas as pd
class CategoricalFeature(Feature):
    def summary(self,target):
        return {
            "categories": self.data.unique(),
            "missing_values": self.data.isnull().sum(),
            "frequency": self.data.value_counts()
        }



    def handle_categorical2(self,target:Feature):
        """Handle a categorical feature using ANOVA and Chi-Square."""

        # Apply One-Hot Encoding for categorical features
        encoder = OneHotEncoder(sparse_output=False)#, drop='first')
        encoded_feature = encoder.fit_transform(self.data.values.reshape(-1, 1))

        # Chi-Square Test
        contingency_table = pd.crosstab(self.data, target.data)
        chi2, p_chi, _, _ = chi2_contingency(contingency_table)

        # ANOVA for significance testing
        f_stat, p_anova = f_oneway(*[target.data[self.data == level] for level in self.data.unique()])

        return {'encoded': encoded_feature, 'chi2_p_value': p_chi, 'anova_p_value': p_anova}

    def handle_categorical(self, target):
        """Handle a categorical feature based on cardinality and importance."""
        # Check cardinality
        cardinality = self.data.nunique()

        if cardinality > 100:  # High cardinality
            print("High cardinality detected. Recommending target encoding.")
            # You would implement target encoding here.
        elif cardinality < 10:  # Low cardinality
            print("Low cardinality detected. Recommending one-hot encoding.")
            # encoder = OneHotEncoder(sparse=False, drop='first')
            # encoded_feature = encoder.fit_transform(self.data.values.reshape(-1, 1))
        else:
            print("Medium cardinality detected. Recommending frequency encoding.")

        # Chi-Square test for significance (for classification)
        contingency_table = pd.crosstab(self.data, target)
        chi2, p, dof, ex = chi2_contingency(contingency_table)
        if p < 0.05:
            print(f"Feature {self.data.name} is significant for the target.")
        else:
            print(f"Feature {self.data.name} is not significant for the target.")

        # return encoded_feature

    def recommendation(self, target):
        pass