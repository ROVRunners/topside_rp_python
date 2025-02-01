# Length:
from enum import Enum


class Lengths (Enum):
    METER = 1.0
    CENTIMETER = 0.01
    MILLIMETER = 0.001
    KILOMETER = 1000.0
    INCH = 0.0254
    FOOT = 0.3048
    YARD = 0.9144
    MILE = 1609.344
    NAUTICAL_MILE = 1852.0
    FATHOM = 1.8288
    LIGHT_YEAR = 9460730472580800.0
    PARSEC = 30856775814671900.0
    ASTRONOMICAL_UNIT = 149597870700.0


# Area:
class Areas (Enum):
    SQUARE_METER = 1.0
    HECTARE = 10000.0
    ACRE = 4046.8564224
    SQUARE_CENTIMETER = 0.0001
    SQUARE_MILLIMETER = 0.000001
    SQUARE_KILOMETER = 1000000.0
    SQUARE_INCH = 0.00064516
    SQUARE_FOOT = 0.09290304
    SQUARE_YARD = 0.83612736
    SQUARE_MILE = 2589988.110336
    SQUARE_NAUTICAL_MILE = 3429904.0


# Volume:
class Volumes (Enum):
    LITER = 1.0
    MILLILITER = 0.001
    CUBIC_METER = 1000.0
    CUBIC_CENTIMETER = 0.001
    CUBIC_MILLIMETER = 0.000001
    GALLON = 3.78541
    QUART = 0.946353
    PINT = 0.473176
    CUP = 0.236588
    FLUID_OUNCE = 0.0295735
    TABLESPOON = 0.0147868
    TEASPOON = 0.00492892
    CUBIC_FOOT = 28.3168
    CUBIC_INCH = 0.0163871


# Mass:
class Masses (Enum):
    KILOGRAM = 1.0
    GRAM = 0.001
    MILLIGRAM = 0.000001
    METRIC_TON = 1000.0
    LONG_TON = 1016.0469088
    SHORT_TON = 907.18474
    POUND = 0.453592
    OUNCE = 0.0283495
    CARAT = 0.0002
    TROY_OUNCE = 0.0311035
    TROY_POUND = 0.373242
    TROY_GRAIN = 0.00006479891


# Force:
class Forces (Enum):
    NEWTON = 1.0
    KILONEWTON = 1000.0
    MEGANEWTON = 1000000.0
    MILLINEWTON = 0.001
    POUND_FORCE = 4.44822
    KILOGRAM_FORCE = 9.80665
    POUNDAL = 0.138255
    SLUG = 14.5939
    KILOPOND = 9.80665


# Pressure:
class Pressures (Enum):
    PASCAL = 1.0
    KILOPASCAL = 1000.0
    MEGAPASCAL = 1000000.0
    GIGAPASCAL = 1000000000.0
    HECTOPASCAL = 100.0
    MILLIBAR = 100.0
    BAR = 100000.0
    ATMOSPHERE = 101325.0
    TORR = 133.322
    PSI = 6894.76

# Energy:
class Energies (Enum):
    JOULE = 1.0
    KILOJOULE = 1000.0
    CALORIE = 4.184
    KILOCALORIE = 4184.0
    WATT_HOUR = 3600.0
    KILOWATT_HOUR = 3600000.0
    ELECTRONVOLT = 1.602176634e-19
    BRITISH_THERMAL_UNIT = 1055.06
    US_THERM = 105506000.0


# Power:
class Powers (Enum):
    WATT = 1.0
    KILOWATT = 1000.0
    MEGAWATT = 1000000.0
    GIGAWATT = 1000000000.0
    HORSEPOWER = 745.7


# Frequency:
class Frequencies (Enum):
    HERTZ = 1.0
    KILOHERTZ = 1000.0
    MEGAHERTZ = 1000000.0
    GIGAHERTZ = 1000000000.0
    RPM = 1.0 / 60.0


# Angle:
_radian = 1.0
_degree = 0.0174533
_minute = 0.000290888
_second = 0.00000484814
_gradian = 0.0157079
_revolution = 6.28319

# Temperature:
_celsius = 1.0
_fahrenheit = 0.555556
_kelvin = 1.0
_rankine = 0.555556

# Time:
_second = 1.0
_millisecond = 0.001
_microsecond = 0.000001
_nanosecond = 0.000000001
_minute = 60.0
_hour = 3600.0
_day = 86400.0
_week = 604800.0
_month = 2628000.0
_year = 31536000.0
_decade = 315360000.0
_century = 3153600000.0
_millennium = 31536000000.0

# Speed:
_meter_per_second = 1.0
_kilometer_per_hour = 0.277778
_mile_per_hour = 0.44704
_knot = 0.514444
_foot_per_second = 0.3048
_mach = 340.29
_speed_of_light = 299792458.0

# Acceleration:
_meter_per_second_squared = 1.0
_gal = 0.01
_foot_per_second_squared = 0.3048
_standard_gravity = 9.80665



