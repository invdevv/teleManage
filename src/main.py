#!/usr/bin/env python3

from pathlib import Path
import logging
import subprocess

import typer
from rich.logging import RichHandler

from config import TG_FOLDER_PATH
from utils import (
    create_account,
    import_account,
    get_accs_data,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()],
)

log = logging.getLogger("teleManage")

app = typer.Typer(
    help="Tool for managing multiple Telegram Desktop instances"
)


def handle_error(exc: Exception) -> None:
    log.error(str(exc))


def create_acc(name: str) -> Path | None:
    """
    Create telegram account directory.
    """

    try:
        acc_path = create_account(name)
        log.info(f"Account '{name}' created at {acc_path}")

        return acc_path

    except Exception as exc:
        handle_error(exc)
        return None


@app.command(short_help="Create empty account")
def create(name: str):
    create_acc(name)


@app.command(name="import", short_help="Import tdata into account")
def import_(
    name: str,
    tdata: Path,
):
    """
    Create account and import tdata
    """

    try:
        acc_path = create_acc(name)

        if not acc_path:
            raise RuntimeError("Failed to create account")

        import_account(acc_path, tdata)

        log.info(f"Imported '{tdata}' into '{acc_path}'")

    except Exception as exc:
        handle_error(exc)


@app.command(name="list", short_help="List all accounts")
def list_accounts():
    """
    Show all available accounts
    """

    try:
        accs = get_accs_data()

        if not accs:
            log.info("No accounts found")
            return

        for acc in accs:
            log.info(acc.name)

    except Exception as exc:
        handle_error(exc)


def launch_account(account_id: str) -> bool:
    """
    Launch Telegram instance for account (shell equivalent of:
    cd ... && ./Telegram &>/dev/null)
    """

    account_path = TG_FOLDER_PATH / account_id
    telegram_bin = account_path / "Telegram"

    if not account_path.is_dir():
        log.warning(f"No account directory: {account_id}")
        return False

    if not telegram_bin.exists():
        log.warning(f"Telegram binary not found: {telegram_bin}")
        return False

    subprocess.Popen(
        [str(telegram_bin)],
        cwd=str(account_path),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    log.info(f"Launched account: {account_id}")
    return True


@app.command(short_help="Launch accounts by IDs or names")
def run(accounts: list[str]):
    """
    Launch multiple Telegram accounts
    """

    launched = 0

    for account_id in accounts:
        if launch_account(account_id):
            launched += 1

    log.info(f"Launched {launched}/{len(accounts)} accounts")


if __name__ == "__main__":
    app()