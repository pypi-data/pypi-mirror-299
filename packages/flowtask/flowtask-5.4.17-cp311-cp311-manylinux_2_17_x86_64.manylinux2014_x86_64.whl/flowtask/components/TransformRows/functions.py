"""
Functions.

Tree of TransformRows functions.

TODO: add a function to apply a util function to all rows in Column.
"""
import ast
import datetime
from typing import Any, Dict, List, Optional, Union
from functools import reduce
import traceback
import orjson
import requests
import numpy as np
import pandas
from pandas import json_normalize
from bs4 import BeautifulSoup
import timezonefinder
import locale
from navconfig.logging import logging
from pandas.tseries.offsets import MonthEnd
from querysource.types import strtobool
from ...conf import DEFAULT_TIMEZONE, BARCODELOOKUP_API_KEY


def extract_from_array(df: pandas.DataFrame, field: str = "", column: str = "", index = 0):
    if index == 'first':
        idx = 0
    elif index == 'last':
        idx = -1
    else:
        idx = index
    try:
        df[field] = df[column].apply(lambda x: x[idx] if isinstance(x, list) and x is not None else None)
    except Exception as err:
        logging.error(f"extract_from_array Error: {err}")
    finally:
        return df


def explode(
    df: pandas.DataFrame,
    field: str,
    columns: list = None,
    is_string: bool = True,
    delimiter: str = ",",
):
    splitcols = [field]
    if columns is not None:
        splitcols = splitcols + columns
    ### first: convert all colums to list:
    if is_string is True:
        for col in splitcols:
            try:
                df[col] = [x.strip("()").split(delimiter) for x in df[col]]
            except KeyError:
                pass  # TODO: remove column from list of columns
            except AttributeError:
                # capturing when col cannot be splitted:
                df[col] = df[col].str.strip("()").str.split(delimiter)
    try:
        df = df.explode(splitcols, ignore_index=True)
    except ValueError as err:
        logging.error(f"Explode Error: {err}")
    finally:
        return df  # pylint: disable=W0150


def sum(df: pandas.DataFrame, field: str = "", columns: list = []):
    try:
        if columns and isinstance(columns, list):
            df[field] = df[columns].sum(axis=1)
        return df
    except Exception as err:
        print("SUM Error ", err)
        return df


def div(df, field: str, numerator: str, denominator: str):
    try:
        df[field] = df[numerator].div(df[denominator].values)
        return df
    except Exception as err:
        print("DIV Error ", err)
        return df


def to_time(
    df,
    field: str,
    replace_nulls: bool = False,
    value: str = "00:00:00",
    format: str = "%I:%M %p",
    fallback_format: str = "%I:%M%p",
    as_timedelta: bool = False
):
    try:
        locale.setlocale(locale.LC_TIME, ('en_US', 'UTF-8'))
        # Attempt to convert directly if already a datetime object
        df[field] = df[field].dt.time
    except AttributeError:
        # If it's not a datetime object, convert it
        try:
            try:
                df[field] = pandas.to_datetime(df[field], format=format).dt.time
            except ValueError:
                df[field] = pandas.to_datetime(df[field], format=fallback_format).dt.time
        except ValueError:
            df[field] = df[field].apply(
                lambda x: datetime.datetime.strptime(
                    x.strip(), format
                ).time() if pandas.notnull(x) else x
            )
        except Exception as err:
            print('DT Error > ', err)
            return df
    try:
        if as_timedelta is True:
            # Convert datetime.time to timedelta64[ns] (representing time)
            df[field] = df[field].apply(
                lambda t: pandas.to_timedelta(
                    f"{t.hour:02}:{t.minute:02}:{t.second:02}"
                )
                if t is not None
                else pandas.NaT
            )
        else:
            # Create a new series with datetime objects, preserving time-only
            time_series = df[field].apply(
                lambda t: pandas.Timestamp(
                    year=1900, month=1, day=1, hour=t.hour, minute=t.minute, second=t.second
                )
                if t is not None
                else pandas.NaT
            )
            # Convert to datetime64[ns] and extract time component
            df[field] = pandas.to_datetime(time_series)
    except Exception as e:
        print(f"Error converting '{field}' to time: {e}")

    # avoid NaT values on field:
    if replace_nulls:
        df[field] = np.where(df[field].isnull(), value, df[field])
    return df


def middle_time(df: pandas.DataFrame, field: str, columns: list) -> pandas.DataFrame:
    # Calculate the middle time
    c1 = columns[0]
    c2 = columns[1]
    df[field] = df[c1] + (df[c2] - df[c1]) / 2
    return df


def drop_column(df: pandas.DataFrame, field: str):
    return df.drop([field], axis=1)


def add_days(df: pandas.DataFrame, field: str, column="", days=1):
    df[field] = df[column] + pandas.DateOffset(days=days)
    return df


def add_timestamp_to_time(df: pandas.DataFrame, field: str, date: str, time: str):
    # Combine the date with the time to create the new columns
    df[field] = pandas.to_datetime(
        df[date].dt.date.astype(str) + " " + df[time].dt.time.astype(str)
    )
    return df


def substract_days(df: pandas.DataFrame, field: str, column="", days=1):
    df[field] = df[column] - pandas.DateOffset(days=days)
    return df


def rename_column(df: pandas.DataFrame, field: str, rename=""):
    return df.rename(columns={field: rename})


def regex_match(df: pandas.DataFrame, field: str, column="", regex=""):
    df[field] = df[column].str.extract(regex)
    return df


def zerofill(df: pandas.DataFrame, field: str, num_zeros=1):
    """Fill with zeroes an string until the length"""
    df[field] = df[field].astype(str).str.zfill(num_zeros)
    return df


