from commands2 import SubsystemBase
from ctre import CANCoder, AbsoluteSensorRange, SensorInitializationStrategy, WPI_Pigeon2
from util.McqWrappers import MCQ_TalonFX
from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.kinematics import SwerveModuleState, SwerveDrive4Odometry, ChassisSpeeds, SwerveDrive4Kinematics
from wpimath.geometry import Rotation2d, Translation2d, Pose2d
from Constants import kSwerve
import util.Conversions as Conversions
from Constants import SwerveModuleConstants

# from commands.Defaults.DefaultSwerve import DefaultSwerve
# DEFAULT_COMMAND = DefaultSwerve



class CTRE_SwerveModuleState:

    @staticmethod
    def optimize(desiredState:SwerveModuleState, currentAngle:Rotation2d):
        targetAngle:float = CTRE_SwerveModuleState.placeInAppropriate0To360Scope(currentAngle.degrees(), desiredState.angle.degrees())#type: ignore
        targetSpeed:float = desiredState.speed
        delta:float = targetAngle - float(currentAngle.degrees()) #type: ignore
        if abs(delta) > 90:                                       #^^^^^^^^^^^^ weird whats happening here
            targetSpeed = -targetSpeed
            if delta > 90:
                targetAngle -= 180
            else:
                targetAngle += 180
        return SwerveModuleState(targetSpeed, Rotation2d.fromDegrees(targetAngle))

    @staticmethod
    def placeInAppropriate0To360Scope(scopeReference:float, newAngle:float):
        lowerBound:float
        upperBound:float
        lowerOffset:float = scopeReference % 360
        if lowerOffset >= 0:
            lowerBound = scopeReference - lowerOffset
            upperBound = scopeReference + (360 - lowerOffset)
        else:
            upperBound = scopeReference - lowerOffset
            lowerBound = scopeReference - (360 + lowerOffset)
        while newAngle < lowerBound:
            newAngle += 360
        while newAngle > upperBound:
            newAngle -= 360
        if newAngle - scopeReference > 180:
            newAngle -= 360
        elif newAngle - scopeReference < -180:
            newAngle += 360
        return newAngle




class SwerveModule:
    # ----------Constant Attributes / SubClasses----------#
    __feedforward = SimpleMotorFeedforwardMeters(
        kSwerve.DRIVE_KS, kSwerve.DRIVE_KV, kSwerve.DRIVE_KA)

    # ----------Initialization----------#
    def __init__(self, _moduleNumber: int, canivore: str, ModuleConstants: SwerveModuleConstants) -> None:
        self.moduleNumber = _moduleNumber
        self.__angleOffset = ModuleConstants.angle_offset

        # Angle Encoder Config
        self.__angleEncoder = CANCoder(ModuleConstants.can_coder_id, canivore)
        self.__angleEncoder.configAbsoluteSensorRange(
            AbsoluteSensorRange.Unsigned_0_to_360)
        self.__angleEncoder.configSensorDirection(kSwerve.CAN_CODER_INVERT)
        self.__angleEncoder.configSensorInitializationStrategy(
            SensorInitializationStrategy.BootToAbsolutePosition)

        # Angle Motor Config
        self.__angleMotor = MCQ_TalonFX(
            ModuleConstants.angle_motor_id, canivore)
        self.__angleMotor.configPIDF(
            kSwerve.ANGLE_KP, kSwerve.ANGLE_KI, kSwerve.ANGLE_KD, kSwerve.ANGLE_KF)
        self.__angleMotor.configCurrentLimit(
            kSwerve.ANGLE_CONTINOUS_CURRENT_LIMIT, kSwerve.ANGLE_PEEK_CURRENT_LIMIT, kSwerve.ANGLE_PEAK_CURRENT_DURATION)

        # Drive Motor Config
        self.__driveMotor = MCQ_TalonFX(
            ModuleConstants.drive_motor_id, canivore)
        self.__driveMotor.configPIDF(
            kSwerve.DRIVE_KP, kSwerve.DRIVE_KI, kSwerve.DRIVE_KD, kSwerve.DRIVE_KF)
        self.__driveMotor.configCurrentLimit(
            kSwerve.DRIVE_CONTINUOUS_CURRENT_LIMIT, kSwerve.DRIVE_PEAK_CURRENT_LIMIT, kSwerve.DRIVE_PEAK_CURRENT_DURATION)

        lastAngle = Conversions.falconToDegrees(self.__angleMotor.getSelectedSensorPosition(), kSwerve.ANGLE_GEAR_RATIO)

    # ----------Instance Methods----------#
    def setDesiredState(self, desiredState: SwerveModuleState, isOpenLoop: bool) -> None:
        desiredState = CTRE_SwerveModuleState.optimize(desiredState, self.getState().angle)

        if isOpenLoop:
            percentOutput = desiredState.speed / kSwerve.ADJUSTED_MAX_SPEED
            self.__driveMotor.set(percentOutput)
        else:
            velocity = Conversions.MPSToFalcon(desiredState.speed,
                                               kSwerve.WHEEL_CIRCUMFERENCE, kSwerve.DRIVE_GEAR_RATIO) * kSwerve.DRIVE_SPEED_MULT
            self.__driveMotor.set(velocity, self.__feedforward.calculate(
                desiredState.speed))

        if abs(desiredState.speed) <= (kSwerve.ADJUSTED_MAX_SPEED * 0.03):
            angle = self.lastAngle
        else: #TODO: figure out if Rotation2d#degrees() is working as intended
            angle = float(desiredState.angle.degrees())#type: ignore
        self.__angleMotor.set(Conversions.degreesToFalcon(
            angle, kSwerve.ANGLE_GEAR_RATIO))
        self.lastAngle = angle


    def getState(self) -> SwerveModuleState:
        velocity: float = Conversions.falconToMPS(self.__driveMotor.getSelectedSensorVelocity(
        ), kSwerve.WHEEL_CIRCUMFERENCE, kSwerve.DRIVE_GEAR_RATIO)
        angle = Rotation2d.fromDegrees(Conversions.falconToDegrees(
            self.__angleMotor.getSelectedSensorPosition(), kSwerve.ANGLE_GEAR_RATIO))
        return SwerveModuleState(velocity, angle)

    def getCanCoder(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.__angleEncoder.getAbsolutePosition())

    def getDriveMotor(self) -> MCQ_TalonFX:
        return self.__driveMotor


