import io
import base64
import numpy as np
import matplotlib.pyplot as plt

class WaterQualityEvaluator:
    """
    Evaluates water quality based on various parameters using linear and
    piecewise linear methods. Calculates an overall water quality score
    and generates a detailed report.
    """

    def __init__(self, weights=None, quality_ratings=None):
        """
        Initializes the WaterQualityEvaluator with optional custom weights and
        quality ratings.
        """
        self.default_weights = {
            "Temperature": 0.04,
            "pH": 0.10,
            "Turbidity": 0.09,
            "Dissolved Oxygen": 0.10,
            "Conductivity": 0.06,
            "Total Dissolved Solids": 0.06,
            "Nitrate": 0.08,
            "Phosphate": 0.09,
            "Total Coliforms": 0.08,
            "E. coli": 0.08,
            "BOD": 0.05,
            "COD": 0.05,
            "Hardness": 0.05,
            "Alkalinity": 0.04,
            "Iron": 0.03
        }

        # Adjusted quality ratings for better logic
        self.default_quality_ratings = {
            "Temperature": {"ideal": 20, "good_low": 15, "good_high": 20, "poor_low": 20, "poor_high": 25, "unit": "°C"},
            "pH": {"ideal": 7.0, "good_low": 6.5, "good_high": 8.5, "poor_low": 8.5, "poor_high": 9.0, "unit": ""},
            "Turbidity": {"ideal": 0, "good_low": 0, "good_high": 1, "poor_low": 1, "poor_high": 5, "unit": "NTU"},
            "Dissolved Oxygen": {"ideal": 8, "good_low": 6, "good_high": 12, "poor_low": 5, "poor_high": 6, "unit": "mg/L"},
            "Conductivity": {"ideal": 200, "good_low": 50, "good_high": 1000, "poor_low": 1000, "poor_high": 2500, "unit": "µS/cm"},
            "Total Dissolved Solids": {"ideal": 250, "good_low": 30, "good_high": 500, "poor_low": 500, "poor_high": 1000, "unit": "mg/L"},
            "Nitrate": {"ideal": 2, "good_low": 0, "good_high": 5, "poor_low": 5, "poor_high": 10, "unit": "mg/L"},
            "Phosphate": {"ideal": 0.05, "good_low": 0, "good_high": 0.1, "poor_low": 0.1, "poor_high": 0.5, "unit": "mg/L"},
            "Total Coliforms": {"ideal": 0, "good_low": 0, "good_high": 0, "poor_low": 0, "poor_high": 10, "unit": "CFU/100mL"},
            "E. coli": {"ideal": 0, "good_low": 0, "good_high": 0, "poor_low": 0, "poor_high": 1, "unit": "CFU/100mL"},
            "BOD": {"ideal": 1, "good_low": 0, "good_high": 2, "poor_low": 2, "poor_high": 5, "unit": "mg/L"},
            "COD": {"ideal": 10, "good_low": 0, "good_high": 20, "poor_low": 20, "poor_high": 50, "unit": "mg/L"},
            "Hardness": {"ideal": 150, "good_low": 60, "good_high": 300, "poor_low": 300, "poor_high": 500, "unit": "mg/L"},
            "Alkalinity": {"ideal": 100, "good_low": 20, "good_high": 200, "poor_low": 200, "poor_high": 300, "unit": "mg/L"},
            "Iron": {"ideal": 0.1, "good_low": 0, "good_high": 0.3, "poor_low": 0.3, "poor_high": 0.5, "unit": "mg/L"},
        }
        self.weights = weights if weights is not None else self.default_weights
        self.quality_ratings = quality_ratings if quality_ratings is not None else self.default_quality_ratings

        if abs(sum(self.weights.values()) - 1) > 1e-6:
            raise ValueError("The sum of the weights should be equal to 1")

    def calculate_quality_rating(self, parameter, value):
        """
        Calculates the quality rating (Qi) for a parameter.
        """
        rating = self.quality_ratings[parameter]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"], rating["poor_low"], rating["poor_high"]
        )

        if parameter in ["Turbidity", "Total Coliforms", "E. coli", "BOD", "COD", "Iron", "Phosphate", "Nitrate", "Conductivity", "Total Dissolved Solids"]:
            # Lower is better
            if value <= ideal:
                qi = 100
            elif ideal < value <= good_high:
                qi = 100 - (value - ideal) / (good_high - ideal) * 50
            elif good_high < value <= poor_high:
                qi = 50 - (value - good_high) / (poor_high - good_high) * 50
            else:
                qi = 0 # Value outside the defined range
        elif parameter in ["pH", "Dissolved Oxygen", "Temperature", "Hardness", "Alkalinity"]:
            # Range is best
            if good_low <= value <= good_high:
                if value <= ideal:
                    qi = 50 + (value - good_low) / (ideal - good_low if ideal > good_low else 1) * 50
                else:
                    qi = 50 + (good_high - value) / (good_high - ideal if good_high > ideal else 1) * 50
            elif poor_low <= value < good_low:
                qi = (value - poor_low) / (good_low - poor_low if good_low > poor_low else 1) * 50
            elif good_high < value <= poor_high:
                qi = (poor_high - value) / (poor_high - good_high if poor_high > good_high else 1) * 50
            else:
                qi = 0 # Value outside the defined range
        else:
            return 0  # Unknown parameter

        return max(0, min(qi, 100))

    def _calculate_quality_rating_temperature(self, value):
        return self.calculate_quality_rating("Temperature", value)

    def _calculate_quality_rating_turbidity(self, value):
        return self.calculate_quality_rating("Turbidity", value)

    def _calculate_quality_rating_conductivity(self, value):
        return self.calculate_quality_rating("Conductivity", value)

    def _calculate_quality_rating_tds(self, value):
        return self.calculate_quality_rating("Total Dissolved Solids", value)

    def _calculate_quality_rating_nitrate(self, value):
        return self.calculate_quality_rating("Nitrate", value)

    def _calculate_quality_rating_phosphate(self, value):
        return self.calculate_quality_rating("Phosphate", value)

    def _calculate_quality_rating_total_coliforms(self, value):
        return self.calculate_quality_rating("Total Coliforms", value)

    def _calculate_quality_rating_e_coli(self, value):
        return self.calculate_quality_rating("E. coli", value)

    def _calculate_quality_rating_bod(self, value):
        return self.calculate_quality_rating("BOD", value)

    def _calculate_quality_rating_cod(self, value):
        return self.calculate_quality_rating("COD", value)

    def _calculate_quality_rating_hardness(self, value):
        return self.calculate_quality_rating("Hardness", value)

    def _calculate_quality_rating_alkalinity(self, value):
        return self.calculate_quality_rating("Alkalinity", value)

    def _calculate_quality_rating_iron(self, value):
        return self.calculate_quality_rating("Iron", value)

    def calculate_overall_quality(self, data):
        """
        Calculates the overall water quality score using a weighted arithmetic method.
        """
        quality_sum = 0
        for parameter, value in data.items():
            if parameter not in self.weights:
                print(f"Warning: Unknown parameter '{parameter}' found in data. Skipping.")
                continue
            qi = self.calculate_quality_rating(parameter, value)
            quality_sum += qi * self.weights[parameter]

        return quality_sum

    def generate_report(self, data, quality_score):
        """
        Generates a formatted report of the water quality analysis with additional
        contextual comments.
        """
        report = ''

        # Overall quality interpretation
        if quality_score >= 90:
            overall_quality_comment = "Excellent water quality. Suitable for all uses."
        elif quality_score >= 70:
            overall_quality_comment = "Good water quality. Generally suitable for most uses."
        elif quality_score >= 50:
            overall_quality_comment = "Fair water quality. May be suitable for some uses but might require treatment for others."
        elif quality_score >= 25:
            overall_quality_comment = "Poor water quality. Requires significant treatment before use."
        else:
            overall_quality_comment = "Very poor water quality. Not suitable for use without extensive treatment."

        report += f"Overall Quality Interpretation: {overall_quality_comment}\n\n"

        report += f"Parameter Details:\n"
        for parameter, value in data.items():
            if parameter not in self.weights:
                continue

            unit = self.quality_ratings[parameter]["unit"]
            qi = self.calculate_quality_rating(parameter, value)
            weighted_qi = qi * self.weights[parameter]

            # Parameter-specific interpretation
            if parameter == "pH":
                if value < 6.5:
                    param_comment = "pH is acidic, which can be corrosive and may affect aquatic life."
                elif 6.5 <= value <= 8.5:
                    param_comment = "pH is optimal, well-suited for most aquatic life and uses."
                elif value > 8.5:
                    param_comment = "pH is alkaline, which can be unpleasant to taste and may affect aquatic life."

            elif parameter == "Dissolved Oxygen":
                if value < 5:
                    param_comment = "Dissolved oxygen levels are critically low, severely stressing aquatic life."
                elif 5 <= value <= 7:
                    param_comment = "Dissolved oxygen levels are moderate, sufficient for some aquatic life but could be better."
                elif value > 7:
                    param_comment = "Dissolved oxygen levels are high, indicating a healthy and well-oxygenated aquatic ecosystem."

            elif parameter == "Temperature":
                if value < 15:
                    param_comment = "Temperature is low, which can slow down biological processes in aquatic ecosystems."
                elif 15 <= value <= 25:
                    param_comment = "Temperature is optimal for a wide range of aquatic organisms."
                elif value > 25:
                    param_comment = "Temperature is high, which can reduce dissolved oxygen levels and stress aquatic life."

            elif parameter == "Turbidity":
                if value <= 1:
                    param_comment = "Turbidity is very low, indicating exceptionally clear water."
                elif 1 < value <= 5:
                    param_comment = "Turbidity is low, indicating clear water."
                elif 5 < value <= 50:
                    param_comment = "Turbidity is moderate, which may impact light penetration and visual clarity."
                elif value > 50:
                    param_comment = "Turbidity is high, indicating cloudy water with a significant amount of suspended particles."

            elif parameter == "Conductivity":
                if value <= 100:
                    param_comment = "Conductivity is very low, indicating very pure water with minimal dissolved substances."
                elif 100 < value <= 500:
                    param_comment = "Conductivity is within a normal range for freshwater systems."
                elif 500 < value <= 1500:
                    param_comment = "Conductivity is elevated, suggesting a higher concentration of dissolved substances."
                elif value > 1500:
                    param_comment = "Conductivity is very high, which can be detrimental to aquatic life and indicates significant dissolved solids."

            elif parameter == "Total Dissolved Solids":
                if value <= 100:
                    param_comment = "TDS levels are very low, indicating high purity."
                elif 100 < value <= 500:
                    param_comment = "TDS levels are acceptable for drinking water."
                elif 500 < value <= 1000:
                    param_comment = "TDS levels are moderately high and may affect taste or be noticeable."
                elif value > 1000:
                    param_comment = "TDS levels are high, potentially making the water unpalatable or unsuitable for certain uses."

            elif parameter == "Nitrate":
                if value <= 1:
                    param_comment = "Nitrate levels are very low and well within safe limits."
                elif 1 < value <= 5:
                    param_comment = "Nitrate levels are within acceptable limits."
                elif 5 < value <= 10:
                    param_comment = "Nitrate levels are elevated and could contribute to eutrophication in sensitive waters."
                elif value > 10:
                    param_comment = "Nitrate levels are high, posing a significant risk of eutrophication and potential health concerns."

            elif parameter == "Phosphate":
                if value <= 0.02:
                    param_comment = "Phosphate levels are very low and well within acceptable limits."
                elif 0.02 < value <= 0.1:
                    param_comment = "Phosphate levels are within acceptable limits."
                elif 0.1 < value <= 0.5:
                    param_comment = "Phosphate levels are elevated and could contribute to algal blooms."
                elif value > 0.5:
                    param_comment = "Phosphate levels are high, significantly increasing the risk of nuisance algal blooms."

            elif parameter == "Total Coliforms":
                if value == 0:
                    param_comment = "Total coliforms are not detected, indicating excellent sanitary quality."
                elif 0 < value <= 10:
                    param_comment = "Low levels of total coliforms detected, suggesting a potential for minor contamination."
                elif value > 10:
                    param_comment = "High levels of total coliforms, indicating likely fecal contamination and the need for further investigation."

            elif parameter == "E. coli":
                if value == 0:
                    param_comment = "E. coli is not detected, indicating the water is likely safe from recent fecal contamination."
                elif value > 0:
                    param_comment = "E. coli is detected, indicating fecal contamination and a potential risk of waterborne illness. This requires immediate attention."

            elif parameter == "BOD":
                if value <= 1:
                    param_comment = "BOD is very low, indicating excellent water quality with minimal organic pollution."
                elif 1 < value <= 3:
                    param_comment = "BOD is low, indicating good water quality with minimal organic pollution."
                elif 3 < value <= 8:
                    param_comment = "BOD is moderate, suggesting some organic pollution that could impact dissolved oxygen levels."
                elif value > 8:
                    param_comment = "BOD is high, indicating significant organic pollution and a potential for oxygen depletion."

            elif parameter == "COD":
                if value <= 1:
                    param_comment = "COD is very low, indicating very clean water with minimal chemical pollutants."
                elif 1 < value <= 5:
                    param_comment = "COD is low, indicating minimal chemical pollutants."
                elif 5 < value <= 20:
                    param_comment = "COD is moderate, suggesting the presence of some chemical pollutants."
                elif value > 20:
                    param_comment = "COD is high, indicating significant chemical pollution that may require treatment."

            elif parameter == "Hardness":
                if value <= 60:
                    param_comment = "Water is soft, which is generally good but may lack some minerals."
                elif 60 < value <= 120:
                    param_comment = "Water is moderately hard, generally considered good for consumption."
                elif 120 < value <= 180:
                    param_comment = "Water is hard, which may lead to scale buildup."
                elif value > 180:
                    param_comment = "Water is very hard, likely to cause significant scale buildup and may affect soap effectiveness."

            elif parameter == "Alkalinity":
                if value < 20:
                    param_comment = "Alkalinity is low, making the water susceptible to pH changes."
                elif 20 <= value <= 100:
                    param_comment = "Alkalinity is within the optimal range, providing good buffering capacity."
                elif 100 < value <= 200:
                    param_comment = "Alkalinity is slightly elevated but generally acceptable."
                elif value > 200:
                    param_comment = "Alkalinity is high, which may be associated with high pH and can affect the taste of water."

            elif parameter == "Iron":
                if value <= 0.1:
                    param_comment = "Iron levels are very low, unlikely to cause any issues."
                elif 0.1 < value <= 0.3:
                    param_comment = "Iron levels are low, with a minimal risk of staining or taste issues."
                elif 0.3 < value <= 1.0:
                    param_comment = "Iron levels are moderate and may cause noticeable staining in plumbing fixtures."
                elif value > 1.0:
                    param_comment = "Iron levels are high, likely causing significant staining and a metallic taste."

            else:
                param_comment = "No specific comment available for this parameter."

            report += (
                f"\n{parameter}:\n"
                f"    Measured Value: {value} {unit}\n"
                f"    Quality Rating (Qi): {qi:.2f} (out of 100)\n"
                f"    Weighted Qi: {weighted_qi:.2f}\n"
                f"    Interpretation: {param_comment}\n"
            )

        return report

    def validate_data(self, data):
        """
        Validates the input data dictionary against defined quality ranges.
        """
        for parameter, value in data.items():
            if parameter not in self.quality_ratings:
                raise ValueError(f"Warning: Unknown parameter '{parameter}' found in data.")

            if value is None:
                raise ValueError(f"No value found for parameter '{parameter}'.")

            if not isinstance(value, (int, float)):
                raise ValueError(f"Non-numeric value '{value}' found for parameter '{parameter}'.")

    def plot_parameter_contributions(self, data, quality_score):
        """
        Plots the contributions of each parameter to the overall quality score.
        """
        parameter_contributions = {
            parameter: self.calculate_quality_rating(parameter, value) * self.weights[parameter]
            for parameter, value in data.items()
            if parameter in self.weights
        }

        plt.figure(figsize=(10, 6))
        plt.bar(parameter_contributions.keys(), parameter_contributions.values())
        plt.xlabel("Parameters")
        plt.ylabel("Contribution to Quality Score")
        plt.title(f"Overall Quality Score: {quality_score:.2f} (Parameter Contributions)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        bytes = io.BytesIO()
        plt.savefig(bytes, format='png')
        bytes.seek(0)
        return base64.b64encode(bytes.read()).decode()