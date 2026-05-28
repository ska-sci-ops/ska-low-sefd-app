"""
SKA-Low SEFD Dashboard
======================
Interactive dashboard for exploring the System Equivalent Flux Density (SEFD)
returned by sefd.get_sefd().

Launch with:
    panel serve dashboard.py
"""

import io

import numpy as np
import panel as pn
import holoviews as hv
from holoviews import opts

import sefd as sefd_module

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")

# ── Preload the SEFD table once so the HDF5 file isn't reopened on every call ──
_sefd_table = sefd_module.SEFDTable()

# ── Widgets ───────────────────────────────────────────────────────────────────
alt_slider = pn.widgets.FloatSlider(
    name="Altitude (deg)", start=0, end=90, step=1, value=45
)
az_slider = pn.widgets.FloatSlider(
    name="Azimuth (deg)", start=0, end=360, step=1, value=0
)
lst_start_slider = pn.widgets.FloatSlider(
    name="LST start (hr)", start=0, end=24, step=0.5, value=0
)
lst_stop_slider = pn.widgets.FloatSlider(
    name="LST stop (hr)", start=0, end=24, step=0.5, value=4
)
n_station_slider = pn.widgets.IntSlider(
    name="Number of stations", start=1, end=512, step=1, value=1
)

# Fixed frequency grid
FREQ = np.linspace(50, 350, 51)


# ── Helper: compute SEFD for current widget values ────────────────────────────
def _compute_sefd():
    """Return (freq, sefd_values) for the current slider settings."""
    alt = alt_slider.value
    az = az_slider.value
    lst_start = lst_start_slider.value
    lst_stop = lst_stop_slider.value
    n_station = n_station_slider.value

    if lst_start == lst_stop:
        lst_stop = lst_start + 0.5
        if lst_stop > 24:
            lst_stop = 0.5

    sefd_values = (
        _sefd_table.lookup_stokes_i_sefd(az, alt, lst_start, lst_stop, FREQ)
        / n_station
    )
    return FREQ, sefd_values


# ── CSV download callback ─────────────────────────────────────────────────────
def _make_filename():
    alt = alt_slider.value
    az = az_slider.value
    lst_start = lst_start_slider.value
    lst_stop = lst_stop_slider.value
    n_station = n_station_slider.value
    return f"sefd_alt{alt:.0f}_az{az:.0f}_lst{lst_start:.1f}-{lst_stop:.1f}_N{n_station}.csv"


def _download_csv():
    """Return a StringIO CSV for the current SEFD data."""
    freq, sefd_values = _compute_sefd()
    buf = io.StringIO()
    buf.write("frequency_mhz,sefd_jy\n")
    for f, s in zip(freq, sefd_values):
        buf.write(f"{f:.2f},{s:.6f}\n")
    buf.seek(0)
    return buf


download_button = pn.widgets.FileDownload(
    callback=_download_csv,
    filename=_make_filename(),
    button_type="success",
    label="Download CSV",
)


def _update_filename(*_):
    download_button.filename = _make_filename()


for _w in [alt_slider, az_slider, lst_start_slider, lst_stop_slider, n_station_slider]:
    _w.param.watch(_update_filename, "value")


# ── Reactive computation ──────────────────────────────────────────────────────
@pn.depends(
    alt_slider, az_slider, lst_start_slider, lst_stop_slider, n_station_slider
)
def sefd_plot(alt, az, lst_start, lst_stop, n_station):
    """Compute SEFD and return a HoloViews Curve."""
    freq, sefd_values = _compute_sefd()

    curve = hv.Curve(
        (freq, sefd_values),
        kdims=["Frequency (MHz)"],
        vdims=["SEFD (Jy)"],
    ).opts(
        opts.Curve(
            title=f"SEFD  |  alt={alt:.0f}°  az={az:.0f}°  LST={lst_start:.1f}–{lst_stop:.1f} h  N={n_station}",
            line_width=2,
            color="#1f77b4",
            tools=["hover"],
            height=450,
            responsive=True,
            logy=True,
            ylabel="SEFD (Jy)",
            fontsize={"title": "11pt", "labels": "11pt", "ticks": "10pt"},
        )
    )
    return curve


# ── Layout ────────────────────────────────────────────────────────────────────
sidebar = pn.Column(
    pn.pane.Markdown("## Parameters"),
    alt_slider,
    az_slider,
    pn.layout.Divider(),
    lst_start_slider,
    lst_stop_slider,
    pn.layout.Divider(),
    n_station_slider,
    pn.layout.Divider(),
    download_button,
    width=300,
)

main_area = pn.Column(
    pn.pane.Markdown("# SKA-Low SEFD Explorer"),
    pn.pane.HoloViews(sefd_plot, sizing_mode="stretch_both"),
)

template = pn.template.MaterialTemplate(
    title="SKA-Low SEFD Dashboard",
    sidebar=[sidebar],
    main=[main_area],
)

template.servable()
