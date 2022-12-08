from commands2 import CommandScheduler
import wpilib
from wpilib import DataLogManager, TimedRobot, DriverStation
from wpiutil._wpiutil import log
from setups.RobotSetup import RobotSetup
from enum import Enum


class containers(Enum):
    PRIMARY = 0
    SECONDARY = 1
    SIMULATION = 2


__CONTAINER = containers.PRIMARY


class McQRobot(TimedRobot):

    # ----------Static methods----------
    @staticmethod
    def getDataLog() -> log.DataLog:
        return DataLogManager.getLog()

    # ----------Overridden methods----------
    # ==base robot==
    def robotInit(self) -> None:

        if __CONTAINER == containers.PRIMARY:
            _robotContainer = RobotSetup()
        else:
            raise NotImplementedError("No other containers implemented yet")

        DataLogManager.start("/U")
        DriverStation.startDataLog(self.getDataLog())

    def robotPeriodic(self) -> None:
        CommandScheduler.getInstance().run()  # type: ignore
        # TODO: gonna add it in java first but add better shuffleboard command logging

    # ==disabled==

    def disabledInit(self) -> None:
        DataLogManager.getLog().flush()

    def disabledPeriodic(self) -> None:
        pass

    # ==autonomous==
    def autonomousInit(self) -> None:
        pass  # TODO: add autonomous command initialization

    def autonomousPeriodic(self) -> None:
        pass

    # ==teleop==
    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        pass

    # ----------Instance methods----------


if __name__ == "__main__":
    wpilib.run(McQRobot)
