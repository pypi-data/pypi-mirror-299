import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import xarray
import matplotlib.colors as mcolors
import numpy as np
import cftime
import nc_time_axis
from waffle.definitions import *


plt.style.use(PATH_MPLSTYLE_PACL)
cmap_temp_seq = mcolors.LinearSegmentedColormap.from_list('colormap', np.loadtxt(PATH_CMAP_TEMPSEQ))


def addSubPlotLabels(f):
    for index, ax in enumerate(f.axes):
        label = chr(ord('@') + (index + 1 % 26))
        ax.set_title(f"{label})", loc="left", fontweight="bold")


def generateReferenceFigure():
    sample_spatial_ds = xarray.open_dataset(PATH_SAMPLE_SPATIAL)[SAMPLE_VAR] - 273.15
    sample_ts_ds = xarray.open_dataset(PATH_SAMPLE_TS)[SAMPLE_VAR] - 273.15
    sample_day_ts_ds = xarray.open_dataset(PATH_SAMPLE_TS_DAY)[SAMPLE_VAR] - 273.15

    sample_ts_ds = sample_ts_ds.sel(time=slice(
        cftime.DatetimeNoLeap(2015, 12, 31, 0, 0, 0, 0, has_year_zero=True),
        cftime.DatetimeNoLeap(2080, 1, 1, 0, 0, 0, 0, has_year_zero=True)
    ))

    f = plt.figure()
    gridspec = f.add_gridspec(2, 2, height_ratios=[2, 2])

    ax1 = f.add_subplot(gridspec[0, 0])
    ax2 = f.add_subplot(gridspec[0, 1])

    ax3 = f.add_subplot(gridspec[1, 0])
    ax4 = f.add_subplot(gridspec[1, 1])

    ax1.set_title("Closed Line Plot Title (12 pt)")
    ax2.set_title("Map Plot Title (12 pt)")

    ax3.set_title("Open Line Plot Title (12 pt)")
    ax4.set_title("Scatter Plot Title (12 pt)")

    f.suptitle("WAFFLE Reference Figure Version 1.0 (16 pt)")

    ax1.set_xlabel("Time (Year)")
    ax3.set_xlabel("Time (Year)")
    ax4.set_xlabel("Time (Day of Year)")

    ax1.set_ylabel("Temperature ($\\degree$C)")
    ax3.set_ylabel("Temperature ($\\degree$C)")
    ax4.set_ylabel("Temperature ($\\degree$C)")

    addSubPlotLabels(f)

    ax1.xaxis.set_major_formatter(nc_time_axis.CFTimeFormatter("%Y", "noleap"))

    ax1.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values, label="Legend 1")
    ax1.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values + 1, label="Legend 2")
    ax1.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values + 2, label="Legend 3")

    ax1.legend(fancybox=False)

    ax1.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3, sample_ts_ds.mean(dim="member").values + 0.3, alpha=0.3)
    ax1.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3 + 1, sample_ts_ds.mean(dim="member").values + 0.3 + 1, alpha=0.3)
    ax1.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3 + 2, sample_ts_ds.mean(dim="member").values + 0.3 + 2, alpha=0.3)

    ax1.set_xlim(cftime.DatetimeNoLeap(2015, 12, 31, 0, 0, 0, 0, has_year_zero=True),
                 cftime.DatetimeNoLeap(2080, 1, 1, 0, 0, 0, 0, has_year_zero=True))
    ax1.set_ylim(6, 12)

    ax3.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values + 3, color=LINE_COLORS[3])
    ax3.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values + 4, color=LINE_COLORS[4])
    ax3.plot(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values + 5, color=LINE_COLORS[5])

    ax3.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3 + 3, sample_ts_ds.mean(dim="member").values + 0.3 + 3, alpha=0.3, color=LINE_COLORS[3])
    ax3.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3 + 4, sample_ts_ds.mean(dim="member").values + 0.3 + 4, alpha=0.3, color=LINE_COLORS[4])
    ax3.fill_between(sample_ts_ds.time.values, sample_ts_ds.mean(dim="member").values - 0.3 + 5, sample_ts_ds.mean(dim="member").values + 0.3 + 5, alpha=0.3, color=LINE_COLORS[5])

    ax3.set_xlim(cftime.DatetimeNoLeap(2015, 12, 31, 0, 0, 0, 0, has_year_zero=True),
                 cftime.DatetimeNoLeap(2100, 1, 1, 0, 0, 0, 0, has_year_zero=True))

    date_pt = cftime.DatetimeNoLeap(2080, 12, 31, 0, 0, 0, 0, has_year_zero=True)
    ax3.text(date_pt, sample_ts_ds.mean(dim="member").values[-1] + 3, "Legend 1", fontdict=dict(color=LINE_COLORS[3]))
    ax3.text(date_pt, sample_ts_ds.mean(dim="member").values[-1] + 4, "Legend 2", fontdict=dict(color=LINE_COLORS[4]))
    ax3.text(date_pt, sample_ts_ds.mean(dim="member").values[-1] + 5, "Legend 3", fontdict=dict(color=LINE_COLORS[5]))

    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.grid(False)

    ax2.xaxis.set_visible(False)
    ax2.yaxis.set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.grid(False)

    props = dict(facecolor='white', pad=0.4, edgecolor='white')
    ax2.text(0, 0.1, f"{round(float(sample_spatial_ds.mean().values), 2)}$\\pm {round(float(sample_spatial_ds.std().values), 2)}$", bbox=props)

    ax2 = f.add_axes(ax2.get_position(), frameon=True, projection=WinkelTripel(), zorder=-1)

    cyclic_values, cyclic_lons = add_cyclic_point(sample_spatial_ds.values, sample_spatial_ds.lon.values, axis=-1)
    ax2_contour = ax2.contourf(cyclic_lons, sample_spatial_ds.lat.values, cyclic_values, transform=ccrs.PlateCarree(), cmap=cmap_temp_seq)
    ax2_cbar = f.colorbar(ax2_contour, location="bottom", anchor=(0.0, 0.0), pad=0)
    ax2_cbar.set_label("Temperature ($\\degree$C)")
    ax2.coastlines()

    days = [date.dayofyr + 1 for date in sample_day_ts_ds.time.values]
    vals = sample_day_ts_ds.values

    indices = [int(index) for index in np.random.random(200)*len(days)]
    ax4.scatter([days[index] for index in indices], [vals[index] for index in indices])

    indices = [int(index) for index in np.random.random(200)*len(days)]
    ax4.scatter([days[index] for index in indices], [vals[index] for index in indices])

    indices = [int(index) for index in np.random.random(200)*len(days)]
    ax4.scatter([days[index] for index in indices], [vals[index] for index in indices])

    ax4.set_xlim(1, 365)

    # Add PACL copyright
    # Figure out legend

    f.show()
    return f