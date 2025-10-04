# IS211_Assignment6

## Overview
This assignment focuses on writing unit tests and refactoring conversion functions. 
It demonstrates Python unit testing with the `unittest` module, and the use of a generalized converter function.

## Files
- **conversions.py** 
  Contains 6 temperature conversion functions:
  - Celsius ↔ Kelvin 
  - Celsius ↔ Fahrenheit 
  - Fahrenheit ↔ Kelvin 

- **conversions_refactored.py** 
  Contains a generalized `convert(fromUnit, toUnit, value)` function that handles:
  - Temperature (Celsius, Fahrenheit, Kelvin) 
  - Distance (Miles, Yards, Meters) 
  - Same-unit conversions (value returned unchanged) 
  - Raises `ConversionNotPossible` for incompatible conversions. 

- **tests.py** 
  Unit tests for:
  - All 6 temperature conversion functions (5 cases each). 
  - The refactored converter, including:
    - Temperature conversions 
    - Distance conversions 
    - Same-unit conversions 
    - Invalid/incompatible conversions 

## Running Tests
To run all tests:
```bash
python3 tests.py

