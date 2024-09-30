import subprocess
from importlib import metadata as _metadata
from pathlib import Path

from loguru import logger
from rich import traceback
from typer import Argument, Typer
from typing_extensions import Annotated

from genpypress.app import (
    app_cc,
    app_join,
    app_patch_to_validtime,
    app_rewrite,
    app_to_async,
)
from genpypress.app.app_deploy import app_deploy
from genpypress.app.app_transfer.transfer import (
    get_transfer_objects,
    load_transfer_objects,
    transfer_objects,
)

traceback.install(show_locals=False, max_frames=1)

app = Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command()
def transfer_prep(
    db_from: str,
    db_to: str,
    batch_file: str,
):
    """
    Připraví soubor s podklady pro přenos mezi databázemi.

    Args:
        - db_from (str): zdrojová databáze
        - db_to (str): cílová databáze
        - batch_file: soubor do kterého zapíšeme získané DDL skripty
    """
    _batch_file = None if not batch_file else batch_file
    get_transfer_objects(db_from, db_to, store_to=_batch_file)


@app.command()
def transfer_run(
    batch_file: Annotated[
        str,
        Argument(help="Název souboru připraveného pomocí transfer-prep."),
    ],
    rewrites: None | list[str],
    filter: list[str] | None = None,
):
    """
    Provede přenos mezi databázemi, podle souboru definovaného pomocí transfer-prep.

    Args:
    - batch_file (str): název souboru, který byl připraven pomocí transfer-prep
    - rewrites (list[str] | None): seznam regulárních výrazů pro přepis DDL
        - syntax: SEARCH/REPLACE/i - kde /i je optional suffix pro "ignorecase"
        - příklad: EP_TGT[.]/ED0_TGT/i - přepíše v DDL z produkce na DEV
    - filter (list[str] | None): seznam regulárních výrazů s filtrem

    Příklad použití:

    ph transfer-run ep_tgt_v.json --rewrites EP_TGT[.]/ED0_TGT --filter "PARTY.*"
    """

    if rewrites:
        logger.info(rewrites)
    batch = load_transfer_objects(Path(batch_file))
    transfer_objects(batch, rewrites=rewrites, store_to=batch_file, filter=filter)


@app.command()
def version():
    vrs = _metadata.version("genpypress")
    print(f"genpypress version: {vrs}")


@app.command()
def deploy(
    path: str = ".",
    to_prod: bool = False,
):
    """Připraví nasazovací obálku v podobě shell skriptů (linux, náhrada za bihelp)."""
    app_deploy._scandir(Path(path), to_prod=to_prod)


@app.command()
def rewrite(
    directory: str = ".",
    config_file_name: str = "rewrite.json",
    max_files: int = 20,
    run_press: bool = False,
):
    """
    Umožní přepis souborů na základě konfigurace (rewrite.json).
    Pokud ještě konfigurační soubor neexistuje, založí ho.

    Args:
        directory (str): _description_
    """
    if run_press:
        raise Exception
    _directory = Path(directory)
    print(f"rewrite in: {directory=}")
    config_file = _directory / config_file_name
    print(f"{config_file=}")
    try:
        config = app_rewrite.read_config(config_file)
    except app_rewrite.exceptions.ConfigEmptyContent as err:
        # OK, chybějící config file
        print(err)
        print(f"vytvářím vzorovový soubor: {config_file}")
        app_rewrite.create_sample_config(config_file)
        return
    except Exception:  # chyba o které nic nevím
        raise

    project_json = _directory / "project.json"
    if run_press and project_json.is_file():
        print("press run")
        subprocess.run(["press", "run"])

    # proveď přepis
    print("rewrite")
    app_rewrite.rewrite_in_dir(config, _directory, max_files)


@app.command()
def join(
    directory: str,
    join_to: str = "part_1.sql",
    delete: bool = True,
    mask: str = "*.sql",
    encoding: str = "utf-8",
    add_comment: bool = True,
):
    """sloučí sadu SQL souborů do jednoho, a smaže je"""
    app_join.join_files(
        directory=directory,
        join_to=join_to,
        delete=delete,
        mask=mask,
        encoding=encoding,
        add_comment=add_comment,
    )
    print("done")


@app.command()
def apatch(directory: str, limit: int = 50, encoding: str = "utf-8"):
    """apatch: patch TPT skriptů pro async stage

    Args:
        directory (str): adresář, kde jsou TPT skripty
        limit (int): kolik maximálně souborů upravit
        encoding (str): jak jsou soubory nakódované
    """
    d = Path(directory)
    if not d.is_dir():
        print(f"toto není adresář: {directory}")
        exit(1)
    app_patch_to_validtime.async_patch(d, limit, encoding)


@app.command()
def cc(
    directory: str,
    scenario: str = "drop",
    input_encoding: str = "utf-8",
    output_encoding: str = "utf-8",
    max_files: int = 20,
):
    """cc: conditional create

    Args:
        directory (str): directory where to do the work
        scenario (str): ["drop", "create", "cleanup", "drop-only"]
        input_encoding (str): Defaults to "utf-8".
        output_encoding (str): Defaults to "utf-8".
    """
    app_cc.conditional_create(
        directory, scenario, input_encoding, output_encoding, max_files
    )


@app.command()
def ddl_to_async(
    folder: str,
    max_files: int = 20,
    encoding: str = "utf-8",
    default_type: str | None = None,
):
    """ddl_to_async: change DDL scripts to async stage implementaton

    Args:
        folder (str): the directory containing DDL scripts (MUST be *_LND or *_STG)
        max_files (int, optional): defaults to 20.
        encoding (str, optional): defaults to "utf-8".
        default_type (str, optional): if set, apply (s) or (i) to STG tables
    """
    app_to_async.to_async(
        folder=folder,
        max_files=max_files,
        encoding=encoding,
        default_type=default_type,
    )


def main():
    app()


if __name__ == "__main__":
    main()
