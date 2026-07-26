import sys
from pathlib import Path

# Prevent package shadowing: remove 'client/' from sys.path and add the project root
script_dir = str(Path(__file__).resolve().parent)
if script_dir in sys.path:
    sys.path.remove(script_dir)

project_root = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, project_root)
sys.path.insert(0, str(Path(project_root) / "generated"))

from client.terminal import Terminal


def main():

    username = input("Username: ")

    room = input("Room: ")

    terminal = Terminal(username, room)

    terminal.start()


if __name__ == "__main__":
    main()