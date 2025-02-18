import pydobot
from .position import Position

class DobotController:
    def __init__(self, home_position: Position):
        self.tool_enable = False
        self.home_position = home_position
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
        print(current_position)
    
    def set_speed(self, speed, acceleration):
        self.dobot.speed(speed, acceleration)

    def move_to(self, position, wait=True):
        self.dobot.move_to(*position.to_list(), wait=wait)

    def set_home(self, position): 
        self.home_position = position

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