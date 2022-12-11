#Everything in here has to be static and caps
from math import pi
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.geometry import Translation2d
from wpimath.trajectory import TrapezoidProfile
from ctre import NeutralMode
from util.Conversions import inchesToMeters
from typing import Any


STICK_DEADZONE = 0.05

class final:
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == __name.upper():
            pass
        else:
            super().__setattr__(__name, __value)

class SwerveModuleConstants:
    def __init__(self, drive_motor_id, angle_motor_id, can_coder_id, angle_offset) -> None:
        self.drive_motor_id = drive_motor_id
        self.angle_motor_id = angle_motor_id
        self.can_coder_id = can_coder_id
        self.angle_offset = angle_offset

class kSwerve(final):
    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    class kModule:
        def __init__(self, drive_motor_id:int, angle_motor_id:int, can_coder_id:int, angle_offset:float) -> None:
            self.DRIVE_MOTOR_ID = drive_motor_id
            self.ANGLE_MOTOR_ID = angle_motor_id
            self.CAN_CODER_ID = can_coder_id
            self.ANGLE_OFFSET = angle_offset
            self.CONSTANTS = SwerveModuleConstants(self.DRIVE_MOTOR_ID, self.ANGLE_MOTOR_ID, self.CAN_CODER_ID, self.ANGLE_OFFSET)

    #convert to python
    canivoreName = "McQDriveBus"
    PIDGEON_ID = 33
    INVERT_GYRO = False # Always ensure Gyro is CCW+ CW-

    # Drivetrain Constants
    TRACK_WIDTH = inchesToMeters(21.73)
    WHEEL_BASE = inchesToMeters(21.73)
    WHEEL_DIAMETER = inchesToMeters(3.94)
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * pi

    OPEN_LOOP_RAMP = 0.25
    CLOSED_LOOP_RAMP = 0.0

    DRIVE_GEAR_RATIO = (6.86 / 1.0) # 6.86:1
    ANGLE_GEAR_RATIO = (12.8 / 1.0) # 12.8:1

    SWERVE_KINEMATICS = SwerveDrive4Kinematics(
        Translation2d(WHEEL_BASE / 2.0, TRACK_WIDTH / 2.0),
        Translation2d(WHEEL_BASE / 2.0, -TRACK_WIDTH / 2.0),
        Translation2d(-WHEEL_BASE / 2.0, TRACK_WIDTH / 2.0),
        Translation2d(-WHEEL_BASE / 2.0, -TRACK_WIDTH / 2.0))

    # Swerve Current Limiting
    ANGLE_CONTINOUS_CURRENT_LIMIT = 25
    ANGLE_PEEK_CURRENT_LIMIT = 40
    ANGLE_PEAK_CURRENT_DURATION = 0.1
    ANGLE_ENABLE_CURRENT_LIMIT = True

    DRIVE_CONTINUOUS_CURRENT_LIMIT = 35
    DRIVE_PEAK_CURRENT_LIMIT = 60
    DRIVE_PEAK_CURRENT_DURATION = 0.1
    DRIVE_ENABLE_CURRENT_LIMIT = True

    # Angle Motor PID Values
    ANGLE_KP = 0.6
    ANGLE_KI = 0.0
    ANGLE_KD = 12.0
    ANGLE_KF = 0.0

    # Drive Motor PID Values
    DRIVE_KP = 0.10
    DRIVE_KI = 0.0
    DRIVE_KD = 0.0
    DRIVE_KF = 0.0

    # Drive Motor Characterization Values
    DRIVE_KS = (0.667 / 12) # divide by 12 to convert from volts to percent output for CTRE
    DRIVE_KV = (2.44 / 12)
    DRIVE_KA = (0.27 / 12)

    # Swerve Profiling Values
    DRIVE_SPEED_MULT = 1.0 # drive speed
    ANGEL_SPEED_MULT = 1.0 # drive speed
    MAX_SPEED = 4.5
    MAX_ANGULAR = 11.5
    ADJUSTED_MAX_SPEED = MAX_SPEED * DRIVE_SPEED_MULT # meters per second
    ADJUSTED_MAX_ANGULAR = MAX_ANGULAR * ANGEL_SPEED_MULT

    # Neutral Modes
    ANGLE_NEUTRAL_MODE = NeutralMode.Coast
    DRIVE_NEUTRAL_MODE = NeutralMode.Brake

    # Motor Inverts
    DRIVE_MOTOR_INVERT = False
    ANGLE_MOTOR_INVERT = False

    # Angle Encoder Invert
    CAN_CODER_INVERT = False

    # Module Specific Constants
    # Front Left Module - Module 0
    Mod0 = kModule(1, 2, 21, 74.7)
    # Front Right Module - Module 1
    Mod1 = kModule(3, 4, 22, 298.5)
    # Back Left Module - Module 2
    Mod2 = kModule(5, 6, 23, 251.4)
    # Back Right Module - Module 3
    Mod3 = kModule(7, 8, 24, 14.3)

class kAquisition(final):
    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    ACQUISITION_VELOCITY = 8000
    LEFT_MOTOR_ID = 10
    RIGHT_MOTOR_ID = 9
    ARM_SOLENOID_ID = 0
    PIDF = {"P": 0.1, "I": 0.0, "D": 0.0, "F": 0.05}

class kIndex(final):
    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    INDEX_MOTOR_ID = 12
    BB_ENTER_PIN = 11
    BB_EXIT_PIN = 12
    INDEX_PERCENTOUT = 0.33