def pad(df: pandas.DataFrame, field: str, num_chars=4, side="left", char="0"):
    """Pad (add) chars until the string lenght based on side (left, right)."""
    df[field] = df[field].astype(str).str.pad(num_chars, side=side, fillchar=char)
    return df


def concat(df: pandas.DataFrame, field: str, columns=[], separator=" "):
    try:
        if columns and isinstance(columns, list):
            df[field] = (
                df[columns]
                .fillna("")
                .astype(str)
                .apply(lambda x: x.str.cat(sep=separator), axis=1)
            )
        return df
    except Exception as err:
        print("CONCAT Error ", err)
        return df
    
def concat_column_values(df: pandas.DataFrame, field: str, column: str, separator=","):
    """
    Concatenates all values in the specified column of a DataFrame into a single string, 
    separated by a specified delimiter, and assigns this string to a new or existing field in the DataFrame.
    """
    try:
        df[field] = separator.join(df[column].fillna("").astype(str))
    except Exception as err:
        print("CONCAT Error: ", err)
    
    return df

def concat_column_values(df: pandas.DataFrame, field: str, column: str, separator=","):
    """
    Concatenates all values in the specified column of a DataFrame into a single string, 
    separated by a specified delimiter, and assigns this string to a new or existing field in the DataFrame.
    """
    try:
        df[field] = separator.join(df[column].fillna("").astype(str))
    except Exception as err:
        print("CONCAT Error: ", err)
    
    return df

def _apply_affix(df, field: str, column: str, prefix: str = "", suffix: str = ""):
    """Helper function to apply a prefix or suffix to a column."""
    if not column:
        column = field
    try:
        df[field] = df[column].apply(lambda x: f"{prefix!s}{x}{suffix!s}")
        return df
    except Exception as err:
        print("Affix Error ", err)
        return df

def prefix(df, field: str, column: str = None, prefix: str = ""):
    """Adding a string prefix to a Column."""
    return _apply_affix(df, field, column, prefix=prefix)

def suffix(df, field: str, column: str = None, suffix: str = ""):
    """Adding a string suffix to a Column."""
    return _apply_affix(df, field, column, suffix=suffix)

def normalize_strings(
    df: pandas.DataFrame,
    field: str,
    column="",
    lowercase: bool = True,
    clean_strings: bool = False,
    replacement: str = "_",
):
    """Lowercase and remove spaces for replacement char on strings."""
    try:
        col = column if column else field
        df[field] = df[col]
        if clean_strings is True:
            charsToRemove = [",", ".", r"\.", r"\'"]
            df[field] = df[field].str.replace(
                r"{}".format(charsToRemove), replacement, regex=True
            )
        if lowercase is True:
            df[field] = df[field].str.lower()
        df[field] = df[field].str.replace(" ", replacement, regex=True)
        return df
    except Exception as err:
        print("Normalize Error ", err)
        return df


def coalesce(df: pandas.DataFrame, field: str, column: str = None, match: str = None):
    "Coalesce mimic the Coalesce of DB, when a column is null, put a new value"
    if column:
        try:
            df[field] = np.where(df[field].isnull(), df[column], df[field])
        except Exception as err:
            print("COALESCE Error: ", err)
    elif match:
        # if match is string then:
        if isinstance(match, list):
            # is a function
            fname = match[0]
            args = {}
            result = None
            func = globals()[fname]
            if len(match) > 1:
                args = match[1]
            if callable(func):
                try:
                    result = func(**args)
                except Exception as err:
                    print("Coalesce Error ", err)
                    result = func()
            if result:
                try:
                    df[field] = df[field].fillna(result)
                except Exception as err:
                    print("Coalesce Error ", err)
                    return df
        else:
            df[field] = np.where(df[field].isnull(), match, df[field])
    else:
        return df
    return df


def split_array(df: pandas.DataFrame, field: str, column="", separator=" ", trim=False):
    try:
        col = column if column else field
        df[col] = df[field].str.split(separator)
        # if trim is True:
        #     df[col] = df[col].apply(lambda x: separator.join(x), axis=1)
        return df
    except Exception as err:
        print("Split Error: ", err)
        return df


def split(
    df: pandas.DataFrame,
    field: str,
    column: str,
    separator: str = " ",
    idx: int = 0,
    is_integer: bool = False,
) -> pandas.DataFrame:
    """
    This function takes a pandas DataFrame and splits the values in a specified column
      into multiple values based on a specified separator,
    and stores the resulting split values in a new column in the same DataFrame.

    :param df: pandas DataFrame to be modified.
    :param field: Optional, name of the new column to store the split values.
       Defaults to an empty string ('') which will store the split values in a
       column with the same name as the original column, but with the index
       of the split value appended.
    :param column: Name of the column in the df DataFrame to be splitted.
    :param separator: Optional, the character or string used as the separator
        to split the values in the specified column. Defaults to a space (' ').
    :param index: Optional, the index of the split value to be extracted and stored in
        the new column. Defaults to 0 which will store the first split value.
    :param is_integer: Optional, a boolean flag that determines whether the
        split value should be converted to an integer data type. Defaults to False.
    :return: Modified pandas DataFrame with the split values stored in a new column.
    """
    try:
        # Split the values in the specified column using the provided separator and
        # store the resulting split values in a new column
        try:
            idx = int(idx)
        except (ValueError, TypeError) as ex:
            idx = 0
        if not field:
            field = column + "_" + str(idx)
        df[field] = df[column].str.split(separator).str[idx]
        if is_integer is True:
            df[field] = pandas.to_numeric(df[field], errors="coerce")
            df[field] = df[field].astype("Int64")
        return df
    except Exception as err:
        print("Split Error: ", err)
        return df


