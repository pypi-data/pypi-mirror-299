# STDLIB
import sys
from typing import Optional

# EXT
import click

# PROJ
try:
    from . import __init__conf__
    from . import security_dependency_pinning
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__  # type: ignore  # pragma: no cover
    import security_dependency_pinning  # type: ignore  # pragma: no cover

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


def flush_streams() -> None:
    """
    flush the streams - make sure the output is written early,
    otherwise the output might be printed even after another CLI
    command is launched


    Examples
    --------


    >>> flush_streams()

    """
    # flush_streams}}}
    try:
        sys.stdout.flush()
    except Exception:  # noqa # pragma: no cover
        pass  # pragma: no cover
    try:
        sys.stderr.flush()
    except Exception:  # noqa # pragma: no cover
        pass  # pragma: no cover


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.version_option(
    version=__init__conf__.version, prog_name=__init__conf__.shell_command, message=f"{__init__conf__.shell_command} version {__init__conf__.version}"
)
@click.option("--traceback/--no-traceback", is_flag=True, type=bool, default=None, help="return traceback information on cli")
def cli_main(traceback: Optional[bool] = None) -> None:
    if traceback is not None:
        pass
    security_dependency_pinning.main()


@cli_main.command("info", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_info() -> None:
    """get program information"""
    info()


# entry point if main
if __name__ == "__main__":
    try:
        cli_main()  # type: ignore
    except Exception as exc:  # noqa
        pass
    finally:
        flush_streams()
