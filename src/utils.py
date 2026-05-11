from pathlib import Path
import json
import shutil

from models import Account
from config import TG_FOLDER_PATH


DB_PATH = TG_FOLDER_PATH / ".db.json"


def ensure_db_exists() -> None:
    """
    Create empty database file if missing
    """

    TG_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        DB_PATH.write_text("[]")


def get_accs_data() -> list[Account]:
    """
    Load accounts database
    """

    ensure_db_exists()

    data = json.loads(DB_PATH.read_text())

    return [
        Account.model_validate(acc)
        for acc in data
    ]


def write_accs_data(accounts: list[Account]) -> None:
    """
    Save accounts database
    """

    ensure_db_exists()

    DB_PATH.write_text(
        json.dumps(
            [
                account.model_dump()
                for account in accounts
            ],
            indent=2,
            ensure_ascii=False,
        )
    )


def get_next_account_id(accounts: list[Account]) -> int:
    """
    Generate next account ID
    """

    if not accounts:
        return 0

    return max(acc.id for acc in accounts) + 1


def create_symlink(source: Path, target: Path) -> None:
    """
    Create symlink if it does not exist
    """

    if target.exists() or target.is_symlink():
        return

    if not source.exists():
        raise FileNotFoundError(
            f"Missing reference binary: {source}"
        )

    target.symlink_to(source)


def create_account_folder(account_id: int) -> Path:
    """
    Create account folder structure
    """

    account_path = TG_FOLDER_PATH / str(account_id)
    ref_path = TG_FOLDER_PATH / "base"

    account_path.mkdir(parents=True, exist_ok=True)

    create_symlink(
        ref_path / "Telegram",
        account_path / "Telegram",
    )

    create_symlink(
        ref_path / "Updater",
        account_path / "Updater",
    )
    
    (account_path / "TelegramForcePortable").mkdir(parents=True, exist_ok=True)

    return account_path


def import_account(
    account_path: Path,
    tdata_path: Path,
) -> None:
    """
    Import Telegram tdata directory
    """

    if not tdata_path.exists():
        raise FileNotFoundError(
            f"tdata path does not exist: {tdata_path}"
        )

    if not tdata_path.is_dir():
        raise ValueError(
            f"tdata must be a directory: {tdata_path}"
        )

    target = account_path / "tdata"

    if target.exists():
        raise FileExistsError(
            f"Target tdata already exists: {target}"
        )

    shutil.copytree(tdata_path, target)


def create_account(name: str) -> Path:
    """
    Create new Telegram account
    """

    accounts = get_accs_data()

    account_id = get_next_account_id(accounts)

    account = Account(
        id=account_id,
        name=name,
    )

    accounts.append(account)

    write_accs_data(accounts)

    return create_account_folder(account_id)