def split_to_columns(df, field: str, columns: list, regex: str = "\s+", expand: bool = True):
    try:
        df[columns] = df[field].str.extract(regex, expand=expand)
    except Exception as err:
        print("Split to Columns Error: ", err)
    finally:
        return df


def slice(
    df: pandas.DataFrame,
    field: str,
    column="",
    start=0,
    end=1,
    is_integer: bool = False,
):
    """Slice: substring an string between 2 characters."""
    try:
        df[field] = df[column].astype(str).str.slice(start, end)
        if is_integer is True:
            df[field] = df[field].astype("Int64")
        return df
    except Exception as err:
        print("Slice Error: ", err)
        return df


def case(
    df: pandas.DataFrame,
    field: str,
    column="",
    condition: Any = None,
    match=None,
    notmatch=None,
):
    """Case.

    Generate a selection of option like a CASE.
    """
    if type(condition) == list:
        # conditions = [df[column].eq(condition[0]) & df[column].eq(condition[1])]
        df[field] = np.select([df[column].isin(condition)], [match], default=notmatch)
    else:
        df[field] = np.select([df[column] == condition], [match], default=notmatch)
    return df


def divide(df: pandas.DataFrame, field: str, divisor=100):
    df[field] = pandas.to_numeric(df[field], errors="coerce")
    df[field] = df[field].replace([-np.inf, np.inf], np.nan)
    df[field] = df[field].apply(lambda x: x / divisor)
    return df


def nullif(df: pandas.DataFrame, field: str, chars=[]):
    df.loc[(df[field].isin(chars)), field] = None
    return df


def to_null(df, field: str, words: list):
    try:
        df[field] = df[field].apply(lambda x: np.nan if x in words else x)
    except Exception as err:
        print(err)
    return df


def capitalize(df: pandas.DataFrame, field: str):
    df[field] = df[field].str.title()
    return df


def to_round(df, field: str, ndecimals: int = 2):
    try:
        df[field].astype("float")
        df[field] = df[field].apply(lambda x: round(x, ndecimals))
    except Exception as err:
        print(err)
    return df


def uppercase(df: pandas.DataFrame, field: str, from_column: str = None):
    if from_column is not None:
        column = from_column
    else:
        column = field
    df[field] = df[column].str.upper()
    return df


def lowercase(df: pandas.DataFrame, field: str, from_column: str = None):
    if from_column is not None:
        column = from_column
    else:
        column = field
    df[field] = df[column].str.lower()
    return df


def both_strip(df: pandas.DataFrame, field: str, character=" "):
    df[field] = df[field].str.strip(character)
    return df


def trim(df: pandas.DataFrame, field: str, characters=" ", remove_empty: bool = False):
    df[field] = df[field].str.strip()
    df[field] = df[field].str.strip(characters)
    if remove_empty is True:
        df[field] = df[field].replace("", None)
    return df


def ltrim(df, field: str, characters=" "):
    df[field] = df[field].str.strip()
    try:
        df[field] = df[field].str.lstrip(characters)
    except Exception as err:
        print(err)
    return df


def ltrip(df, field: str, nchars: int = 0):
    df[field] = [i[nchars:] for i in df[field]]
    return df


def rtrip(df, field: str, nchars: int = 0):
    df[field] = [i[:nchars] for i in df[field]]
    return df


def left_strip(df, field: str, column: str = None, character=" "):
    try:
        if not column:
            column = field
        df[field] = df[column].str.lstrip(character)
    except Exception as err:
        print(traceback.format_exc())
        print(err)
    return df


def right_strip(df: pandas.DataFrame, field: str, character=" "):
    df[field] = df[field].str.rstrip(character)
    return df


def string_replace(
    df: pandas.DataFrame,
    field: str,
    column: str = None,
    to_replace: str = "",
    value: str = "",
):
    """Replaces an string on a Column and optionally returned in another column."""
    if not column:
        column = field
    try:
        df[column] = df[field].str.replace(to_replace, value)
    except Exception as err:
        print(err)
    return df


def replace_regex(df: pandas.DataFrame, field: str, to_replace="", value=""):
    try:
        if isinstance(to_replace, list):
            for rplc in to_replace:
                df[field] = df[field].str.replace(rplc, value, regex=True)
        else:
            df[field] = df[field].astype(str).str.replace(to_replace, value, regex=True)
    except Exception as err:
        print(traceback.format_exc())
        print(err)
    return df


def ereplace(df: pandas.DataFrame, field: str, columns=[], newvalue=""):
    col1 = columns[0]
    col2 = columns[1]
    df[field] = df.apply(lambda x: x[col1].replace((x[col2]), ""), 1)
    return df

def replace_to_nan(df: pandas.DataFrame, field: str, to_replace=[]):
    df[field] = df[field].replace(to_replace, np.nan)
    return df

def convert_to_object(df: pandas.DataFrame, field: str = "", remove_nan: bool = False):
    df[field] = df[field].astype(str)
    df[field] = df[field].fillna("")
    if remove_nan is True:
        df[field] = df[field].str.replace(np.nan, "", regex=True)
    return df


def convert_to_string(
    df: pandas.DataFrame,
    field: str = "",
    remove_nan: bool = False,
    avoid_empty: bool = True,
):
    try:
        df[field] = df[field].astype(str, errors="raise")
        df[field] = df[field].fillna("")
        if remove_nan is True:
            df[field] = df[field].str.replace(np.nan, "", regex=True)
        if avoid_empty is True:
            df[field] = df[field].astype(str).replace(r"^\s*$", None, regex=True)
    except TypeError:
        raise
    finally:
        return df


