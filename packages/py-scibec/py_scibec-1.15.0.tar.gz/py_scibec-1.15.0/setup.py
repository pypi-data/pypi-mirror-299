import os
import pathlib
import subprocess
import sys

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

openapi_client = f"{current_path}/../py_scibec_openapi_client/"

__version__ = "1.15.0"


def run_install(setup_args: dict, bec_deps: list, editable=False):
    """
    Run the setup function with the given arguments.

    Args:
        setup_args (dict): Arguments for the setup function.
        bec_deps (list): List of tuples with the dependencies.
        editable (bool, optional): If True, the dependencies are installed in editable mode. Defaults to False.
    """
    if editable:
        # check if "[dev]" was requested
        if "dev" in os.environ.get("EXTRAS_REQUIRE", ""):
            suffix = "[dev]"
        else:
            suffix = ""
        setup(**setup_args)
        deps = [dep[2] for dep in bec_deps]
        for dep in deps:
            subprocess.run(f"pip install -e {dep}{suffix}", shell=True, check=True)
        return

    install_deps = [dep[0] for dep in bec_deps]
    setup_args["install_requires"].extend(install_deps)
    print(setup_args)
    setup(**setup_args)


if __name__ == "__main__":
    setup_args = {
        "install_requires": ["requests", "tqdm"],
        "version": __version__,
        "extras_require": {
            "dev": ["pytest", "pytest-random-order", "coverage", "black", "pylint", "python-dotenv"]
        },
    }
    bec_deps = [("py_scibec_openapi_client", "py_scibec_openapi_client", openapi_client)]
    # is_local = os.path.dirname(os.path.abspath(__file__)).split("/")[-1] == "py_scibec"
    is_build = "bdist_wheel" in sys.argv

    editable = not is_build
    run_install(setup_args, bec_deps, editable=False)
