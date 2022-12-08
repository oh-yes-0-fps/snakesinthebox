from re import T
from typing import Callable
from commands2 import Command, CommandScheduler
from wpilib.interfaces._interfaces import GenericHID

#Don't change this
__KITERUPTIBLE = True

#TODO: actually just copy wpilibJ and separate trigger and button so u can do "#or", "#and", "#negate", "#debounce"
#      ideally make it so code that uses this interface doesn't have to be changed in any way

class ButtonFunc:
    def __init__(self, condition:str, button, command:Command) -> None:
        self.__condition = condition
        self.__button = button
        self.__lastPressed = button.get()
        self.__command = command

    def get(self) -> bool:
        return self.__button.get()

    def __call__(self) -> None:
        if self.__condition == "whenPressed":
            if not self.__lastPressed and self.get():
                self.__command.schedule(__KITERUPTIBLE)
            self.__lastPressed = self.get()
        elif self.__condition == "whenReleased":
            if self.__lastPressed and not self.get():
                self.__command.schedule(__KITERUPTIBLE)
            self.__lastPressed = self.get()
        elif self.__condition == "whileHeld":
            if self.get():
                self.__command.schedule()
        elif self.__condition == "toggleWhenPressed":
            if not self.__lastPressed and self.get():
                if self.__command.isScheduled():
                    self.__command.cancel()
                else:
                    self.__command.schedule(__KITERUPTIBLE)
            self.__lastPressed = self.get()
        elif self.__condition == "cancelWhenPressed":
            if not self.__lastPressed and self.get() and self.__command.isScheduled():
                self.__command.cancel()
            self.__lastPressed = self.get()
        else:
            raise ValueError("Invalid condition")

class Button:

    @staticmethod
    def addButtonWrapper(buttonFunc:Callable) -> None:
        CommandScheduler.getInstance().addButton(buttonFunc)

    def __init__(self, _humanInputDevice:GenericHID, _buttonNumber:int) -> None:
        self.__humanInputDevice = _humanInputDevice
        self.__buttonNumber = _buttonNumber

    def get(self) -> bool:
        return self.__humanInputDevice.getRawButton(self.__buttonNumber)

    def whenPressed(self, _command:Command) -> None:
        Button.addButtonWrapper(ButtonFunc("whenPressed", self, _command))

    def whenReleased(self, _command:Command) -> None:
        Button.addButtonWrapper(ButtonFunc("whenReleased", self, _command))

    def whileHeld(self, _command:Command) -> None:
        Button.addButtonWrapper(ButtonFunc("whileHeld", self, _command))

    def toggleWhenPressed(self, _command:Command) -> None:
        Button.addButtonWrapper(ButtonFunc("toggleWhenPressed", self, _command))

    def cancelWhenPressed(self, _command:Command) -> None:
        Button.addButtonWrapper(ButtonFunc("cancelWhenPressed", self, _command))