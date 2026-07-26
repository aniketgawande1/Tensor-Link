import sys
from pathlib import Path

# Prevent package shadowing: remove 'server/' from sys.path and add the project root
script_dir = str(Path(__file__).resolve().parent)
if script_dir in sys.path:
    sys.path.remove(script_dir)

project_root = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, project_root)
sys.path.insert(0, str(Path(project_root) / "generated"))

from server.grpc_server import create_server


def main() -> None:
    """
    Starts the gRPC server and waits indefinitely.
    """
    server = create_server()

    print("=" * 60)
    print("🚀 gRPC Terminal Chat Server Started")
    print("Listening on :50051")
    print("=" * 60)

    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(grace=5)


if __name__ == "__main__":
    main()