from math import pi

#FALCONS
def falconToDegrees(counts, gearRatio):
    return counts * (360.0 / (gearRatio * 2048.0))

def degreesToFalcon(degrees, gearRatio):
    ticks =  degrees / (360.0 / (gearRatio * 2048.0))
    return ticks

def falconToRPM(velocityCounts, gearRatio):
    motorRPM = velocityCounts * (600.0 / 2048.0)        
    mechRPM = motorRPM / gearRatio
    return mechRPM

def RPMToFalcon(RPM, gearRatio):
    motorRPM = RPM * gearRatio
    sensorCounts = motorRPM * (2048.0 / 600.0)
    return sensorCounts

def falconToMPS(velocitycounts, circumference, gearRatio):
    wheelRPM = falconToRPM(velocitycounts, gearRatio)
    wheelMPS = (wheelRPM * circumference) / 60
    return wheelMPS

def MPSToFalcon(velocity, circumference, gearRatio):
    wheelRPM = ((velocity * 60) / circumference)
    wheelVelocity = RPMToFalcon(wheelRPM, gearRatio)
    return wheelVelocity

#Measurements
def inchesToMeters(inches):
    return inches * 0.0254

def metersToInches(meters):
    return meters * 39.3701

def radiansToDegrees(radians):
    return radians * 180.0 / pi

def degreesToRadians(degrees):
    return degrees * pi / 180.0

