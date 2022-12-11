from commands2 import SubsystemBase
from ctre import ControlMode
from Constants import kIndex
from enum import Enum
from util.McqWrappers import MCQ_TalonFX, MCQ_BeamBreak

# from commands.Defaults.DefaultIndex import DefaultIndex
# DEFAULT_COMMAND = DefaultIndex

class ChamberState(Enum):
    EMPTY = 0
    BOTTOM = 1
    TOP = 1
    FULL = 2

class Index(SubsystemBase):
    #----------Initialization----------#
    def __init__(self) -> None:
        super().__init__()
        self.__motor = MCQ_TalonFX(kIndex.INDEX_MOTOR_ID)
        self.__bbEnter = MCQ_BeamBreak(kIndex.BB_ENTER_PIN)
        self.__bbExit = MCQ_BeamBreak(kIndex.BB_EXIT_PIN)
        self.__chamberState = ChamberState.EMPTY

        self.__bbEnter.invert(True)
        self.__bbExit.invert(True)

    #----------Overridden Methods----------#
    def periodic(self) -> None:
        pass

    #----------Instance Methods----------#
    def startMotor(self, _speedMult:float = 1) -> None:
        """supports negative speeds for reverse indexing"""
        self.__motor.set(ControlMode.PercentOutput, kIndex.INDEX_PERCENTOUT*_speedMult)

    def stopMotor(self) -> None:
        self.__motor.stopMotor()

    def isMotorOn(self) -> bool:
        return self.__motor.isSpinning()

    def getChamberState(self) -> ChamberState:
        return self.__chamberState

    def setChamberState(self, state:ChamberState) -> None:
        self.__chamberState = state

    def numOfBalls(self) -> int:
        return self.__chamberState.value

    def wasEnterJustBroken(self) -> bool:
        return self.__bbEnter.wasJust(True)

    def wasExitJustBroken(self) -> bool:
        return self.__bbExit.wasJust(True)

    def getExitState(self) -> bool:
        return self.__bbExit.get()

    def getEnterState(self) -> bool:
        return self.__bbEnter.get()