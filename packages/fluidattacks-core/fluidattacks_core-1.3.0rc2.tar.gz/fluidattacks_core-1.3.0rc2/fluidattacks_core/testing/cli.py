from .aws.plugins import (
    MotoPlugin,
)
from .plugins import (
    CustomFixturesPlugin,
)
import argparse
import os
import pathlib
import pytest as _pytest
import sys as _sys
from typing import (
    NamedTuple,
)


class Args(NamedTuple):
    target: pathlib.Path
    scope: str | None


def get_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="fluidattacks_core.testing",
        description=(
            "🏹 Python package for unit and integration testing through "
            "Fluid Attacks projects 🏹"
        ),
    )

    parser.add_argument(
        "--target",
        metavar="TARGET",
        type=pathlib.Path,
        default=os.getcwd(),
        help="Directory to start the tests. Default is current directory.",
    )

    parser.add_argument(
        "--scope",
        metavar="SCOPE",
        type=str,
        default=None,
        help="Type and module to test.",
    )
    args = parser.parse_args()

    return Args(
        target=args.target,
        scope=args.scope,
    )


def execute() -> None:
    args = get_args()

    _scope_args = ["-m", f"{args.scope}"] if args.scope else []
    _pytest_args = [
        "--disable-warnings",
        "--showlocals",
        "--strict-markers",
        "--verbose",
        *_scope_args,
    ]
    _sys.exit(
        _pytest.main(
            [str(args.target), *_pytest_args],
            plugins=[
                CustomFixturesPlugin(),
                MotoPlugin(),
            ],
        )
    )
