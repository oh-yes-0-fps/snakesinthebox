from commands2 import CommandBase
from subsystems.Index import Index, ChamberState
from subsystems.Acquisition import Acquisition

class DefaultAcquisition(CommandBase):

    #----------Initialization----------#
    def __init__(self, _acquisition:Acquisition, _index:Index) -> None:
        super().__init__()
        self.__acquisition = _acquisition
        self.__index = _index
        self.addRequirements(_acquisition)#exclude index as its just data polling

    #----------Overridden Methods----------#
    def execute(self) -> None:
        if self.__index.getChamberState() == ChamberState.FULL and self.__acquisition.getArmsExtended():
            self.__acquisition.retractArms()
        if self.__acquisition.getArmsExtended():
            self.__acquisition.startRollers()
        else:
            self.__acquisition.stopRollers()
