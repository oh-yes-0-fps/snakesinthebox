from commands2 import CommandBase, Subsystem
from wpilib import Joystick
from subsystems.Swerve import Swerve
from wpimath.geometry import Translation2d
from Constants import STICK_DEADZONE, kSwerve

class DefaultSwerve(CommandBase):
    #----------Constant Attributes / SubClasses----------#

    #----------Initialization----------#
    def __init__(self, _swerve:Swerve, _controller:Joystick, _translationAxis:int, _strafeAxis:int, _rotationAxis:int,
                    _fieldRelative:bool, _openLoop:bool) -> None:
        super().__init__()
        self.__swerve = _swerve
        self.addRequirements(_swerve)

        self.__controller = _controller
        self.__translationAxis = _translationAxis
        self.__strafeAxis = _strafeAxis
        self.__rotationAxis = _rotationAxis
        self.__fieldRelative = _fieldRelative
        self.__openLoop = _openLoop

    #----------Overridden Methods----------#
    def execute(self) -> None:
        yAxis:float = self.__controller.getRawAxis(self.__translationAxis)
        xAxis:float = self.__controller.getRawAxis(self.__strafeAxis)
        rAxis:float = self.__controller.getRawAxis(self.__rotationAxis)

        #Deadzone stuff
        if (abs(yAxis) < STICK_DEADZONE):
            yAxis = 0
        if (abs(xAxis) < STICK_DEADZONE):
            xAxis = 0
        if (abs(rAxis) < STICK_DEADZONE):
            rAxis = 0

        translation = Translation2d(yAxis, xAxis)*kSwerve.ADJUSTED_MAX_SPEED
        rotation = rAxis*kSwerve.ADJUSTED_MAX_ANGULAR
        self.__swerve.drive(translation, rotation, self.__fieldRelative, self.__openLoop)