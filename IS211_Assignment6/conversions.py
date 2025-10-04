def convertCelsiusToKelvin(celsius: float) -> float:
  return celsius + 273.15

def convertCelsiusToFahrenheit(celsius: float) -> float:
  return (celsius * 9/5) + 32

def convertFahrenheitToCelsius(fahrenheit: float) -> float:
  return (fahrenheit - 32) * 5/9

def convertFahrenheitToKelvin(fahrenheit: float) -> float:
  return (fahrenheit - 32) * 5/9 + 273.15

def convertKelvinToCelsius(kelvin: float) -> float:
  return kelvin - 273.15

def convertKelvinToFahrenheit(kelvin: float) -> float:
  return (kelvin - 273.15) * 9/5 + 32
