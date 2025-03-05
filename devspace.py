from libs.hyprland import Hyprland
from libs.shell import run_cmd, run_cmd_args
import asyncio

TERM = "alacritty"
MULTIPLEXER = "tmux"
GUI_EDITOR = "code"
CLI_EDITOR = "nvim"


async def main():
    hyprland = Hyprland()

    await hyprland.set_workspace(1)
    await run_cmd_args(GUI_EDITOR, ["--new-window"])
    await asyncio.sleep(1)  # wait for the window to open

    await hyprland.set_workspace(10)
    # start a terminal in the background, disown it
    await run_cmd(f"alacritty &>/dev/null &")


asyncio.run(main())
