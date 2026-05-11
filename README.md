## TeleManage - tool for managing multiple telegram instances via CLI

Requirements:
 - Python 3.11+
 - pydantic>=2.13.4
 - typer>=0.25.1

Instalation:
```bash
DATA_FOLDER_PATH="$HOME/.local/share/teleManage"

python3 -m pip install pydantic typer --break-system-packages

mkdir -p ~/.config/teleManage
mkdir -p $DATA_FOLDER_PATH/base

if [ -d "$DATA_FOLDER_PATH/script/.git" ]; then
    cd "$DATA_FOLDER_PATH/script"
    git pull --rebase
else
    git clone --depth=1 https://github.com/invdevv/teleManage "$DATA_FOLDER_PATH/script"
fi

chmod +x $DATA_FOLDER_PATH/script/src/main.py
ln -sf $DATA_FOLDER_PATH/script/src/main.py ~/.local/bin/tm

curl -L https://telegram.org/dl/desktop/linux -o /tmp/telegram.tar.xz
tar -xvf /tmp/telegram.tar.xz -C $DATA_FOLDER_PATH/base --strip-components=1

printf $DATA_FOLDER_PATH > ~/.config/teleManage/tgf.path

tm --help
```

Usage:
```bash
# All docs
tm --help
```

