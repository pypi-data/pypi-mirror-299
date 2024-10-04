# mypy: ignore-errors
"""(Deprecated since 1.0.0)

> Will be removed from the source code

```console
Usage:
    snapsheets [-h] [--config CONFIG] [--url URL] [-v]

Options:
    -h, --help            show this help message and exit.
    --config CONFIG       set config directory. (default = './config/')
    --url URL             copy and paste an URL of the Google spreadsheet.
    -v, --version         show version and exit.
```

"""

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from datetime import datetime

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import yaml
from deprecated.sphinx import deprecated, versionadded, versionchanged
from loguru import logger

# ic.disable()

from snapsheets import __version__


@dataclass
class Config:
    """Config
    設定用クラス

    Parameters
    ----------
    confd: str
        設定用のディレクトリ (default: "config/")
    saved: str
        ダウンロード先のディレクトリ (default: "snapd/")
    logf: str
        ログファイルの名前（未実装）
    size: int
        ログのサイズ上限（未実装）
    backups: int
        バックアップ数（未実装）
    """

    confd: str = "./config/"
    saved: str = "./snapd/"
    logf: str = None
    size: int = 1000000
    backups: int = 10

    def __post_init__(self) -> None:
        self.check_paths()
        self.load_config()
        return

    @staticmethod
    def check_path(path: str) -> str:
        """引数 ``path`` に渡したディレクトリが存在するかチェックする

        - ディレクトリが存在しない場合はカレントディレクトリに変更する

        Parameters
        ----------
        path: str
            ディレクトリ名

        Returns
        -------
        path: str
            ディレクトリ名
        """
        _path = Path(path)
        if not _path.is_dir():
            path = "."
            warning = f"Directory {_path} not found. Switch to current directory."
            logger.warning(warning)
        return path

    def check_paths(self) -> None:
        """デフォルト値に指定したパスが存在するかチェックする"""

        self.confd = self.check_path(self.confd)
        self.saved = self.check_path(self.saved)
        # self.logd = self.check_path(self.logd)
        return

    @deprecated(version="0.6.0", reason="Will be removed at next major update.")
    def reset_config(self):
        self.confg = "./config/"
        self.saved = "./snapd/"
        self.logf = None
        self.size = 1000000
        self.backups = 10

    @deprecated(version="0.6.0", reason="Will be removed at next major update.")
    def get_fnames(self, pattern: str) -> List[Path]:
        p = Path(self.confd)
        fnames = sorted(p.glob(pattern))
        n = len(fnames)
        if n == 0:
            warning = f"No file found : {n} / {pattern}"
            logger.warning(warning)
        return n, fnames

    def load_yaml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        n, fnames = self.get_fnames("*.yml")
        info = f"Number of YAMLs found :{n}"
        logger.info(info)
        for i, fname in enumerate(fnames):
            debug = f"Loaded YAMLs [{i+1}/{n}]: {fname}"
            logger.debug(debug)
            with open(fname) as f:
                c = yaml.safe_load(f)
                config.update(c)
        return config

    def load_toml(self) -> Dict[Any, Any]:
        """Load configurations from TOMLs

        設定を読み込んだ辞書型をリターンする

        - 初めて読み込む場合 : TOMLを直接代入してOK
        - 2回目以降 : シートの情報だけ追記
        """
        config: Dict[Any, Any] = {}
        config.setdefault("tool", {})
        config.setdefault("sheets", {})
        debug = f"config.setdefault: {config}"
        logger.debug(debug)
        n, fnames = self.get_fnames("*.toml")
        info = f"Number of TOMLs found : {n}"
        logger.info(info)
        for i, fname in enumerate(fnames):
            debug = f"==> Load TOMLs [{i+1}/{n}]: {fname}"
            logger.debug(debug)
            with fname.open("rb") as f:
                _loaded = tomllib.load(f)
            config = self.update_config(config, _loaded)
        return config

    def update_config(self, config, new):
        """update config"""
        # debug = f"current config: {config}"
        # ic(debug)

        _sheets = new.get("sheets")
        _tool = new.get("tool")

        if _sheets is not None:
            config["sheets"].update(_sheets)
        if _tool is not None:
            config["tool"].update(_tool)

        # debug = f"updated config: {config}"
        # ic(debug)
        return config

    def load_config(self) -> None:
        config: Dict[Any, Any] = {}
        c = self.load_yaml()
        config.update(c)
        c = self.load_toml()
        config.update(c)
        self._config = config
        return

    def get_config(self):
        """Get pyproject-like configuration

        [tool.snapsheets]
        """
        if self._config.get("tool"):
            cfg = self._config.get("tool").get("snapsheets")
        else:
            cfg = self._config.get("snapsheets")

        if cfg is None:
            error = "None found. Check your configuration."
            logger.error(error)
            sys.exit(1)
        return cfg

    def sections(self) -> List[str]:
        return sorted(self._config.keys())

    def volumes(self) -> Optional[str]:
        _volumes = self._config.get("volumes")
        _cfg = self.get_config()
        if _cfg:
            _volumes = _cfg.get("volumes")
        return _volumes

    def options(self) -> Optional[str]:
        _options = self._config.get("options")
        _cfg = self.get_config()
        if _cfg:
            _options = _cfg.get("options")
        return _options

    def datefmt(self) -> Optional[str]:
        _datefmt = self._config.get("datefmt")
        _cfg = self.get_config()
        if _cfg:
            _datefmt = _cfg.get("datefmt")
        return _datefmt

    def sheets(self) -> Any:
        _sheets = self._config.get("sheets")
        return _sheets

    def sheet_names(self) -> Any:
        sheets = self.sheets()
        names = sorted(sheets.keys())
        return names

    def sheet(self, name: str) -> Any:
        sheets = self.sheets()
        return sheets.get(name)


