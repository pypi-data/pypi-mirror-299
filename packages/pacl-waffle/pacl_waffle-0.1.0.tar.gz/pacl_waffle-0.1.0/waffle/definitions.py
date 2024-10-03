import os


PATH_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_CMAP_TEMPSEQ = f"{PATH_ROOT_DIR}/ipcc_colormaps/continuous_colormaps_rgb_0-1/temp_seq.txt"
PATH_MPLSTYLE_PACL = f'{PATH_ROOT_DIR}/pacl.mplstyle'
PATH_SAMPLE_SPATIAL = f"{PATH_ROOT_DIR}/reference_datasets/sample_spatial_ds.nc"
PATH_SAMPLE_TS = f"{PATH_ROOT_DIR}/reference_datasets/sample_timeseries_ds.nc"
PATH_SAMPLE_TS_DAY = f"{PATH_ROOT_DIR}/reference_datasets/sample_day_timeseries_ds.nc"

# CONFIGS
SAMPLE_VAR = "tasmax"
LINE_COLORS = ['#000000', '#70A0CD', '#C47900', '#B2B2B2', '#003466', '#004F00']
SHADE_COLORS = ['#808080', '#5BAEB2', '#CCAE71', '#BFBFBF', '#4393C3', '#DFEDC3']