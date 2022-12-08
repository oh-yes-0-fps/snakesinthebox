from commands2 import SubsystemBase
from Constants import kIndex

from util.McqWrappers import MCQ_TalonFX


class Index(SubsystemBase):
    #----------Constant Attributes / SubClasses----------#

    #----------Initialization----------#
    def __init__(self) -> None:
        self.__motor = MCQ_TalonFX(kIndex.INDEX_MOTOR_ID)
        
    #----------Static Methods----------#

    #----------Overridden Methods----------#
    def periodic(self) -> None:
        pass

    #----------Instance Methods----------#