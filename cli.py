import typer
from yaspin import yaspin
import json

from typing_extensions import Annotated
from dobot.dobotController import DobotController
from dobot.position import Position

cli = typer.Typer()

dobot = DobotController()

@cli.command()
def move_j_to(
    x: Annotated[float, typer.Argument(help="X coordinate to move to")],
    y: Annotated[float, typer.Argument(help="Y coordinate to move to")],
    z: Annotated[float, typer.Argument(help="Z coordinate to move to")],
    r: Annotated[float, typer.Argument(help="R coordinate to move to")],
    wait: Annotated[bool, typer.Option(help="Wait for the movement to finish")] = True,
):
    dobot.move_j_to(Position(x, y, z, r), wait)

@cli.command()
def move_l_to(
    x: Annotated[float, typer.Argument(help="X coordinate to move to")],
    y: Annotated[float, typer.Argument(help="Y coordinate to move to")],
    z: Annotated[float, typer.Argument(help="Z coordinate to move to")],
    r: Annotated[float, typer.Argument(help="R coordinate to move to")],
    wait: Annotated[bool, typer.Option(help="Wait for the movement to finish")] = True,
):
    dobot.move_l_to(Position(x, y, z, r), wait)

@cli.command()
def home(
    wait: Annotated[bool, typer.Option(help="Wait for the movement to finish")] = True
):
    dobot.home(wait)

@cli.command()
def enable_tool(
    time: Annotated[float, typer.Option(help='Wait time')] = 100
):
    dobot.enable_tool(time)
    
@cli.command()
def disable_tool(
    time: Annotated[float, typer.Option(help='Wait time')] = 100
):
    dobot.disable_tool(time)
    
@cli.command()
def current():
    dobot.pose()

@cli.command()
def set_speed(
    speed: Annotated[float, typer.Argument(help='Dobot speed')],
    acceleration: Annotated[float, typer.Argument(help='Dobot acceleration')]
):
    dobot.set_speed(speed, acceleration)

@cli.command()
def save(
    file_path: Annotated[str, typer.Argument(help="Path to save the current position")],
):

    current_position = dobot.pose()

    try:
        with open(file_path, "r") as file:
            saved_positions = json.load(file)
    except FileNotFoundError:
        saved_positions = {"positions": []}

    with open(file_path, "w") as file:
        saved_positions["positions"].append(current_position.to_dict())
        json.dump(saved_positions, file, indent=4)


@cli.command()
def run(
    file_path: Annotated[str, typer.Argument(help="Path to the file with positions")],
):
    with open(file_path, "r") as file:
        data = json.load(file)

    for position in data["bin_1"]:
        if (position["suction"]):
            enable_tool()
        else:
            disable_tool()
        spinner = yaspin(text=f"Moving to {position}...")
        current_position = Position()
        current_position.load_from_dict(position)
        dobot.move_l_to(current_position, wait=True)
        spinner.stop()
    
    for position in data["delivery"]:
        if (position["suction"]):
            enable_tool()
        else:
            disable_tool()
        spinner = yaspin(text=f"Moving to {position}...")
        current_position = Position()
        current_position.load_from_dict(position)
        dobot.move_l_to(current_position, wait=True)
        spinner.stop()

    
def main():
    port = '/dev/ttyACM0'
    spinner = yaspin(text=f"Connecting with port {port}...")
    spinner.start()
    dobot.connect(port)
    spinner.stop()
    cli()

if __name__ == '__main__':
    main()
