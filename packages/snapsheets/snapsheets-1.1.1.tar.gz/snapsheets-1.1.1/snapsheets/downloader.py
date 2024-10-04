import subprocess
import httpx
from loguru import logger
from pathlib import Path
from typing import Any


def via_httpx(filename: str, export_url: str) -> dict[str, Any]:
    """Download spreadsheet via httpx.get

    - Downlaod using `httpx` module
    - Output filename can be configured with CLI option and config.

    Parameters
    ----------
    filename: str
        output filename
    export_url: str
        download URL

    Returns
    --------
    dict[str, any]
    """
    msg = f"Download via httpx.get({export_url})"
    logger.debug(msg)

    try:
        response = httpx.get(url=export_url, follow_redirects=True)
        logger.debug(f"{response=}")
        logger.debug(f"{response.url=}")
        logger.debug(f"{response.request.url=}")
        if response.is_success:
            content = response.text
            p = Path(filename)
            with p.open("w", encoding="utf-8") as f:
                f.write(content)
            msg = f"🤖 Downloaded as {filename}"
            logger.success(msg)
        return {"ok": response.is_success, "err": None}
    except Exception as e:
        msg = f"Failed to download the file: {e}"
        logger.error(msg)
        return {"ok": False, "err": e}


def via_wget(filename: str, export_url: str) -> dict[str, Any]:
    """Download spreadsheet via wget

    - Download using `wget` command
    - Output filename can be configured with CLI option and config.

    Parameters
    ----------
    filename : str
        output filename
    export_url : str
        download URL

    Returns
    --------
    dict[str, any]
    """
    msg = "Download via wget"
    logger.debug(msg)

    cmd = ["wget", "--quiet", "-O", filename, export_url]
    cmd = [str(c) for c in cmd if c]
    try:
        # check=True to raise an exception automatically.
        subprocess.run(cmd, check=True)
        msg = f"🤖 Downloaded as {filename}"
        logger.success(msg)
        return {"ok": True, "err": None}
    except subprocess.CalledProcessError as e:
        msg = f"Failed to download the file: {e}"
        logger.error(msg)
        return {"ok": False, "err": e}
