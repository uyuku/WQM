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

        # Default quality ratings and units
        self.default_quality_ratings = {
            "Temperature": {
                "ideal": 20,
                "good_low": 15,
                "good_high": 25,
                "poor_low": 0,  # Adjusted to allow evaluation
                "poor_high": 40, # Adjusted to allow evaluation
                "unit": "°C"
            },
            "pH": {  # Using linear interpolation now
                "ideal": 7,
                "good_low": 6.5,
                "good_high": 8.5,
                "poor_low": 0,   # Adjusted to allow evaluation
                "poor_high": 14,  # Adjusted to allow evaluation
                "unit": ""
            },
            "Turbidity": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 100, # Adjusted to allow evaluation
                "unit": "NTU"
            },
            "Dissolved Oxygen": {  # Using linear interpolation now
                "ideal": 9,
                "good_low": 7,
                "good_high": 11,
                "poor_low": 0,   # Adjusted to allow evaluation
                "poor_high": 15,  # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "Conductivity": {
                "ideal": 200,
                "good_low": 100,
                "good_high": 500,
                "poor_low": 0,      # Adjusted to allow evaluation
                "poor_high": 2000,  # Adjusted to allow evaluation
                "unit": "µS/cm"
            },
            "Total Dissolved Solids": {
                "ideal": 100,
                "good_low": 50,
                "good_high": 500,
                "poor_low": 0,      # Adjusted to allow evaluation
                "poor_high": 1500, # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "Nitrate": {
                "ideal": 1,
                "good_low": 0,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 20,  # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "Phosphate": {
                "ideal": 0.02,
                "good_low": 0,
                "good_high": 0.1,
                "poor_low": 0,
                "poor_high": 1.0,  # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "Total Coliforms": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 10,
                "poor_low": 0,
                "poor_high": 1000, # Adjusted to allow evaluation
                "unit": "CFU/100mL"
            },
            "E. coli": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 1,
                "poor_low": 0,
                "poor_high": 100, # Adjusted to allow evaluation
                "unit": "CFU/100mL"
            },
            "BOD": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 3,
                "poor_low": 0,
                "poor_high": 20,  # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "COD": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 50,  # Adjusted to allow evaluation
                "unit": "mg/L"
            },
            "Hardness": {
                "ideal": 75,
                "good_low": 60,
                "good_high": 180,
                "poor_low": 0,
                "poor_high": 800, # Adjusted to allow evaluation
                "unit": "mg/L"  # as CaCO3
            },
            "Alkalinity": {
                "ideal": 100,
                "good_low": 20,
                "good_high": 200,
                "poor_low": 0,
                "poor_high": 1000, # Adjusted to allow evaluation
                "unit": "mg/L" # as CaCO3
            },
            "Iron": {
                "ideal": 0.0,
                "good_low": 0,
                "good_high": 0.3,
                "poor_low": 0,
                "poor_high": 5.0,  # Adjusted to allow evaluation
                "unit": "mg/L"
            }
        }

        self.weights = weights if weights is not None else self.default_weights
        self.quality_ratings = quality_ratings if quality_ratings is not None else self.default_quality_ratings

        if abs(sum(self.weights.values()) - 1) > 1e-6:
            raise ValueError("The sum of the weights should be equal to 1")

    def calculate_quality_rating(self, parameter, value):
        """
        Calculates the quality rating (Qi) for a parameter using appropriate logic.
        Now focuses on "how good" the quality is.
        """
        rating = self.quality_ratings[parameter]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"],
            rating["good_low"],
            rating["good_high"],
            rating["poor_low"],
            rating["poor_high"],
        )

        # Ensure the value falls within the defined evaluation range
        if not (poor_low <= value <= poor_high):
            # Still provide a rating, even if outside the typical "poor" range
            if value < poor_low:
                # Extrapolate linearly below the poor range
                return max(0, 50 - ((poor_low - value) / (good_low - poor_low if good_low > poor_low else 1)) * 50)
            else:  # value > poor_high
                # Extrapolate linearly above the poor range
                return min(100, 50 - ((value - poor_high) / (poor_high - good_high if poor_high > good_high else 1)) * 50)

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 50 + ((value - good_low) / (ideal - good_low if ideal > good_low else 1)) * 50
            else:
                qi = 50 + ((good_high - value) / (good_high - ideal if good_high > ideal else 1)) * 50
        elif value < good_low:
            # Below good range
            qi = (value - poor_low) / (good_low - poor_low if good_low > poor_low else 1) * 50
        else:
            # Above good range
            qi = (poor_high - value) / (poor_high - good_high if poor_high > good_high else 1) * 50

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
                    param_comment = "pH is within the optimal range, suitable for most aquatic life and uses."
                elif value > 8.5:
                    param_comment = "pH is alkaline, which can be unpleasant to taste and may affect aquatic life."

            elif parameter == "Dissolved Oxygen":
                if value < 5:
                    param_comment = "Dissolved oxygen levels are low, potentially stressing aquatic life."
                elif 5 <= value <= 7:
                    param_comment = "Dissolved oxygen levels are moderate, sufficient for some aquatic life but could be better."
                elif value > 7:
                    param_comment = "Dissolved oxygen levels are good, supporting a healthy aquatic ecosystem."

            elif parameter == "Temperature":
                if value < 15:
                    param_comment = "Temperature is low, which can slow down biological processes."
                elif 15 <= value <= 25:
                    param_comment = "Temperature is optimal for most aquatic organisms."
                elif value > 25:
                    param_comment = "Temperature is high, which can reduce dissolved oxygen levels and stress aquatic life."

            elif parameter == "Turbidity":
                if value <= 5:
                    param_comment = "Turbidity is low, indicating clear water."
                elif 5 < value <= 50:
                    param_comment = "Turbidity is moderate, which may impact light penetration."
                elif value > 50:
                    param_comment = "Turbidity is high, indicating cloudy water with suspended particles."

            elif parameter == "Conductivity":
                if value <= 500:
                    param_comment = "Conductivity is within a normal range for freshwater."
                elif 500 < value <= 1500:
                    param_comment = "Conductivity is elevated, suggesting a higher concentration of dissolved substances."
                elif value > 1500:
                    param_comment = "Conductivity is very high, which can be detrimental to aquatic life and indicates significant dissolved solids."

            elif parameter == "Total Dissolved Solids":
                if value <= 500:
                    param_comment = "TDS levels are acceptable for drinking water."
                elif 500 < value <= 1000:
                    param_comment = "TDS levels are moderately high and may affect taste."
                elif value > 1000:
                    param_comment = "TDS levels are high, potentially making the water unpalatable or unsuitable for certain uses."

            elif parameter == "Nitrate":
                if value <= 5:
                    param_comment = "Nitrate levels are within acceptable limits."
                elif 5 < value <= 10:
                    param_comment = "Nitrate levels are elevated and could contribute to eutrophication."
                elif value > 10:
                    param_comment = "Nitrate levels are high, posing a risk of eutrophication and potential health concerns."

            elif parameter == "Phosphate":
                if value <= 0.1:
                    param_comment = "Phosphate levels are within acceptable limits."
                elif 0.1 < value <= 0.5:
                    param_comment = "Phosphate levels are elevated and could contribute to algal blooms."
                elif value > 0.5:
                    param_comment = "Phosphate levels are high, significantly increasing the risk of algal blooms."

            elif parameter == "Total Coliforms":
                if value == 0:
                    param_comment = "Total coliforms are not detected, indicating good sanitary quality."
                elif 0 < value <= 10:
                    param_comment = "Low levels of total coliforms detected, suggesting a potential for contamination."
                elif value > 10:
                    param_comment = "High levels of total coliforms, indicating likely fecal contamination."

            elif parameter == "E. coli":
                if value == 0:
                    param_comment = "E. coli is not detected, indicating the water is likely safe from fecal contamination."
                elif value > 0:
                    param_comment = "E. coli is detected, indicating fecal contamination and a risk of waterborne illness."

            elif parameter == "BOD":
                if value <= 3:
                    param_comment = "BOD is low, indicating good water quality with minimal organic pollution."
                elif 3 < value <= 8:
                    param_comment = "BOD is moderate, suggesting some organic pollution."
                elif value > 8:
                    param_comment = "BOD is high, indicating significant organic pollution that can deplete oxygen."

            elif parameter == "COD":
                if value <= 5:
                    param_comment = "COD is low, indicating minimal chemical pollutants."
                elif 5 < value <= 20:
                    param_comment = "COD is moderate, suggesting some chemical pollution."
                elif value > 20:
                    param_comment = "COD is high, indicating significant chemical pollution."

            elif parameter == "Hardness":
                if value <= 75:
                    param_comment = "Water is soft."
                elif 75 < value <= 150:
                    param_comment = "Water is moderately hard."
                elif 150 < value <= 300:
                    param_comment = "Water is hard."
                elif value > 300:
                    param_comment = "Water is very hard."

            elif parameter == "Alkalinity":
                if value < 20:
                    param_comment = "Alkalinity is low, making the water susceptible to pH changes."
                elif 20 <= value <= 200:
                    param_comment = "Alkalinity is within a desirable range, providing good buffering capacity."
                elif value > 200:
                    param_comment = "Alkalinity is high, which may be associated with high pH."

            elif parameter == "Iron":
                if value <= 0.3:
                    param_comment = "Iron levels are low, unlikely to cause staining or taste issues."
                elif 0.3 < value <= 1.0:
                    param_comment = "Iron levels are moderate and may cause staining."
                elif value > 1.0:
                    param_comment = "Iron levels are high, likely causing staining and a metallic taste."

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