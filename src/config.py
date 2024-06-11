from pathlib import Path


# Define paths
# All paths are relative to the project root
# This allows for easy access to all paths from any file in the project
ROOT_PATH = Path(__file__).parent.parent
PROJECT_PATH = Path(__file__).parent
KEY_PATH = ROOT_PATH.joinpath("keys")

OUTPUT_PATH = PROJECT_PATH.parent.joinpath("output")
DATA_PATH = OUTPUT_PATH.joinpath("data")
API_PATH = OUTPUT_PATH.joinpath("api")
TMP_PATH = OUTPUT_PATH.joinpath("tmp")


# initialize critical/necessary paths to run
def init_paths() -> None:
    KEY_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    TMP_PATH.mkdir(parents=True, exist_ok=True)
