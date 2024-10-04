import warnings

import typer

# Here to ignore the warning from yaspin
# about running in Jupyter
# TODO make this a more specific ignore
warnings.filterwarnings("ignore", category=UserWarning)

from . import vms
from . import data
from . import rc

cli = typer.Typer(no_args_is_help=True)
cli.add_typer(data.app, name="data")
cli.add_typer(rc.app, name="rc")
cli.add_typer(vms.app, name="vms")


__version__ = "0.18.1"


def version_callback(value: bool):
    if value:
        typer.echo(f"Eye CLI: {__version__}")
        raise typer.Exit()


@cli.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    # Do other global stuff, handle other global options here
    return