def to_string(
    df: pandas.DataFrame, field: str, remove_nan: bool = False
) -> pandas.DataFrame:
    df[field] = df[field].astype("string")
    if remove_nan is True:
        df[field] = df[field].str.replace(np.nan, "", regex=True)
    return df


def convert_to_array(
    df: pandas.DataFrame,
    field: str,
    column: str = None,
    separator=",",
    remove_empty: bool = False,
    no_duplicates: bool = False,
):
    # Convert NaN to empty string
    col = column if column else field
    df[field] = df[col].fillna("")
    df[field] = df[field].str.split(pat=separator)
    if no_duplicates is True:
        # Trim whitespace from each word, handle "nan" strings, and remove duplicates
        df[field] = df[field].apply(
            lambda x: list(set([word.strip() for word in x if word.strip() != "nan"]))
        )
    else:
        # Trim whitespace from each word and handle "nan" strings
        df[field] = df[field].apply(
            lambda x: [word.strip() for word in x if word.strip() != "nan"]
        )
    if remove_empty is True:
        df[field] = df[field].apply(lambda x: list(filter(lambda y: y != "", x)))
        df[field] = df[field].apply(lambda x: x if x else np.nan)
    return df


def to_json(df: pandas.DataFrame, field: str):
    try:
        # remove Nan
        df[field].fillna("[]", inplace=True)
        df[field] = df[field].str.replace("'", '"', regex=True)
        df[field] = df[field].apply(orjson.loads)
    except Exception as err:
        print(err)
    return df


def convert_json(value: str) -> str:
    try:
        value = ast.literal_eval(value)
    except Exception:
        pass
    try:
        value = orjson.dumps(value).decode("utf-8")
    except Exception as err:
        print(err)
    return value


def convert_to_json(df: pandas.DataFrame, field: str):
    try:
        df[field] = df.apply(lambda x: convert_json(x[field]), axis=1)
    except Exception as err:
        print(err)
    return df


def convert_to_datetime(df: pandas.DataFrame, field: str, remove_nat=False):
    try:
        df[field] = pandas.to_datetime(df[field], errors="coerce")
        df[field] = df[field].where(df[field].notnull(), None)
        df[field] = df[field].astype("datetime64[ns]")
    except Exception as err:
        print(err)
    return df


def to_datetime(df: pandas.DataFrame, field: str, format="%Y-%m-%d"):
    # Convert the 'dates' column to datetime format
    try:
        df[field] = pandas.to_datetime(df[field], format=format, errors="coerce")
    except Exception as err:
        print(err)
    return df


def convert_to_time(
    df: pandas.DataFrame, field: str, format="%H:%M:%S", not_null=False
):
    df[field] = df[field].where(df[field].notnull(), None)
    df[field] = pandas.to_datetime(df[field], format=format, errors="coerce").apply(
        pandas.Timestamp
    )
    if not_null:
        df[field] = df[field].where(df[field].notnull(), datetime.time(0, 0))
    return df


def column_to_date(df: pandas.DataFrame, field: str, column="", format="%Y-%m-%d"):
    if not column:
        column = field
    df[field] = pandas.to_datetime(df[column], format=format, errors="coerce")
    df[field] = df[field].astype(object).where(df[field].notnull(), None)
    df[field] = df[field].astype("datetime64[ns]")
    # df1 = df.assign(field=e.values)
    return df


def to_date(df: pandas.DataFrame, field: str, format="%Y-%m-%d", use_utc: bool = True):
    df[field] = pandas.to_datetime(
        df[field], utc=use_utc, format=format, errors="coerce"
    )
    return df


def datetime_format(df: pandas.DataFrame, field: str, column="", format="%Y-%m-%d"):
    try:
        if not column:
            column = field
        df[field] = df[column].dt.strftime(format)
    except Exception as err:
        print("format_from_column error:", err)
    return df


def column_to_integer(df: pandas.DataFrame, field: str, column=""):
    df[field] = pandas.to_numeric(df[column], errors="coerce")
    df[field] = df[field].astype("Int64")
    return df


def convert_to_date(
    df: pandas.DataFrame, field: str, format="%Y-%m-%d", remove_nat=False
):
    df[field] = pandas.to_datetime(df[field], format=format, errors="coerce")
    df[field] = df[field].astype("datetime64[ns]")
    df[field] = df[field].dt.normalize()
    if remove_nat:
        df[field] = df[field].where(df[field].notnull(), None)
    return df


def string_to_date(df: pandas.DataFrame, field: str, column="", format="%Y-%m-%d"):
    df[field] = pandas.to_datetime(df[column], format=format, errors="coerce")
    df[field] = df[field].replace({pandas.NaT: None}, inplace=True)
    df[field].astype("datetime64[ns]")
    return df


def epoch_to_date(
    df: pandas.DataFrame, field: str, column: str = None, unit: str = "ms"
):
    df[field] = pandas.to_numeric(df[field], errors="coerce")
    df[field] = df[field].astype("Int64", copy=False)
    if column:
        # using another column instead current:
        try:
            df[field] = pandas.to_datetime(df[column], unit=unit, errors="coerce")
        except Exception as err:
            logging.error(err)
    else:
        try:
            df[field] = pandas.to_datetime(df[field], unit=unit, errors="coerce")
        except Exception as err:
            logging.error(err)
    df[field].astype("datetime64[ns]")
    return df


def num_formatter(n):
    if type(n) == str:
        return (
            f"-{n.rstrip('-').lstrip('(').rstrip(')')}"
            if n.endswith("-") or n.startswith("(")
            else n.replace(",", ".")
        )
    else:
        return n


