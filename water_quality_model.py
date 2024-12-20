import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class WaterQualityEvaluator:
    """
    Evaluates water quality based on various parameters using a combination of
    linear, piecewise linear, and fuzzy logic methods. Calculates an overall
    water quality score and generates a detailed report.
    """

    def __init__(self, weights=None, quality_ratings=None):
        """
        Initializes the WaterQualityEvaluator with optional custom weights and
        quality ratings.
        """
        # Example Parameters with Fuzzy Logic for pH and Dissolved Oxygen
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

        # Default quality ratings and units (you can customize these)
        self.default_quality_ratings = {
            "Temperature": {
                "ideal": 20,
                "good_low": 15,
                "good_high": 25,
                "poor_low": 5,
                "poor_high": 35,
                "unit": "°C"
            },
            "pH": {  # Fuzzy logic will be used here
                "ideal": 7,
                "good_low": 6.5,
                "good_high": 8,
                "poor_low": 4,
                "poor_high": 10,
                "unit": ""  # pH is unitless
            },
            "Turbidity": {
                "ideal": 0,
                "good_low": 1,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 50,
                "unit": "NTU"
            },
            "Dissolved Oxygen": {  # Fuzzy logic will be used here
                "ideal": 9,
                "good_low": 7,
                "good_high": 11,
                "poor_low": 3,
                "poor_high": 14,
                "unit": "mg/L"
            },
            "Conductivity": {
                "ideal": 200,
                "good_low": 100,
                "good_high": 400,
                "poor_low": 50,
                "poor_high": 1000,
                "unit": "µS/cm"
            },
            "Total Dissolved Solids": {
                "ideal": 100,
                "good_low": 50,
                "good_high": 300,
                "poor_low": 0,
                "poor_high": 500,
                "unit": "mg/L"
            },
            "Nitrate": {
                "ideal": 1,
                "good_low": 0,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 10,
                "unit": "mg/L"
            },
            "Phosphate": {
                "ideal": 0.02,
                "good_low": 0,
                "good_high": 0.1,
                "poor_low": 0,
                "poor_high": 0.3,
                "unit": "mg/L"
            },
            "Total Coliforms": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 5,
                "poor_low": 0,
                "poor_high": 100,
                "unit": "CFU/100mL"
            },
            "E. coli": {
                "ideal": 0,
                "good_low": 000.1,
                "good_high": 1,
                "poor_low": 0,
                "poor_high": 10,
                "unit": "CFU/100mL"
            },
            "BOD": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 2,
                "poor_low": 0,
                "poor_high": 6,
                "unit": "mg/L"
            },
            "COD": {
                "ideal": 0,
                "good_low": 0,
                "good_high": 4,
                "poor_low": 0,
                "poor_high": 20,
                "unit": "mg/L"
            },
            "Hardness": {
                "ideal": 75,
                "good_low": 60,
                "good_high": 150,
                "poor_low": 0,
                "poor_high": 500,
                "unit": "mg/L"  # as CaCO3
            },
            "Alkalinity": {
                "ideal": 100,
                "good_low": 20,
                "good_high": 200,
                "poor_low": 0,
                "poor_high": 500,
                "unit": "mg/L" # as CaCO3
            },
            "Iron": {
                "ideal": 0.0,
                "good_low": 0,
                "good_high": 0.3,
                "poor_low": 0,
                "poor_high": 1.0,
                "unit": "mg/L"
            }
        }

        self.weights = weights if weights is not None else self.default_weights
        self.quality_ratings = quality_ratings if quality_ratings is not None else self.default_quality_ratings

        if abs(sum(self.weights.values()) - 1) > 1e-6:
            raise ValueError("The sum of the weights should be equal to 1")

        # Initialize fuzzy logic controllers (only for demonstration)
        self._initialize_fuzzy_logic()

    def _initialize_fuzzy_logic(self):
        """
        Initializes fuzzy logic controllers for pH and Dissolved Oxygen.
        """
        # pH fuzzy logic
        # 1. Define the Antecedent (input)
        pH = ctrl.Antecedent(np.arange(0, 14, 0.1), 'pH_input')

        # 2. Define membership functions for pH
        pH['poor'] = fuzz.trapmf(pH.universe, [0, 0, 4, 6.5])
        pH['good'] = fuzz.gaussmf(pH.universe, 7, 0.5)
        pH['excellent'] = fuzz.trapmf(pH.universe, [7.5, 8.5, 14, 14])

        # 3. Define the Consequent (output)
        quality = ctrl.Consequent(np.arange(0, 100, 1), 'pH_quality')

        # 4. Define membership functions for the output quality
        quality['poor'] = fuzz.trimf(quality.universe, [0, 0, 50])
        quality['good'] = fuzz.trimf(quality.universe, [0, 50, 100])
        quality['excellent'] = fuzz.trimf(quality.universe, [50, 100, 100])

        # 5. Now create the control system and add rules
        self.pH_ctrl = ctrl.ControlSystem()
        self.pH_ctrl.addrule(ctrl.Rule(pH['poor'], quality['poor']))
        self.pH_ctrl.addrule(ctrl.Rule(pH['good'], quality['good']))
        self.pH_ctrl.addrule(ctrl.Rule(pH['excellent'], quality['excellent']))

        # Dissolved Oxygen fuzzy logic (similar structure)
        # 1. Define the Antecedent (input)
        do = ctrl.Antecedent(np.arange(0, 20, 0.1), 'do_input')

        # 2. Define membership functions for DO
        do['poor'] = fuzz.trapmf(do.universe, [0, 0, 3, 7])
        do['good'] = fuzz.gaussmf(do.universe, 9, 1)
        do['excellent'] = fuzz.trapmf(do.universe, [11, 14, 20, 20])

        # 3. Define the Consequent (output)
        do_quality = ctrl.Consequent(np.arange(0, 100, 1), 'do_quality')

        # 4. Define membership functions for the output quality
        do_quality['poor'] = fuzz.trimf(do_quality.universe, [0, 0, 50])
        do_quality['good'] = fuzz.trimf(do_quality.universe, [0, 50, 100])
        do_quality['excellent'] = fuzz.trimf(do_quality.universe, [50, 100, 100])

        # 5. Create the control system and add rules
        self.do_ctrl = ctrl.ControlSystem()
        self.do_ctrl.addrule(ctrl.Rule(do['poor'], do_quality['poor']))
        self.do_ctrl.addrule(ctrl.Rule(do['good'], do_quality['good']))
        self.do_ctrl.addrule(ctrl.Rule(do['excellent'], do_quality['excellent']))

    def calculate_quality_rating(self, parameter, value):
        """
        Calculates the quality rating (Qi) for a parameter using appropriate logic.
        Now focuses on "how good" the quality is.
        """
        rating = self.quality_ratings[parameter]

        if parameter == "pH":
            return self._calculate_fuzzy_quality_ph(value)
        elif parameter == "Dissolved Oxygen":
            return self._calculate_fuzzy_quality_do(value)
        elif parameter == "Temperature":
            return self._calculate_quality_rating_temperature(value)
        elif parameter == "Turbidity":
            return self._calculate_quality_rating_turbidity(value)
        elif parameter == "Conductivity":
            return self._calculate_quality_rating_conductivity(value)
        elif parameter == "Total Dissolved Solids":
            return self._calculate_quality_rating_tds(value)
        elif parameter == "Nitrate":
            return self._calculate_quality_rating_nitrate(value)
        elif parameter == "Phosphate":
            return self._calculate_quality_rating_phosphate(value)
        elif parameter == "Total Coliforms":
            return self._calculate_quality_rating_total_coliforms(value)
        elif parameter == "E. coli":
            return self._calculate_quality_rating_e_coli(value)
        elif parameter == "BOD":
            return self._calculate_quality_rating_bod(value)
        elif parameter == "COD":
            return self._calculate_quality_rating_cod(value)
        else:
            # Default: Linear interpolation (you can customize this)
            ideal, good_low, good_high, poor_low, poor_high = (
                rating["ideal"],
                rating["good_low"],
                rating["good_high"],
                rating["poor_low"],
                rating["poor_high"],
            )

            if not (poor_low <= value <= poor_high):
                return 0  # Value is outside the defined poor range

            if good_low == good_high:  # Linear interpolation for single good range
                if value <= ideal:
                    qi = 100 - ((ideal - value) / (ideal - poor_low)) * (100 - 0)
                else:
                    qi = 100 - ((value - ideal) / (poor_high - ideal)) * (100 - 0)
            else:  # Piecewise linear interpolation
                if good_low <= value <= good_high:
                    qi = 100 - ((value - good_low) / (good_high - good_low)) * (100 - 0)
                elif value < good_low:
                    qi = 100 - ((good_low - value) / (good_low - poor_low)) * (100 - 0)
                else:  # value > good_high
                    qi = 100 - ((value - good_high) / (poor_high - good_high)) * (100 - 0)

            return max(0, min(qi, 100))  # Ensure qi is within 0-100 range

    def _calculate_fuzzy_quality_ph(self, pH_value):
        """
        Calculates the quality rating for pH using fuzzy logic.
        """
        # Define fuzzy sets and membership functions for pH
        pH = ctrl.Antecedent(np.arange(0, 14, 0.1), 'pH_input')
        quality = ctrl.Consequent(np.arange(0, 100, 1), 'pH_quality')

        # Define membership functions
        pH['poor'] = fuzz.trapmf(pH.universe, [0, 0, 4, 6.5])
        pH['good'] = fuzz.gaussmf(pH.universe, 7, 0.5)
        pH['excellent'] = fuzz.trapmf(pH.universe, [7.5, 8.5, 14, 14])

        quality['poor'] = fuzz.trimf(quality.universe, [0, 0, 50])
        quality['good'] = fuzz.trimf(quality.universe, [0, 50, 100])
        quality['excellent'] = fuzz.trimf(quality.universe, [50, 100, 100])

        # Create control system simulation
        pH_sim = ctrl.ControlSystemSimulation(self.pH_ctrl)
        pH_sim.input['pH_input'] = pH_value

        # Compute the result
        pH_sim.compute()
        quality_value = pH_sim.output['pH_quality']

        return quality_value
    
    def _calculate_fuzzy_quality_do(self, do_value):
        """
        Calculates the quality rating for Dissolved Oxygen using fuzzy logic.
        """
        # Define fuzzy sets and membership functions for Dissolved Oxygen
        do = ctrl.Antecedent(np.arange(0, 20, 0.1), 'do_input')
        quality = ctrl.Consequent(np.arange(0, 100, 1), 'do_quality')

        # Define membership functions
        do['poor'] = fuzz.trapmf(do.universe, [0, 0, 3, 7])
        do['good'] = fuzz.gaussmf(do.universe, 9, 1)
        do['excellent'] = fuzz.trapmf(do.universe, [11, 14, 20, 20])

        quality['poor'] = fuzz.trimf(quality.universe, [0, 0, 50])
        quality['good'] = fuzz.trimf(quality.universe, [0, 50, 100])
        quality['excellent'] = fuzz.trimf(quality.universe, [50, 100, 100])

        # Create control system simulation
        do_sim = ctrl.ControlSystemSimulation(self.do_ctrl)
        do_sim.input['do_input'] = do_value

        # Compute the result
        do_sim.compute()
        quality_value = do_sim.output['do_quality']

        return quality_value

    def _calculate_quality_rating_temperature(self, value):
        """Calculates the quality rating for temperature."""
        rating = self.quality_ratings["Temperature"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0  # Value is outside the defined poor range

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_turbidity(self, value):
        """Calculates the quality rating for turbidity."""
        rating = self.quality_ratings["Turbidity"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_conductivity(self, value):
        """Calculates the quality rating for conductivity."""
        rating = self.quality_ratings["Conductivity"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_tds(self, value):
        """Calculates the quality rating for Total Dissolved Solids."""
        rating = self.quality_ratings["Total Dissolved Solids"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_nitrate(self, value):
        """Calculates the quality rating for nitrate."""
        rating = self.quality_ratings["Nitrate"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_phosphate(self, value):
        """Calculates the quality rating for phosphate."""
        rating = self.quality_ratings["Phosphate"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_total_coliforms(self, value):
        """Calculates the quality rating for Total Coliforms."""
        rating = self.quality_ratings["Total Coliforms"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_e_coli(self, value):
        """Calculates the quality rating for E. coli."""
        rating = self.quality_ratings["E. coli"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                if ideal == good_low:  # Avoid division by zero
                    qi = 100 if value == ideal else 50 #Here if the value is ideal you get 100 else 50
                else:
                    qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_bod(self, value):
        """Calculates the quality rating for BOD."""
        rating = self.quality_ratings["BOD"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_cod(self, value):
        """Calculates the quality rating for COD."""
        rating = self.quality_ratings["COD"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))
    def _calculate_quality_rating_hardness(self, value):
        """Calculates the quality rating for hardness."""
        rating = self.quality_ratings["Hardness"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_alkalinity(self, value):
        """Calculates the quality rating for alkalinity."""
        rating = self.quality_ratings["Alkalinity"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def _calculate_quality_rating_iron(self, value):
        """Calculates the quality rating for iron."""
        rating = self.quality_ratings["Iron"]
        ideal, good_low, good_high, poor_low, poor_high = (
            rating["ideal"], rating["good_low"], rating["good_high"],
            rating["poor_low"], rating["poor_high"]
        )

        if not (poor_low <= value <= poor_high):
            return 0

        if good_low <= value <= good_high:
            # Within good range
            if value <= ideal:
                qi = 100 - ((ideal - value) / (ideal - good_low)) * 50  # 100 to 50 for good_low to ideal
            else:
                qi = 100 - ((value - ideal) / (good_high - ideal)) * 50  # 100 to 50 for ideal to good_high
        elif value < good_low:
            # Below good range
            qi = 50 - ((good_low - value) / (good_low - poor_low)) * 50  # 50 to 0 for poor_low to good_low
        else:
            # Above good range
            qi = 50 - ((value - good_high) / (poor_high - good_high)) * 50  # 50 to 0 for good_high to poor_high

        return max(0, min(qi, 100))

    def calculate_overall_quality(self, data):
        """
        Calculates the overall water quality score using a weighted arithmetic method.
        """
        quality_sum = 0
        for parameter, value in data.items():
            if parameter not in self.weights:
                print(f"Warning: Unknown parameter '{parameter}' found in data. Skipping.")
                continue
            if parameter == "Alkalinity" or parameter == "Hardness" or parameter == "Iron":
                qi = self.calculate_quality_rating(parameter, value)
            else:
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
                if qi >= 90:
                    param_comment = "pH is in the ideal range, indicating balanced acidity/alkalinity."
                elif qi >= 70:
                    param_comment = "pH is within acceptable limits, but may slightly deviate from the ideal."
                else:
                    param_comment = "pH is outside the optimal range, which could affect aquatic life and water usability."
         
            elif parameter == "Dissolved Oxygen":
                if qi >= 90:
                    param_comment = "High dissolved oxygen levels, indicating a healthy aquatic ecosystem."
                elif qi >= 70:
                    param_comment = "Dissolved oxygen levels are adequate but could be improved."
                else:
                    param_comment = "Low dissolved oxygen levels, which could be detrimental to aquatic life."
        
            elif parameter == "Temperature":
                if qi >= 90:
                    param_comment = "Temperature is within the optimal range for most aquatic organisms."
                elif qi >= 70:
                    param_comment = "Temperature is slightly outside the ideal range but may not pose significant issues."
                else:
                    param_comment = "Temperature is in a range that could stress aquatic life or affect water chemistry."
          
            elif parameter == "Turbidity":
                if qi >= 90:
                    param_comment = "Low turbidity, indicating clear water with minimal suspended particles."
                elif qi >= 70:
                    param_comment = "Water has moderate turbidity, which may impact light penetration and aquatic life."
                else:
                    param_comment = "High turbidity, indicating poor water clarity and potential issues with sedimentation and pollutants."
          
            elif parameter == "Conductivity":
                if qi >= 90:
                    param_comment = "Conductivity is within the normal range for freshwater systems."
                elif qi >= 70:
                    param_comment = "Conductivity is slightly elevated, suggesting a moderate presence of dissolved solids."
                else:
                    param_comment = "High conductivity, indicating a significant presence of dissolved ions, which could affect water usability and aquatic ecosystems."
           
            elif parameter == "Total Dissolved Solids":
                if qi >= 90:
                    param_comment = "Low levels of total dissolved solids, indicating good water quality."
                elif qi >= 70:
                    param_comment = "Moderate levels of total dissolved solids, which may be acceptable for some uses but could impact taste."
                else:
              
                    param_comment = "High levels of total dissolved solids, which could make the water unsuitable for drinking and some industrial uses."
            elif parameter == "Nitrate":
                if qi >= 90:
                    param_comment = "Nitrate levels are within safe limits, posing minimal risk of eutrophication."
                elif qi >= 70:
                    param_comment = "Nitrate levels are slightly elevated but may not pose immediate concerns."
                else:
              
                    param_comment = "High nitrate levels, which could contribute to eutrophication and pose health risks if consumed."
            elif parameter == "Phosphate":
                if qi >= 90:
                    param_comment = "Phosphate levels are within acceptable limits, posing minimal risk of eutrophication."
                elif qi >= 70:
                    param_comment = "Phosphate levels are slightly elevated but may not pose immediate concerns."
                else:
             
                    param_comment = "High phosphate levels, which could contribute to eutrophication and algal blooms."
            elif parameter == "Total Coliforms":
                if qi >= 90:
                    param_comment = "Total coliform levels are low or absent, indicating a low risk of fecal contamination."
                elif qi >= 70:
                    param_comment = "Moderate levels of total coliforms detected, suggesting potential contamination issues."
                else:
             
                    param_comment = "High levels of total coliforms, indicating significant fecal contamination and health risks."
            elif parameter == "E. coli":
                if qi >= 90:
                    param_comment = "E. coli is absent or present at very low levels, indicating a low risk of harmful pathogens."
                elif qi >= 70:
                    param_comment = "Low levels of E. coli detected, suggesting possible contamination."
                else:
             
                    param_comment = "High levels of E. coli, indicating significant fecal contamination and a high risk of waterborne illness."
            elif parameter == "BOD":
                if qi >= 90:
                    param_comment = "Low BOD, indicating minimal organic pollution and good oxygen availability for aquatic life."
                elif qi >= 70:
                    param_comment = "Moderate BOD, suggesting some organic pollution that could impact dissolved oxygen levels."
                else:
            
                    param_comment = "High BOD, indicating significant organic pollution and potential depletion of dissolved oxygen."
            elif parameter == "COD":
                if qi >= 90:
                    param_comment = "Low COD, indicating minimal chemical pollution and good water quality."
                elif qi >= 70:
                    param_comment = "Moderate COD, suggesting some chemical pollution that could impact water quality."
                else:
                    param_comment = "High COD, indicating significant chemical pollution and potential toxicity issues."
          
            elif parameter == "Hardness":
                if qi >= 90:
                    param_comment = "Soft water, which is excellent for most uses but may lack essential minerals."
                elif qi >= 70:
                    param_comment = "Slightly hard water, which is generally acceptable but may start to exhibit some scaling in appliances."
                elif qi >= 50:
                    param_comment = "Moderately hard water. While not typically a health concern, it may cause scaling in pipes and appliances and reduce the effectiveness of soaps and detergents."
                else:
                    param_comment = "Hard to very hard water. Expect significant scaling, reduced soap effectiveness, and potential aesthetic issues."

            elif parameter == "Alkalinity":
                if qi >= 90:
                    param_comment = "High alkalinity, indicating a strong ability to resist pH changes. May be associated with hard water."
                elif qi >= 70:
                    param_comment = "Alkalinity is within the acceptable range. It indicates a good buffering capacity, meaning the water can resist significant changes in pH."
                elif qi >= 50:
                    param_comment = "Slightly low alkalinity. The water may be more susceptible to pH fluctuations."
                else:
                    param_comment = "Low alkalinity, indicating limited buffering capacity. The water's pH could be unstable and potentially corrosive."
           
            elif parameter == "Iron":
                if qi >= 90:
                    param_comment = "Very low iron levels, unlikely to cause any aesthetic issues."
                elif qi >= 70:
                    param_comment = "Low iron levels, minimal risk of staining or metallic taste."
                elif qi >= 50:
                    param_comment = "Moderate iron levels. Some staining of fixtures or laundry may occur."
                else:
                    param_comment = "Elevated iron levels. This may cause staining of laundry and plumbing fixtures (e.g., reddish-brown stains) and impart a metallic taste to the water. It is not typically a health concern at these levels, but aesthetic issues are common."
            
            else:
                param_comment = "No specific comment available for this parameter."

            report += (
                f"  {parameter}:\n"
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
