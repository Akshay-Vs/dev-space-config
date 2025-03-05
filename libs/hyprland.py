from . import shell


class Hyprland:
    async def __init__(self, workspace_number=1) -> None:
        self.workspace = "hyprland"
        self.set_workspace(workspace_number)
        self.workspace_number = workspace_number

    def get_workspace(self):
        return self.workspace

    async def set_workspace(self, workspace_number: int) -> None:
        try:
            if workspace_number == self.workspace_number:
                return

            await shell.run_cmd_args(
                "hyprctl", ["dispatch", "workspace", str(workspace_number)]
            )
            self.workspace_number = workspace_number
        except Exception as e:
            print(f"Error: {e}")

        except ValueError as e:
            print(f"Error: {e}")
