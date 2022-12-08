from commands2 import CommandBase, Subsystem

class commandTMP(CommandBase):
    #----------Constant Attributes / SubClasses----------#

    #----------Initialization----------#
    def __init__(self, subsystem:Subsystem) -> None:
        super().__init__()
        self.subsystem = subsystem
        self.addRequirements(subsystem)
    #----------Static Methods----------#

    #----------Overridden Methods----------#
    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def end(self, interrupted:bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False

    #----------Instance Methods----------#