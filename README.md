# SKA-Low SEFD app

Interactive dashboard for exploring the System Equivalent Flux Density (SEFD)
of SKA-Low stations.

![screenshot.jpg](https://github.com/ska-sci-ops/ska-low-sefd-app/raw/main/screenshot.jpg)

## Setup

Create a virtual environment and install the required packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy h5py panel holoviews hvplot
```

> **Note:** The HDF5 data file `ska_station_sensitivity_AAVS2.h5` must be
> present in the project directory. You can download it by running:
>
> ```bash
> python download_data.py
> ```

## Running the dashboard

```bash
source .venv/bin/activate
panel serve dashboard.py --show
```

The dashboard will open in your browser at <http://localhost:5006/dashboard>.

## Parameters

| Parameter          | Range       | Description                        |
|--------------------|-------------|------------------------------------|
| Altitude           | 0 – 90°    | Elevation angle                    |
| Azimuth            | 0 – 360°   | Azimuth angle                      |
| LST start / stop   | 0 – 24 hr  | Local Sidereal Time range          |
| Number of stations | 1 – 512     | Stations included in the array     |

The SEFD is computed over a frequency grid of 50 – 350 MHz (51 points).
