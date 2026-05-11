from pathlib import Path

with open(Path("~/.config/teleManage/tdf.path").expanduser()) as f:
    TG_FOLDER_PATH = Path(f.read()).expanduser()
