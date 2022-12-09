from ctre import SupplyCurrentLimitConfiguration, WPI_TalonFX, SensorInitializationStrategy
from typing import overload

from wpilib import DigitalInput


class MCQ_TalonFX(WPI_TalonFX):
    """Wrapper for the WPI_TalonFX class to add some useful methods. I want this, fight me"""

    def __init__(self, deviceNumber: int, canbus: str = '') -> None:
        super().__init__(deviceNumber, canbus)
        self.configFactoryDefault()
        self.configIntegratedSensorInitializationStrategy(
            SensorInitializationStrategy.BootToZero)

    def isSpinning(self) -> bool:
        if self.getSelectedSensorVelocity() > 1 or self.getStatorCurrent() > 0.5 or self.getMotorOutputPercent() > 0.03:
            return True
        return False

    def configPIDF(self, kP: float, kI: float, kD: float, kF: float = 0) -> None:
        self.config_kP(0, kP)
        self.config_kI(0, kI)
        self.config_kD(0, kD)
        self.config_kF(0, kF)

    def configPIDFdict(self, pidf: dict[str, float]):
        self.configPIDF(pidf['kP'], pidf['kI'], pidf['kD'], pidf['kF'])

    def configPeakOutput(self, percentOut: float, timeoutMs: int = 0) -> None:
        """Applys in both directions"""
        self.configPeakOutputForward(percentOut, timeoutMs)
        self.configPeakOutputReverse(-percentOut, timeoutMs)

    def configCurrentLimit(self, currentLimit: float, currentLimitTrigger: float, currentLimitTriggerTime: float) -> None:
        self.configSupplyCurrentLimit(SupplyCurrentLimitConfiguration(
            True, currentLimit, currentLimitTrigger, currentLimitTriggerTime))

    # TODO: Add datalogging stuff here to remove clutter from subsystems


class MCQ_BeamBreak(DigitalInput):
    """Wrapper for the DigitalInput class to add some methods"""

    def __init__(self, channel: int) -> None:
        super().__init__(channel)
        self.__dbArray = []
        self.__debounceCycles = 0
        self.__prevValue = False
        self.__inverted = False

    def invert(self, enable:bool) -> None:
        self.__inverted = enable

    def enableDebounce(self, _debounceCycles: int) -> None:
        self.__debounceCycles = _debounceCycles
        for _ in range(_debounceCycles):
            self.__dbArray.append(False)

    def disableDebounce(self) -> None:
        self.__dbArray = []
        self.__debounceCycles = 0

    def __get(self):
        if self.__debounceCycles == 0:
            return super().get() != self.__inverted
        else:
            self.__dbArray.append(super().get() != self.__inverted)
            self.__dbArray.pop(0)
            if self.__inverted:
                return not any(self.__dbArray)#help
            return all(self.__dbArray)        #why does this hurt my head

    def get(self) -> bool:
        outVal = self.__get()
        self.__prevValue = outVal
        return outVal

    def wasJust(self, checkValue:bool) -> bool:
        if self.__get() == checkValue and self.__prevValue != checkValue:
            return True
        return False