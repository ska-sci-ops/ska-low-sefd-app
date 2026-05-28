"""Download the SKA station sensitivity HDF5 data file.

Usage:
    python download_data.py

The file will be saved to the current directory as
``ska_station_sensitivity_AAVS2.h5``.
"""

import os
import sys
import urllib.request
import shutil

URL = (
    "https://gitlab.com/ska-telescope/ost/ska-ost-senscalc/"
    "-/raw/master/src/ska_ost_senscalc/static/lookups/"
    "ska_station_sensitivity_AAVS2.h5?ref_type=heads"
)
FILENAME = "ska_station_sensitivity_AAVS2.h5"


def download(url: str = URL, dest: str = FILENAME) -> None:
    if os.path.exists(dest):
        print(f"{dest} already exists — skipping download.")
        return

    print(f"Downloading {dest} ...")
    try:
        with urllib.request.urlopen(url) as response, open(dest, "wb") as out:
            shutil.copyfileobj(response, out)
    except Exception as exc:
        # Clean up partial file on failure
        if os.path.exists(dest):
            os.remove(dest)
        print(f"Download failed: {exc}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(dest) / 1e6
    print(f"Saved {dest} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    download()
