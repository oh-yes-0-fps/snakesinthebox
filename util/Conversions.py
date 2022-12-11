from math import pi

#FALCONS
def falconToDegrees(_counts, _gearRatio):
    return _counts * (360.0 / (_gearRatio * 2048.0))

def degreesToFalcon(_degrees, _gearRatio):
    ticks =  _degrees / (360.0 / (_gearRatio * 2048.0))
    return ticks

def falconToRPM(_velocityCounts, _gearRatio):
    motorRPM = _velocityCounts * (600.0 / 2048.0)        
    mechRPM = motorRPM / _gearRatio
    return mechRPM

def RPMToFalcon(_RPM, _gearRatio):
    motorRPM = _RPM * _gearRatio
    sensorCounts = motorRPM * (2048.0 / 600.0)
    return sensorCounts

def falconToMPS(_velocitycounts, _circumference, _gearRatio):
    wheelRPM = falconToRPM(_velocitycounts, _gearRatio)
    wheelMPS = (wheelRPM * _circumference) / 60
    return wheelMPS

def MPSToFalcon(velocity, circumference, gearRatio):
    wheelRPM = ((velocity * 60) / circumference)
    wheelVelocity = RPMToFalcon(wheelRPM, gearRatio)
    return wheelVelocity

#Measurements
def inchesToMeters(_inches):
    return _inches * 0.0254

def metersToInches(_meters):
    return _meters * 39.3701

def radiansToDegrees(radians):
    return radians * 180.0 / pi

def degreesToRadians(_degrees):
    return _degrees * pi / 180.0

