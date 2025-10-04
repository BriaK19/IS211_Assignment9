class ConversionNotPossible(Exception):
  pass

def convert(fromUnit: str, toUnit: str, value: float) -> float:
    fromUnit = fromUnit.lower()
    toUnit = toUnit.lower()

    # Tempature conversion
    if fromUnit in ["celsius", "fahrenheit", "kelvin"] and toUnit in ["celsius", "fahrenheit", "kelvin"]:
        if fromUnit == toUnit:
            return value
        if fromUnit == "celsius":
            if toUnit == "fahrenheit":
                return (value * 9/5) + 32
            elif toUnit == "kelvin":
                return value + 273.15
        elif fromUnit == "fahrenheit":
            if toUnit == "celsius":
                return (value - 32) * 5/9
            elif toUnit == "kelvin":
                return (value - 32) * 5/9 + 273.15
        elif fromUnit == "kelvin":
            if toUnit == "celsius":
                return value - 273.15
            elif toUnit == "fahrenheit":
                return (value - 273.15) * 9/5 + 32
    # Distance conversion (miles, yards, meters)
    distance_units = {
        "miles": 1609.344,
        "yards": 0.9144,
        "meters": 1.0
    }

    if fromUnit in distance_units and toUnit in distance_units:
        return value * (distance_units[fromUnit] / distance_units[toUnit])

    # Incompatible units
    raise ConversionNotPossible(f"Cannot convert from {fromUnit} to {toUnit}")
