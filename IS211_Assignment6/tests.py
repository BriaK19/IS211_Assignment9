import unittest
import conversions
import conversions_refactored as cref


class TestConversions(unittest.TestCase):

    def test_convertCelsiusToKelvin(self):
        cases = [(0, 273.15), (100, 373.15), (-273.15, 0), (25, 298.15), (300, 573.15)]
        for c, expected in cases:
            self.assertAlmostEqual(conversions.convertCelsiusToKelvin(c), expected, places=2)

    def test_convertCelsiusToFahrenheit(self):
        cases = [(0, 32), (100, 212), (-40, -40), (25, 77), (300, 572)]
        for c, expected in cases:
            self.assertAlmostEqual(conversions.convertCelsiusToFahrenheit(c), expected, places=2)

    def test_convertFahrenheitToCelsius(self):
        cases = [(32, 0), (212, 100), (-40, -40), (77, 25), (572, 300)]
        for f, expected in cases:
            self.assertAlmostEqual(conversions.convertFahrenheitToCelsius(f), expected, places=2)

    def test_convertFahrenheitToKelvin(self):
        cases = [(32, 273.15), (212, 373.15), (-40, 233.15), (77, 298.15), (572, 573.15)]
        for f, expected in cases:
            self.assertAlmostEqual(conversions.convertFahrenheitToKelvin(f), expected, places=2)

    def test_convertKelvinToCelsius(self):
        cases = [(273.15, 0), (373.15, 100), (0, -273.15), (298.15, 25), (573.15, 300)]
        for k, expected in cases:
            self.assertAlmostEqual(conversions.convertKelvinToCelsius(k), expected, places=2)

    def test_convertKelvinToFahrenheit(self):
        cases = [(273.15, 32), (373.15, 212), (0, -459.67), (298.15, 77), (573.15, 572)]
        for k, expected in cases:
            self.assertAlmostEqual(conversions.convertKelvinToFahrenheit(k), expected, places=2)


class TestRefactoredConversions(unittest.TestCase):

    def test_temperature_all_pairs(self):
        cases = [
            ("celsius", "kelvin", 0, 273.15),
            ("celsius", "fahrenheit", 100, 212),
            ("fahrenheit", "celsius", 32, 0),
            ("fahrenheit", "kelvin", -40, 233.15),
            ("kelvin", "celsius", 273.15, 0),
            ("kelvin", "fahrenheit", 373.15, 212),
        ]
        for f, t, v, expected in cases:
            self.assertAlmostEqual(cref.convert(f, t, v), expected, places=2)

    def test_distance_all_pairs(self):
        cases = [
            ("miles", "meters", 1, 1609.344),
            ("meters", "miles", 1609.344, 1),
            ("yards", "meters", 1, 0.9144),
            ("meters", "yards", 1, 1.09361),
            ("miles", "yards", 1, 1760),
        ]
        for f, t, v, expected in cases:
            self.assertAlmostEqual(cref.convert(f, t, v), expected, places=4)

    def test_same_unit_returns_same_value(self):
        for u in ["celsius", "fahrenheit", "kelvin", "miles", "yards", "meters"]:
            self.assertEqual(cref.convert(u, u, 123.456), 123.456)

    def test_incompatible_units_raise(self):
        with self.assertRaises(cref.ConversionNotPossible):
            cref.convert("celsius", "meters", 10)


if __name__ == "__main__":
    unittest.main()


