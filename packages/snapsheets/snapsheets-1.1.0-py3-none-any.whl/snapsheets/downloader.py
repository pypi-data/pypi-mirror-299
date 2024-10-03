import subprocess
from loguru import logger


def via_wget(filename: str, export_url: str) -> dict[str, any]:
    """Download spreadsheet via wget

    - Download using `wget` command
    - Output filename can be configured with CLI option and config.

    Parameters
    ----------
    filename : str
        filename
    export_url : str
        download URL

    Returns
    --------
        dict[str, any]: {"ok", "err"}
    """
    cmd = ["wget", "--quiet", "-O", filename, export_url]
    cmd = [str(c) for c in cmd if c]
    try:
        # check=True to raise an exception automatically.
        subprocess.run(cmd, check=True)
        msg = f"🤖 Downloaded as {filename}"
        logger.success(msg)
        return {"ok": True, "err": None}
    except subprocess.CalledProcessError as e:
        # if failed, set self.skip to True
        msg = f"Failed to download the file: {e}"
        logger.error(msg)
        return {"ok": False, "err": e}
