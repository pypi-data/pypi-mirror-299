#!/usr/bin/env python
# -*- coding: utf-8 -*-

__docformat__ = "NumPy"
__author__ = "Lukas Gold"

__doc__ = """
Created on Fri Jul 26 08:44:00 2024
Last modified: see git version control

@author: LukasGold | lukas.gold@isc.fraunhofer.de
"""

# import modules
from datetime import timedelta
from enum import Enum

# Python version dependent import statements:
try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from pathlib import Path
from typing import Any
from warnings import warn

import pandas as pd
from batt_utility.data_models import (
    DataFormat,
    DecimalSeparator,
    Encoding,
    ReadFileParameter,
    ReadTableResult,
    Separator,
    TabularData,
    ThousandsSeparator,
)
from batt_utility.helper_functions import (
    apply_regex_return_match_groups,
    read_first_x_lines,
    read_specific_line_from_file,
)
from pydantic import BaseModel, field_validator
from typing_extensions import Callable, Dict, List, Literal, Optional, Tuple, Union


class DigatronDataFormat(StrEnum):
    german_client_csv = "German client CSV"


class DigatronTabularData(TabularData):
    data_format: DigatronDataFormat = DigatronDataFormat.german_client_csv

    def change_column_names(self, target_format: DataFormat):
        pass


class Language(StrEnum):
    de = "Deutsch"
    en = "English"


class HeaderStart(StrEnum):
    de = "Zeitstempel"
    en = "Timestamp"


class ReadDigatronCsvFileParameter(ReadFileParameter):
    lang: Language
    sep: Separator
    skiprows: int = None
    index_col: Union[Any, Literal[False], None] = None  # IndexLabel,
    usecols: Any = None  # UsecolsArgType
    column_names: Union[List[str], Callable] = None
    skip_blank_lines: bool = None
    infer_datetime_format: bool = None
    parse_dates: Union[bool, List[int], Dict[str, List[int]]] = None
    date_format: str = (None,)
    apply_to_cols: Dict[int, Tuple[Callable, str]] = {}
    exclude_from_params: List[str] = ["lang", "apply_to_cols"]


class HeaderRegExs(StrEnum):
    german_client_csv = r"([^\t\n\d\:]+)\:*\t([^\t\n]*)[\n]{1}"


def estimate_header(
    file_path: Union[str, Path],
    lang: Language = "de",
    encoding: Encoding = Encoding.iso8859_1,
) -> int:
    with open(file_path, "r", encoding=encoding.value) as f:
        header = 0
        for line in f:
            if line.startswith(HeaderStart[lang.name].value):
                return header
            header += 1
        warn(f"Could not find header in file {file_path}")
        return 0


class HeaderInfo(BaseModel):
    header: int
    columns: List[str]
    units: Dict[str, str]


def get_columns_and_units(
    file_path: Union[str, Path],
    lang: Language = "de",
    encoding: Encoding = Encoding.iso8859_1,
) -> HeaderInfo:
    header = estimate_header(file_path, lang, encoding)
    columns = read_specific_line_from_file(file_path, header).split("\n")[0].split("\t")
    units = (
        read_specific_line_from_file(file_path, header + 1).split("\n")[0].split("\t")
    )
    units_dict = {
        column: unit.strip("[]") for column, unit in zip(columns, units) if column != ""
    }  # todo: eventually strip needs to be language specific
    return HeaderInfo(header=header, columns=columns, units=units_dict)


def time_to_seconds(time_obj: Union[str, timedelta], time_format: str = None):
    """Convert a time object to seconds. This function is specific to the non-standard
    time format used in the Digatron data files."""
    time_str = str(time_obj)
    parts = time_str.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def time_array_to_seconds(
    time_array: Union[List[str], pd.Series], time_format: str = None
):
    if isinstance(time_array, list):
        return [time_to_seconds(t, time_format) for t in time_array]
    elif isinstance(time_array, pd.Series):
        new_vals = time_array_to_seconds(time_array.to_list(), time_format)
        time_array.update(new_vals)
        return time_array


class Configurations(Enum):
    german_client_csv = ReadDigatronCsvFileParameter(
        lang=Language.de,
        header=get_columns_and_units,
        encoding=Encoding.iso8859_1,
        sep=Separator.tab,
        decimal=DecimalSeparator.point,
        thousands=ThousandsSeparator.comma,
        skip_blank_lines=False,
        parse_dates=[0],
        date_format="%d.%m.%Y %H:%M:%S",
        apply_to_cols={
            3: (time_array_to_seconds, "s"),
            4: (time_array_to_seconds, "s"),
        },
    )


class DigatronDataTxtFile(ReadTableResult):
    """A class to read Digatron data files"""

    file_path: Union[str, Path]
    export_format: DigatronDataFormat
    meta: Optional[dict] = None
    data: Optional[DigatronTabularData] = None

    def read(self, remove_nan_cols: bool = True, remove_nan_rows: bool = True):
        """Read the data from the file

        Parameters
        ----------
        remove_nan_cols : Remove columns that only contain NaN values
        remove_nan_rows : Remove rows that contain NaN values (especially at the
            beginning where the checks are done)
        """
        self.meta = {}
        first_ten_lines = read_first_x_lines(self.file_path, 10)
        ftl_str = "\n".join(first_ten_lines)
        new_meta = apply_regex_return_match_groups(
            HeaderRegExs[self.export_format.name].value,
            ftl_str,
        )
        # todo: translate meta
        self.meta.update(new_meta)
        config = Configurations[self.export_format.name].value
        params = {
            key: (getattr(value, "value", value))
            for key, value in config.model_dump().items()
            if value is not None
        }
        # Get header, columns and units
        if callable(config.header):
            call_res = config.header(self.file_path, config.lang, config.encoding)
            params["header"] = call_res.header + 1
            params["names"] = call_res.columns
            self.meta["Units"] = call_res.units
        # Delete keys that are no valid parameters for pd.read_csv
        for key in config.exclude_from_params:
            if key in params:
                del params[key]
        # Read the data
        df = pd.read_csv(self.file_path, **params)
        # Apply functions to columns
        for col, (func, unit) in config.apply_to_cols.items():
            col_name = df.columns[col]
            df[col_name] = func(df[col_name])
            if unit:
                self.meta["Units"][col_name] = unit
        # Tidy up the data
        if remove_nan_cols:
            df.dropna(axis="columns", how="all", inplace=True)
        if remove_nan_rows:
            df.dropna(axis="index", how="any", inplace=True)
        self.data = DigatronTabularData(
            as_list=df.to_dict(orient="records"),
        )

        return self

    @field_validator("export_format")
    def check_export_format(cls, v):
        if v not in DigatronDataFormat:
            raise ValueError(f"Export format '{v}' not supported!")
        return v


# Functions
def read_digatron_data_file(
    file_path: Union[str, Path],
    frmt: DigatronDataFormat = DigatronDataFormat.german_client_csv,
):
    """Read a Digatron data file in the specified format

    Parameters
    ----------
    file_path : The path to the file
    frmt : The format of the file
    """
    digatron_data_txt_file = DigatronDataTxtFile(
        file_path=file_path, export_format=frmt
    )
    digatron_data_txt_file.read()
    return digatron_data_txt_file
