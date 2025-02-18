import typer
from yaspin import yaspin
import json
import os

from typing_extensions import Annotated
from dobot.dobotController import DobotController
from dobot.position import Position

cli = typer.Typer()
home_file_path = "config.json"

with open(home_file_path, "r") as file:
    home_saved_positions = json.load(file)
    
    home_position = Position()
    home_position.home_from_dict(home_saved_positions["home"])

dobot = DobotController(home_position)

@cli.command()
def move_to(
    x: Annotated[float, typer.Argument(help="X coordinate to move to")],
    y: Annotated[float, typer.Argument(help="Y coordinate to move to")],
    z: Annotated[float, typer.Argument(help="Z coordinate to move to")],
    r: Annotated[float, typer.Argument(help="R coordinate to move to")],
    wait: Annotated[bool, typer.Option(help="Wait for the movement to finish")] = True,
):
    dobot.move_to(Position(x, y, z, r), wait)


@cli.command()
def home(
    wait: Annotated[bool, typer.Option(help="Wait for the movement to finish")] = True
):
    dobot.home(wait)


@cli.command()
def set_home(
    x: Annotated[float, typer.Argument(help="X coordinate to set home")],
    y: Annotated[float, typer.Argument(help="Y coordinate to set home")],
    z: Annotated[float, typer.Argument(help="Z coordinate to set home")],
    r: Annotated[float, typer.Argument(help="R coordinate to set home")],
):

    try:
        with open(home_file_path, "r") as file:
            saved_positions = json.load(file)
    except FileNotFoundError:
        saved_positions = {"home": []}

    saved_positions["home"] = (Position(x, y, z, r).to_home_dict())

    with open(home_file_path, "w") as file:
        json.dump(saved_positions, file, indent=4)

    dobot.set_home(Position(x, y, z, r))

@cli.command()
def enable_tool(
    time: Annotated[float, typer.Option(help='Wait time')]
):
    dobot.enable_tool(time)
    
@cli.command()
def disable_tool(
    time: Annotated[float, typer.Option(help='Wait time')]
):
    dobot.disable_tool(time)
    
@cli.command()
def current():
    dobot.pose()

@cli.command()
def set_speed(
    speed: Annotated[float, typer.Option(help='Dobot speed')],
    acceleration: Annotated[float, typer.Option(help='Dobot acceleration')]
):
    dobot.set_speed(speed, acceleration)

@cli.command()
def save(
    save_file_path: Annotated[str, typer.Argument(help="Path .json to save the current position")]
        ):
    
    current_position = dobot.pose()

    try:
        with open(save_file_path, "r") as file:
            saved_positions = json.load(file)
    except FileNotFoundError:
        saved_positions = {"positions": []}

    with open(save_file_path, "w") as file:
        saved_positions["positions"].append(current_position.to_dict())
        json.dump(saved_positions, file, indent=4)

@cli.command()
def run(
    run_file_path: Annotated[str, typer.Argument(help="Path .json to the file with positions")]
    ):
    with open(run_file_path, "r") as file:
        data = json.load(file)
    
    for position in data["positions"]:
        spinner = yaspin(text=f"Moving to {position}...")
        current_position = Position()
        current_position.load_from_dict(position)
        dobot.move_to(current_position, wait=True)
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
