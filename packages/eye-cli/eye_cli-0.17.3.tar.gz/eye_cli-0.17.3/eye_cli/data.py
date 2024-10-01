from itertools import islice
from pathlib import Path
from typing import Optional

import inquirer
import pyperclip
import typer
from rich import print
from typing_extensions import Annotated
from yaspin import yaspin
from yaspin.spinners import Spinners

from eye_cli.util import message, color, cmd

app = typer.Typer()


APP_NAME = "eye-cli"
BUCKET = "gs://gecko-chase-photogrammetry-dev"
CAPTURE = f"{BUCKET}/capture"
LOCAL = Path.home() / "Downloads" / "bucket"
LOCAL_CAPTURE = LOCAL / "capture"


def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def find_bucket(search_external_drives: bool = False) -> str:
    paths = []

    # search on attached drives
    if search_external_drives:
        attached = [d / "bucket" for d in Path("/Volumes").iterdir()]
        paths.extend(attached)

    # search on local machine
    paths.append(LOCAL)

    # narrow to those that are present
    paths = [d for d in paths if d.is_dir()]

    # add option to input your own
    let_me = "Let me specify..."
    paths.append(let_me)

    paths = [str(p) for p in paths]
    path = inquirer.list_input("Where is your bucket?", choices=paths)

    if path == let_me:
        message(
            f"{color("NOT IMPLEMENTED", "red")} specify your own path", padding="around"
        )
        # prompt for path
        # store path in preferences
        raise NotImplementedError

    return path


@app.command()
def config():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        message("No config present", padding="around")
    else:
        message("You have a config", padding="around")


@app.command()
def bucket(preview: bool = True, testing: bool = False):
    """Upload everything in your local bucket to the cloud"""
    m = color("UPLOAD", "red")
    message(f"{m} your whole bucket", padding="around")

    path = find_bucket(search_external_drives=True)

    message(f"{color("UPLOAD BUCKET", "red")} from {path}", padding="above")

    message("╮", indent=4)
    for i in Path(path).iterdir():
        message(f"├── {str(i.name)}", indent=4)
    message("╯", indent=4)

    to_path = (
        "gs://gecko-chase-photogrammetry-dev/testing/"
        if testing
        else "gs://gecko-chase-photogrammetry-dev/"
    )
    to_path = f'"{to_path}"'
    message(f"{color("TO", "red")} to {to_path}", padding="below")
    path = f'"{path}"'

    if not inquirer.confirm(
        "Are you sure you want to upload everything here?", default=False
    ):
        message(f"{color("ABORTED", "yellow")}", padding="around")
        return

    args = ["gsutil", "-m", "rsync", "-r"]
    if preview:
        args.append("-n")
    args.extend([path, to_path])

    command = " ".join(args)
    message(f"{color("RUN THIS TO UPLOAD", "green")}  {command}", padding="above")
    message(
        f"{color(" └────> copied to your clipboard paste", "yellow")}", padding="below"
    )
    pyperclip.copy(command)


def get_local_captures():
    """Get the local Capture folders"""
    bucket = find_bucket(search_external_drives=True)
    capture_dir = Path(bucket) / "capture"
    return [d for d in capture_dir.iterdir() if d.is_dir]


def quoted(s: str) -> str:
    """Put quotes around the str"""
    return f'"{s}"'


@app.command()
def capture(
    name: Annotated[Optional[str], typer.Argument()] = None,
    preview: bool = True,
):
    """Upload a capture folder to the cloud."""
    message(f"{color("UPLOAD", "red")} a capture folder", padding="around")

    if not name:
        print()
        path = inquirer.list_input("Which project?", choices=get_local_captures())
        path = Path(path)
        name = path.name
    else:
        bucket = find_bucket(search_external_drives=True)
        path = Path(bucket) / "capture" / name
        if not path.is_dir():
            message(
                f"{color("ABORTED", "yellow")}: No directory at {str(path)}",
                padding="around",
            )
            typer.Abort(f"No directory at {str(path)}")

    message(f"{color("UPLOAD", "red")} {name} ({path})", padding="around")
    message("╮", indent=4)
    for i in islice(path.iterdir(), 10):
        message(f"├── {str(i.name)}", indent=4)
    message("╯", indent=4)

    to_path = f"gs://gecko-chase-photogrammetry-dev/capture/{name}"
    to_path = quoted(to_path)
    path = quoted(str(path))
    message(f"{color("TO", "red")} to {to_path}", padding="below")

    if not inquirer.confirm("Are you sure?", default=False):
        message(f"{color("ABORTED", "yellow")}: by your request", padding="around")
        typer.Abort()

    args = ["gsutil", "-m", "rsync", "-r"]
    if preview:
        args.append("-n")
    args.extend([path, to_path])

    command = " ".join(args)
    message(f"{color("RUN THIS TO UPLOAD", "green")}  {command}", padding="above")
    message(
        f"{color(" └────> copied to your clipboard paste", "yellow")}", padding="below"
    )
    pyperclip.copy(command)


@app.command()
def down(name: str):
    m = color("DOWNLOAD", "green")
    message(f"{m} {name}", padding="around")

    from_path = f"{CAPTURE}/{name}"
    to = LOCAL_CAPTURE / name
    ensure(to)

    f = color(from_path, "blue")
    t = color(to, "orange")
    message(f"{m}\n{f} ->\n{t}", padding="around")

    cmd(["gsutil", "-m", "rsync", "-r", from_path, to])


@app.command()
def folders(path=""):
    for r in get_cloud_folders(path=path):
        message(r, indent=4)


@yaspin(Spinners.aesthetic, text="Grabbing folders...", color="yellow")
def get_cloud_folders(path=""):
    res = cmd(["gsutil", "ls", f"{BUCKET}/{path}"])
    paths = res.stdout.split("\n")
    results = [p.split("/")[-2] for p in paths if p and p.split("/")[-1] == ""]
    results.sort(key=lambda s: s.lower())
    return results


if __name__ == "__main__":
    app()
