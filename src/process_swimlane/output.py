"""Publish complete SVG bytes without replacing any existing diagram."""
import os
from pathlib import Path
import tempfile


def publish_svg(data, stem, directory=Path("output")):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".swimlane-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        number = 1
        while True:
            suffix = "" if number == 1 else f"_{number}"
            destination = directory / f"{stem}_swimlane{suffix}.svg"
            try:
                # On Windows rename fails if the destination exists.
                if os.name != "nt":
                    raise OSError("Output publication is supported on Windows only.")
                os.rename(temporary, destination)
                return destination
            except FileExistsError:
                number += 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _remove_pair_files(paths):
    """Try every cleanup and identify leftovers if the OS refuses removal."""
    failures = []
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError as error:
            failures.append(f"{path}: {error}")
    if failures:
        raise OSError("Incomplete output cleanup; remove these files manually: " + "; ".join(failures))


def publish_pair(svg, html, stem, directory=Path("output")):
    """Stage both formats, retry no-replace collisions, roll back handled errors.

    Two renames are not crash-atomic. No success is returned until both finish.
    """
    if os.name != "nt":
        raise OSError("Output publication is supported on Windows only.")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    number = 1
    while True:
        suffix = "" if number == 1 else f"_{number}"
        destinations = tuple(directory / f"{stem}_swimlane{suffix}.{ext}" for ext in ("svg", "html"))
        if any(os.path.lexists(path) for path in destinations):
            number += 1
            continue
        staged, published = [], []
        complete = False
        try:
            for data in (svg, html):
                with tempfile.NamedTemporaryFile(dir=directory, prefix=".swimlane-", suffix=".tmp", delete=False) as stream:
                    staged.append(Path(stream.name))
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
            try:
                for temporary, destination in zip(staged, destinations):
                    os.rename(temporary, destination)
                    published.append(destination)
            except FileExistsError:
                # finally rolls back this attempt before trying the next pair.
                number += 1
                continue
            complete = True
        finally:
            _remove_pair_files(staged + ([] if complete else published))
        return destinations
