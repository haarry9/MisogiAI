def celsius_to_fahrenheit(temp:float) -> float:
    return (temp * 9/5) + 32


def fahrenheit_to_kelvin(temp:float) -> float:
    return (temp - 32) * 5/9 + 273.15


def kelvin_to_celsius(temp:float) -> float:
    return temp - 273.15



if __name__ == "__main__":
    c = 25.0
    f = celsius_to_fahrenheit(c)
    k = fahrenheit_to_kelvin(f)
    c2 = kelvin_to_celsius(k)

    print(f"{c}°C = {f}°F")
    print(f"{f}°F = {k}K")
    print(f"{k}K = {c2}°C")