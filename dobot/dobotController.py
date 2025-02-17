import pydobot
from .position import Position

class DobotController:
    def __init__(self):
        self.tool_enable = False
        self.home_position = Position(
            100.0, 0.0, 150.0, 0.0, 0.0, 0.0, 0.0, 0.0, False, False
        )
        self.conected = False

    def connect(self, port):
        self.dobot = pydobot.Dobot(port=port, verbose=False)
        self.conect = True
        
    def disconect(self):
        self.dobot.close
        self.conected = False

    def pose(self):
        current_position = Position(*self.dobot.pose())
        current_position.suck == self.tool_enable
        return current_position
    
    def set_speed(self, speed, acceleration):
        self.dobot.speed(speed, acceleration)

    def move_to(self, position, wait=True):
        self.dobot.move_to(*position.to_list(), wait=wait)


    def home(self, wait=True):
            self.move_to(self.home_position, wait=wait)
        
    def enable_tool(self, time):
        self.dobot.suck(True)
        self.dobot.wait(time)
        self.tool_enabled = True

    def disable_tool(self, time):
        self.dobot.suck(False)
        self.dobot.wait(time)
        self.tool_enabled = False