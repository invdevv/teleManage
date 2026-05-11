from pathlib import Path

with open(Path("~/.config/teleManage/tgf.path").expanduser()) as f:
    TG_FOLDER_PATH = Path(f.read()).expanduser()
