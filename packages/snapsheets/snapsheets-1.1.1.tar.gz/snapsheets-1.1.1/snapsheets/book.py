"""

```python
from snapsheets.book import Book

book = Book("config.toml")
book.snapshots()

# 📣 Sample spreadsheet for snapsheets. (%Y%m%d)
# 🤖 Downloaded sample1.csv
# 🚀 Rnamed sample1.csv to 20220602_sample1.csv
# 📣 Sample spreadsheet for snapsheets. (%Y%m)
# 🤖 Downloaded sample2.csv
# 🚀 Rnamed sample2.csv to 202206_sample2.csv
```
"""

import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import yaml
from loguru import logger

from snapsheets.sheet import Sheet


@dataclass
class Book:
    """
    A class for collection of spreadsheets
    """

    fname: str = "config.toml"
    """config filename or directory"""

    def __post_init__(self) -> None:
        msg = f"Initializing Book with config: {self.fname}"
        logger.info(msg)

        p = Path(self.fname)
        if not p.exists():
            msg = f"Unable to locate config file/directory: {p}."
            logger.error(msg)
            msg = "Maybe you need to create a new config file/directory."
            logger.error(msg)
            sys.exit()

        self.fnames = self.get_fnames()
        self.config = self.load_config()
        self.sheets = self.get_sheets()

        msg = f"Book initialized successfully with {len(self.sheets)} sheets."
        logger.info(msg)

    def get_fnames(self) -> list[Path]:
        """Get list of configuration files.

        Returns
        -------
        list[Path]
            list of configuration files
        """
        p = Path(self.fname)
        msg = f"Loading configuration from: {p}"
        logger.info(msg)

        if p.is_file():
            return [p]

        fnames = sorted(p.glob("*.toml"))
        if not fnames:
            msg = f"No configuration found in directory: {p}"
            logger.warning(msg)
        return fnames

    def load_config(self) -> dict:
        """Load configuration from files.

        - Supported format: ``toml``, ``.yml``, and ``.yaml``

        Returns
        -------
        dict
            configuration in dict-object
        """
        config = {}
        loaders = {
            ".toml": self.load_config_toml,
            ".yml": self.load_config_yaml,
            ".yaml": self.load_config_yaml,
        }

        for fname in self.fnames:
            msg = f"Loading configuration from file: {fname}"
            logger.debug(msg)

            # Get the appropriate loader function based on file suffix
            loader = loaders.get(fname.suffix)

            if not loader:
                msg = f"Unsupported configuration format: {fname.suffix}"
                logger.error(msg)
                raise ValueError(msg)

            _config = loader(fname)
            config.update(_config)
        return config

    def load_config_toml(self, fname: Path) -> dict:
        """Load configurations from TOML format.

        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("rb") as f:
            config = tomllib.load(f)
        msg = f"Loaded TOML configuration from {fname}"
        logger.debug(msg)
        return config

    def load_config_yaml(self, fname: Path) -> dict:
        """
        Load configurations from YAML format.

        Parameters
        ----------
        fname : Path
            config filename

        Returns
        -------
        dict
            config as dict-object
        """
        with fname.open("r") as f:
            config = yaml.safe_load(f)
        msg = f"Loaded YAML configuration from {fname}"
        logger.debug(msg)
        return config

    def get_sheets(self) -> list[Sheet]:
        """
        Get list of sheets in configuration.

        Returns
        -------
        list[Sheet]
            list of Sheet objects
        """
        sheets_config = self.config.get("sheets")
        if sheets_config is None:
            msg = "No '[[sheets]]' section found in configuration."
            logger.warning(msg)
            return []

        sheets = []
        for sheet_config in sheets_config:
            msg = f"Processing sheet config: {sheet_config}"
            logger.debug(msg)
            try:
                sheet = Sheet(
                    url=sheet_config.get("url"),
                    filename=sheet_config.get("filename"),
                    description=sheet_config.get("description"),
                    datefmt=sheet_config.get("datefmt"),
                    skip=sheet_config.get("skip"),
                )
                sheets.append(sheet)
            except Exception as e:
                logger.error(e)
                msg = "Failed to create Sheet from config: {sheet}"
                logger.exception(msg)
        return sheets

    def snapshots(self) -> None:
        """
        Take a snapshot of sheets.
        """

        for sheet in self.sheets:
            try:
                msg = f"Taking snapshot for sheet: {sheet}"
                logger.debug(msg)
                sheet.snapshot()
            except Exception as e:
                logger.error(e)
                msg = "Failed to take snapshot for sheet: {sheet}"
                logger.exception(msg)
