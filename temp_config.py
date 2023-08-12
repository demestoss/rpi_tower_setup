#from enum import Enum
from types import SimpleNamespace

#class Temperature(Enum):
#    Normal = 43.0
#    Medium = 48.0
#    High   = 60.0

temperatureDict = {
    "Normal": 44.0,
    "Medium": 49.0,
    "High":   60.0
}
Temperature = SimpleNamespace(**temperatureDict)

