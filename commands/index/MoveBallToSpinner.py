from commands2 import CommandBase
from subsystems.Index import Index, ChamberState


class MoveBallToSpinner(CommandBase):
    # ----------Initialization----------#
    def __init__(self, _index: Index) -> None:
        super().__init__()
        self.__index = _index
        self.__hasChambered = False
        self.__hasShot = False
        self.addRequirements(_index)

    # ----------Overridden Methods----------#
    def initialize(self) -> None:
        self.__ballsHeld = self.__index.numOfBalls()

    def execute(self) -> None:
        if self.__index.getChamberState() == ChamberState.EMPTY:
            self.__hasChambered = True
            return

        self.__index.startMotor()
        if not self.__hasShot and not self.__index.getExitState():
            self.__hasShot = True

        if self.__hasShot and self.__ballsHeld == 1:
            self.__index.stopMotor()
            self.__index.setChamberState(ChamberState.EMPTY)
            self.__hasChambered = True

        if self.__hasShot and self.__index.getExitState():
            self.__index.stopMotor()
            self.__index.setChamberState(ChamberState.TOP)
            self.__hasChambered = True

    def end(self, interrupted: bool) -> None:
        self.__index.stopMotor()

    def isFinished(self) -> bool:
        return self.__hasChambered