def convert_to_numeric(
    df, field: str, remove_nan: bool = True, fix_negatives: bool = False
):
    if fix_negatives is True:
        mask = df[field].str.endswith("-")
        df.loc[mask, field] = "-" + df.loc[mask, field].str[:-1]
    try:
        df[field] = pandas.to_numeric(df[field], errors="coerce")
        df[field] = df[field].replace([-np.inf, np.inf], np.nan)
    except Exception as err:
        print(field, "->", err)
    if remove_nan is True:
        df[field] = df[field].fillna(0)
    return df


def convert_to_integer(
    df: pandas.DataFrame, field: str, not_null=False, fix_negatives: bool = False
):
    try:
        if fix_negatives is True:
            df[field] = df[field].apply(num_formatter)  # .astype('float')
        df[field] = pandas.to_numeric(df[field], errors="coerce")
        df[field] = df[field].astype("Int64", copy=False)
    except Exception as err:
        print(field, "->", err)
    if not_null is True:
        df[field] = df[field].fillna(0)
    return df


def to_integer(df, field: str):
    try:
        df[field] = pandas.to_numeric(df[field], errors="coerce")
        df[field] = df[field].astype("Int64", copy=False)
    except TypeError as err:
        print(f"TO Integer {field}: Unable to safely cast non-equivalent float to int.")
        df[field] = np.floor(pandas.to_numeric(df[field], errors="coerce")).astype(
            "Int64"
        )
        print(err)
    except ValueError as err:
        print(
            f"TO Integer {field}: Unable to safely cast float to int due to out-of-range values: {err}"
        )
        df[field] = np.floor(pandas.to_numeric(df[field], errors="coerce")).astype(
            "Int64"
        )
    except Exception as err:
        print(f"TO Integer {field}: An error occurred during conversion.")
        print(err)
    return df


def convert_to_boolean(
    df: pandas.DataFrame,
    field: str,
    boolDict={"True": True, "False": False},
    true_values: Optional[dict] = None,
    nan: bool = False,
    preserve_nulls: bool = False,
):
    if field not in df.columns:
        # column doesn't exists
        df = df.assign(field=nan)
    try:
        if true_values is not None:
            if preserve_nulls is True:
                df[field] = df[field].map(
                    lambda x: True if x in true_values else (x if pandas.isna(x) else False)
                )
            else:
                df[field] = df[field].map(
                    lambda x: True if x in true_values else False
                )
        else:
            if preserve_nulls is True:
                df[field] = df[field].map(boolDict).where(df[field].notna(), df[field])
            else:
                pandas.set_option('future.no_silent_downcasting', True)
                df[field] = df[field].fillna(nan).astype(str).replace(boolDict).infer_objects(copy=False)
                df[field] = df[field].astype(bool)
    except Exception as err:
        print("TO Boolean Error: ", err)
    return df


to_boolean = convert_to_boolean


