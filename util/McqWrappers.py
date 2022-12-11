from ctre import SupplyCurrentLimitConfiguration, WPI_TalonFX, SensorInitializationStrategy
# from typing import overload

from wpilib import DigitalInput


class MCQ_TalonFX(WPI_TalonFX):
    """Wrapper for the WPI_TalonFX class to add some useful methods. I want this, fight me"""

    def __init__(self, _deviceNumber: int, _canbus: str = '') -> None:
        super().__init__(_deviceNumber, _canbus)
        self.configFactoryDefault()
        self.configIntegratedSensorInitializationStrategy(
            SensorInitializationStrategy.BootToZero)

    def isSpinning(self) -> bool:
        if self.getSelectedSensorVelocity() > 1 or self.getStatorCurrent() > 0.5 or self.getMotorOutputPercent() > 0.03:
            return True
        return False

    def configPIDF(self, _P: float, _I: float, _D: float, _F: float = 0) -> None:
        self.config_kP(0, _P)
        self.config_kI(0, _I)
        self.config_kD(0, _D)
        self.config_kF(0, _F)

    def configPIDFdict(self, _pidf: dict[str, float]):
        self.configPIDF(_pidf['P'], _pidf['I'], _pidf['D'], _pidf['F'])

    def configPeakOutput(self, _percentOut: float, _timeoutMs: int = 0) -> None:
        """Applys in both directions"""
        self.configPeakOutputForward(_percentOut, _timeoutMs)
        self.configPeakOutputReverse(-_percentOut, _timeoutMs)

    def configCurrentLimit(self, _currentLimit: float, _currentLimitTrigger: float, _currentLimitTriggerTime: float) -> None:
        self.configSupplyCurrentLimit(SupplyCurrentLimitConfiguration(
            True, _currentLimit, _currentLimitTrigger, _currentLimitTriggerTime))

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

    def wasJust(self, _checkValue:bool) -> bool:
        if self.__get() == _checkValue and self.__prevValue != _checkValue:
            return True
        return False