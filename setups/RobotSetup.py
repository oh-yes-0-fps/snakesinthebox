from typing import Optional
from commands2 import InstantCommand, Subsystem
from wpilib import Joystick, XboxController
from subsystems.Swerve import Swerve
from util.ButtonInterface import Button
from commands.Defaults.DefaultSwerve import DefaultSwerve


class RobotSetup:

    __driver = Joystick(0)

    __yAxis_id: int = XboxController.Axis.kLeftY
    __xAxis_id: int = XboxController.Axis.kLeftX
    __rAxis_id: int = XboxController.Axis.kRightX

    def configureButtonBindings(self):
        # TODO: Add button bindings
        Button(self.__driver, XboxController.Button.kA).whenPressed(
            InstantCommand(lambda: print("Hello World!")))

    class Subsystems:
        Swerve = Swerve()

        def get(self, subsystem: str) -> Optional[Subsystem]:
            return getattr(self, subsystem, None)

    def __init__(self) -> None:
        self.Subsystems.Swerve.setDefaultCommand(DefaultSwerve(
            self.Subsystems.Swerve, self.__driver, self.__yAxis_id, self.__xAxis_id, self.__rAxis_id, True, False))
