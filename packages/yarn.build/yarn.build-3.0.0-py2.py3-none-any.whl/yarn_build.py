"""zest.releaser plugin to build JavaScript projects"""

import logging
import subprocess
import sys
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from zest.releaser.utils import ask

logger = logging.getLogger("yarn.build")


def get_metadata(path):
    setup_cfg = path / "setup.cfg"
    if setup_cfg.exists():
        config = ConfigParser()
        config.read(setup_cfg)
        try:
            folder_path = Path(config.get("yarn.build", "folder"))
            if folder_path.exists():
                install_cmd = config.get("yarn.build", "install").split(" ")
                build_cmd = config.get("yarn.build", "build").split(" ")
                return folder_path, install_cmd, build_cmd
            logger.warning(f"{folder_path} does not exist")
        except NoSectionError:
            pass
        except (NoOptionError, ValueError):
            logger.warning(
                "No valid `folder` option found in `yarn.build` section "
                "within setup.cfg"
            )

    return None


def build(metadata):
    """Build the JavaScript project at the given location"""
    logger.debug("build JS assets: Compile dependencies")
    folder_path, install_cmd, build_cmd = metadata
    subprocess.call(install_cmd, cwd=folder_path)
    logger.debug("build JS assets: Build the project")
    subprocess.call(build_cmd, cwd=folder_path)


def build_project(data):
    """Build a JavaScript project from a zest.releaser tag directory"""
    tagdir = data.get("tagdir")
    if not tagdir:
        msg = "build JS assets: no tagdir found in data."
        logger.warning(msg)
        return
    logger.debug(f"build JS assets: find and build JavaScript projects on {tagdir}")
    try:
        metadata = get_metadata(Path(tagdir))
        if metadata:
            build(metadata)
    except Exception:  # noqa: B902
        logger.warning(
            "build JS assets: building the project failed.",
            exc_info=True,
        )
        if data:
            # We were called as an entry point of zest.releaser.
            if not ask("Error building JS project. Do you want to continue?"):
                sys.exit(1)
