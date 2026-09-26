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
