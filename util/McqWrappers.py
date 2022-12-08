from ctre import SupplyCurrentLimitConfiguration, WPI_TalonFX, SensorInitializationStrategy
from typing import overload

from wpilib import DigitalInput


class MCQ_TalonFX(WPI_TalonFX):
    """Wrapper for the WPI_TalonFX class to add some useful methods. I want this, fight me"""
    def __init__(self, deviceNumber:int, canbus:str = '') -> None:
        super().__init__(deviceNumber, canbus)
        self.configFactoryDefault()
        self.configIntegratedSensorInitializationStrategy(SensorInitializationStrategy.BootToZero)

    def isSpinning(self) -> bool:
        if self.getSelectedSensorVelocity() > 1 or self.getStatorCurrent() > 0.5:
            return True
        return False

    def configPIDF(self, kP:float, kI:float, kD:float, kF:float = 0) -> None:
        self.config_kP(0, kP)
        self.config_kI(0, kI)
        self.config_kD(0, kD)
        self.config_kF(0, kF)

    def configPIDFdict(self, pidf:dict[str,float]):
        self.configPIDF(pidf['kP'], pidf['kI'], pidf['kD'], pidf['kF'])

    def configPeakOutput(self, percentOut: float, timeoutMs: int = 0) -> None:
        """Applys in both directions"""
        self.configPeakOutputForward(percentOut, timeoutMs)
        self.configPeakOutputReverse(-percentOut, timeoutMs)

    def configCurrentLimit(self, currentLimit:float, currentLimitTrigger:float, currentLimitTriggerTime:float) -> None:
        self.configSupplyCurrentLimit(SupplyCurrentLimitConfiguration(True, currentLimit, currentLimitTrigger, currentLimitTriggerTime))

    #TODO: Add datalogging stuff here to remove clutter from subsystems


class MCQ_BeamBreak(DigitalInput):
    """Wrapper for the DigitalInput class to add some methods"""
    def __init__(self, channel: int) -> None:
        super().__init__(channel)
        self.__dbArray = []
        self.__debounceCycles = 0
        self.prevValue = False


    def enableDebounce(self, _debounceCycles: int) -> None:
        self.__debounceCycles = _debounceCycles
        for _ in range(_debounceCycles):
            self.__dbArray.append(False)


    def disableDebounce(self) -> None:
        self.__dbArray = []
        self.__debounceCycles = 0


    def get(self):
        if self.__debounceCycles == 0:
            return super().get()
        else:
            self.__dbArray.append(super().get() == False)
            self.__dbArray.pop(0)
            return not any(self.__dbArray)#HELP