class Swerve(SubsystemBase):
    # ----------Constant Attributes / SubClasses----------#

    # ----------Initialization----------#
    def __init__(self) -> None:
        super().__init__()
        self.gyro = WPI_Pigeon2(kSwerve.PIDGEON_ID, kSwerve.canivoreName)
        self.gyro.configFactoryDefault()
        self.zeroGyro()

        self.swerveOdometry = SwerveDrive4Odometry(kSwerve.SWERVE_KINEMATICS, self.getYaw())

        self.swerveMods:tuple[SwerveModule, SwerveModule, SwerveModule, SwerveModule] = (
            SwerveModule(0, kSwerve.canivoreName, kSwerve.Mod0.CONSTANTS),
            SwerveModule(1, kSwerve.canivoreName, kSwerve.Mod1.CONSTANTS),
            SwerveModule(2, kSwerve.canivoreName, kSwerve.Mod2.CONSTANTS),
            SwerveModule(3, kSwerve.canivoreName, kSwerve.Mod3.CONSTANTS)
        )
    # ----------Overridden Methods----------#
    def periodic(self) -> None:
        pass

    # ----------Instance Methods----------#
    def getYaw(self) -> Rotation2d:
        ypr = self.gyro.getYawPitchRoll()[1]
        if kSwerve.INVERT_GYRO:
            return Rotation2d.fromDegrees(360 - ypr[0])
        return Rotation2d.fromDegrees(ypr[0])

    def drive(self, translation:Translation2d, rotation:float, fieldRelative:bool, isOpenLoop:bool) -> None:
        if fieldRelative:
            chassisSpeedParam = ChassisSpeeds.fromFieldRelativeSpeeds(translation.x, translation.y, rotation, self.getYaw())
        else:
            chassisSpeedParam = ChassisSpeeds(translation.x, translation.y, rotation)
        swerveModuleStates:tuple = kSwerve.SWERVE_KINEMATICS.toSwerveModuleStates(chassisSpeedParam)
        SwerveDrive4Kinematics.desaturateWheelSpeeds(swerveModuleStates, kSwerve.ADJUSTED_MAX_SPEED)

        for mod in self.swerveMods:
            mod.setDesiredState(swerveModuleStates[mod.moduleNumber], isOpenLoop)

    def getPose(self) -> Pose2d:
        return self.swerveOdometry.getPose()

    def resetOdometry(self, pose:Pose2d) -> None:
        self.swerveOdometry.resetPosition(pose, self.getYaw())

    def setModuleStates(self, states:tuple[SwerveModuleState, SwerveModuleState, SwerveModuleState, SwerveModuleState]) -> None:
        SwerveDrive4Kinematics.desaturateWheelSpeeds(states, kSwerve.ADJUSTED_MAX_SPEED)
        for mod in self.swerveMods:
            mod.setDesiredState(states[mod.moduleNumber], False)

    def getModuleStates(self) -> tuple[SwerveModuleState, SwerveModuleState, SwerveModuleState, SwerveModuleState]:
        return tuple(mod.getState() for mod in self.swerveMods)

    def zeroGyro(self) -> None:
        self.gyro.setYaw(0)