def string_to_bool(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    df[field] = df[field].apply(strtobool)
    df[field] = df[field].astype(bool)
    return df


def replace_args(df, field: str, column: str, args: Union[List, Dict] = None):
    if isinstance(args, list):
        for arg in args:
            df[field] = df[column].astype(str).replace(arg)
    else:
        df[field] = df[column].astype(str).replace(args)
    return df


def replace(df, field: str, args: List = None, is_regex: bool = False):
    if isinstance(args, list):
        if len(args) > 1:
            for arg in args:
                df[field] = df[field].astype(str).replace(*arg, regex=is_regex)
        else:
            df[field] = df[field].astype(str).replace(*args, regex=is_regex)
    else:
        df[field] = df[field].astype(str).replace(args, regex=is_regex)
    return df


def from_currency(df, field: str, symbol="$", remove_nan=True):
    df[field] = (
        df[field]
        .replace("[\\{},) ]".format(symbol), "", regex=True)
        .replace("[(]", "-", regex=True)
        .replace("[ ]+", np.nan, regex=True)
        .str.strip(",")
    )
    if remove_nan is True:
        df[field] = df[field].fillna("")
    df[field] = pandas.to_numeric(df[field], errors="coerce")
    df[field] = df[field].replace([-np.inf, np.inf], np.nan)
    return df


def to_percentile(df, field: str, symbol="%", divisor=None, remove_nan=True):
    df[field] = (
        df[field]
        .replace("[\\{},) ]".format(symbol), "", regex=True)
        .replace("[(]", "-", regex=True)
        .replace("[ ]+", np.nan, regex=True)
        .str.strip(",")
    )
    df[field] = pandas.to_numeric(df[field], errors="coerce")
    df[field] = df[field].replace([-np.inf, np.inf], np.nan)
    if divisor is not None:
        df[field] = df[field].apply(lambda x: x / divisor)
    if remove_nan is True:
        df[field] = df[field].fillna(0)
    else:
        df[field] = df[field].where(df[field].notnull(), None)
    return df


def split_cols(df, field: str, separator=",", columns=[], numcols=2):
    if isinstance(columns, list):
        try:
            df[columns] = df[field].str.split(separator, n=numcols, expand=True)
        except Exception as err:
            print("Error in split_cols:", err)
    return df


def startofweek(df, field: str, column=""):
    try:
        df[field] = df[column] - pandas.to_timedelta(df[column].dt.dayofweek, unit="d")
    except Exception as err:
        print(f'Error in startofweek: {err}')
    return df


def endofweek(df, field: str, column=""):
    try:
        df[field] = df[column] - pandas.to_timedelta(df[column].dt.dayofweek, unit="d") + pandas.to_timedelta(6, unit="d")
    except Exception as err:
        print(f'Error in endofweek: {err}')
    return df


def xlsdate(excel_time):
    if excel_time:
        return pandas.to_datetime("1899-12-30") + pandas.to_timedelta(excel_time, "D")
    else:
        return pandas.NaT


def excel_to_date(df, field: str):
    try:
        df[field] = df.apply(lambda row: xlsdate(row[field]), axis=1)
    except Exception as err:
        print("Error in excel_to_date:", err)
    return df

def is_datetime_column(column) -> bool:
    return pandas.api.types.is_datetime64_any_dtype(column)

def is_time_column(column) -> bool:
    return pandas.api.types.is_datetime64_any_dtype(column) and not pandas.api.types.is_timedelta64_dtype(column)

def extract(df, field: str, column="", to_date=None, value="day"):
    if not column:
        column = field
    if to_date is not None:
        df = convert_to_date(df, field, to_date)

    value = value.lower()

    if not is_datetime_column(df[column]):
        # convert to datetime, but only if not time:
        if not is_time_column(df[column]):
            try:
                df[column] = pandas.to_datetime(df[column])
            except TypeError:
                pass

    if value == "day":
        df[field] = df[column].dt.day
    elif value == "dow" or value.lower() == "dayofweek":
        df[field] = df[column].dt.dayofweek
    elif value == "doy" or value.lower() == "dayofyear":
        df[field] = df[column].dt.dayofyear
    elif value == "month":
        df[field] = df[column].dt.month
        df[field] = df[field].astype("Int64")
    elif value == "year":
        df[field] = df[column].dt.year
        df[field] = df[field].astype("Int64")
    elif value == "quarter":
        df[field] = df[column].dt.quarter
    elif value == "hour":
        try:
            df[field] = df[column].dt.hour
        except AttributeError:
            df[field] = df[column].dt.components.hours
    elif value == "minute":
        df[field] = df[column].dt.minute
    elif value == "second":
        df[field] = df[column].dt.second
    elif value == "ldom":
        df[field] = df[column] + MonthEnd(0)
    else:
        df[field] = df[column].dt.to_period(value)
    return df


def date_trunc(df, field: str, column: str, value: str = "dow", iso: bool = True):
    if value == "dow":
        unit = "d"
        if iso is False:
            df[field] = df[column] - pandas.to_timedelta(
                (df[column].dt.weekday + 1) - 7, unit="d"
            )
        else:
            df[field] = df[column] - pandas.to_timedelta(
                df[column].dt.dayofweek, unit=unit
            )
    return df


def date_diff(df, field: str, end: str, start: str, unit: str = "s"):
    df[field] = (df[end] - df[start]) / np.timedelta64(1, unit)
    return df


def replace_nulls(df, field: str = "", value: Any = None):
    try:
        df[field] = df[field].fillna(value)
    except Exception as err:
        print(err)
    return df


def fill_nulls(df: pandas.DataFrame, field: str, column: str):
    """Fill nulls with the value of another column."""
    if field not in df.columns.values:
        df[field] = df[column]
    else:
        # first: replace empty strings with nulls
        try:
            df[field] = df[field].apply(lambda x: x.strip()).replace("", np.nan)
        except Exception as err:
            print("ERROR = ", err)
        try:
            df.loc[df[field].isnull(), field] = df[column]
        except KeyError:
            logging.error(f"Fill Nulls: Column {field} doens't exists")
    return df


def fill_column(df, field: str, value: Any, variables: Any = None):
    if variables is not None:
        if value in variables:
            value = variables[value]
    if field not in df.columns.values:
        df[field] = value
    else:
        df[field] = df[field].replace(df[field], value)
    return df


def fn_get_timezone(latitudes, longitudes):
    tz = timezonefinder.TimezoneFinder()
    zones = np.full_like(latitudes, DEFAULT_TIMEZONE, dtype=object)
    mask = ~np.isnan(latitudes) & ~np.isnan(longitudes)
    latitudes = latitudes[mask]
    longitudes = longitudes[mask]
    if len(latitudes) > 0:
        zones[mask] = [tz.timezone_at(lng=long, lat=lat) for lat, long in zip(latitudes, longitudes)]
        zones[zones == "uninhabited"] = DEFAULT_TIMEZONE
        zones[zones is None] = DEFAULT_TIMEZONE
    return zones


def get_timezone(df, field: str, lat: str, long: str):
    if not set([lat, long]).issubset(df.columns):
        df[field] = None
    try:
        df[lat] = pandas.to_numeric(df[lat], errors='coerce')
        df[long] = pandas.to_numeric(df[long], errors='coerce')
    except Exception as err:
        print("Failed to convert Lat/Long to Float: ", err)
    try:
        df[field] = fn_get_timezone(df[lat].values, df[long].values)
    except Exception as err:
        print("GET TIMEZONE ERROR: ", err)
    return df


def split_into_series(df, field: str):
    try:
        df = df[field].apply(pandas.Series)
    except Exception as err:
        print("Split Series Error: ", err)
    finally:
        return df


def change_timezone(df, field: str, from_tz: str = None, to_tz: str = "UTC"):
    df[field] = pandas.to_datetime(df[field], errors="coerce")
    try:
        infer_dst = np.array([False] * df.shape[0])
        df[field] = (
            df[field].dt.tz_localize(from_tz, ambiguous=infer_dst).dt.tz_convert(to_tz)
        )
    except Exception as err:
        print("Error Changing timezone: ", err)
    finally:
        return df


def to_numeric(df, field: str, remove_alpha: bool = True, to_integer: bool = False):
    """
    Converts a column of a pandas DataFrame to numeric values, optionally removing
    non-numeric characters and converting to integer.

    Args:
    - df (pandas.DataFrame): The DataFrame containing the column to be converted.
    - field (str): The name of the column to be converted.
    - remove_alpha (bool, optional): If True, removes non-numeric characters from the
      column before converting. Default is True.
    - to_integer (bool, optional): If True, converts the column to integer dtype
      after converting to numeric. Default is False.

    Returns:
    - pandas.DataFrame: The input DataFrame with the converted column.

    Raises:
    - Exception: If an error occurs during the conversion process.

    Example:
    >>> import pandas as pd
    >>> data = {'A': ['1', '2', '3'], 'B': ['4', '5', '6a']}
    >>> df = pd.DataFrame(data)
    >>> df = to_numeric(df, 'B', remove_alpha=True, to_integer=True)
    >>> print(df)
         A  B
    0  1.0  4
    1  2.0  5
    2  3.0  6
    """
    try:
        if remove_alpha is True:
            df[field] = df[field].astype("string")
            df[field] = df[field].str.replace(r"\D+", "", regex=True)
        df[field] = pandas.to_numeric(df[field], errors="coerce")
        if to_integer is True:
            df[field] = df[field].astype("Int64", copy=False)
    except Exception as err:
        print(f"TO Integer {field}:", err)
    return df


def remove_scientific_notation(df: pandas.DataFrame, field: str):
    # df[field].apply(lambda x: '%.17f' % x).values.tolist()
    pandas.set_option("display.float_format", lambda x: f"%.{len(str(x%1))-2}f" % x)
    # use regular expressions to remove scientific notation
    df[field] = df[field].str.replace(
        r"(\d+\.\d+)([Ee])([\+\-]?\d+)", r"\1*10^\3", regex=True
    )
    df[field] = df[field].str.replace(
        r"(\d+)([Ee])([\+\-]?\d+)", r"\1*10^\3", regex=True
    )
    df[field] = df[field].str.replace(r"\*", r"", regex=True)
    # convert the column to a string data type
    df[field] = df[field].astype("string")
    return df


def first_not_null(
    df: pandas.DataFrame, field: str, columns: list[str]
) -> pandas.DataFrame:
    """
    Create a new column called "field" in a Pandas DataFrame
    filled with the first non-null value from columns in list.
    """
    # Create a new Series containing the first non-null value from
    try:
        series = df[columns].apply(lambda x: x.dropna().iloc[0], axis=1)
        # Add the new Series as a new column in the DataFrame
        df[field] = series
    except Exception as err:
        print(f"Error first_not_null {field}:", err)
    return df


def remove_html_tags(text):
    """Function to remove HTML tags from a text string."""
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()
    return cleaned_text


def clean_html_tags(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    """
    Clean all HTML tags from columns.
    """
    try:
        # Apply the 'remove_html_tags' function to the desired column
        df[field] = df[field].apply(remove_html_tags)
    except Exception as err:
        print(f"Error on clean_html_tags {field}:", err)
    return df


def autoincrement(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    """Fill a Column with autoincrement value."""
    try:
        # Add a correlative auto-increment column
        df[field] = range(1, len(df) + 1)
    except Exception as err:
        print(f"Error on autoincrement {field}:", err)
    return df


def row_to_column(
    df: pandas.DataFrame,
    field: str,
    column: str,
    row_to_pivot: str,
    value: str,
    pivot: list,
):
    """
    Add a pivoted column to the dataframe based on the given column name.

    Parameters:
    - df: The input dataframe.
    - field: The name of the column to be transposed.
    - pivot: The column name[s] to pivot.
    - value: Column name for extracting the value.

    Returns:
    - Dataframe with the new pivoted column.
    """
    # Filter the dataframe to only include rows with the desired column_name
    try:
        df_filtered = df[df[column] == row_to_pivot]
    except KeyError as e:
        logging.warning(f"Missing Column: {e}")
        return df
    print(df_filtered)
    # Pivot the filtered dataframe
    df_pivot = df_filtered.pivot_table(
        index=pivot, columns=column, values=value, aggfunc="first"
    ).reset_index()

    df_pivot = df_pivot.rename(columns={row_to_pivot: field})

    # Merge the pivoted dataframe with the original dataframe
    df_merged = pandas.merge(df, df_pivot, on=pivot, how="left")
    # Drop the original column_name and value columns for the pivoted rows
    df_merged = df_merged.drop(df_merged[(df_merged[column] == row_to_pivot)].index)
    return df_merged


def datetime_to_string(df: pandas.DataFrame, field: str, mask: str, column: str = None):
    """datetime_to_string.


    Converts a Datetime Column to an string using a Format.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        column (str): Column used for transformation.
        mask (list): Format Mask for transformation
    """
    if not column:
        column = field
    try:
        df[field] = df[column].dt.strftime(mask)
    except Exception as err:
        print(f"Error on datetime_to_string {field}:", err)
    return df


def flatten_array_row(row, field, attribute=None, prefix=""):
    if pandas.notna(row[field]):
        if attribute is not None:
            # Check if the attribute exists in the field
            if attribute in row[field]:
                for key, value in row[field][attribute].items():
                    row[f"{prefix}{key}"] = value
        else:
            # If no attribute is specified, assume the field itself is a dictionary
            for key, value in row[field].items():
                row[f"{prefix}{key}"] = value
    return row


def flatten_array(
    df: pandas.DataFrame, field: str, attribute: str = None, prefix: str = ""
):
    """flatten_array.
    Converts a nested value in a column to a flat fields in dataframe.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        column (str): Column used for transformation.
        mask (list): Format Mask for transformation
    """
    try:
        df = df.apply(flatten_array_row, axis=1, args=(field, attribute, prefix))
    except Exception:
        print(f"Error on flatten_array {field}:")
    return df


def extract_json_data(row, field: str, column: str):
    try:
        rows = row[column]
        if isinstance(rows, list):
            # Extract the column from the dictionary column
            _data = [row[field] for row in rows]
            return _data
        else:
            # Extract the column from the dictionary column
            return row[column][field]
    except KeyError:
        # Return None or some default value if 'column' key is not found
        return None


def extract_column(df: pandas.DataFrame, field: str, column: str):
    """extract_column.
    Converts a nested JSON value in a column in dataframe.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        column (str): Column used for transformation
    """
    try:
        df[field] = df.apply(extract_json_data, axis=1, args=(field, column))
    except Exception as exc:
        print(f"Error on extract_column {field}: {exc}")
    return df


def sum_columns(df: pandas.DataFrame, field: str, startswith: str = None, columns: list = None):
    """sum_columns.
    Sums all columns that start with a given string.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        startswith (str): String to filter columns.
        columns (list): List of columns.
    """
    if startswith is not None:
        try:
            # Filter columns that start with the given string
            columns = [col for col in df.columns if col.startswith(startswith)]
            # Sum the values in the columns
            df[field] = df[columns].sum(axis=1)
        except Exception as exc:
            print(f"Error on sum_columns {field}: {exc}")
    elif columns is not None:
        try:
            if columns and isinstance(columns, list):
                df[field] = df[columns].astype(float).sum(axis=1)
        except Exception as exc:
            print(f"Error on sum_columns {field}: {exc}")
    return df


def sub_columns(df: pandas.DataFrame, field: str, startswith: str = None, columns: list = None):
    """sub_columns.
    Subtract all columns that start with a given string.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        startswith (str): String to filter columns.
        columns (list): List of columns.
    """
    if startswith is not None:
        try:
            # Filter columns that start with the given string
            columns = [col for col in df.columns if col.startswith(startswith)]
            # Sum the values in the columns
            df[field] = reduce(lambda x, y: x.sub(y), [df[col] for col in columns])
        except Exception as exc:
            print(f"Error on sub_columns {field}: {exc}")
    elif columns is not None:
        try:
            if columns and isinstance(columns, list):
                df[field] = reduce(lambda x, y: x.sub(y), [df[col].astype(float) for col in columns])
        except Exception as exc:
            print(f"Error on sub_columns {field}: {exc}")
    return df

def autoincrement_by_group(df: pandas.DataFrame, field: str, group_column: str) -> pandas.DataFrame:
    """
    autoincrement_by_group.

    Autoincrement a column (if empty or NAN) based on a group column.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        group_column (str): Column used for grouping.

    Returns:
        pandas.DataFrame: Dataframe with the new autoincremented column.
    """
    try:
        # Apply a group function to every row in group:
        def auto_group_function(group):
            i = 1
            for idx in group.index:
                if pandas.isna(group.at[idx, field]) or group.at[idx, field] == "":
                    group.at[idx, field] = i
                    i += 1
            return group

        # Apply the group function to the dataframe
        df = df.groupby(group_column).apply(auto_group_function).reset_index(drop=True)
        return df
    except Exception as err:
        print(f"Error on autoincrement_by_group {field}:", err)
        return df

def autoincrement_by_column(
    df: pandas.DataFrame,
    field: str,
    group_column: str,
    suffix: bool = True,
    separator: str = ''
) -> pandas.DataFrame:
    """
    autoincrement_by_column.

    Add an autoincrement number (prefix, suffix) to a column based on a group column.

    Args:
        df (pandas.DataFrame): Pandas Dataframe.
        field (str): Column used to create a new column.
        group_column (str): Column used for grouping.

    Returns:
        pandas.DataFrame: Dataframe with the new autoincremented column.
    """
    try:
        # Create a group key that will maintain order within groups
        df['group_key'] = df.groupby(group_column).cumcount() + 1
        # Generate the new field values by combining the original field value with the group_key
        if suffix:
            df[field] = df.apply(lambda x: f"{x[field]}{separator}{x['group_key']}", axis=1)
        else:
            df[field] = df.apply(lambda x: f"{x['group_key']}{separator}{x[field]}", axis=1)

        # Clean up the temporary group_key column
        df.drop('group_key', axis=1, inplace=True)
        return df
    except Exception as err:
        print(f"Error on autoincrement_by_group {field}:", err)
        return df


def get_product(row, field, columns):
    barcode = row[field]
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode}&key={BARCODELOOKUP_API_KEY}'
    response = requests.get(url)
    result = response.json()['products'][0]
    for col in columns:
        try:
            row[col] = result[col]
        except KeyError:
            row[col] = None
    return row


def upc_to_product(
    df: pandas.DataFrame,
    field: str,
    columns: list = ['barcode_formats', 'mpn', 'asin', 'title', 'category', 'model', 'brand']
) -> pandas.DataFrame:
    try:
        df = df.apply(lambda x: get_product(x, field, columns), axis=1)
        return df
    except Exception as err:
        print(f"Error on upc_to_product {field}:", err)
        return df

def fill_map(
    df: pandas.DataFrame,
    field: str,
    column: str
) -> pandas.DataFrame:
    try:
        # Replace empty strings with None
        df[field] = df[field].replace('', None)

        # Create the map explicitly
        mapa = df.groupby(column)[field].apply(lambda x: x.dropna().iloc[0] if not x.dropna().empty else None).to_dict()

        # Apply the map explicitly
        df[field] = df.apply(lambda row: mapa.get(row[column], row[field]) if pandas.isnull(row[field]) else row[field], axis=1)

        return df
    except Exception as err:
        print(f"Error en fill_map {field}:", err)
        return df
