import functools
import logging
from datetime import datetime
from os import PathLike
from pathlib import Path
from threading import Lock
from typing import Union

import numpy as np
import pandas as pd
import xarray as xr

from gcviz.utils import timeit
from gcviz.flags import Flags

lock_on_files_lock = Lock()
files_locks: dict[Path, Lock] = {}


logger = logging.getLogger("gcviz.netcdf")


def parse_flag_arg(func):
    """Decorator that converts the list argument to a tuple."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        key = "flags_selected"
        if key in kwargs and isinstance(kwargs[key], list):
            kwargs[key] = tuple(kwargs[key])
        return func(*args, **kwargs)

    return wrapper


# List of flag and their values (that are kept or removed)
registered_flags = {
    "met_office_baseline_flag": 66,  # 'B' in ascii for baseline
    "git_pollution_flag": 80,  # 'P' in ascii for pollution
    "baseline": int(1),  # "0, 1": "not_baseline, baseline";
}
flag_type = {
    "met_office_baseline_flag": Flags.ONLY_BASELINE,
    "git_pollution_flag": Flags.REMOVE_POLLUTION,
    "baseline": Flags.ONLY_BASELINE,
}


class NetcdfLoader:
    """Loader class for the netcdf files.

    Read all files in the given directory to know networks, sites, compounds and instruments.



    """

    def __init__(
        self,
        directory: PathLike,
        stem_format: str = "network-instrument_site_compound",
        invalid_value: float | None = None,
    ) -> None:
        d = Path(directory)

        if not d.is_dir():
            raise FileNotFoundError(f"{d} is not a directory")

        self.directory = d

        self.logger = logging.getLogger("gcviz.NetcdfLoader")

        variables = stem_format.split("_") + ["file"]

        data = [f.stem.split("_") + [f] for f in d.rglob("*.nc")]

        bad_data = [d for d in data if len(d) != len(variables)]
        if len(bad_data) > 0:
            self.logger.warning(
                f"Files found that do not match format {stem_format} : {bad_data}"
            )

        data = [d for d in data if len(d) == len(variables)]
        if len(data) == 0:
            self.logger.warning(f"No netcdf files found in {d}")

        self.df_files = pd.DataFrame(data, columns=variables)

        self.sites = self.df_files["site"].unique()
        self.compounds = self.df_files["compound"].unique()
        self.instruments = self.df_files["network-instrument"].unique()

        self.invalid_value = invalid_value

    @parse_flag_arg
    @timeit
    @functools.lru_cache
    def read_data(
        self,
        site: str,
        compound: str,
        date_interval: tuple[datetime | None, datetime | None] = (None, None),
        flags_selected: list[Flags] = [],
    ) -> pd.Series | None:
        """Read the data from the netcdf files.

        Parameters
        ----------
        sites : list[str]
            The sites to read.
        compounds : list[str]
            The compounds to read.
        date_interval : tuple[datetime, datetime]
            The date interval to read.

        Returns
        -------
        pd.DataFrame
            The dataframe with the data.
        """
        # Get the files to read
        series = []
        self.logger.info(f"Reading {site=} {compound=} {date_interval=}")

        df_this_files = self.df_files[
            (self.df_files["site"] == site) & (self.df_files["compound"] == compound)
        ]
        if len(df_this_files) == 0:
            self.logger.warning(f"No netcdf file found for {site} {compound}")
            return None

        with lock_on_files_lock:
            for file in df_this_files["file"]:
                if file not in files_locks:
                    files_locks[file] = Lock()

        # Aquire the lock for the files
        for file in df_this_files["file"]:
            files_locks[file].acquire()

        try:

            dss = [xr.open_dataset(f) for f in df_this_files["file"]]

            ds = (
                xr.concat([ds for ds in dss], dim="time")
                .sortby("time")
                .sel(time=slice(date_interval[0], date_interval[1]))
            )

            # Check length of the data
            if len(ds["time"]) == 0:
                self.logger.warning(
                    f"No data found for {site=} {compound=} included in {date_interval=} \n"
                    f"Valid times are {ds['time'].values}"
                )
                return None

            if "mf" not in ds:
                self.logger.warning(f"No `mf` found for {site=} {compound=}")
                return None

            mask = np.ones_like(ds["mf"].values, dtype=bool)
            if self.invalid_value is not None:
                mask &= ds["mf"] != self.invalid_value
                logger.debug(
                    f"Removing {self.invalid_value=}: {(~mask).sum().values} / {len(mask)} values flagged"
                )

            for flag_name, flag_value in registered_flags.items():
                if flag_type[flag_name] not in flags_selected:
                    continue
                if flag_name not in ds:
                    self.logger.warning(f"No {flag_name} found for {site=} {compound=}")
                    continue
                match flag_type[flag_name]:
                    case Flags.ONLY_BASELINE:
                        flag_mask = ds[flag_name] == flag_value
                    case Flags.REMOVE_POLLUTION:
                        flag_mask = ds[flag_name] != flag_value
                    case _:
                        raise ValueError(f"Flag type {flag_type} not implemented")
                logger.debug(
                    f"For {flag_name=} {flag_value=}: {(~flag_mask).sum().values} / {len(flag_mask)} values flagged"
                )

                mask &= flag_mask

            logger.debug(
                f"Final mask: {(~mask).sum().values} / {len(mask)} values flagged"
            )

            serie = ds["mf"].loc[mask].to_pandas()
        except Exception as e:
            self.logger.error(f"Error reading {site=} {compound=} {date_interval=}")
            self.logger.error(e)
            serie = None
        finally:
            for ds in dss:
                ds.close()
            for file in df_this_files["file"]:
                files_locks[file].release()

        return serie


class GlobalLoader:
    # Global pointer to the loader
    _loader: NetcdfLoader | None = None

    @classmethod
    def set(cls, loader: NetcdfLoader):
        if cls._loader is not None:
            raise RuntimeError("Global loader already set")
        cls._loader = loader

    @classmethod
    def get(cls) -> NetcdfLoader:
        if cls._loader is None:
            raise RuntimeError("Global loader not set")
        return cls._loader


if __name__ == "__main__":
    loader = NetcdfLoader(r"C:\Users\coli\Documents\Data\gcdata")
    print(loader.df_files)

    print(loader.sites, loader.compounds, loader.instruments)

    df = loader.read_data("ASA", "cfc-12", (datetime(2001, 1, 1), datetime(2023, 1, 2)))
    print(df.head())
