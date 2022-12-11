from commands2 import SubsystemBase
from wpilib import PneumaticsModuleType, Solenoid
from util.McqWrappers import MCQ_TalonFX
from ctre import ControlMode, NeutralMode
from Constants import kAquisition

# from commands.Defaults.DefaultAcquisition import DefaultAcquisition
# DEFAULT_COMMAND = DefaultAcquisition

class Acquisition(SubsystemBase):
    #----------Constant Attributes / SubClasses----------#

    #----------Initialization----------#
    def __init__(self) -> None:
        super().__init__()
        self.__motorMaster = MCQ_TalonFX(kAquisition.LEFT_MOTOR_ID)
        self.__motorFollower = MCQ_TalonFX(kAquisition.RIGHT_MOTOR_ID)
        self.__motorMaster.setInverted(True)
        self.__motorFollower.follow(self.__motorMaster)
        #all these *should* apply to both motors
        self.__motorMaster.setNeutralMode(NeutralMode.Coast)
        self.__motorMaster.configPIDFdict(kAquisition.PIDF)

        self.__arms = Solenoid(60, PneumaticsModuleType.REVPH, kAquisition.ARM_SOLENOID_ID)
    #----------Overridden Methods----------#
    def periodic(self) -> None:
        pass

    #----------Instance Methods----------#
    #==Motors==
    def startRollers(self) -> None:
        self.__motorMaster.set(ControlMode.Velocity, kAquisition.ACQUISITION_VELOCITY)

    def stopRollers(self) -> None:
        self.__motorMaster.stopMotor()

    def getRollerSpeed(self, rpm:bool) -> float: #TODO: implement rpm reporting
        return self.__motorMaster.getSelectedSensorVelocity()

    #==Arms==
    def extendArms(self) -> None:
        self.__arms.set(True)

    def retractArms(self) -> None:
        self.__arms.set(False)

    def getArmsExtended(self) -> bool:
        return self.__arms.get()