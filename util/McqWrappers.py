from ctre import SupplyCurrentLimitConfiguration, WPI_TalonFX, SensorInitializationStrategy
from typing import overload


class MCQ_TalonFX(WPI_TalonFX):
    """Wrapper for the WPI_TalonFX class to add some useful methods. I want this, fight me"""
    def __init__(self, deviceNumber:int, canbus:str = '') -> None:
        super().__init__(deviceNumber, canbus)
        self.configFactoryDefault()
        self.configIntegratedSensorInitializationStrategy(SensorInitializationStrategy.BootToZero)

    def configPIDF(self, kP:float, kI:float, kD:float, kF:float = 0) -> None:
        self.config_kP(0, kP)
        self.config_kI(0, kI)
        self.config_kD(0, kD)
        self.config_kF(0, kF)

    def configPeakOutput(self, percentOut: float, timeoutMs: int = 0) -> None:
        """Applys in both directions"""
        self.configPeakOutputForward(percentOut, timeoutMs)
        self.configPeakOutputReverse(-percentOut, timeoutMs)

    def configCurrentLimit(self, currentLimit:float, currentLimitTrigger:float, currentLimitTriggerTime:float) -> None:
        self.configSupplyCurrentLimit(SupplyCurrentLimitConfiguration(True, currentLimit, currentLimitTrigger, currentLimitTriggerTime))

    #TODO: Add datalogging stuff here to remove clutter from subsystems



