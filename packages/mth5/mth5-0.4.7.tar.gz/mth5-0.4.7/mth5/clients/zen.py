#!/usr/bin/env python
# coding: utf-8

# # Make an MTH5 from Phoenix Data
#
# This example demonstrates how to read Phoenix data into an MTH5 file.  The data comes from example data in [PhoenixGeoPy](https://github.com/torresolmx/PhoenixGeoPy). Here I downloaded those data into a local folder on my computer by forking the main branch.

# ## Imports

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from loguru import logger

from mth5.mth5 import MTH5
from mth5 import read_file
from mth5.io.zen import Z3DCollection

# =============================================================================


class ZenClient:
    def __init__(
        self,
        data_path,
        sample_rates=[4096, 1024, 256],
        save_path=None,
        calibration_path=None,
        **kwargs,
    ):
        self.logger = logger
        self.data_path = data_path
        self.sample_rates = sample_rates
        self.mth5_filename = "from_zen.h5"
        self.save_path = save_path
        self.calibration_path = calibration_path

        self.mth5_version = "0.2.0"
        self.interact = False
        self.compression = "gzip"
        self.compression_opts = 4
        self.shuffle = True
        self.fletcher32 = True
        self.data_level = 1

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.collection = Z3DCollection(self.data_path)

    @property
    def data_path(self):
        """Path to phoenix data"""
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if value is not None:
            self._data_path = Path(value)
            if not self._data_path.exists():
                raise IOError(f"Could not find {self._data_path}")

            self.collection = Z3DCollection(self.data_path)

        else:
            raise ValueError("data_path cannot be None")

    @property
    def calibration_path(self):
        """Path to calibration data"""
        return self._calibration_path

    @calibration_path.setter
    def calibration_path(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if value is not None:
            self._calibration_path = Path(value)
            if not self._calibration_path.exists():
                raise IOError(f"Could not find {self._calibration_path}")

        else:
            raise ValueError("calibration_path cannot be None")

    @property
    def sample_rates(self):
        """sample rates to look for"""
        return self._sample_rates

    @sample_rates.setter
    def sample_rates(self, value):
        """
        sample rates set to a list

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if isinstance(value, (int, float)):
            self._sample_rates = [value]
        elif isinstance(value, str):
            self._sample_rates = [float(v) for v in value.split(",")]

        elif isinstance(value, (tuple, list)):
            self._sample_rates = [float(v) for v in value]
        else:
            raise TypeError(f"Cannot parse {type(value)}")

    @property
    def save_path(self):
        """Path to save mth5"""
        return self._save_path

    @save_path.setter
    def save_path(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if value is not None:
            self._save_path = Path(value)
            if self._save_path.is_dir():
                self._save_path = self._save_path.joinpath(self.mth5_filename)

        else:
            self._save_path = self.data_path.joinpath(self.mth5_filename)

    def get_run_dict(self):
        """
        Get Run information

        :return: DESCRIPTION
        :rtype: TYPE

        """

        return self.collection.get_runs(
            sample_rates=self.sample_rates,
            calibration_path=self.calibration_path,
        )

    def get_survey(self, station_dict):
        """
        get survey name from a dictionary of a single station of runs
        :param station_dict: DESCRIPTION
        :type station_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        return list(
            set(
                [
                    station_dict[k].survey.unique()[0]
                    for k in station_dict.keys()
                ]
            )
        )[0]

    def make_mth5_from_zen(self, survey_id=None, combine=True, **kwargs):
        """
        Make an MTH5 from Phoenix files.  Split into runs, account for filters

        :param data_path: DESCRIPTION, defaults to None
        :type data_path: TYPE, optional
        :param sample_rates: DESCRIPTION, defaults to None
        :type sample_rates: TYPE, optional
        :param save_path: DESCRIPTION, defaults to None
        :type save_path: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

        runs = self.get_run_dict()

        with MTH5() as m:
            m.file_version = self.file_version
            m.compression = self.compression
            m.compression_opts = self.comporession_opts
            m.shuffle = self.shuffle
            m.fletcher32 = self.fletcher32
            m.data_level = self.data_level

            m.open_mth5(self.save_path, "w")
            for station_id, station_dict in runs.items():
                if survey_id is None:
                    survey_id = self.get_survey(station_dict)
                survey_group = m.add_survey(survey_id)
                station_group = survey_group.stations_group.add_station(
                    station_id
                )
                station_group.metadata.update(
                    self.collection.station_metadata_dict[station_id]
                )
                station_group.write_metadata()
                if combine:
                    run_list = []
                for run_id, run_df in station_dict.items():
                    run_group = station_group.add_run(run_id)
                    for row in run_df.itertuples():
                        ch_ts = read_file(
                            row.fn,
                            calibration_fn=row.calibration_fn,
                        )
                        run_group.from_channel_ts(ch_ts)
                    run_group.update_metadata()
                    if combine:
                        run_list.append(run_group.to_runts())
                if combine:
                    # Combine runs and down sample to 1 second.
                    combined_run = run_list[0].merge(
                        run_list[1:], new_sample_rate=1
                    )
                    combined_run.run_metadata.id = "sr1_0001"
                    combined_run_group = station_group.add_run("sr1_0001")
                    combined_run_group.from_runts(combined_run)
                    combined_run_group.update_metadata()
                station_group.update_metadata()
            survey_group.update_metadata()

        self.logger.info(f"Wrote MTH5 file to: {self.save_path}")

        return self.save_path
