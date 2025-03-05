import asyncio
from typing import List, Optional, Tuple


async def run_cmd(cmd: str) -> str:
    """
    Executes a shell command and returns the result.
    """
    try:
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
            raise Exception(f"Command failed: {cmd}")

        output = stdout.decode()
        print(f"Output:\n{output}")
        return output
    except Exception as e:
        print(f"Error: {e}")
        raise


async def run_cmd_args(
    cmd: str, args: List[str], background: bool = False
) -> Optional[asyncio.subprocess.Process]:
    """
    Executes a command with arguments safely.
    If background is True, the command runs in the background without blocking execution.
    """
    try:
        if background:
            process = await asyncio.create_subprocess_exec(
                cmd,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            print(f"Started in background: {cmd} {' '.join(args)} (PID: {process.pid})")
            return process  # Return process handle if needed

        # Run the command and wait for completion
        process = await asyncio.create_subprocess_exec(
            cmd, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
            raise Exception(f"Command failed: {cmd}")

        output = stdout.decode()
        print(f"Output:\n{output}")
        return process
    except Exception as e:
        print(f"Error: {e}")
        raise


async def run_cmd_input(cmd: str, inp: str) -> str:
    """
    Executes a command with provided input.
    """
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate(input=inp.encode())

        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
            raise Exception(f"Command failed: {cmd}")

        output = stdout.decode()
        print(f"Output:\n{output}")
        return output
    except Exception as e:
        print(f"Error: {e}")
        raise


async def run_cmd_timeout(cmd: str, timeout: float = 5) -> Optional[str]:
    """
    Executes a command with a timeout.
    """
    try:
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            print(f"Timeout after {timeout}s")
            return None

        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
            raise Exception(f"Command failed: {cmd}")

        output = stdout.decode()
        print(f"Output:\n{output}")
        return output
    except Exception as e:
        print(f"Error: {e}")
        raise


async def run_piped(cmds: List[str]) -> Tuple[str, str]:
    """
    Executes multiple commands in a pipeline.
    """
    try:
        # Create the initial subprocess
        process = await asyncio.create_subprocess_shell(
            cmds[0], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # Chain the other commands in the pipeline
        for cmd in cmds[1:]:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdin=process.stdout,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
            raise Exception(f"Pipeline failed")

        output = stdout.decode()
        print(f"Piped Output:\n{output}")
        return output, stderr.decode()
    except Exception as e:
        print(f"Pipeline Error: {e}")
        raise


async def main():
    await run_cmd("hyprctl dispatch workspace 1")
    await run_cmd_args("hyprctl", ["dispatch", "workspace", "2"])
    await run_cmd_input("wc -l", "Hello\nWorld\nPython")
    await run_cmd_timeout("sleep 2", timeout=3)
    await run_piped(["echo 'Hello World'", "grep World", "wc -c"])


if __name__ == "__main__":
    asyncio.run(main())