@dataclass
class Sheet(Config):
    """
    シート用クラス

    Parameters
    ----------
    url: str or None
        GoogleスプレッドシートのURL
    key: str or None
        該当シートのスプレッドシートID
    gid: str or None
        該当シートのシートID
    fmt: str
        ダウンロード形式 (default=".xlsx")
    desc: str or None
        該当シートの説明 (default="snapsheet")
    fname: str or None
        ダウンロードしたときのファイル名
    name: str or None
        該当シートのID的なもの (default="snapsheet")
    datefmt: str or None
        ダウンロードしたときの日付フォーマット (default="%Y%m%dT%H%M%S")
    skip: bool
        スキップ用フラグ (default=False)
    """

    url: Union[str, Optional[str]] = None
    key: Optional[str] = None
    gid: Optional[str] = None
    fmt: str = "xlsx"
    desc: Optional[str] = "snapsheet"
    fname: Optional[str] = None
    name: Optional[str] = "snapsheet"
    datefmt: Optional[str] = "%Y%m%dT%H%M%S"
    skip: bool = False

    def __post_init__(self) -> None:
        self.check_paths()
        self.set_name()
        self.set_savef()

        if self.url is not None:
            self.set_key_gid_from_url()
        else:
            msg = f"URL : {self.url} / key : {self.key}"
            logger.info(msg)
        return

    def set_name(self):
        warning = "fname will be deprecated. Use name instead."
        if self.fname is not None:
            self.name = self.fname
            logger.warning(warning)
        return

    def set_savef(self) -> None:
        fmt = f".{self.fmt}"
        name = Path(self.name)
        self.savef = Path(self.saved) / name.with_suffix(fmt)
        return

    def set_key_gid_from_url(self) -> None:
        url = self.url
        if url.startswith("https://"):
            self.key = url.split("/")[-2]
            self.gid = url.split("#")[-1].split("=")[1]
        else:
            self.key = self.url
            self.gid = None
        return

    def info(self) -> None:
        print(self.confd)
        print(self.saved)
        print(self.url)
        print(self.key)
        print(self.gid)
        print(self.fmt)
        print(self.desc)
        print(self.name)
        print(self.savef)
        print(self.export_url())
        return

    def load(self, sheet: Dict[str, Any]) -> None:
        self.url = sheet.get("url")
        self.desc = sheet.get("desc")
        self.gid = sheet.get("gid")
        self.fmt = sheet.get("format")
        self.fname = sheet.get("stem")
        self.name = sheet.get("name")
        self.datefmt = sheet.get("datefmt")
        return

    def export_url(self) -> str:
        if self.key is None:
            self.set_key_gid_from_url()
            msg = f"Got key from URL : {self.url}"
            logger.info(msg)

        self.check_fmt()
        fmt = self.fmt
        key = self.key
        gid = self.gid
        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url

    def check_fmt(self) -> None:
        """出力ファイルの形式をチェック

        - サポートしている形式: ``.xlsx``, ``.ods``, ``.csv``, ``.tsv``
        - 上記以外の拡張子の場合は ``sys.exit``
        """
        fmt = self.fmt
        ok = ["xlsx", "ods", "csv", "tsv"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {ok}. ... Exit."
            logger.info(msg)
            sys.exit()
        return

    def download(self) -> str:
        url = self.export_url()
        savef = str(self.savef)
        cmd = ["wget", "--quiet", "-O", savef, url]
        cmd = [str(c) for c in cmd if c]
        if self.skip:
            info = f"Skipped downloading {savef}"
            logger.info(info)
        else:
            subprocess.run(cmd)
            info = f"🤖 Downloaded {savef}"
            logger.success(info)
        return savef

    def backup(self) -> str:
        datefmt = self.datefmt
        now = datetime.now().strftime(datefmt)

        fmt = f".{self.fmt}"
        fname = Path(f"{now}_{self.name}")
        movef = Path(self.saved) / fname.with_suffix(fmt)
        savef = str(self.savef)
        movef = str(movef)
        if self.skip:
            info = f"Skipped renaming {savef}"
            logger.info(info)
        else:
            shutil.move(savef, movef)
            info = f"🚀 Renamed to {movef}"
            logger.success(info)
        return str(movef)

    @deprecated(version="0.6.0", reason="Will be removed at next major update.")
    def snapshot(self):
        logger.info(f"📣 {self.desc}")
        self.download()
        movef = self.backup()
        return movef


@dataclass
class Book(Config):
    """Book
    A class for collection or spreadsheets
    """

    sheets: List[Sheet] = field(default_factory=list)

    def __post_init__(self):
        self.check_paths()
        self.load_config()

        names = self.get_sheet_names()
        for name in names:
            _sheet = self.make_sheet(name)
            self.add_sheet(_sheet)
        return

    def get_sheet_names(self):
        names = sorted(self._config.get("sheets").keys())
        return names

    def get_sheet_dict(self, name: str):
        sheet = self._config.get("sheets").get(name)
        return sheet

    def make_sheet(self, name: str) -> Sheet:
        """
        Make Sheet object from configuration file

        Parameters
        ----------
        name : str
            Name of sheet in configuration file

        Returns
        -------
        Sheet
            Sheet
        """
        _sheet = self.get_sheet_dict(name)
        url = _sheet.get("url")
        sheet = Sheet(
            confd=self.confd,
            saved=self.saved,
            url=url,
        )
        sheet.fname = _sheet.get("name")
        sheet.name = _sheet.get("name")
        sheet.desc = _sheet.get("desc")
        sheet.fmt = _sheet.get("format")
        sheet.datefmt = _sheet.get("datefmt")
        sheet.skip = _sheet.get("skip")
        return sheet

    def add_sheet(self, sheet: Sheet) -> None:
        """
        Add Sheet object to Book object.
        Skip when sheet.skip = True.

        Parameters
        ----------
        sheet : Sheet
            設定ファイルから作成した Sheet オブジェクト
        """
        if sheet.skip:
            info = f"Skipped : {sheet.name}"
        else:
            info = f"Add sheet : {sheet.name}"
            self.sheets.append(sheet)
        logger.info(info)
        return

    @deprecated(version="0.6.0", reason="Will be removed at next major update.")
    def snapshots(self) -> None:
        """
        Take snapshots of all sheet in the Book
        """
        _sheets = self.sheets
        n = len(_sheets)
        for i, sheet in enumerate(_sheets):
            name = sheet.name
            desc = sheet.desc
            debug = f"[{i+1}/{n}] {name} - {desc}"
            logger.debug(debug)
            sheet.snapshot()
        return

    def export_urls(self) -> None:
        """
        Show export URLs
        """
        _sheets = self.sheets
        n = len(_sheets)
        for i, sheet in enumerate(_sheets):
            url = sheet.export_url()
            info = f"[{i+1}/{n}] {url}"
            print(info)
        return


@versionadded(version="0.5.0")
def cli() -> None:
    """
    Command Line Interface for Snapsheets
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="./config/",
        help="set config directory (default: ./config/)",
    )
    parser.add_argument("--url", help="copy and paste an URL of the Google spreadsheet")
    parser.add_argument("--debug", action="store_true", help="show more messages")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    args = parser.parse_args()

    # setup logger
    logger.remove()
    if args.debug:
        fmt = "{time:YYYY-MM-DDTHH:mm:ss} | <level>{level:8}</level> | <cyan>{name}.{function}:{line}</cyan> | <level>{message}</level>"
        logger.add(sys.stderr, format=fmt, level="DEBUG")
    else:
        fmt = "{time:YYYY-MM-DDTHH:mm:ss} | <level>{level:8}</level> | <level>{message}</level>"
        logger.add(sys.stderr, format=fmt, level="SUCCESS")

    if args.url:
        sheet = Sheet(url=args.url)
        sheet.snapshot()
    else:
        book = Book(confd=args.config)
        book.snapshots()

    return


if __name__ == "__main__":
    cli()
