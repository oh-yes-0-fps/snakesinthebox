from commands2 import CommandBase
from subsystems.Index import Index, ChamberState


class DefaultIndex(CommandBase):
    #----------Initialization----------#
    def __init__(self, _index:Index) -> None:
        super().__init__()
        self.__index = _index
        self.addRequirements(_index)

    #----------Overridden Methods----------#
    def execute(self) -> None:
        currExitState = self.__index.getExitState()
        currEnterState = self.__index.getEnterState()

        if currExitState:
            self.__index.stopMotor()
            self.__index.setChamberState(ChamberState.FULL)
            return

        if not currExitState and not currEnterState and self.__index.isMotorOn():
            self.__index.stopMotor()
            self.__index.setChamberState(ChamberState.BOTTOM)
            return

        if currEnterState:
            self.__index.startMotor()
            return
