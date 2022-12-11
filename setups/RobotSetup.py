from typing import Optional
from commands2 import InstantCommand, Subsystem
from wpilib import Joystick, XboxController
import subsystems.Swerve as Swerve
import subsystems.Index as Index
import subsystems.Acquisition as Acquisition
from util.ButtonInterface import Button
from commands.CommandDir import * #do this just to make imports here a lil cleaner


class RobotSetup:

    __driver = Joystick(0)

    __yAxis_id: int = XboxController.Axis.kLeftY
    __xAxis_id: int = XboxController.Axis.kLeftX
    __rAxis_id: int = XboxController.Axis.kRightX

    def configureButtonBindings(self):
        # TODO: Add button bindings
        Button(self.__driver, XboxController.Button.kA).whenPressed(
            InstantCommand(lambda: print("Hello World!")))
        Button(self.__driver, XboxController.Button.kRightBumper).whenPressed(
            InstantCommand(lambda: self.Subsystems.i_Acquisition.extendArms()))
        Button(self.__driver, XboxController.Button.kLeftBumper).whenPressed(
            InstantCommand(lambda: self.Subsystems.i_Acquisition.retractArms()))

    class Subsystems:
        i_Swerve = Swerve.Swerve()
        i_Acquisition = Acquisition.Acquisition()
        i_Index = Index.Index()

        def get(self, subsystem: str) -> Optional[Subsystem]:
            return getattr(self, subsystem, None)

    def __init__(self) -> None:
        self.Subsystems.i_Swerve.setDefaultCommand(cDefaultSwerve(
            self.Subsystems.i_Swerve, self.__driver, self.__yAxis_id, self.__xAxis_id, self.__rAxis_id, True, False))
        self.Subsystems.i_Acquisition.setDefaultCommand(cDefaultAcquisition(self.Subsystems.i_Acquisition, self.Subsystems.i_Index))
        self.Subsystems.i_Index.setDefaultCommand(cDefaultIndex(self.Subsystems.i_Index))
